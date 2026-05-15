from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    user_in = User(username=user.username)

    db.add(user_in)

    try:
        await db.commit()
        await db.refresh(user_in)
        
        return user_in
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with such name already exist!"
        )




