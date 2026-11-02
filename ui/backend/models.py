"""Pydantic API response models."""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    """Request to start a new scan run."""

    repos: list[str] = Field(..., description="List of repository paths")
    output_dir: str = Field(default="./depshield-output", description="Output directory")
    dry_run: bool = Field(default=True, description="Run in dry-run mode")
    apply: bool = Field(default=False, description="Apply remediations")
    ecosystems: list[str] = Field(
        default=["jvm", "python", "javascript", "go", "rust"],
        description="Ecosystems to scan"
    )


class VulnerabilityResponse(BaseModel):
    """Vulnerability response model."""

    id: str
    package: str
    severity: str
    cvss_score: float
    description: str
    fixed_version: str
    current_version: str
    advisory: str
    repo_name: Optional[str] = None


class DependencyMatrixRow(BaseModel):
    """Dependency matrix row."""

    package: str
    repos: list[str]
    versions: dict[str, list[str]]
    has_conflict: bool


class UpgradeMatrixRow(BaseModel):
    """Upgrade matrix row."""

    package: str
    current_version: str
    safe_version: str
    severity: str
    cvss_score: float
    cve_count: int
    cves: list[str]


class RepoStatus(BaseModel):
    """Per-repo status."""

    name: str
    ecosystems: list[str]
    dependency_count: int
    vulnerability_count: int
    critical_count: int
    high_count: int
    build_succeeded: Optional[bool] = None
    test_succeeded: Optional[bool] = None


class RunResponse(BaseModel):
    """Complete run response."""

    id: str
    repos: list[str]
    output_dir: str
    dry_run: bool
    apply: bool
    ecosystems: list[str]
    status: Literal["pending", "running", "done", "error"]
    started_at: datetime
    finished_at: Optional[datetime] = None
    error_message: Optional[str] = None
    logs: list[str]
    total_dependencies: int
    total_vulnerabilities: int
    repo_statuses: list[RepoStatus] = Field(default_factory=list)


class RunSummary(BaseModel):
    """Brief run summary for list view."""

    id: str
    repos: list[str]
    status: Literal["pending", "running", "done", "error"]
    started_at: datetime
    finished_at: Optional[datetime] = None
    total_repos: int
    total_dependencies: int
    total_vulnerabilities: int


class LogMessage(BaseModel):
    """Log message for SSE."""

    line: str
    timestamp: datetime
