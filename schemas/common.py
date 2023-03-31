from typing import Optional, Union, List
from uuid import UUID

from pydantic import BaseModel
from humps import camelize

from database import Base


def to_camel(string):
    return camelize(string)


class BaseModel(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True

    @classmethod
    def from_orm_list(cls, orm_list: List[Base]) -> List[any]:
        return [cls.from_orm(orm) for orm in orm_list]



class MetaSchema(BaseModel):
    id: int
    name: Optional[str]




class SuccessSchema(BaseModel):
    message: str = "Success !"



