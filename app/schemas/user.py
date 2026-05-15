from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Unique user name")


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: UUID
    created_at: datetime


    model_config = ConfigDict(from_attributes=True)