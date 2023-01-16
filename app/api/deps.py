from typing import AsyncGenerator
from fastapi import Depends, HTTPException , status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from app.core import security
from pydantic import ValidationError

from app.db.async_session import async_session_factory
from app.core.config import settings 
from app.models.user import User
from app.schemas.token import TokenPayload
from app.crud.crud_user import user as crud_user

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session: AsyncSession = async_session_factory()  # type: ignore
    try:
        yield async_session
    finally:
        await async_session.close()

async def get_current_user(db: AsyncSession = Depends(get_async_session), token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await crud_user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not await crud_user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
