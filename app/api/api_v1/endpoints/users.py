from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from app.schemas import user
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.crud_user import user as crud_user
from app.schemas import response as res
from app.models.user import User


router = APIRouter()


@router.post('/createUser', response_model=res.GenericResponseModel)
async def createUser(*, db: AsyncSession = Depends(deps.get_async_session), user_in: user.UserCreate):
    user = await crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail='The user with this username already exists in the system.'
        )

    user = await crud_user.create(db, obj_in=user_in)
    return res.GenericResponseModel(data=user)


@router.get('/me')
async def checkAuth(*,db: AsyncSession = Depends(deps.get_async_session), current_user : User =  Depends(deps.get_current_active_user)):
    return res.GenericResponseModel(data=current_user)

