"""SBOM generation using Syft."""

import logging
from pathlib import Path

from depshield.models import RepoManifest, ScanResult
from depshield.scanners.base import BaseScanner

logger = logging.getLogger(__name__)


class SyftScanner(BaseScanner):
    """Generate SBOM using Syft."""

    def scan(self) -> ScanResult:
        """Generate SBOM for the repository.

        Returns:
            ScanResult with SBOM path
        """
        try:
            # Create output directory
            sbom_dir = self.config.output_dir / "sbom"
            sbom_dir.mkdir(parents=True, exist_ok=True)

            sbom_file = sbom_dir / f"{self.repo.name}-sbom.json"

            cmd = [
                self.config.syft_path,
                str(self.repo.path),
                "-o", "cyclonedx-json",
                "--file", str(sbom_file)
            ]

            stdout, stderr, rc = self._run_command(cmd)

            if rc != 0:
                self.result.error = f"Syft failed: {stderr}"
                logger.error(f"Syft scan failed for {self.repo.name}: {stderr}")
                return self.result

            self.result.sbom_path = sbom_file
            self.result.success = True
            logger.info(f"Generated SBOM: {sbom_file}")

            return self.result

        except Exception as e:
            self.result.error = f"Syft scan error: {str(e)}"
            logger.error(f"Exception in Syft scan: {e}")
            return self.result
