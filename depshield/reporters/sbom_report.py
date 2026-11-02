"""Generate SBOM report."""

import logging
from typing import List

from depshield.models import Dependency

logger = logging.getLogger(__name__)


class SBOMReporter:
    """Generate SBOM documentation."""

    @staticmethod
    def format_sbom(dependencies: List[Dependency]) -> str:
        """Format SBOM as Markdown table.

        Args:
            dependencies: List of dependencies

        Returns:
            Markdown-formatted SBOM
        """
        if not dependencies:
            return "# SBOM (Software Bill of Materials)\n\nNo dependencies found.\n"

        lines = [
            "# SBOM (Software Bill of Materials)\n",
            "| Component | Version | Ecosystem | License | Vulnerabilities |",
            "|-----------|---------|-----------|---------|-----------------|",
        ]

        for dep in sorted(dependencies, key=lambda d: d.name):
            vuln_count = len(dep.vulnerabilities) if dep.vulnerabilities else 0
            vuln_str = f"{vuln_count} CVEs" if vuln_count > 0 else "Clean"
            license_str = dep.license if dep.license else "Unknown"

            lines.append(
                f"| {dep.name} | {dep.version} | {dep.ecosystem.value} | "
                f"{license_str} | {vuln_str} |"
            )

        return "\n".join(lines)

    @staticmethod
    def format_detailed_sbom(dependencies: List[Dependency]) -> str:
        """Format detailed SBOM with CycloneDX-style information.

        Args:
            dependencies: List of dependencies

        Returns:
            Detailed Markdown SBOM
        """
        lines = ["# Software Bill of Materials (SBOM)\n"]
        lines.append(f"**Total Components**: {len(dependencies)}\n")

        # Group by ecosystem
        by_ecosystem = {}
        for dep in dependencies:
            ecosystem = dep.ecosystem.value
            if ecosystem not in by_ecosystem:
                by_ecosystem[ecosystem] = []
            by_ecosystem[ecosystem].append(dep)

        for ecosystem in sorted(by_ecosystem.keys()):
            deps = by_ecosystem[ecosystem]
            lines.append(f"## {ecosystem.upper()}\n")
            lines.append(f"**Count**: {len(deps)}\n")
            lines.append("| Component | Version | License |")
            lines.append("|-----------|---------|---------|")

            for dep in sorted(deps, key=lambda d: d.name):
                license_str = dep.license if dep.license else "Unknown"
                lines.append(f"| {dep.name} | {dep.version} | {license_str} |")

            lines.append("")

        return "\n".join(lines)
