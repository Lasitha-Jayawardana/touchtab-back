from typing import Optional, Any
from uuid import UUID
from pydantic.utils import GetterDict
# from stringcase import snakecase
# from pydantic import AnyUrl
#
# from constants.custom_types import RoleEnum
# from schemas.common import BaseModel, ContentSchema
#
#
# class ObjectMapper(GetterDict):
#     def __getitem__(self, key: str) -> Any:
#         try:
#             return self._obj.get(key)
#         except AttributeError as e:
#             raise KeyError(key) from e
#
#     def get(self, key: Any, default: Any = None) -> Any:
#         if key == "firstName":
#             return self._obj.user.first_name
#         elif key == "lastName":
#             return self._obj.user.last_name
#         elif key == "imageUrl":
#             return self._obj.user.image_url
#         else:
#             return getattr(self._obj, snakecase(key))
#
#
# class AddressSchema(BaseModel):
#     id: Optional[UUID]
#     street_address: Optional[str]
#     country: ContentSchema
#     state: ContentSchema
#     city: ContentSchema
#     zip_code: Optional[str]
#
#
# class AddressOutSchema(AddressSchema):
#     country: Optional[ContentSchema]
#     state: Optional[ContentSchema]
#     city: Optional[ContentSchema]
#
#
# class InvitationVerifySchema(BaseModel):
#     email: str
#     role: RoleEnum
#
#
# class ResponsiblePersonSchema(BaseModel):
#     id: Optional[UUID]
#     first_name: str
#     last_name: str
#     image_url: Optional[AnyUrl]
#
#
# class ResponsibleAgentSchema(ResponsiblePersonSchema):
#     id: UUID
#     first_name: Optional[str]
#     last_name: Optional[str]
#     agent_type: Optional[AgentTypeEnum]
#
#     class Config:
#         getter_dict = ObjectMapper
#
#
# class CompanyGenericSchema(BaseModel):
#     id: UUID
#     business_name: str
#     image_url: Optional[AnyUrl]
