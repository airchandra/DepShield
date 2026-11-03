"""Base remediation abstraction."""

import logging
import shlex
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from depshield.models import RemediationResult, RepoManifest

logger = logging.getLogger(__name__)


class BaseRemediator(ABC):
    """Abstract base class for dependency remediators."""

    def __init__(self, repo: RepoManifest, config):
        """Initialize remediator.

        Args:
            repo: Repository manifest
            config: DepShield configuration
        """
        self.repo = repo
        self.config = config
        self.result = RemediationResult(repo=repo)

    @abstractmethod
    def remediate(self, dry_run: bool = True) -> RemediationResult:
        """Execute remediation and return results."""
        pass

    def _run_command(
        self,
        cmd: list[str],
        cwd: Optional[Path] = None,
        check: bool = False
    ) -> tuple[str, str, int]:
        """Run a shell command and capture output.

        Args:
            cmd: Command and arguments
            cwd: Working directory (defaults to repo path)
            check: Raise on non-zero exit code

        Returns:
            (stdout, stderr, return_code)
        """
        if cwd is None:
            cwd = self.repo.path

        try:
            proc = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=600,
                check=check
            )
            return proc.stdout, proc.stderr, proc.returncode
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {' '.join(cmd)}")
            return "", "Timeout", -1
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed with code {e.returncode}")
            return e.stdout, e.stderr, e.returncode
        except Exception as e:
            logger.error(f"Command failed: {e}")
            return "", str(e), -1

    def _create_stash(self) -> bool:
        """Create a git stash for rollback."""
        try:
            stdout, stderr, rc = self._run_command(["git", "stash"])
            return rc == 0
        except Exception as e:
            logger.warning(f"Failed to create stash: {e}")
            return False

    def _pop_stash(self) -> bool:
        """Pop the stash to rollback changes."""
        try:
            stdout, stderr, rc = self._run_command(["git", "stash", "pop"])
            return rc == 0
        except Exception as e:
            logger.warning(f"Failed to pop stash: {e}")
            return False

    def _build_and_test(self) -> tuple[bool, bool]:
        """Attempt to build and test after remediation.

        Returns:
            (build_succeeded, test_succeeded)
        """
        build_ok = True
        test_ok = True

        if self.repo.build_command:
            _, stderr, rc = self._run_command(shlex.split(self.repo.build_command))
            build_ok = rc == 0
            if not build_ok:
                logger.warning(f"Build failed: {stderr}")

        if self.repo.test_command:
            _, stderr, rc = self._run_command(shlex.split(self.repo.test_command))
            test_ok = rc == 0
            if not test_ok:
                logger.warning(f"Tests failed: {stderr}")

        return build_ok, test_ok
