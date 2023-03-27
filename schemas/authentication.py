from typing import Optional, Union

from pydantic import EmailStr

from constants.custom_types import RoleEnum, TokenIssuerEnum
from schemas.common import BaseModel


class TokenPayloadSchema(BaseModel):
    user_id: str
    exp: int
    iss: TokenIssuerEnum


class TokenUserSchema(BaseModel):
    id: str
    email: EmailStr
    role: RoleEnum
    first_name: str
    access_token: Optional[str]
    refresh_token: Optional[str]


class ResetOTPSchema(BaseModel):
    email: EmailStr
    token: str


class ResetSchema(ResetOTPSchema):
    password: Union[bytes, str]

class CreatePasswordSchema(BaseModel):
    id: int = None
    password: Union[bytes, str]
