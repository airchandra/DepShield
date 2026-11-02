"""Base scanner abstraction."""

import json
import logging
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from depshield.models import RepoManifest, ScanResult

logger = logging.getLogger(__name__)


class BaseScanner(ABC):
    """Abstract base class for vulnerability scanners."""

    def __init__(self, repo: RepoManifest, config):
        """Initialize scanner.

        Args:
            repo: Repository manifest
            config: DepShield configuration
        """
        self.repo = repo
        self.config = config
        self.result = ScanResult(repo=repo)

    @abstractmethod
    def scan(self) -> ScanResult:
        """Execute the scan and return results."""
        pass

    def _run_command(self, cmd: list[str], cwd: Optional[Path] = None) -> tuple[str, str, int]:
        """Run a shell command and capture output.

        Args:
            cmd: Command and arguments
            cwd: Working directory (defaults to repo path)

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
                timeout=300
            )
            return proc.stdout, proc.stderr, proc.returncode
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {' '.join(cmd)}")
            return "", "Timeout", -1
        except Exception as e:
            logger.error(f"Command failed: {e}")
            return "", str(e), -1

    def _parse_json_output(self, text: str) -> dict:
        """Safely parse JSON output."""
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON: {e}")
            return {}
