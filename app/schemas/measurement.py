from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MeasurementCreate(BaseModel):
    x: float
    y: float
    z: float


class MeasurementRead(BaseModel):
    id: int
    device_id: str
    timestamp: datetime
    x: float
    y: float
    z: float

    model_config = ConfigDict(from_attributes=True)