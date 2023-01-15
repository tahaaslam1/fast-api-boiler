from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.core.config import settings

from app.api.api_v1.api import api_router


from app.db.async_session import engine
from app.db import base
from app.db.base_class import Base
from starlette.exceptions import HTTPException as StarletteHTTPException



app = FastAPI(
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": str(exc.status_code),
                 "error_message": str(exc.detail)}
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
