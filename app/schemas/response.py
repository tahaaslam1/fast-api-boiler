from pydantic import Field
from pydantic.generics import GenericModel
from typing import TypeVar, Generic, Optional, List

DataT = TypeVar('DataT')


class GenericResponseModel(GenericModel, Generic[DataT]):
    code: int = 200
    data: Optional[DataT] = Field(None)

    class Config:
        allow_population_by_field_name = True
