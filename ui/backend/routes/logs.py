"""Server-Sent Events (SSE) for live logs."""

import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from ui.backend.store import store

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/runs", tags=["logs"])


@router.get("/{run_id}/logs")
async def stream_logs(run_id: str):
    """Stream logs via Server-Sent Events.

    Args:
        run_id: Run identifier

    Yields:
        SSE messages with log lines
    """
    run = store.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    async def log_generator():
        """Generate log lines as SSE events."""
        last_index = 0

        while True:
            # Send any new logs
            current_logs = run.logs
            if len(current_logs) > last_index:
                for i in range(last_index, len(current_logs)):
                    line = current_logs[i]
                    message = f"data: {line}\n\n"
                    yield message
                last_index = len(current_logs)

            # If run is done, send completion and close
            if run.status in ["done", "error"]:
                yield f"data: [RUN_COMPLETE: {run.status}]\n\n"
                break

            # Sleep briefly before checking again
            import asyncio
            await asyncio.sleep(0.5)

    return StreamingResponse(
        log_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )
