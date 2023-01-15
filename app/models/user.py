"""
Defines base class with shared attributes for models (database tables).
"""

from sqlalchemy import Column, Integer, String, Boolean
# from .db.async_session import Base
# from ..db.async_session import Base

from app.db.base_class import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid 

class User(Base):

    id = Column(UUID(as_uuid=True), primary_key=True,default = uuid.uuid4)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    __mapper_args__ = {"eager_defaults": True}

# def ResponseModel(data, message):
#     return {
#         "data": [data],
#         "code": 200,
#         "message": message,
#     }
