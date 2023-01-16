
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import select
from app.crud.base import BaseCRUD
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash , verify_password


class CrudUser(BaseCRUD[User, UserCreate, UserUpdate]):

    
    async def get_by_email(self, db: AsyncSession, email: str):
        db_excute = await db.execute(select(User).where(User.email == email))
        return db_excute.scalars().first()

    async def create(self, db: AsyncSession, obj_in: UserCreate):
        db_obj = User(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            is_active= obj_in.is_active
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, id : Any):
        db_excute = await db.execute(select(User).where(User.id == id))
        return db_excute.scalars().first()
    
    async def authenticate(self,db:AsyncSession,email : str, password : str):
        user = await self.get_by_email(db,email=email)
        if not user:
            return None
        if not verify_password(plain_password=password,hashed_password=user.hashed_password):
            return None
        return user

    async def is_active(self, user: User) -> bool:
        return user.is_active


user = CrudUser(User)
