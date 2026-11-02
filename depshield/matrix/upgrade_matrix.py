"""Build upgrade recommendations matrix."""

import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional

from depshield.models import RemediationResult, Vulnerability

logger = logging.getLogger(__name__)


@dataclass
class UpgradeRecommendation:
    """Upgrade recommendation for a package."""
    package: str
    current_version: str
    safe_version: str
    vulnerabilities: List[Vulnerability]
    severity_level: str
    cvss_score: float


class UpgradeMatrix:
    """Build and analyze upgrade recommendations."""

    def __init__(self, vulnerabilities: List[Vulnerability]):
        """Initialize with vulnerabilities.

        Args:
            vulnerabilities: List of Vulnerability objects
        """
        self.vulnerabilities = vulnerabilities
        self.recommendations: Dict[str, UpgradeRecommendation] = {}

    def build(self) -> Dict[str, UpgradeRecommendation]:
        """Build upgrade matrix from vulnerabilities.

        Returns:
            Dictionary mapping package to UpgradeRecommendation
        """
        vulns_by_package = defaultdict(list)

        for vuln in self.vulnerabilities:
            vulns_by_package[vuln.package].append(vuln)

        for package, vulns in vulns_by_package.items():
            # Get the highest severity
            severities = [v.severity.value for v in vulns]
            max_severity = max(severities) if severities else "unknown"

            # Calculate max CVSS
            max_cvss = max([v.cvss_score for v in vulns] or [0.0])

            # Find safe version (prefer fixed_version from first vuln with one)
            safe_version = ""
            for v in vulns:
                if v.fixed_version:
                    safe_version = v.fixed_version
                    break

            if not safe_version and vulns:
                safe_version = f">=0"  # Fallback: upgrade to any version

            self.recommendations[package] = UpgradeRecommendation(
                package=package,
                current_version=vulns[0].current_version if vulns else "unknown",
                safe_version=safe_version,
                vulnerabilities=vulns,
                severity_level=max_severity,
                cvss_score=max_cvss
            )

        return self.recommendations

    def get_critical_and_high(self) -> Dict[str, UpgradeRecommendation]:
        """Get critical and high-severity upgrade recommendations.

        Returns:
            Filtered recommendations
        """
        return {
            pkg: rec
            for pkg, rec in self.recommendations.items()
            if rec.severity_level in ["critical", "high"]
        }

    def format_as_markdown(self) -> str:
        """Format upgrade matrix as Markdown table.

        Returns:
            Markdown-formatted upgrade matrix
        """
        if not self.recommendations:
            return "# Upgrade Matrix\n\nNo vulnerabilities found.\n"

        lines = ["# Upgrade Matrix\n"]
        lines.append("| Package | Current | Safe Version | Severity | CVSS | CVEs |")
        lines.append("|---------|---------|--------------|----------|------|------|")

        for pkg in sorted(self.recommendations.keys()):
            rec = self.recommendations[pkg]
            cve_ids = ", ".join([v.id for v in rec.vulnerabilities[:3]])
            if len(rec.vulnerabilities) > 3:
                cve_ids += f" +{len(rec.vulnerabilities) - 3} more"

            lines.append(
                f"| {pkg} | {rec.current_version} | {rec.safe_version} | "
                f"{rec.severity_level} | {rec.cvss_score:.1f} | {cve_ids} |"
            )

        return "\n".join(lines)
