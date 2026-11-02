"""Container and filesystem scanning using Trivy."""

import json
import logging

from depshield.models import RepoManifest, ScanResult, Severity, Vulnerability
from depshield.scanners.base import BaseScanner

logger = logging.getLogger(__name__)


class TrivyScanner(BaseScanner):
    """Scan using Trivy (filesystem and container)."""

    def scan(self) -> ScanResult:
        """Scan repository using Trivy.

        Returns:
            ScanResult with vulnerabilities
        """
        try:
            # Scan filesystem
            output_file = self.config.output_dir / "trivy" / f"{self.repo.name}-trivy.json"
            output_file.parent.mkdir(parents=True, exist_ok=True)

            cmd = [
                self.config.trivy_path,
                "fs", str(self.repo.path),
                "-f", "json"
            ]

            stdout, stderr, rc = self._run_command(cmd)

            # Trivy exits with 0 if no vulns, 1 if vulns found
            if rc == 0 or rc == 1:
                trivy_data = self._parse_json_output(stdout)
                self.result.vulnerabilities = self._parse_vulnerabilities(trivy_data)
                self.result.success = True
                logger.info(f"Trivy scan found {len(self.result.vulnerabilities)} vulnerabilities")
            else:
                logger.warning(f"Trivy scan returned {rc}")
                self.result.success = True

            return self.result

        except Exception as e:
            self.result.error = f"Trivy scan error: {str(e)}"
            logger.error(f"Exception in Trivy scan: {e}")
            return self.result

    def _parse_vulnerabilities(self, data: dict) -> list[Vulnerability]:
        """Parse Trivy JSON output."""
        vulns = []
        results = data.get("Results", [])

        for result in results:
            misconfigs = result.get("Misconfigurations", [])
            vulnerabilities = result.get("Vulnerabilities", [])

            for vuln_data in vulnerabilities:
                severity_str = vuln_data.get("Severity", "unknown").lower()
                severity = Severity(severity_str) if severity_str in Severity.__members__ else Severity.UNKNOWN

                vuln = Vulnerability(
                    id=vuln_data.get("VulnerabilityID", ""),
                    package=vuln_data.get("PkgName", ""),
                    severity=severity,
                    cvss_score=float(vuln_data.get("CVSS", {}).get("ghsa", {}).get("V3Score", 0.0)),
                    description=vuln_data.get("Title", ""),
                    fixed_version=vuln_data.get("FixedVersion", ""),
                    current_version=vuln_data.get("InstalledVersion", ""),
                    advisory=vuln_data.get("PrimaryURL", "")
                )
                vulns.append(vuln)

        return vulns
