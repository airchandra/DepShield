"""Repository discovery and ecosystem detection."""

import logging
from pathlib import Path
from typing import List

from depshield.models import Ecosystem, RepoManifest

logger = logging.getLogger(__name__)


class RepositoryDiscovery:
    """Discover and analyze repositories."""

    @staticmethod
    def discover_repos(repo_paths: List[str]) -> List[RepoManifest]:
        """Discover and analyze repositories.

        Args:
            repo_paths: List of repository paths

        Returns:
            List of RepoManifest objects
        """
        repos = []

        for repo_path in repo_paths:
            repo_path_obj = Path(repo_path).resolve()

            if not repo_path_obj.exists():
                logger.warning(f"Repository path does not exist: {repo_path}")
                continue

            if not repo_path_obj.is_dir():
                logger.warning(f"Repository path is not a directory: {repo_path}")
                continue

            # Detect ecosystems
            ecosystems = RepositoryDiscovery._detect_ecosystems(repo_path_obj)

            if not ecosystems:
                logger.warning(f"No supported ecosystems detected in {repo_path}")
                continue

            # Detect commands
            build_cmd = RepositoryDiscovery._detect_build_command(repo_path_obj)
            test_cmd = RepositoryDiscovery._detect_test_command(repo_path_obj)
            lint_cmd = RepositoryDiscovery._detect_lint_command(repo_path_obj)

            repo = RepoManifest(
                path=repo_path_obj,
                name=repo_path_obj.name,
                ecosystems=ecosystems,
                build_command=build_cmd,
                test_command=test_cmd,
                lint_command=lint_cmd,
            )

            repos.append(repo)
            logger.info(f"Discovered repo: {repo.name} ({', '.join([e.value for e in ecosystems])})")

        return repos

    @staticmethod
    def _detect_ecosystems(repo_path: Path) -> List[Ecosystem]:
        """Detect supported ecosystems in repository.

        Args:
            repo_path: Repository path

        Returns:
            List of detected Ecosystem enums
        """
        ecosystems = []

        # Check for ecosystem markers
        checks = [
            ("pom.xml", Ecosystem.JVM),
            ("build.gradle", Ecosystem.JVM),
            ("build.gradle.kts", Ecosystem.JVM),
            ("package.json", Ecosystem.JAVASCRIPT),
            ("package-lock.json", Ecosystem.JAVASCRIPT),
            ("pyproject.toml", Ecosystem.PYTHON),
            ("requirements.txt", Ecosystem.PYTHON),
            ("setup.py", Ecosystem.PYTHON),
            ("go.mod", Ecosystem.GO),
            ("Cargo.toml", Ecosystem.RUST),
        ]

        for filename, ecosystem in checks:
            if (repo_path / filename).exists():
                if ecosystem not in ecosystems:
                    ecosystems.append(ecosystem)

        return ecosystems

    @staticmethod
    def _detect_build_command(repo_path: Path) -> str:
        """Detect build command for repository.

        Args:
            repo_path: Repository path

        Returns:
            Build command string or empty string
        """
        # Check for Maven
        if (repo_path / "pom.xml").exists():
            return "mvn clean package"

        # Check for Gradle
        if (repo_path / "build.gradle").exists() or (repo_path / "build.gradle.kts").exists():
            return "./gradlew build"

        # Check for npm
        if (repo_path / "package.json").exists():
            return "npm run build"

        # Check for Go
        if (repo_path / "go.mod").exists():
            return "go build ./..."

        # Check for Rust
        if (repo_path / "Cargo.toml").exists():
            return "cargo build"

        # Check for Python
        if (repo_path / "setup.py").exists():
            return "python setup.py build"

        return ""

    @staticmethod
    def _detect_test_command(repo_path: Path) -> str:
        """Detect test command for repository.

        Args:
            repo_path: Repository path

        Returns:
            Test command string or empty string
        """
        # Check for Maven
        if (repo_path / "pom.xml").exists():
            return "mvn test"

        # Check for Gradle
        if (repo_path / "build.gradle").exists() or (repo_path / "build.gradle.kts").exists():
            return "./gradlew test"

        # Check for npm
        if (repo_path / "package.json").exists():
            return "npm test"

        # Check for Go
        if (repo_path / "go.mod").exists():
            return "go test ./..."

        # Check for Rust
        if (repo_path / "Cargo.toml").exists():
            return "cargo test"

        # Check for Python
        if (repo_path / "pyproject.toml").exists() or (repo_path / "setup.py").exists():
            return "pytest"

        return ""

    @staticmethod
    def _detect_lint_command(repo_path: Path) -> str:
        """Detect lint command for repository.

        Args:
            repo_path: Repository path

        Returns:
            Lint command string or empty string
        """
        # Check for Maven
        if (repo_path / "pom.xml").exists():
            return "mvn checkstyle:check"

        # Check for npm
        if (repo_path / "package.json").exists():
            return "npm run lint"

        # Check for Rust
        if (repo_path / "Cargo.toml").exists():
            return "cargo clippy"

        # Check for Go
        if (repo_path / "go.mod").exists():
            return "golangci-lint run"

        return ""
