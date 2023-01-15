from typing import Any
from fastapi import APIRouter


router = APIRouter()


@router.get('/')
async def root() -> Any:
    return {"Howdy!": "hurrah"}
