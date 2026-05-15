from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.schemas.user import UserCreate, UserRead
from app.crud import crud_user


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
async def register_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await crud_user.create_user(db=db, user=user)