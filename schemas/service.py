from datetime import datetime
from typing import Optional, Union, List
from uuid import UUID
from pydantic import EmailStr, AnyUrl

from constants.custom_types import RoleEnum, ServiceCategoryEnum, FoodTypeEnum
from schemas.common import BaseModel, MetaSchema
from schemas.partner import PartnerSchema


class ServiceSchema(BaseModel):
    id: Optional[int]
    name: str
    service_category: Optional[ServiceCategoryEnum]
    partner: Optional[PartnerSchema]


class MeetingRoomSchema(ServiceSchema):
    place: str = None
    price: float
    capacity: int
    image_url: str = None


class RestaurantSchema(ServiceSchema):
    cuisine_type: str
    place: str = None
    open_time: str = None
    close_time: str = None
    description: str = None
    image_url: str = None


class BoatSchema(ServiceSchema):
    seats: int
    place: str = None
    start_time: datetime = None
    end_time: datetime = None
    description: str = None
    image_url: str = None
    price: float
    rate: float
    reserved: int


class BabySitterSchema(ServiceSchema):
    place: str = None
    open_time: str = None
    close_time: str = None
    description: str = None
    image_url: str = None
    reserved: int = None
    capacity: int
    rate: float
    price: float


class FoodSchema(BaseModel):
    id: Optional[int]
    name: str
    description: str = None
    food_category: MetaSchema
    type: FoodTypeEnum
    image_url: str = None
    rate: float = None
    price: float

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
