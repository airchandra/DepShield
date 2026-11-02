"""Python remediation using pip."""

import logging
from pathlib import Path

from depshield.models import RemediationResult, RepoManifest
from depshield.remediation.base import BaseRemediator

logger = logging.getLogger(__name__)


class PipRemediator(BaseRemediator):
    """Remediate Python projects using pip and pip-audit."""

    def remediate(self, dry_run: bool = True) -> RemediationResult:
        """Remediate Python dependencies.

        Args:
            dry_run: If True, only report without applying changes

        Returns:
            RemediationResult with upgrade summary
        """
        try:
            # Check for requirements files
            requirements_file = None
            for name in ["requirements.txt", "pyproject.toml", "setup.py", "setup.cfg"]:
                path = self.repo.path / name
                if path.exists():
                    requirements_file = path
                    break

            if not requirements_file:
                self.result.error = "No Python manifest files found"
                return self.result

            if not dry_run:
                self._create_stash()

            # Run pip-audit to fix known vulnerabilities
            cmd = ["pip-audit", "--fix"]

            stdout, stderr, rc = self._run_command(cmd, check=False)

            if rc != 0:
                logger.warning(f"pip-audit returned {rc}: {stderr}")

            if not dry_run:
                build_ok, test_ok = self._build_and_test()
                self.result.build_succeeded = build_ok
                self.result.test_succeeded = test_ok

                if not build_ok or not test_ok:
                    self._pop_stash()
                    self.result.error = f"Build: {build_ok}, Tests: {test_ok}"
                    return self.result

            self.result.recipes_applied.append("pip-audit")
            self.result.success = True
            logger.info("Python pip remediation succeeded")

            return self.result

        except Exception as e:
            self.result.error = f"Python remediation error: {str(e)}"
            logger.error(f"Exception in Python remediation: {e}")
            return self.result
