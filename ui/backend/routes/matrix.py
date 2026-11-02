"""Dependency and upgrade matrix routes."""

from fastapi import APIRouter, HTTPException

from ui.backend.models import DependencyMatrixRow, UpgradeMatrixRow
from ui.backend.store import store

router = APIRouter(prefix="/api/runs", tags=["matrix"])


@router.get("/{run_id}/matrix/dependency", response_model=list[DependencyMatrixRow])
async def get_dependency_matrix(run_id: str):
    """Get dependency matrix.

    Args:
        run_id: Run identifier

    Returns:
        List of DependencyMatrixRow objects
    """
    run = store.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    rows = []
    for pkg_name, pkg_data in run.dep_matrix.items():
        repos = pkg_data.get("repos", [])
        versions = pkg_data.get("versions", {})

        # Check for version conflicts
        all_versions = set()
        for version_list in versions.values():
            all_versions.update(version_list)

        has_conflict = len(all_versions) > 1

        rows.append(
            DependencyMatrixRow(
                package=pkg_name,
                repos=sorted(list(repos)),
                versions=versions,
                has_conflict=has_conflict,
            )
        )

    return sorted(rows, key=lambda r: r.package)


@router.get("/{run_id}/matrix/upgrade", response_model=list[UpgradeMatrixRow])
async def get_upgrade_matrix(run_id: str):
    """Get upgrade matrix.

    Args:
        run_id: Run identifier

    Returns:
        List of UpgradeMatrixRow objects
    """
    run = store.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    rows = []
    for pkg_name, upgrade_data in run.upgrade_matrix.items():
        cves = upgrade_data.get("cves", [])

        rows.append(
            UpgradeMatrixRow(
                package=pkg_name,
                current_version=upgrade_data.get("current_version", "unknown"),
                safe_version=upgrade_data.get("safe_version", "N/A"),
                severity=upgrade_data.get("severity", "unknown"),
                cvss_score=upgrade_data.get("cvss_score", 0.0),
                cve_count=len(cves),
                cves=cves,
            )
        )

    # Sort by severity (critical first) then CVSS
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "unknown": 4}
    rows.sort(
        key=lambda r: (severity_order.get(r.severity.lower(), 999), -r.cvss_score, r.package)
    )

    return rows
