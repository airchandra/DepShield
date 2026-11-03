"""Vulnerability scanning using Grype."""

import json
import logging
from pathlib import Path

from depshield.models import RepoManifest, ScanResult, Severity, Vulnerability
from depshield.scanners.base import BaseScanner

logger = logging.getLogger(__name__)


class GrypScanner(BaseScanner):
    """Scan vulnerabilities using Grype."""

    def scan(self) -> ScanResult:
        """Scan repository using Grype.

        Returns:
            ScanResult with vulnerabilities
        """
        try:
            if not self.result.sbom_path:
                # Generate SBOM first
                from depshield.scanners.sbom import SyftScanner
                syft = SyftScanner(self.repo, self.config)
                sbom_result = syft.scan()
                self.result.sbom_path = sbom_result.sbom_path

                if not self.result.sbom_path:
                    self.result.error = "Failed to generate SBOM"
                    return self.result

            # Run Grype on SBOM
            output_file = self.config.output_dir / "grype" / f"{self.repo.name}-vulns.json"
            output_file.parent.mkdir(parents=True, exist_ok=True)

            cmd = [
                self.config.grype_path,
                str(self.result.sbom_path),
                "-o", "json"
            ]

            stdout, stderr, rc = self._run_command(cmd)

            if rc == 0:
                vulns_data = self._parse_json_output(stdout)
                self.result.vulnerabilities = self._parse_vulnerabilities(vulns_data)
                self.result.success = True
                logger.info(f"Found {len(self.result.vulnerabilities)} vulnerabilities in {self.repo.name}")
            else:
                logger.warning(f"Grype scan returned {rc}: {stderr}")
                self.result.success = True  # Continue even if no vulnerabilities found

            return self.result

        except Exception as e:
            self.result.error = f"Grype scan error: {str(e)}"
            logger.error(f"Exception in Grype scan: {e}")
            return self.result

    def _parse_vulnerabilities(self, data: dict) -> list[Vulnerability]:
        """Parse Grype JSON output into Vulnerability objects."""
        vulns = []
        matches = data.get("matches", [])

        for match in matches:
            vuln_data = match.get("vulnerability", {})
            artifact = match.get("artifact", {})

            severity_str = vuln_data.get("severity", "unknown").lower()
            severity = Severity(severity_str) if severity_str in Severity.__members__ else Severity.UNKNOWN

            # Safely parse CVSS score
            cvss_value = vuln_data.get("cvss", 0.0)
            try:
                cvss_score = float(cvss_value) if cvss_value else 0.0
            except (ValueError, TypeError):
                cvss_score = 0.0

            vuln = Vulnerability(
                id=vuln_data.get("id", ""),
                package=artifact.get("name", ""),
                severity=severity,
                cvss_score=cvss_score,
                description=vuln_data.get("description", ""),
                fixed_version=vuln_data.get("fix", {}).get("versions", [""])[0] if vuln_data.get("fix") else "",
                current_version=artifact.get("version", ""),
                advisory=vuln_data.get("dataSource", "")
            )
            vulns.append(vuln)

        return vulns
