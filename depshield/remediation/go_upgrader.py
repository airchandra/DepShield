"""Go remediation using govulncheck and go get."""

import logging
from pathlib import Path

from depshield.models import RemediationResult, RepoManifest
from depshield.remediation.base import BaseRemediator

logger = logging.getLogger(__name__)


class GoRemediator(BaseRemediator):
    """Remediate Go projects using govulncheck."""

    def remediate(self, dry_run: bool = True) -> RemediationResult:
        """Remediate Go dependencies.

        Args:
            dry_run: If True, only report without applying changes

        Returns:
            RemediationResult with upgrade summary
        """
        try:
            go_mod = self.repo.path / "go.mod"

            if not go_mod.exists():
                self.result.error = "No go.mod found"
                return self.result

            if not dry_run:
                self._create_stash()

            # Check for vulnerabilities
            cmd = ["govulncheck", "./..."]
            stdout, stderr, rc = self._run_command(cmd, check=False)

            if not dry_run:
                # Update Go modules (this will upgrade to latest compatible)
                cmd = ["go", "get", "-u"]
                self._run_command(cmd, check=False)

                build_ok, test_ok = self._build_and_test()
                self.result.build_succeeded = build_ok
                self.result.test_succeeded = test_ok

                if not build_ok or not test_ok:
                    self._pop_stash()
                    self.result.error = f"Build: {build_ok}, Tests: {test_ok}"
                    return self.result

            self.result.recipes_applied.append("govulncheck")
            self.result.success = True
            logger.info("Go remediation succeeded")

            return self.result

        except Exception as e:
            self.result.error = f"Go remediation error: {str(e)}"
            logger.error(f"Exception in Go remediation: {e}")
            return self.result
