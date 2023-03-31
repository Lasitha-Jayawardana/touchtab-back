from datetime import datetime
from typing import Optional, Union, List
from uuid import UUID
from pydantic import EmailStr, AnyUrl

from constants.custom_types import RoleEnum
from schemas.common import BaseModel


class PartnerSchema(BaseModel):
    id: Optional[int]
    name: str
    location: str = None
    # image_url: Optional[AnyUrl]
    # hotel_admins:Optional[List[UserSchema]]
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
