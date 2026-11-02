"""Build a cross-repo dependency matrix."""

import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Set

from depshield.models import RepoManifest, Vulnerability

logger = logging.getLogger(__name__)


@dataclass
class DependencyEntry:
    """A dependency used across repos."""
    name: str
    versions: Dict[str, List[str]]  # {repo_path: [versions]}
    repos: Set[str]  # unique repo names using it


class DependencyMatrix:
    """Build and analyze cross-repo dependencies."""

    def __init__(self, repos: List[RepoManifest]):
        """Initialize with scanned repositories.

        Args:
            repos: List of RepoManifest objects
        """
        self.repos = repos
        self.matrix: Dict[str, DependencyEntry] = {}

    def build(self) -> Dict[str, DependencyEntry]:
        """Build the dependency matrix.

        Returns:
            Dictionary mapping dependency name to DependencyEntry
        """
        deps_by_name = defaultdict(lambda: {"versions": defaultdict(set), "repos": set()})

        for repo in self.repos:
            for dep in repo.dependencies:
                deps_by_name[dep.name]["versions"][str(repo.path)].add(dep.version)
                deps_by_name[dep.name]["repos"].add(repo.name)

        # Convert to DependencyEntry objects
        for name, data in deps_by_name.items():
            versions_dict = {k: list(v) for k, v in data["versions"].items()}
            self.matrix[name] = DependencyEntry(
                name=name,
                versions=versions_dict,
                repos=data["repos"]
            )

        return self.matrix

    def get_shared_dependencies(self) -> Dict[str, DependencyEntry]:
        """Get dependencies used by multiple repos.

        Returns:
            Dictionary of shared dependencies (used by 2+ repos)
        """
        return {
            name: entry
            for name, entry in self.matrix.items()
            if len(entry.repos) > 1
        }

    def get_version_conflicts(self) -> Dict[str, Dict]:
        """Identify dependencies with different versions across repos.

        Returns:
            Dictionary mapping dep name to conflict info
        """
        conflicts = {}
        for name, entry in self.matrix.items():
            if len(entry.repos) < 2:
                continue

            all_versions = set()
            for versions in entry.versions.values():
                all_versions.update(versions)

            if len(all_versions) > 1:
                conflicts[name] = {
                    "versions": entry.versions,
                    "unique_versions": sorted(all_versions)
                }

        return conflicts

    def format_as_markdown(self) -> str:
        """Format matrix as Markdown table.

        Returns:
            Markdown-formatted dependency matrix
        """
        if not self.matrix:
            return "# Dependency Matrix\n\nNo dependencies found.\n"

        lines = ["# Dependency Matrix\n"]
        lines.append("| Dependency | Repos | Versions |")
        lines.append("|-----------|-------|----------|")

        for name in sorted(self.matrix.keys()):
            entry = self.matrix[name]
            repos_str = ", ".join(sorted(entry.repos))
            versions_str = "; ".join([
                f"{repo}: {', '.join(sorted(vers))}"
                for repo, vers in sorted(entry.versions.items())
            ])
            lines.append(f"| {name} | {repos_str} | {versions_str} |")

        return "\n".join(lines)
