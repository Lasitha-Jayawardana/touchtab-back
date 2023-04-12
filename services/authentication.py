import json
import jwt
import pyotp
from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from constants.custom_types import TokenIssuerEnum, RoleEnum
from env import CREDENTIALS
from models.user import User, Admin
from schemas.authentication import TokenPayloadSchema, TokenUserSchema, ResetSchema, ResetOTPSchema
from schemas.common import MetaSchema
from services.mail import EmailService
from utilities.exceptions import HTTPException
from constants.exceptions import ErrorMessages
from utilities.logger import logger


class TokenService:
    def __init__(self):
        self.secret = CREDENTIALS.AUTHENTICATION_SECRET
        self.mechanism = CREDENTIALS.AUTHENTICATION_MECHANISM
        self.refresh_expiry = datetime.now(tz=timezone.utc) + timedelta(days=CREDENTIALS.REFRESH_TOKEN_EXPIRY)
        self.access_expiry = datetime.now(tz=timezone.utc) + timedelta(minutes=CREDENTIALS.ACCESS_TOKEN_EXPIRY)
        self.reset_expiry = datetime.now(tz=timezone.utc) + timedelta(minutes=CREDENTIALS.RESET_TOKEN_EXPIRY)

        self.totp = pyotp.TOTP('base32secret3232', interval=CREDENTIALS.RESET_TOKEN_EXPIRY * 60)

    def encode_token(self, user_id, token_issuer: TokenIssuerEnum):
        if token_issuer == TokenIssuerEnum.refresh:
            expiry = self.refresh_expiry
        elif token_issuer == TokenIssuerEnum.access:
            expiry = self.access_expiry
        elif token_issuer == TokenIssuerEnum.reset:
            expiry = self.reset_expiry
        else:
            expiry = datetime.now(tz=timezone.utc) + timedelta(minutes=15)

        token_payload = TokenPayloadSchema(user_id=user_id,
                                           exp=int(expiry.timestamp()),
                                           iss=token_issuer.value
                                           )

        token = jwt.encode(json.loads(token_payload.json()), self.secret, algorithm=self.mechanism)
        return token

    def decode_token(self, token, token_issuer: TokenIssuerEnum):
        try:
            data = jwt.decode(token, self.secret, issuer=token_issuer.value, algorithms=self.mechanism)
            payload = TokenPayloadSchema(**data)
            return payload

        except jwt.ExpiredSignatureError as e:
            raise HTTPException(401, ErrorMessages.EXPIRED_TOKEN)
        except jwt.InvalidIssuerError as e:
            raise HTTPException(401, ErrorMessages.INVALID_TOKEN)
        except jwt.InvalidTokenError as e:
            raise HTTPException(401, ErrorMessages.INVALID_TOKEN)
        except:
            return None

    def refresh_token(self, refresh_token):
        payload: TokenPayloadSchema = self.decode_token(refresh_token, TokenIssuerEnum.refresh)
        if payload:
            new_token = self.encode_token(payload.user_id, TokenIssuerEnum.access)
            return new_token
        return None

    def get_OTP(self):
        otp = self.totp.now()
        return otp

    def verify_OTP(self, otp) -> bool:
        return self.totp.verify(otp)


class AuthenticationService:
    def __new__(cls, session: Session, email):
        # Overridden to make sure UserSession is only creatable if user exists. For creating users use create_user.
        cls._instance = super(AuthenticationService, cls).__new__(cls)
        cls._instance.session = session
        cls._instance._orm_user = cls._instance._get_user(email)
        if not cls._instance._orm_user:
            return None
        cls.token_service = TokenService()
        cls.email_service = EmailService()
        return cls._instance

    def _create_user_token(self) -> TokenUserSchema:
        orm_user: User = self._orm_user
        hotel = None
        if orm_user.role == RoleEnum.guest:
            role_user = orm_user.guest
        else:
            role_user: Admin = orm_user.admin

        if role_user.hotel:
            hotel = MetaSchema.from_orm(role_user.hotel)

        access_token = self.token_service.encode_token(role_user.id, TokenIssuerEnum.access)
        refresh_token = self.token_service.encode_token(role_user.id, TokenIssuerEnum.refresh)

        token_user = TokenUserSchema(
            id=role_user.id,
            email=orm_user.email,
            role=orm_user.role,
            name=orm_user.name,
            image_url=orm_user.image_url,
            hotel=hotel,
            access_token=access_token,
            refresh_token=refresh_token
        )

        return token_user

    def check_account_status(self) -> bool:
        # account_status = self._orm_user.status
        # if account_status is None or account_status == StatusEnum.pending:
        #     self._orm_user.status = StatusEnum.active
        #     self.session.add(self._orm_user)
        #     self.session.commit()
        #     return True
        # if account_status == StatusEnum.inactive:
        #     return False
        return True

    def _get_user(self, email):
        stmt = select(User).where(User.email == email)
        orm_user = self.session.execute(stmt).scalars().first()
        if not orm_user:
            return None
        return orm_user

    def login_user(self, password):
        try:
            if True:
                # if self._orm_user.password == password:
                # if self.check_account_status():
                return self._create_user_token()
                # else:
                #     return None
            return None
        except:
            return None

    def send_OTP(self):
        otp = self.token_service.get_OTP()
        orm_user = self._orm_user
        # template = EmailTemplate(
        #     receiver_email=orm_user.email,
        #     subject="Password reset OTP",
        #     alt_text="HTML Does not working",
        #     path='/resources/email_templates/otp.html',
        #     params={
        #         'receiver_name': orm_user.first_name,
        #         'otp': otp
        #     }
        # )
        # try:
        #
        #     otp_sent_user = self.get_otp_from_email()
        #     self.email_service.send_email_template(template)
        #     if not otp_sent_user:
        #         otp_data = OTP(
        #             email=orm_user.email,
        #             otp=otp
        #         )
        #         self.session.add(otp_data)
        #     else:
        #         otp_sent_user.otp = otp
        #         self.session.add(otp_sent_user)
        #         self.session.flush()
        #     self.session.commit()
        # except Exception as exc:
        #     raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorMessages.RESET_EMAIL_SENDING_FAILED)

    def get_otp_from_email(self):
        orm_user = self._orm_user
        # stmt = select(OTP).where(OTP.email == orm_user.email)
        # orm_otp = self.session.execute(stmt).scalars().first()
        # return orm_otp

    def verify_OTP(self, otp):
        orm_otp = self.get_otp_from_email()
        if not orm_otp or orm_otp.otp != otp:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, ErrorMessages.INVALID_OTP)
        valid = self.token_service.verify_OTP(otp)
        if not valid:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, ErrorMessages.EXPIRED_OTP)
        token = self.get_reset_token()
        return token

    def get_reset_token(self):
        orm_user = self._orm_user
        token = self.token_service.encode_token(orm_user.id, TokenIssuerEnum.reset)
        return token

    def reset_password(self, reset_schema: ResetSchema):
        token_payload: TokenPayloadSchema = self.token_service.decode_token(reset_schema.token, TokenIssuerEnum.reset)
        if not token_payload or self._orm_user.id != token_payload.user_id:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, ErrorMessages.BAD_RESET_TOKEN
            )
        self._orm_user.password = reset_schema.password
        self._update_user()
        self._delete_otp()

    def _update_user(self):
        self.session.add(self._orm_user)
        self.session.flush()
        self.session.commit()

    def _delete_otp(self):
        orm_otp = self.get_otp_from_email()
        if orm_otp:
            self.session.delete(orm_otp)
            self.session.commit()
