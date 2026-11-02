"""Tests for repository discovery."""

import tempfile
from pathlib import Path

import pytest

from depshield.discovery import RepositoryDiscovery
from depshield.models import Ecosystem


def test_discover_jvm_repo():
    """Test JVM repository discovery."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)

        # Create Maven marker
        (repo_path / "pom.xml").write_text("<project></project>")

        repos = RepositoryDiscovery.discover_repos([str(repo_path)])

        assert len(repos) == 1
        assert Ecosystem.JVM in repos[0].ecosystems
        assert repos[0].build_command == "mvn clean package"
        assert repos[0].test_command == "mvn test"


def test_discover_python_repo():
    """Test Python repository discovery."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)

        # Create Python marker
        (repo_path / "pyproject.toml").write_text("[tool.poetry]")

        repos = RepositoryDiscovery.discover_repos([str(repo_path)])

        assert len(repos) == 1
        assert Ecosystem.PYTHON in repos[0].ecosystems
        assert "pytest" in repos[0].test_command


def test_discover_javascript_repo():
    """Test JavaScript repository discovery."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)

        # Create npm marker
        (repo_path / "package.json").write_text("{}")

        repos = RepositoryDiscovery.discover_repos([str(repo_path)])

        assert len(repos) == 1
        assert Ecosystem.JAVASCRIPT in repos[0].ecosystems
        assert "npm" in repos[0].build_command


def test_discover_multiple_repos():
    """Test discovering multiple repositories."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Create JVM repo
        jvm_repo = tmpdir_path / "jvm-app"
        jvm_repo.mkdir()
        (jvm_repo / "pom.xml").write_text("<project></project>")

        # Create Python repo
        py_repo = tmpdir_path / "py-app"
        py_repo.mkdir()
        (py_repo / "pyproject.toml").write_text("[tool.poetry]")

        repos = RepositoryDiscovery.discover_repos([str(jvm_repo), str(py_repo)])

        assert len(repos) == 2
        assert any(Ecosystem.JVM in r.ecosystems for r in repos)
        assert any(Ecosystem.PYTHON in r.ecosystems for r in repos)


def test_discover_nonexistent_repo():
    """Test handling of nonexistent repository."""
    repos = RepositoryDiscovery.discover_repos(["/nonexistent/path"])
    assert len(repos) == 0
