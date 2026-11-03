"""Run management routes."""

import asyncio
import logging
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException

from ui.backend.models import RunRequest, RunResponse, RunSummary
from ui.backend.store import RunState, store

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/runs", tags=["runs"])


@router.post("", response_model=dict)
async def create_run(req: RunRequest):
    """Create and start a new scan run.

    Args:
        req: RunRequest with repos and options

    Returns:
        Run ID
    """
    run_id = str(uuid.uuid4())[:8]

    # Create run state
    run = store.create(
        run_id=run_id,
        repos=req.repos,
        output_dir=req.output_dir,
        dry_run=req.dry_run,
        apply=req.apply,
        ecosystems=req.ecosystems,
    )

    # Launch background pipeline task
    asyncio.create_task(run_pipeline_async(run_id))

    return {"id": run_id}


@router.get("", response_model=list[RunSummary])
async def list_runs():
    """List all runs with brief summaries.

    Returns:
        List of RunSummary objects
    """
    runs = store.list_all()
    summaries = [
        RunSummary(
            id=run.id,
            repos=run.repos,
            status=run.status,
            started_at=run.started_at,
            finished_at=run.finished_at,
            total_repos=len(run.repos),
            total_dependencies=run.total_dependencies,
            total_vulnerabilities=run.total_vulnerabilities,
        )
        for run in runs
    ]
    return sorted(summaries, key=lambda r: r.started_at, reverse=True)


@router.get("/{run_id}", response_model=RunResponse)
async def get_run(run_id: str):
    """Get full run details.

    Args:
        run_id: Run identifier

    Returns:
        Complete RunResponse
    """
    run = store.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    return RunResponse(
        id=run.id,
        repos=run.repos,
        output_dir=run.output_dir,
        dry_run=run.dry_run,
        apply=run.apply,
        ecosystems=run.ecosystems,
        status=run.status,
        started_at=run.started_at,
        finished_at=run.finished_at,
        error_message=run.error_message,
        logs=run.logs,
        total_dependencies=run.total_dependencies,
        total_vulnerabilities=run.total_vulnerabilities,
    )


async def run_pipeline_async(run_id: str):
    """Run the harness pipeline asynchronously.

    Args:
        run_id: Run identifier
    """
    run = store.get(run_id)
    if not run:
        return

    try:
        store.update_status(run_id, "running")
        store.append_log(run_id, f"Starting scan with {len(run.repos)} repositories...")

        # Import pipeline here to avoid circular imports
        from depshield.config import DepShieldConfig
        from depshield.pipeline import DepShieldPipeline

        # Create config
        config = DepShieldConfig(
            repos=run.repos,
            output_dir=run.output_dir,
            dry_run=run.dry_run,
            apply=run.apply,
            verbose=False,
            ecosystems=run.ecosystems,
        )

        # Create a custom logger that appends to logs
        class ListHandler(logging.Handler):
            def emit(self, record):
                try:
                    msg = self.format(record)
                    store.append_log(run_id, msg)
                except Exception:
                    pass

        handler = ListHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        # Add handler to depshield loggers
        for logger_name in ["depshield", "depshield.pipeline", "depshield.discovery", "depshield.scanners", "depshield.remediation", "depshield.matrix"]:
            logging.getLogger(logger_name).addHandler(handler)

        # Run pipeline
        pipeline = DepShieldPipeline(config)
        pipeline.run()

        # Serialize results
        scan_results = [
            {
                "repo": result.repo.name,
                "vulnerabilities": [
                    {
                        "id": v.id,
                        "package": v.package,
                        "severity": v.severity.value,
                        "cvss_score": v.cvss_score,
                        "description": v.description,
                        "fixed_version": v.fixed_version,
                        "current_version": v.current_version,
                    }
                    for v in result.vulnerabilities
                ],
                "success": result.success,
            }
            for result in pipeline.scan_results
        ]

        remediation_results = [
            {
                "repo": result.repo.name,
                "upgraded_dependencies": result.upgraded_dependencies,
                "recipes_applied": result.recipes_applied,
                "build_succeeded": result.build_succeeded,
                "test_succeeded": result.test_succeeded,
                "success": result.success,
            }
            for result in pipeline.remediation_results
        ]

        dep_matrix_data = {
            name: {
                "repos": list(entry.repos),
                "versions": entry.versions,
            }
            for name, entry in pipeline.dep_matrix.matrix.items()
        }

        upgrade_matrix_data = {
            pkg: {
                "current_version": rec.current_version,
                "safe_version": rec.safe_version,
                "severity": rec.severity_level,
                "cvss_score": rec.cvss_score,
                "cves": [v.id for v in rec.vulnerabilities],
            }
            for pkg, rec in pipeline.upgrade_matrix.recommendations.items()
        }

        # Count totals
        total_deps = sum(len(repo.dependencies) for repo in pipeline.repos)
        total_vulns = sum(len(result.vulnerabilities) for result in pipeline.scan_results)

        store.set_results(
            run_id,
            scan_results=scan_results,
            remediation_results=remediation_results,
            dep_matrix=dep_matrix_data,
            upgrade_matrix=upgrade_matrix_data,
            total_dependencies=total_deps,
            total_vulnerabilities=total_vulns,
        )

        store.append_log(run_id, "✅ Pipeline completed successfully")
        store.update_status(run_id, "done")

    except Exception as e:
        logger.exception(f"Pipeline failed for run {run_id}")
        store.append_log(run_id, f"❌ Error: {str(e)}")
        store.set_error(run_id, str(e))
