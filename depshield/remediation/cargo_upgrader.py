"""Rust remediation using cargo-audit and cargo update."""

import logging
from pathlib import Path

from depshield.models import RemediationResult, RepoManifest
from depshield.remediation.base import BaseRemediator

logger = logging.getLogger(__name__)


class CargoRemediator(BaseRemediator):
    """Remediate Rust projects using cargo-audit."""

    def remediate(self, dry_run: bool = True) -> RemediationResult:
        """Remediate Rust dependencies.

        Args:
            dry_run: If True, only report without applying changes

        Returns:
            RemediationResult with upgrade summary
        """
        try:
            cargo_toml = self.repo.path / "Cargo.toml"

            if not cargo_toml.exists():
                self.result.error = "No Cargo.toml found"
                return self.result

            if not dry_run:
                self._create_stash()

            # Check for vulnerabilities
            cmd = ["cargo", "audit"]
            stdout, stderr, rc = self._run_command(cmd, check=False)

            if not dry_run:
                # Update dependencies
                cmd = ["cargo", "update"]
                self._run_command(cmd, check=False)

                build_ok, test_ok = self._build_and_test()
                self.result.build_succeeded = build_ok
                self.result.test_succeeded = test_ok

                if not build_ok or not test_ok:
                    self._pop_stash()
                    self.result.error = f"Build: {build_ok}, Tests: {test_ok}"
                    return self.result

            self.result.recipes_applied.append("cargo-audit")
            self.result.success = True
            logger.info("Rust remediation succeeded")

            return self.result

        except Exception as e:
            self.result.error = f"Rust remediation error: {str(e)}"
            logger.error(f"Exception in Rust remediation: {e}")
            return self.result
