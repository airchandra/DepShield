"""In-memory run state store."""

import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional

logger = logging.getLogger(__name__)


@dataclass
class RunState:
    """Represents a single scan run."""

    id: str
    repos: list[str]
    output_dir: str
    dry_run: bool
    apply: bool
    ecosystems: list[str]
    status: Literal["pending", "running", "done", "error"]
    started_at: datetime
    finished_at: Optional[datetime] = None
    logs: list[str] = field(default_factory=list)
    error_message: Optional[str] = None
    scan_results: list[dict] = field(default_factory=list)
    remediation_results: list[dict] = field(default_factory=list)
    dep_matrix: dict = field(default_factory=dict)
    upgrade_matrix: dict = field(default_factory=dict)
    total_dependencies: int = 0
    total_vulnerabilities: int = 0


class RunStore:
    """In-memory store for run states."""

    def __init__(self):
        """Initialize store."""
        self.runs: dict[str, RunState] = {}

    def create(
        self,
        run_id: str,
        repos: list[str],
        output_dir: str,
        dry_run: bool,
        apply: bool,
        ecosystems: list[str],
    ) -> RunState:
        """Create a new run state.

        Args:
            run_id: Unique run identifier
            repos: List of repository paths
            output_dir: Output directory for reports
            dry_run: Whether to run in dry-run mode
            apply: Whether to apply remediations
            ecosystems: List of ecosystems to scan

        Returns:
            Created RunState
        """
        run = RunState(
            id=run_id,
            repos=repos,
            output_dir=output_dir,
            dry_run=dry_run,
            apply=apply,
            ecosystems=ecosystems,
            status="pending",
            started_at=datetime.now(),
        )
        self.runs[run_id] = run
        logger.info(f"Created run {run_id}")
        return run

    def get(self, run_id: str) -> Optional[RunState]:
        """Get a run by ID.

        Args:
            run_id: Run identifier

        Returns:
            RunState or None
        """
        return self.runs.get(run_id)

    def list_all(self) -> list[RunState]:
        """List all runs.

        Returns:
            List of RunState objects
        """
        return list(self.runs.values())

    def update_status(self, run_id: str, status: Literal["pending", "running", "done", "error"]):
        """Update run status.

        Args:
            run_id: Run identifier
            status: New status
        """
        if run := self.runs.get(run_id):
            run.status = status
            if status == "done" and run.finished_at is None:
                run.finished_at = datetime.now()

    def append_log(self, run_id: str, line: str):
        """Append a log line.

        Args:
            run_id: Run identifier
            line: Log line to append
        """
        if run := self.runs.get(run_id):
            run.logs.append(line)

    def set_error(self, run_id: str, error: str):
        """Set error message.

        Args:
            run_id: Run identifier
            error: Error message
        """
        if run := self.runs.get(run_id):
            run.error_message = error
            run.status = "error"
            run.finished_at = datetime.now()

    def set_results(
        self,
        run_id: str,
        scan_results: list[dict],
        remediation_results: list[dict],
        dep_matrix: dict,
        upgrade_matrix: dict,
        total_dependencies: int,
        total_vulnerabilities: int,
    ):
        """Set pipeline results.

        Args:
            run_id: Run identifier
            scan_results: Serialized scan results
            remediation_results: Serialized remediation results
            dep_matrix: Dependency matrix data
            upgrade_matrix: Upgrade matrix data
            total_dependencies: Total dependency count
            total_vulnerabilities: Total vulnerability count
        """
        if run := self.runs.get(run_id):
            run.scan_results = scan_results
            run.remediation_results = remediation_results
            run.dep_matrix = dep_matrix
            run.upgrade_matrix = upgrade_matrix
            run.total_dependencies = total_dependencies
            run.total_vulnerabilities = total_vulnerabilities

    def to_dict(self, run: RunState) -> dict:
        """Convert run to dictionary for JSON serialization.

        Args:
            run: RunState to convert

        Returns:
            Dictionary representation
        """
        data = asdict(run)
        data["started_at"] = run.started_at.isoformat()
        data["finished_at"] = run.finished_at.isoformat() if run.finished_at else None
        return data


# Global store instance
store = RunStore()
