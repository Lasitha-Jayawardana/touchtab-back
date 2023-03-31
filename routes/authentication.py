from fastapi.params import Body
from pydantic import EmailStr
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from routes import get_db_session, Authorize
from schemas.authentication import TokenUserSchema, ResetSchema, ResetOTPSchema, CreatePasswordSchema
from schemas.common import SuccessSchema
from services.authentication import AuthenticationService, TokenService
from services.user import UserService
from utilities.exceptions import HTTPException
from constants.exceptions import ErrorMessages

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=TokenUserSchema)
async def login_user(email: EmailStr = Body(...), password=Body(...), session: Session = Depends(get_db_session)):
    authentication_service = AuthenticationService(session, email)
    if not authentication_service:
        raise HTTPException(status.HTTP_404_NOT_FOUND, ErrorMessages.INVALID_USERNAME)

    token_user: TokenUserSchema = authentication_service.login_user(
        password=password
    )
    if token_user:
        return token_user
    raise HTTPException(status.HTTP_400_BAD_REQUEST, ErrorMessages.INVALID_USERNAME_PASSWORD)


@router.post("/token")
async def get_token(
        credentials: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_db_session),
):
    authentication_service = AuthenticationService(session, credentials.username)
    if not authentication_service:
        raise HTTPException(status.HTTP_404_NOT_FOUND, ErrorMessages.INVALID_USERNAME)

    token_user: TokenUserSchema = authentication_service.login_user(
        password=credentials.password
    )
    if token_user:
        return {"access_token": token_user.access_token, "refresh_token": token_user.refresh_token}
    raise HTTPException(status.HTTP_400_BAD_REQUEST, ErrorMessages.INVALID_USERNAME_PASSWORD)


@router.post("/refresh")
async def get_access_token(
        token=Body(..., embed=True),
):
    new_token = TokenService().refresh_token(token)

    if new_token:
        return {"access_token": new_token}


@router.post("/forgot", response_model=SuccessSchema)
async def request_password_reset(
        email: EmailStr = Body(..., embed=True), session: Session = Depends(get_db_session)
):
    authentication_service = AuthenticationService(session, email)
    # to avoid brute force checking, username or email error shouldn't be shown
    if authentication_service:
        authentication_service.send_OTP()
    # TODO can't request another password reset until the previous token has expired (to prevent DoS attacks).
    return SuccessSchema()


@router.post("/verifyOTP", response_model=ResetOTPSchema)
async def verify_otp_token(
        email: EmailStr = Body(..., embed=True), otp_token=Body(..., embed=True, alias="otpToken"),
        session: Session = Depends(get_db_session)
):
    authentication_service = AuthenticationService(session, email)
    if not authentication_service:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, ErrorMessages.INVALID_USERNAME_OTP)
    token = authentication_service.verify_OTP(otp_token)
    reset_user = ResetOTPSchema(email=email, token=token)
    return reset_user


@router.put('/reset', response_model=SuccessSchema)
async def reset_password(reset_schema: ResetSchema, session: Session = Depends(get_db_session)):
    authentication_service = AuthenticationService(session, reset_schema.email)
    if not authentication_service:
        raise HTTPException(status.HTTP_404_NOT_FOUND, ErrorMessages.INVALID_USERNAME)
    authentication_service.reset_password(reset_schema)
    return SuccessSchema()


@router.post('/createPassword', response_model=SuccessSchema)
async def create_password(password_schema: CreatePasswordSchema, session: Session = Depends(get_db_session)):
    UserService(session=session).create_password(password_in=password_schema)
    return SuccessSchema()
