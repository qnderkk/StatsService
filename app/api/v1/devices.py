from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.schemas.device import DeviceCreate, DeviceRead
from app.crud import crud_device


router = APIRouter(prefix="/devices", tags=["Devices"])


@router.post("/register", response_model=DeviceRead, status_code=status.HTTP_201_CREATED)
async def register_device(device: DeviceCreate, db: AsyncSession = Depends(get_db)):
    result = await crud_device.create_device(device=device, db=db)

    return result