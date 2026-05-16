from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.models.measurement import Measurement
from app.schemas.measurement import MeasurementCreate


async def create_measerement(
    measurement: MeasurementCreate,
    device_id: str,
    db: AsyncSession
):
    current_time = datetime.now(timezone.utc)

    measurement_in = Measurement(
        device_id=device_id,
        timestamp=current_time,
        x=measurement.x,
        y=measurement.y,
        z=measurement.z
    )

    db.add(measurement_in)

    try:
        await db.commit()
        await db.refresh(measurement_in)

        return measurement_in
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The device with this ID {device_id} was not found."
        )