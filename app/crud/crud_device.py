from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.device import Device
from app.schemas.device import DeviceCreate


async def create_device(db: AsyncSession, device: DeviceCreate):
    device_in = Device(
        id=device.id,
        name=device.name,
        user_id=device.user_id
    )

    db.add(device_in)

    try:
        await db.commit()
        await db.refresh(device_in)

        return device_in
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error with device registratin: {e}"
        )