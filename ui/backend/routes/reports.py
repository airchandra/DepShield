"""Report file serving routes."""

from pathlib import Path

from fastapi import APIRouter, HTTPException

from ui.backend.store import store

router = APIRouter(prefix="/api/runs", tags=["reports"])

VALID_REPORTS = {
    "SBOM.md",
    "VULNERABILITY_REPORT.md",
    "ARCHITECTURE.md",
    "CODING_GUIDELINES.md",
    "SEQUENCE_DIAGRAMS.md",
    "TEST_CASES.md",
    "UPGRADE_PLAN.md",
}


@router.get("/{run_id}/repos/{repo_name}/reports/{filename}")
async def get_report(run_id: str, repo_name: str, filename: str):
    """Get a markdown report file.

    Args:
        run_id: Run identifier
        repo_name: Repository name (not used for lookup, just validation)
        filename: Report filename (e.g., SBOM.md)

    Returns:
        Markdown file content as plain text
    """
    if filename not in VALID_REPORTS:
        raise HTTPException(status_code=400, detail="Invalid report filename")

    run = store.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    # Find matching repo
    repo_path = None
    for r in run.repos:
        if repo_name.lower() in r.lower() or Path(r).name.lower() == repo_name.lower():
            repo_path = r
            break

    if not repo_path:
        raise HTTPException(status_code=404, detail="Repository not found")

    # Read report file
    report_file = Path(repo_path) / "docs" / filename

    if not report_file.exists():
        raise HTTPException(status_code=404, detail="Report not found")

    try:
        return report_file.read_text()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading report: {str(e)}")


@router.get("/{run_id}/system-reports/{filename}")
async def get_system_report(run_id: str, filename: str):
    """Get a system-level report file.

    Args:
        run_id: Run identifier
        filename: Report filename (e.g., SYSTEM_ARCHITECTURE.md)

    Returns:
        Markdown file content as plain text
    """
    valid_system_reports = {
        "SYSTEM_ARCHITECTURE.md",
        "DEPENDENCY_MATRIX.md",
        "UPGRADE_MATRIX.md",
        "PIPELINE_SEQUENCE.md",
    }

    if filename not in valid_system_reports:
        raise HTTPException(status_code=400, detail="Invalid report filename")

    run = store.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    # Read from output directory
    report_file = Path(run.output_dir) / filename

    if not report_file.exists():
        raise HTTPException(status_code=404, detail="Report not found")

    try:
        return report_file.read_text()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading report: {str(e)}")
