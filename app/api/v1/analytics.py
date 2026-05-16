from datetime import datetime

from fastapi import APIRouter, status, Query
from celery.result import AsyncResult

from app.worker.tasks import process_analytics

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.post("/users/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def start_analytics(
    user_id: str,
    start_dt: datetime | None = Query(None, description="Beginning of the period"),
    end_dt: datetime | None = Query(None, description="End of the period")
):
    start_str = start_dt.isoformat() if start_dt else None
    end_str = end_dt.isoformat() if end_dt else None

    task = process_analytics.apply_async(
        kwargs={
            "user_id": user_id, 
            "start_dt": start_str, 
            "end_dt": end_str
        }
    )

    return {
        "message": "Task has been activated",
        "task_id": task.id
    }


@router.get("/tasks/{task_id}")
async def get_analytics_result(task_id: str):
    task_result = AsyncResult(task_id)

    if task_result.status == "PENDING":
        return {"task_id": task_id, "status": "In the queue"}
    elif task_result.status == "STARTED":
        return {"task_id": task_id, "status": "During the calculation process"}
    elif task_result.status == "SUCCESS":
        return {
            "task_id": task_id, 
            "status": "Ready", 
            "result": task_result.result
        }
    elif task_result.status == "FAILURE":
        return {"task_id": task_id, "status": "Calculation error"}
    else:
        return {"task_id": task_id, "status": task_result.status}