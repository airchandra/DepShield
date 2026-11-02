"""Tests for dependency and upgrade matrices."""

import pytest

from depshield.matrix.dependency_matrix import DependencyMatrix
from depshield.matrix.upgrade_matrix import UpgradeMatrix
from depshield.models import Dependency, Ecosystem, RemediationResult, RepoManifest, Severity, Vulnerability


def test_dependency_matrix_single_repo():
    """Test dependency matrix with single repository."""
    repo = RepoManifest(
        path="/repo1",
        name="repo1",
        ecosystems=[Ecosystem.PYTHON],
        dependencies=[
            Dependency(name="requests", version="2.28.0", ecosystem=Ecosystem.PYTHON),
            Dependency(name="numpy", version="1.23.0", ecosystem=Ecosystem.PYTHON),
        ]
    )

    matrix = DependencyMatrix([repo])
    matrix.build()

    assert len(matrix.matrix) == 2
    assert "requests" in matrix.matrix
    assert "numpy" in matrix.matrix


def test_dependency_matrix_shared_deps():
    """Test dependency matrix with shared dependencies."""
    repo1 = RepoManifest(
        path="/repo1",
        name="repo1",
        ecosystems=[Ecosystem.PYTHON],
        dependencies=[
            Dependency(name="requests", version="2.28.0", ecosystem=Ecosystem.PYTHON),
        ]
    )
    repo2 = RepoManifest(
        path="/repo2",
        name="repo2",
        ecosystems=[Ecosystem.PYTHON],
        dependencies=[
            Dependency(name="requests", version="2.28.1", ecosystem=Ecosystem.PYTHON),
        ]
    )

    matrix = DependencyMatrix([repo1, repo2])
    matrix.build()

    shared = matrix.get_shared_dependencies()
    assert "requests" in shared
    assert len(shared["requests"].repos) == 2


def test_dependency_matrix_conflicts():
    """Test detecting version conflicts."""
    repo1 = RepoManifest(
        path="/repo1",
        name="repo1",
        ecosystems=[Ecosystem.PYTHON],
        dependencies=[
            Dependency(name="django", version="3.2.0", ecosystem=Ecosystem.PYTHON),
        ]
    )
    repo2 = RepoManifest(
        path="/repo2",
        name="repo2",
        ecosystems=[Ecosystem.PYTHON],
        dependencies=[
            Dependency(name="django", version="4.0.0", ecosystem=Ecosystem.PYTHON),
        ]
    )

    matrix = DependencyMatrix([repo1, repo2])
    matrix.build()

    conflicts = matrix.get_version_conflicts()
    assert "django" in conflicts
    assert len(conflicts["django"]["unique_versions"]) == 2


def test_upgrade_matrix_single_vuln():
    """Test upgrade matrix with single vulnerability."""
    vuln = Vulnerability(
        id="CVE-2022-1234",
        package="log4j",
        severity=Severity.CRITICAL,
        cvss_score=9.8,
        current_version="2.14.0",
        fixed_version="2.17.1"
    )

    matrix = UpgradeMatrix([vuln])
    matrix.build()

    assert "log4j" in matrix.recommendations
    assert matrix.recommendations["log4j"].safe_version == "2.17.1"
    assert matrix.recommendations["log4j"].severity_level == "critical"


def test_upgrade_matrix_critical_and_high():
    """Test filtering critical and high severity."""
    vulns = [
        Vulnerability(
            id="CVE-1",
            package="pkg1",
            severity=Severity.CRITICAL,
            fixed_version="1.1.0"
        ),
        Vulnerability(
            id="CVE-2",
            package="pkg2",
            severity=Severity.HIGH,
            fixed_version="2.1.0"
        ),
        Vulnerability(
            id="CVE-3",
            package="pkg3",
            severity=Severity.LOW,
            fixed_version="3.1.0"
        ),
    ]

    matrix = UpgradeMatrix(vulns)
    matrix.build()

    critical_high = matrix.get_critical_and_high()
    assert len(critical_high) == 2
    assert "pkg1" in critical_high
    assert "pkg2" in critical_high
    assert "pkg3" not in critical_high


def test_upgrade_matrix_markdown_format():
    """Test markdown formatting of upgrade matrix."""
    vuln = Vulnerability(
        id="CVE-2022-1234",
        package="requests",
        severity=Severity.HIGH,
        cvss_score=7.5,
        current_version="2.27.0",
        fixed_version="2.28.0"
    )

    matrix = UpgradeMatrix([vuln])
    matrix.build()

    markdown = matrix.format_as_markdown()
    assert "requests" in markdown
    assert "2.27.0" in markdown
    assert "2.28.0" in markdown
    assert "7.5" in markdown
