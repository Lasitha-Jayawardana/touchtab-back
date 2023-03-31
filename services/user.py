import typing
from datetime import datetime
from uuid import uuid4
from sqlalchemy import select, func, and_

from constants.custom_types import RoleEnum
from models.user import User, Admin
from schemas.authentication import  CreatePasswordSchema
from schemas.hotel import HotelSchema
from schemas.partner import PartnerSchema
from schemas.user import UserSchema, AdminSchema
from utilities.exceptions import HTTPException
from constants.exceptions import ErrorMessages
from env import CREDENTIALS
from utilities.logger import logger


class UserService:
    def __init__(self, session):
        self.session = session

    def create_user(self, user_in: UserSchema):
        stmt = select(User).where(User.email == user_in.email)
        existing_user = self.session.execute(stmt).scalars().first()
        if existing_user:
            return existing_user
        try:
            user = User(
                email=user_in.email,
                name=user_in.name,
                phone=user_in.phone,
                role=user_in.role,
                image_url=user_in.image_url,
            )

            self.session.add(user)
            self.session.commit()
            return user
        except Exception as exc:
            logger.debug(exc)
            raise HTTPException(status_code=500, message='')

    def get_hotel_admins(self):
        stmt = select(Admin).join(User).where(User.role == RoleEnum.hotel_admin)
        data: typing.List[Admin] = self.session.execute(stmt).scalars().all()
        res = []
        for admin in data:
            if admin.user:
                admin_schema = AdminSchema(id=admin.id,
                                       name=admin.user.name,
                                       email=admin.user.email,
                                       phone=admin.user.phone,
                                       role=admin.user.role,
                                       hotel=HotelSchema.from_orm(admin.hotel),
                                       )
                res.append(admin_schema)
        return res
    def get_partner_admins(self):
        stmt = select(Admin).join(User).where(User.role == RoleEnum.partner_admin)
        data: typing.List[Admin] = self.session.execute(stmt).scalars().all()
        res = []
        for admin in data:
            if admin.user:
                admin_schema = AdminSchema(id=admin.id,
                                       name=admin.user.name,
                                       email=admin.user.email,
                                       phone=admin.user.phone,
                                       role=admin.user.role,
                                       partner=PartnerSchema.from_orm(admin.partner),
                                       )
                res.append(admin_schema)
        return res
    def create_password(self, password_in: CreatePasswordSchema):
        stmt = select(User).where(User.id == password_in.id)
        user: User = self.session.execute(stmt).scalars().first()
        if not user:
            raise HTTPException(status_code=404, message=ErrorMessages.NOT_EXIST)
        try:
            user.password = password_in.password
            self.session.add(user)
            self.session.flush()
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)
            raise HTTPException(status_code=500, message=ErrorMessages.SERVER_ERROR)
