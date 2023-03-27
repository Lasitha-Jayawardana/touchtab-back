from datetime import datetime
from typing import Optional, Union, List
from uuid import UUID
from pydantic import EmailStr, AnyUrl

from constants.custom_types import RoleEnum
from schemas.common import BaseModel


#
# from constants.custom_types import StatusEnum, RoleEnum, AgentTypeEnum
# from schemas.common import BaseModel, Pagination
# from schemas.company import CompanyOutSchema
# from schemas.shared import AddressSchema, AddressOutSchema, ResponsiblePersonSchema
#

class UserSchema(BaseModel):
    id: Optional[UUID]
    email: EmailStr
    telephone_no: Optional[str]
    first_name: str
    last_name: str
    role: RoleEnum
    image_url: Optional[AnyUrl]


# class UserInSchema(UserSchema):
#     address: AddressSchema
#     invitation_token: str
#
#
# class UserUnprotectedSchema(UserInSchema):
#     password: Union[bytes, str]
#
#
# class UserOutSchema(UserSchema):
#     status: StatusEnum
#     created_user: Optional[ResponsiblePersonSchema]
#
#
# class UserOutItemsSchema(BaseModel):
#     items: List[UserOutSchema]
#
#
# class CompanyOutItemsSchema(BaseModel):
#     items: List[CompanyOutSchema]
#
#
# class UserPaginationSchema(Pagination):
#     items: List[UserOutSchema]
#
#
# class UserOutDetailSchema(UserOutSchema):
#     address: Optional[AddressOutSchema]
#     last_login: Optional[datetime]
#     agent_type: AgentTypeEnum = None
#
#
# class UserInviteSchema(BaseModel):
#     email: EmailStr
#     role: RoleEnum
#
#
# class UserUpdateSchema(UserSchema):
#     email: Optional[EmailStr]
#     first_name: Optional[str]
#     last_name: Optional[str]
#
#     role: Optional[RoleEnum]
#     address: Optional[AddressSchema]
#
#
# class ChangePasswordSchema(BaseModel):
#     old_password: Union[bytes, str]
#     new_password: Union[bytes, str]
