"""Generate test case documentation."""

import logging
from typing import List

from depshield.models import Dependency, RepoManifest

logger = logging.getLogger(__name__)


class TestCasesReporter:
    """Generate test case documentation."""

    @staticmethod
    def format_test_cases(repos: List[RepoManifest]) -> str:
        """Format test cases as Markdown.

        Args:
            repos: List of repositories

        Returns:
            Markdown-formatted test cases
        """
        lines = [
            "# Test Cases\n",
            "## Testing Strategy\n",
            "This document outlines the testing approach for the distributed system.\n",
        ]

        # Per-repo test commands
        lines.append("## Per-Repository Tests\n")

        for repo in sorted(repos, key=lambda r: r.name):
            lines.append(f"### {repo.name}\n")

            if repo.test_command:
                lines.append(f"**Test Command**: `{repo.test_command}`\n")
            else:
                lines.append("No test command detected.\n")

            lines.append("**Test Coverage Areas**:")
            lines.append("- Unit tests for core functionality")
            lines.append("- Integration tests for inter-component communication")
            lines.append("- Dependency upgrade regression tests")
            lines.append("")

        # Dependency upgrade test recommendations
        lines.extend([
            "## Dependency Upgrade Testing\n",
            "When upgrading dependencies, ensure:\n",
            "1. Unit tests pass for all components",
            "2. Integration tests pass across repositories",
            "3. API contracts are maintained",
            "4. No breaking changes in public interfaces",
            "5. Performance benchmarks remain stable",
            ""
        ])

        return "\n".join(lines)

    @staticmethod
    def generate_test_matrix(repos: List[RepoManifest]) -> str:
        """Generate test execution matrix.

        Args:
            repos: List of repositories

        Returns:
            Markdown-formatted test matrix
        """
        lines = [
            "# Test Execution Matrix\n",
            "| Repository | Build | Unit Tests | Integration | Status |",
            "|-----------|-------|-----------|-------------|--------|",
        ]

        for repo in sorted(repos, key=lambda r: r.name):
            build_cmd = "Yes" if repo.build_command else "No"
            test_cmd = "Yes" if repo.test_command else "No"

            lines.append(f"| {repo.name} | {build_cmd} | {test_cmd} | Pending | ⏳ |")

        return "\n".join(lines)
