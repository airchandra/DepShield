"""Generate Mermaid diagrams for system documentation."""

import logging
from typing import List

from depshield.models import RepoManifest

logger = logging.getLogger(__name__)


class DiagramGenerator:
    """Generate Mermaid diagrams."""

    @staticmethod
    def c4_context_diagram(repos: List[RepoManifest], system_name: str = "Distributed System") -> str:
        """Generate C4 context diagram.

        Args:
            repos: List of repositories
            system_name: Name of the system

        Returns:
            Mermaid C4 context diagram
        """
        lines = [
            "```mermaid",
            "graph TB",
            f"    System[{system_name}]",
            f"    Admin[Admin/DevOps]",
            f"    Admin -->|Manages| System",
        ]

        # Add repos as components
        for i, repo in enumerate(repos, 1):
            lines.append(f"    Repo{i}[{repo.name}]")
            lines.append(f"    System -->|Contains| Repo{i}")

        lines.append("```")
        return "\n".join(lines)

    @staticmethod
    def pipeline_sequence_diagram(phases: List[str]) -> str:
        """Generate pipeline execution sequence diagram.

        Args:
            phases: List of pipeline phase names

        Returns:
            Mermaid sequence diagram
        """
        lines = [
            "```mermaid",
            "sequenceDiagram",
            "    participant User",
            "    participant CLI",
            "    participant Scanners",
            "    participant Remediators",
            "    participant Reporters",
            "",
            "    User->>CLI: depshield --repos ./a ./b",
            "    CLI->>Scanners: Phase 1: Discovery",
            "    Scanners->>Scanners: Detect Ecosystems",
            "    CLI->>Scanners: Phase 2: SBOM Generation",
            "    Scanners->>Scanners: Syft SBOM",
            "    CLI->>Scanners: Phase 3: Vulnerability Scan",
            "    Scanners->>Scanners: Grype + OSV + Trivy",
            "    CLI->>CLI: Phase 4: Build Matrices",
            "    CLI->>Remediators: Phase 5: Remediation",
            "    Remediators->>Remediators: Apply Fixes",
            "    CLI->>Reporters: Phase 6: Generate Docs",
            "    Reporters->>Reporters: SBOM, VULN, UPGRADE, ARCH",
            "    Reporters-->>User: Output Generated",
            "```",
        ]
        return "\n".join(lines)

    @staticmethod
    def remediation_flowchart() -> str:
        """Generate remediation process flowchart.

        Returns:
            Mermaid flowchart
        """
        lines = [
            "```mermaid",
            "flowchart TD",
            "    Start([Start Remediation]) --> Stash[Create Git Stash]",
            "    Stash --> Detect{Detect<br/>Ecosystem}",
            "    Detect -->|JVM| OpenRewrite[Run OpenRewrite]",
            "    Detect -->|Python| PipAudit[Run pip-audit --fix]",
            "    Detect -->|JavaScript| NpmAudit[Run npm audit fix]",
            "    Detect -->|Go| GovVuln[Run govulncheck]",
            "    Detect -->|Rust| CargoAudit[Run cargo audit]",
            "    OpenRewrite --> Build[Attempt Build]",
            "    PipAudit --> Build",
            "    NpmAudit --> Build",
            "    GovVuln --> Build",
            "    CargoAudit --> Build",
            "    Build --> BuildOK{Build<br/>Success?}",
            "    BuildOK -->|No| Rollback[Pop Stash]",
            "    BuildOK -->|Yes| Test[Run Tests]",
            "    Test --> TestOK{Tests<br/>Pass?}",
            "    TestOK -->|No| Rollback",
            "    TestOK -->|Yes| Success([Success])",
            "    Rollback --> Failed([Failed])",
            "```",
        ]
        return "\n".join(lines)

    @staticmethod
    def architecture_c4_component(repo: RepoManifest) -> str:
        """Generate C4 component diagram for a repository.

        Args:
            repo: Repository manifest

        Returns:
            Mermaid C4 component diagram
        """
        ecosystems_str = ", ".join([e.value for e in repo.ecosystems])

        lines = [
            "```mermaid",
            "graph TB",
            f"    Repo[{repo.name}]",
            f"    Ecosystems[Ecosystems: {ecosystems_str}]",
            f"    DependencyCount[Dependencies: {len(repo.dependencies)}]",
            f"    Repo --> Ecosystems",
            f"    Repo --> DependencyCount",
        ]

        # Add sample dependencies
        for i, dep in enumerate(repo.dependencies[:5], 1):
            lines.append(f"    Dep{i}[{dep.name}@{dep.version}]")
            lines.append(f"    Repo --> Dep{i}")

        if len(repo.dependencies) > 5:
            lines.append(f"    More[+{len(repo.dependencies) - 5} more dependencies]")
            lines.append(f"    Repo --> More")

        lines.append("```")
        return "\n".join(lines)
