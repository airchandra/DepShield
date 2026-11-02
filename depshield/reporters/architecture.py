"""Generate architecture documentation."""

import logging
from typing import List

from depshield.models import RepoManifest

logger = logging.getLogger(__name__)


class ArchitectureReporter:
    """Generate architecture documentation."""

    @staticmethod
    def format_system_architecture(repos: List[RepoManifest]) -> str:
        """Format system architecture overview.

        Args:
            repos: List of repositories

        Returns:
            Markdown-formatted architecture document
        """
        lines = [
            "# System Architecture\n",
            "## Overview\n",
            f"This distributed system consists of {len(repos)} components:\n",
        ]

        # Repo details
        for repo in sorted(repos, key=lambda r: r.name):
            ecosystems = ", ".join([e.value for e in repo.ecosystems])
            lines.append(f"### {repo.name}")
            lines.append(f"- **Path**: {repo.path}")
            lines.append(f"- **Ecosystems**: {ecosystems}")
            lines.append(f"- **Dependencies**: {len(repo.dependencies)}")
            if repo.build_command:
                lines.append(f"- **Build**: `{repo.build_command}`")
            if repo.test_command:
                lines.append(f"- **Test**: `{repo.test_command}`")
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def format_component_diagram(repos: List[RepoManifest]) -> str:
        """Format C4 component diagram for entire system.

        Args:
            repos: List of repositories

        Returns:
            Mermaid C4 diagram
        """
        lines = [
            "## System Components (C4 Model)\n",
            "```mermaid",
            "graph TB",
            "    System[Distributed System]",
        ]

        for repo in repos:
            safe_name = repo.name.replace("-", "_").replace(" ", "_")
            lines.append(f"    {safe_name}[{repo.name}]")
            lines.append(f"    System --> {safe_name}")

        lines.append("```\n")
        return "\n".join(lines)

    @staticmethod
    def format_dependency_relationships(repos: List[RepoManifest]) -> str:
        """Format inter-repository dependency relationships.

        Args:
            repos: List of repositories

        Returns:
            Markdown-formatted dependency relationships
        """
        lines = ["## Dependency Relationships\n"]

        # Build a map of packages to repos
        pkg_to_repos = {}
        for repo in repos:
            for dep in repo.dependencies:
                if dep.name not in pkg_to_repos:
                    pkg_to_repos[dep.name] = []
                pkg_to_repos[dep.name].append((repo.name, dep.version))

        # Find shared dependencies
        shared = {pkg: repos for pkg, repos in pkg_to_repos.items() if len(repos) > 1}

        if shared:
            lines.append("### Shared Dependencies\n")
            lines.append("| Package | Used By | Versions |")
            lines.append("|---------|---------|----------|")

            for pkg in sorted(shared.keys()):
                repos_using = shared[pkg]
                repos_str = ", ".join([r[0] for r in repos_using])
                versions_str = ", ".join(set([r[1] for r in repos_using]))
                lines.append(f"| {pkg} | {repos_str} | {versions_str} |")
            lines.append("")

        return "\n".join(lines)
