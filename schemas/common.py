from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel
from humps import camelize


def to_camel(string):
    return camelize(string)


class BaseModel(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class ContentSchema(BaseModel):
    id: int
    name: Optional[str]




class SuccessSchema(BaseModel):
    message: str = "Success !"



