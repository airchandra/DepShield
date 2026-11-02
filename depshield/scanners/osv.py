"""Cross-check vulnerability scanning using OSV Scanner."""

import json
import logging

from depshield.models import RepoManifest, ScanResult, Severity, Vulnerability
from depshield.scanners.base import BaseScanner

logger = logging.getLogger(__name__)


class OSVScanner(BaseScanner):
    """Cross-check vulnerabilities using OSV Scanner."""

    def scan(self) -> ScanResult:
        """Scan using OSV Scanner.

        Returns:
            ScanResult with vulnerabilities
        """
        try:
            output_file = self.config.output_dir / "osv" / f"{self.repo.name}-osv.json"
            output_file.parent.mkdir(parents=True, exist_ok=True)

            cmd = [
                self.config.osv_scanner_path,
                "-r", str(self.repo.path),
                "--json"
            ]

            stdout, stderr, rc = self._run_command(cmd)

            if rc == 0 or rc == 1:  # OSV returns 1 if vulns found
                osv_data = self._parse_json_output(stdout)
                self.result.vulnerabilities = self._parse_vulnerabilities(osv_data)
                self.result.success = True
                logger.info(f"OSV scan found {len(self.result.vulnerabilities)} vulnerabilities")
            else:
                logger.warning(f"OSV scan returned {rc}")
                self.result.success = True

            return self.result

        except Exception as e:
            self.result.error = f"OSV scan error: {str(e)}"
            logger.error(f"Exception in OSV scan: {e}")
            return self.result

    def _parse_vulnerabilities(self, data: dict) -> list[Vulnerability]:
        """Parse OSV JSON output."""
        vulns = []
        results = data.get("results", [])

        for result in results:
            packages = result.get("packages", [])
            for pkg in packages:
                pkg_name = pkg.get("package", {}).get("name", "")
                vulnerabilities = pkg.get("vulnerabilities", [])

                for vuln_data in vulnerabilities:
                    severity_str = vuln_data.get("severity", "unknown").lower()
                    severity = Severity(severity_str) if severity_str in Severity.__members__ else Severity.UNKNOWN

                    vuln = Vulnerability(
                        id=vuln_data.get("id", ""),
                        package=pkg_name,
                        severity=severity,
                        cvss_score=float(vuln_data.get("cvss", 0.0)) if vuln_data.get("cvss") else 0.0,
                        description=vuln_data.get("summary", ""),
                        fixed_version="",
                        current_version="",
                        advisory=vuln_data.get("database_specific", {}).get("source", "")
                    )
                    vulns.append(vuln)

        return vulns
