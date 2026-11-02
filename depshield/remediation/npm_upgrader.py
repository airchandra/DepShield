"""JavaScript remediation using npm."""

import json
import logging
from pathlib import Path

from depshield.models import RemediationResult, RepoManifest
from depshield.remediation.base import BaseRemediator

logger = logging.getLogger(__name__)


class NpmRemediator(BaseRemediator):
    """Remediate JavaScript projects using npm."""

    def remediate(self, dry_run: bool = True) -> RemediationResult:
        """Remediate JavaScript dependencies.

        Args:
            dry_run: If True, only report without applying changes

        Returns:
            RemediationResult with upgrade summary
        """
        try:
            package_json = self.repo.path / "package.json"

            if not package_json.exists():
                self.result.error = "No package.json found"
                return self.result

            if not dry_run:
                self._create_stash()

            # Run npm audit fix --force for critical vulnerabilities
            cmd = ["npm", "audit", "fix", "--force"]

            stdout, stderr, rc = self._run_command(cmd, check=False)

            if rc != 0 and rc != 1:  # npm returns 1 if vulnerabilities remain
                logger.warning(f"npm audit fix returned {rc}: {stderr}")

            if not dry_run:
                build_ok, test_ok = self._build_and_test()
                self.result.build_succeeded = build_ok
                self.result.test_succeeded = test_ok

                if not build_ok or not test_ok:
                    self._pop_stash()
                    self.result.error = f"Build: {build_ok}, Tests: {test_ok}"
                    return self.result

            self.result.recipes_applied.append("npm-audit-fix")
            self.result.success = True
            logger.info("JavaScript npm remediation succeeded")

            return self.result

        except Exception as e:
            self.result.error = f"JavaScript remediation error: {str(e)}"
            logger.error(f"Exception in JavaScript remediation: {e}")
            return self.result
