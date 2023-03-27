import typing
from datetime import datetime
from uuid import uuid4
from sqlalchemy import select, func, and_

from models.user import User
from schemas.authentication import  CreatePasswordSchema
from utilities.exceptions import HTTPException
from constants.exceptions import ErrorMessages
from env import CREDENTIALS
from utilities.logger import logger


class UserService:
    def __init__(self, session):
        self.session = session

    # def create_user(self, user_in: UserUnprotectedSchema):
    #     stmt = select(User).where(User.email == user_in.email)
    #     existing_user = self.session.execute(stmt).scalars().first()
    #     if existing_user:
    #         raise HTTPException(status_code=400, message=ErrorMessages.EXISTING_USER_SIGNUP)
    #     try:
    #         user = User(
    #             email=user_in.email,
    #             password=user_in.password,
    #             first_name=user_in.first_name,
    #             last_name=user_in.last_name,
    #             phone=user_in.phone,
    #             role=user_in.role,
    #             image_url=user_in.image_url,
    #         )
    #
    #         self.session.add(user)
    #         self.session.commit()
    #     except Exception as exc:
    #         logger.debug(exc)
    #         raise HTTPException(status_code=500, message=ErrorMessages.ADMIN_SIGNUP_FAILED)

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
