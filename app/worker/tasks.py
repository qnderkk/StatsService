import asyncio
import datetime

from sqlalchemy import func

from app.core.celery_app import celery_app
from app.db.database import session_factory
from app.models.measurement import Measurement
from app.crud.crud_measurement import fetch_aggregate_stats, fetch_per_device_stats
from app.crud.crud_device import get_user_device_ids


def _get_stat_columns(column, prefix: str) -> list:
    return [
        func.min(column).label(f"{prefix}_min"),
        func.max(column).label(f"{prefix}_max"),
        func.sum(column).label(f"{prefix}_sum"),
        func.percentile_cont(0.5).within_group(column).label(f"{prefix}_median"),
    ]


def _build_analytics_columns() -> list:
    return [
        func.count(Measurement.id).label("count"),
        *_get_stat_columns(Measurement.x, "x"),
        *_get_stat_columns(Measurement.y, "y"),
        *_get_stat_columns(Measurement.z, "z"),
    ]


def _format_axis(row, prefix):
    return {
        "min": getattr(row, f"{prefix}_min"),
        "max": getattr(row, f"{prefix}_max"),
        "sum": getattr(row, f"{prefix}_sum"),
        "median": getattr(row, f"{prefix}_median"),
    }


async def calculate_stats(user_id: int, start_dt: str | None, end_dt: str | None) -> dict:
    async with session_factory() as session:
        device_ids = await get_user_device_ids(session, user_id)

        if not device_ids:
            return {"message": "User doesn't have any devices!"}
        
        filters = [Measurement.device_id.in_(device_ids)]

        if start_dt:
            filters.append(Measurement.timestamp >= datetime.fromisoformat(start_dt))
        if end_dt:
            filters.append(Measurement.timestamp <= datetime.fromisoformat(end_dt))

        stat_columns = _build_analytics_columns()

        row_all = await fetch_aggregate_stats(session, device_ids, stat_columns)

        if not row_all or row_all.count == 0:
            return {"message": "No data to analyze!"}
        
        aggregate_data = {
            "count": row_all.count,
            "x": _format_axis(row_all, "x"),
            "y": _format_axis(row_all, "y"),
            "z": _format_axis(row_all, "z"),
        }

        rows_grouped = await fetch_per_device_stats(session, device_ids, stat_columns)

        devices_data = {}
        for row in rows_grouped:
            devices_data[row.device_id] = {
                "count": row.count,
                "x": _format_axis(row, "x"),
                "y": _format_axis(row, "y"),
                "z": _format_axis(row, "z"),
            }
        
        return {
            "status": "success",
            "user_id": user_id,
            "data": {
                "aggregate": aggregate_data,
                "by_device": devices_data
            }
        }


@celery_app.task(bind=True, name="process_analystic_task")
def process_analytics(self, user_id: str, start_dt: str | None = None, end_dt: str | None = None):
    return asyncio.run(calculate_stats(user_id, start_dt, end_dt))