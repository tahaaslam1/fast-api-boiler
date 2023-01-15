from fastapi import APIRouter
from app.api.api_v1.endpoints import root

from app.api.api_v1.endpoints import users


api_router = APIRouter()


api_router.include_router(root.router, tags=['root'])
api_router.include_router(users.router,prefix='/users', tags=['users'])
