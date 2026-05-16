from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.schemas.measurement import MeasurementCreate, MeasurementRead
from app.crud import crud_measurement


router = APIRouter(prefix="/stats", tags=["Stats"])


@router.post("/{device_id}", response_model=MeasurementRead, status_code=status.HTTP_201_CREATED)
async def create_stats(
    stats: MeasurementCreate,
    device_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await crud_measurement.create_measerement(measurement=stats, device_id=device_id, db=db)

    return result