from pydantic import Field 
from pydantic.generics import GenericModel 
from typing import TypeVar, Generic ,Optional 


DataT = TypeVar('DataT')

class GenericErrorModel(GenericModel, Generic[DataT]):
#  success: bool = Field(True)
    code : int = Field(None)
    message : str = Field(None)


    class Config:
        allow_population_by_field_name = True