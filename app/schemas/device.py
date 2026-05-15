from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime


class DeviceBase(BaseModel):
    id: str = Field(..., description="Unique device identifier")
    name: str | None = Field(None, description="Device name")


class DeviceCreate(DeviceBase):
    user_id: UUID = Field(..., description="ID of the owner")


class DeviceRead(DeviceBase):
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)