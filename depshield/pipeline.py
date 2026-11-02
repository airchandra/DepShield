"""Main pipeline orchestrator."""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List

from depshield.config import DepShieldConfig
from depshield.discovery import RepositoryDiscovery
from depshield.matrix.dependency_matrix import DependencyMatrix
from depshield.matrix.upgrade_matrix import UpgradeMatrix
from depshield.models import Ecosystem, RepoManifest, RemediationResult, ScanResult
from depshield.remediation.cargo_upgrader import CargoRemediator
from depshield.remediation.go_upgrader import GoRemediator
from depshield.remediation.npm_upgrader import NpmRemediator
from depshield.remediation.openrewrite import OpenRewriteRemediator
from depshield.remediation.pip_upgrader import PipRemediator
from depshield.reporters.architecture import ArchitectureReporter
from depshield.reporters.coding_guidelines import CodingGuidelinesReporter
from depshield.reporters.diagrams import DiagramGenerator
from depshield.reporters.sbom_report import SBOMReporter
from depshield.reporters.test_cases import TestCasesReporter
from depshield.reporters.vuln_report import VulnerabilityReporter
from depshield.scanners.grype import GrypScanner
from depshield.scanners.sbom import SyftScanner

logger = logging.getLogger(__name__)


class DepShieldPipeline:
    """Main pipeline for zero-critical-vulnerabilities remediation."""

    def __init__(self, config: DepShieldConfig):
        """Initialize pipeline.

        Args:
            config: DepShield configuration
        """
        self.config = config
        self.repos: List[RepoManifest] = []
        self.scan_results: List[ScanResult] = []
        self.remediation_results: List[RemediationResult] = []

    def run(self):
        """Execute the full pipeline."""
        try:
            self._phase_1_discovery()
            self._phase_2_sbom_generation()
            self._phase_3_vulnerability_scan()
            self._phase_4_build_matrices()

            if not self.config.dry_run and self.config.apply:
                self._phase_5_remediation()

            self._phase_6_generate_reports()

            logger.info("Pipeline completed successfully")

        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            raise

    def _phase_1_discovery(self):
        """Phase 1: Repository discovery and ecosystem detection."""
        logger.info("Phase 1: Repository Discovery")

        self.repos = RepositoryDiscovery.discover_repos(self.config.repos)

        if not self.repos:
            raise ValueError("No repositories discovered")

        logger.info(f"Discovered {len(self.repos)} repositories")

    def _phase_2_sbom_generation(self):
        """Phase 2: SBOM generation."""
        logger.info("Phase 2: SBOM Generation")

        for repo in self.repos:
            logger.info(f"Generating SBOM for {repo.name}")
            scanner = SyftScanner(repo, self.config)
            result = scanner.scan()

            if not result.success:
                logger.warning(f"SBOM generation failed for {repo.name}: {result.error}")

    def _phase_3_vulnerability_scan(self):
        """Phase 3: Vulnerability scanning."""
        logger.info("Phase 3: Vulnerability Scanning")

        for repo in self.repos:
            logger.info(f"Scanning {repo.name} for vulnerabilities")
            scanner = GrypScanner(repo, self.config)
            result = scanner.scan()

            self.scan_results.append(result)

            if result.success:
                logger.info(
                    f"Found {len(result.vulnerabilities)} vulnerabilities in {repo.name}"
                )
                repo.dependencies = self._extract_dependencies_from_scan(result)
            else:
                logger.warning(f"Vulnerability scan failed for {repo.name}: {result.error}")

    def _phase_4_build_matrices(self):
        """Phase 4: Build dependency and upgrade matrices."""
        logger.info("Phase 4: Building Matrices")

        # Build dependency matrix
        dep_matrix = DependencyMatrix(self.repos)
        dep_matrix.build()

        # Build upgrade matrix from all vulnerabilities
        all_vulns = []
        for result in self.scan_results:
            all_vulns.extend(result.vulnerabilities)

        upgrade_matrix = UpgradeMatrix(all_vulns)
        upgrade_matrix.build()

        logger.info(f"Dependency matrix: {len(dep_matrix.matrix)} unique packages")
        logger.info(f"Upgrade matrix: {len(upgrade_matrix.recommendations)} packages with vulns")

        # Store for phase 6
        self.dep_matrix = dep_matrix
        self.upgrade_matrix = upgrade_matrix

    def _phase_5_remediation(self):
        """Phase 5: Remediation."""
        logger.info("Phase 5: Remediation")

        for repo in self.repos:
            logger.info(f"Remediating {repo.name}")

            # Select remediator based on ecosystem
            for ecosystem in repo.ecosystems:
                logger.info(f"Running {ecosystem.value} remediator")

                remediator = self._get_remediator(repo, ecosystem)
                if remediator:
                    result = remediator.remediate(dry_run=False)
                    self.remediation_results.append(result)

                    if result.success:
                        logger.info(f"Remediation succeeded for {repo.name}")
                    else:
                        logger.warning(f"Remediation failed for {repo.name}: {result.error}")

    def _phase_6_generate_reports(self):
        """Phase 6: Generate documentation."""
        logger.info("Phase 6: Generating Reports")

        # Create output directory
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        # Generate system-level reports
        self._generate_system_reports()

        # Generate per-repo reports
        for repo in self.repos:
            self._generate_repo_reports(repo)

        logger.info(f"Reports generated in {self.config.output_dir}")

    def _generate_system_reports(self):
        """Generate system-level documentation."""
        # Architecture
        arch_doc = ArchitectureReporter.format_system_architecture(self.repos)
        arch_doc += "\n\n" + ArchitectureReporter.format_component_diagram(self.repos)
        arch_doc += "\n\n" + ArchitectureReporter.format_dependency_relationships(self.repos)

        (self.config.output_dir / "SYSTEM_ARCHITECTURE.md").write_text(arch_doc)

        # Dependency matrix
        dep_matrix_doc = self.dep_matrix.format_as_markdown()
        (self.config.output_dir / "DEPENDENCY_MATRIX.md").write_text(dep_matrix_doc)

        # Upgrade matrix
        upgrade_matrix_doc = self.upgrade_matrix.format_as_markdown()
        (self.config.output_dir / "UPGRADE_MATRIX.md").write_text(upgrade_matrix_doc)

        # Pipeline sequence
        pipeline_seq = DiagramGenerator.pipeline_sequence_diagram(
            ["Discovery", "SBOM", "Scanning", "Matrices", "Remediation", "Reports"]
        )
        sequence_doc = "# Pipeline Execution Sequence\n\n" + pipeline_seq
        (self.config.output_dir / "PIPELINE_SEQUENCE.md").write_text(sequence_doc)

        logger.info("System-level reports generated")

    def _generate_repo_reports(self, repo: RepoManifest):
        """Generate per-repository documentation."""
        docs_dir = repo.path / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)

        # Find scan result for this repo
        repo_scan = next((s for s in self.scan_results if s.repo.path == repo.path), None)

        # SBOM
        sbom_doc = SBOMReporter.format_detailed_sbom(repo.dependencies)
        (docs_dir / "SBOM.md").write_text(sbom_doc)

        # Vulnerabilities
        if repo_scan:
            vuln_doc = VulnerabilityReporter.format_detailed_report(repo_scan.vulnerabilities)
        else:
            vuln_doc = VulnerabilityReporter.format_vulnerabilities([])
        (docs_dir / "VULNERABILITY_REPORT.md").write_text(vuln_doc)

        # Architecture
        arch_doc = f"# {repo.name} Architecture\n\n"
        arch_doc += DiagramGenerator.architecture_c4_component(repo)
        (docs_dir / "ARCHITECTURE.md").write_text(arch_doc)

        # Coding guidelines
        guidelines_doc = CodingGuidelinesReporter.format_guidelines([repo])
        (docs_dir / "CODING_GUIDELINES.md").write_text(guidelines_doc)

        # Sequence diagrams
        seq_doc = "# Remediation Sequence\n\n"
        seq_doc += DiagramGenerator.remediation_flowchart()
        (docs_dir / "SEQUENCE_DIAGRAMS.md").write_text(seq_doc)

        # Test cases
        test_doc = TestCasesReporter.format_test_cases([repo])
        test_doc += "\n\n" + TestCasesReporter.generate_test_matrix([repo])
        (docs_dir / "TEST_CASES.md").write_text(test_doc)

        # Upgrade plan
        upgrade_doc = "# Upgrade Plan\n\n"
        if repo_scan:
            upgrade_matrix = UpgradeMatrix(repo_scan.vulnerabilities)
            upgrade_matrix.build()
            upgrade_doc += upgrade_matrix.format_as_markdown()
        else:
            upgrade_doc += "No vulnerabilities found.\n"
        (docs_dir / "UPGRADE_PLAN.md").write_text(upgrade_doc)

        logger.info(f"Generated reports for {repo.name}")

    def _extract_dependencies_from_scan(self, result: ScanResult) -> list:
        """Extract dependencies from scan result."""
        # TODO: Parse actual SBOM to extract Dependency objects
        return []

    def _get_remediator(self, repo: RepoManifest, ecosystem: Ecosystem):
        """Get remediator for ecosystem."""
        if ecosystem == Ecosystem.JVM:
            return OpenRewriteRemediator(repo, self.config)
        elif ecosystem == Ecosystem.PYTHON:
            return PipRemediator(repo, self.config)
        elif ecosystem == Ecosystem.JAVASCRIPT:
            return NpmRemediator(repo, self.config)
        elif ecosystem == Ecosystem.GO:
            return GoRemediator(repo, self.config)
        elif ecosystem == Ecosystem.RUST:
            return CargoRemediator(repo, self.config)
        return None
