"""Vulnerability query routes."""

from fastapi import APIRouter, HTTPException

from ui.backend.models import VulnerabilityResponse
from ui.backend.store import store

router = APIRouter(prefix="/api/runs", tags=["vulnerabilities"])


@router.get("/{run_id}/vulnerabilities", response_model=list[VulnerabilityResponse])
async def get_vulnerabilities(
    run_id: str,
    severity: str = None,
    repo: str = None,
    ecosystem: str = None,
    sort: str = "severity",
):
    """Get vulnerabilities for a run with optional filtering.

    Args:
        run_id: Run identifier
        severity: Filter by severity (critical/high/medium/low)
        repo: Filter by repository name
        ecosystem: Filter by ecosystem
        sort: Sort by field (severity, cvss_score, package)

    Returns:
        List of VulnerabilityResponse objects
    """
    run = store.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    vulns = []

    # Flatten vulnerabilities from scan results
    for scan_result in run.scan_results:
        repo_name = scan_result.get("repo", "unknown")

        for vuln_data in scan_result.get("vulnerabilities", []):
            vuln = VulnerabilityResponse(
                id=vuln_data.get("id", ""),
                package=vuln_data.get("package", ""),
                severity=vuln_data.get("severity", "unknown"),
                cvss_score=vuln_data.get("cvss_score", 0.0),
                description=vuln_data.get("description", ""),
                fixed_version=vuln_data.get("fixed_version", ""),
                current_version=vuln_data.get("current_version", ""),
                advisory=vuln_data.get("advisory", ""),
                repo_name=repo_name,
            )
            vulns.append(vuln)

    # Apply filters
    if severity:
        vulns = [v for v in vulns if v.severity.lower() == severity.lower()]

    if repo:
        vulns = [v for v in vulns if v.repo_name and repo.lower() in v.repo_name.lower()]

    # Sort
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "unknown": 4}

    if sort == "severity":
        vulns.sort(
            key=lambda v: (severity_order.get(v.severity.lower(), 999), v.package)
        )
    elif sort == "cvss_score":
        vulns.sort(key=lambda v: -v.cvss_score)
    elif sort == "package":
        vulns.sort(key=lambda v: v.package)

    return vulns
