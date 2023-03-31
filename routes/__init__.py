from models.user import User
from schemas.authentication import TokenPayloadSchema
from schemas.user import UserSchema
from services.authentication import TokenService
from utilities.logger import logger, extra
from database.dbm import DatabaseManager
import typing
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from database.dbm import DatabaseManager
from constants.custom_types import RoleEnum, TokenIssuerEnum
from utilities.exceptions import HTTPException
from constants.exceptions import ErrorMessages


def get_db_session():
    """
    call to the singleton
    """
    dbm = DatabaseManager()
    session = dbm.SessionFactory()
    try:
        yield session
    # except Exception as e:
    #     logger.exception("Session failed:", extra=extra)
    #     session.rollback()
    #     session.flush()
    finally:
        logger.debug("closed db session")
        session.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


class AuthorizedUser:

    def __new__(cls, user_id, session: Session):
        # Overridden to make sure UserSession is only creatable if user exists. For creating users use create_user.
        cls._instance = super(AuthorizedUser, cls).__new__(cls)
        cls._instance.session = session
        cls._instance._orm_user = cls._instance._get_user(user_id)
        if not cls._instance._orm_user:
            return None

        return cls._instance

    def _get_user(self, user_id):
        stmt = select(User).where(User.id == user_id)
        orm_user = self.session.execute(stmt).scalars().first()
        return orm_user

    def get_orm_user(self):
        return self._orm_user

    def get_user(self, user_mapping: typing.Type[UserSchema] = UserSchema):
        user_out = user_mapping.from_orm(self._orm_user)
        return user_out

    @property
    def role(self):
        return self._orm_user.role

    @property
    def id(self):
        return self._orm_user.id


class Authorize:
    def __init__(self, role: Optional[RoleEnum] = None) -> None:
        self.role = role
        pass

    def _can_access_role(self, authorized_user: AuthorizedUser) -> bool:
        if self.role is None:
            return True
        user = authorized_user.get_user()

        if user.role == self.role:
            return True
        return False

    def __call__(
            self,
            token: str = Depends(oauth2_scheme),
            session: Session = Depends(get_db_session),
    ):

        token_payload: TokenPayloadSchema = TokenService().decode_token(token, TokenIssuerEnum.access)
        if not token_payload:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, ErrorMessages.INVALID_TOKEN
            )

        authorized_user = AuthorizedUser(token_payload.user_id, session)
        if not authorized_user:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, ErrorMessages.INVALID_TOKEN
            )

        valid = self._can_access_role(authorized_user)
        if not valid:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, ErrorMessages.INVALID_ROLE
            )
        return authorized_user
