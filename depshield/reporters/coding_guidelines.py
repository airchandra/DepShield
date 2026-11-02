"""Generate coding guidelines from detected conventions."""

import logging
from typing import List

from depshield.models import RepoManifest

logger = logging.getLogger(__name__)


class CodingGuidelinesReporter:
    """Generate coding guidelines from repository analysis."""

    @staticmethod
    def detect_conventions(repos: List[RepoManifest]) -> dict:
        """Detect coding conventions from repositories.

        Args:
            repos: List of repositories

        Returns:
            Dictionary of detected conventions
        """
        conventions = {
            "build_tools": set(),
            "test_frameworks": set(),
            "languages": set(),
            "ci_systems": set(),
        }

        for repo in repos:
            for ecosystem in repo.ecosystems:
                conventions["languages"].add(ecosystem.value)

            # Detect from commands
            if repo.build_command:
                if "mvn" in repo.build_command:
                    conventions["build_tools"].add("Maven")
                elif "gradle" in repo.build_command:
                    conventions["build_tools"].add("Gradle")
                elif "npm" in repo.build_command:
                    conventions["build_tools"].add("npm")
                elif "go build" in repo.build_command:
                    conventions["build_tools"].add("Go")
                elif "cargo" in repo.build_command:
                    conventions["build_tools"].add("Cargo")

            if repo.test_command:
                if "pytest" in repo.test_command:
                    conventions["test_frameworks"].add("pytest")
                elif "jest" in repo.test_command:
                    conventions["test_frameworks"].add("Jest")
                elif "junit" in repo.test_command:
                    conventions["test_frameworks"].add("JUnit")
                elif "go test" in repo.test_command:
                    conventions["test_frameworks"].add("Go Testing")

        return {k: sorted(list(v)) for k, v in conventions.items()}

    @staticmethod
    def format_guidelines(repos: List[RepoManifest]) -> str:
        """Format coding guidelines as Markdown.

        Args:
            repos: List of repositories

        Returns:
            Markdown-formatted coding guidelines
        """
        conventions = CodingGuidelinesReporter.detect_conventions(repos)

        lines = [
            "# Coding Guidelines\n",
            "## Detected Conventions\n",
        ]

        if conventions["languages"]:
            lines.append(f"### Languages")
            for lang in conventions["languages"]:
                lines.append(f"- {lang}")
            lines.append("")

        if conventions["build_tools"]:
            lines.append(f"### Build Tools")
            for tool in conventions["build_tools"]:
                lines.append(f"- {tool}")
            lines.append("")

        if conventions["test_frameworks"]:
            lines.append(f"### Testing Frameworks")
            for framework in conventions["test_frameworks"]:
                lines.append(f"- {framework}")
            lines.append("")

        # General guidelines
        lines.extend([
            "## General Guidelines\n",
            "- Run full test suite before committing changes",
            "- Use semantic versioning for releases",
            "- Keep dependencies up-to-date with security patches",
            "- Document public APIs and architecture decisions",
            "- Ensure CI/CD pipelines pass before merging",
            "- Use consistent formatting across the codebase",
            ""
        ])

        return "\n".join(lines)
