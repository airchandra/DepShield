"""Generate vulnerability report."""

import logging
from typing import List

from depshield.models import Severity, Vulnerability

logger = logging.getLogger(__name__)


class VulnerabilityReporter:
    """Generate vulnerability documentation."""

    SEVERITY_ORDER = {
        Severity.CRITICAL: 0,
        Severity.HIGH: 1,
        Severity.MEDIUM: 2,
        Severity.LOW: 3,
        Severity.UNKNOWN: 4,
    }

    @staticmethod
    def format_vulnerabilities(vulnerabilities: List[Vulnerability]) -> str:
        """Format vulnerabilities as Markdown table.

        Args:
            vulnerabilities: List of vulnerabilities

        Returns:
            Markdown-formatted vulnerability report
        """
        if not vulnerabilities:
            return "# Vulnerability Report\n\n✅ No vulnerabilities found.\n"

        lines = [
            "# Vulnerability Report\n",
            "| CVE ID | Package | Severity | CVSS | Description | Fix Version |",
            "|--------|---------|----------|------|-------------|-------------|",
        ]

        # Sort by severity then by package name
        sorted_vulns = sorted(
            vulnerabilities,
            key=lambda v: (VulnerabilityReporter.SEVERITY_ORDER.get(v.severity, 999), v.package)
        )

        for vuln in sorted_vulns:
            desc = vuln.description[:60] + "..." if len(vuln.description) > 60 else vuln.description
            fix_version = vuln.fixed_version if vuln.fixed_version else "TBD"

            lines.append(
                f"| {vuln.id} | {vuln.package} | {vuln.severity.value.upper()} | "
                f"{vuln.cvss_score:.1f} | {desc} | {fix_version} |"
            )

        return "\n".join(lines)

    @staticmethod
    def format_detailed_report(vulnerabilities: List[Vulnerability]) -> str:
        """Format detailed vulnerability report with summaries.

        Args:
            vulnerabilities: List of vulnerabilities

        Returns:
            Detailed Markdown report
        """
        if not vulnerabilities:
            return "# Vulnerability Report\n\n✅ No vulnerabilities found.\n"

        # Count by severity
        by_severity = {}
        for vuln in vulnerabilities:
            severity = vuln.severity
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(vuln)

        lines = ["# Vulnerability Report\n"]

        # Summary
        total = len(vulnerabilities)
        critical = len(by_severity.get(Severity.CRITICAL, []))
        high = len(by_severity.get(Severity.HIGH, []))
        lines.append("## Summary\n")
        lines.append(f"**Total Vulnerabilities**: {total}")
        lines.append(f"- Critical: {critical}")
        lines.append(f"- High: {high}")
        lines.append(f"- Medium: {len(by_severity.get(Severity.MEDIUM, []))}")
        lines.append(f"- Low: {len(by_severity.get(Severity.LOW, []))}\n")

        # Detailed by severity
        for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.UNKNOWN]:
            vulns = by_severity.get(severity, [])
            if not vulns:
                continue

            lines.append(f"## {severity.value.upper()} Severity\n")

            for vuln in sorted(vulns, key=lambda v: v.package):
                lines.append(f"### {vuln.id}")
                lines.append(f"- **Package**: {vuln.package}")
                lines.append(f"- **Current Version**: {vuln.current_version}")
                lines.append(f"- **Fixed Version**: {vuln.fixed_version or 'N/A'}")
                lines.append(f"- **CVSS Score**: {vuln.cvss_score}")
                lines.append(f"- **Description**: {vuln.description}")
                if vuln.advisory:
                    lines.append(f"- **Advisory**: {vuln.advisory}")
                lines.append("")

        return "\n".join(lines)
