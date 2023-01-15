import os
from dotenv import load_dotenv
from typing import Any

from pydantic import BaseSettings, PostgresDsn, validator

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    # PostgreSQL Database Connection
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URL: PostgresDsn | None

    @validator("SQLALCHEMY_DATABASE_URL", pre=True)
    def assemble_db_connection_string(cls, v: PostgresDsn | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT"),
            host= os.getenv("POSTGRES_HOST"),
            path=f"/{os.getenv('POSTGRES_DB')}",  
        )

    # Pagination
    PAGE_SIZE: int = 1000

    class Config:
        case_sensitive = True


settings = Settings()  # type: ignore
