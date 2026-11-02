"""Data models for DepShield pipeline."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class Ecosystem(str, Enum):
    """Supported ecosystems."""
    JVM = "jvm"
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    GO = "go"
    RUST = "rust"


class Severity(str, Enum):
    """Vulnerability severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


@dataclass
class Vulnerability:
    """Represents a vulnerability."""
    id: str
    package: str
    severity: Severity
    cvss_score: float = 0.0
    description: str = ""
    fixed_version: str = ""
    current_version: str = ""
    advisory: str = ""


@dataclass
class Dependency:
    """Represents a dependency."""
    name: str
    version: str
    ecosystem: Ecosystem
    license: str = "Unknown"
    vulnerabilities: list[Vulnerability] = field(default_factory=list)


@dataclass
class RepoManifest:
    """Metadata about a scanned repository."""
    path: Path
    name: str
    ecosystems: list[Ecosystem]
    dependencies: list[Dependency] = field(default_factory=list)
    build_command: Optional[str] = None
    test_command: Optional[str] = None
    lint_command: Optional[str] = None


@dataclass
class ScanResult:
    """Result of a scan operation."""
    repo: RepoManifest
    timestamp: datetime = field(default_factory=datetime.now)
    sbom_path: Optional[Path] = None
    vulnerabilities: list[Vulnerability] = field(default_factory=list)
    success: bool = False
    error: Optional[str] = None


@dataclass
class RemediationResult:
    """Result of a remediation operation."""
    repo: RepoManifest
    timestamp: datetime = field(default_factory=datetime.now)
    upgraded_dependencies: dict[str, tuple[str, str]] = field(default_factory=dict)  # {name: (old, new)}
    recipes_applied: list[str] = field(default_factory=list)
    build_succeeded: bool = False
    test_succeeded: bool = False
    success: bool = False
    error: Optional[str] = None


@dataclass
class SystemSBOM:
    """System-wide SBOM combining all repos."""
    repos: list[RepoManifest] = field(default_factory=list)
    total_dependencies: int = 0
    total_vulnerabilities: int = 0
    generated_at: datetime = field(default_factory=datetime.now)
