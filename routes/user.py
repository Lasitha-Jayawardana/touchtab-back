from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.params import Body
from sqlalchemy.orm import Session

from constants.custom_types import RoleEnum, StatusEnum
from routes import get_db_session, Authorize, AuthorizedUser
from schemas.company import CompanyOutSchema
from schemas.shared import InvitationVerifySchema
from schemas.common import SuccessSchema, PaginationInSchema
from schemas.user import UserUnprotectedSchema, UserOutSchema, UserPaginationSchema, UserInviteSchema, UserUpdateSchema, \
    UserOutDetailSchema, ChangePasswordSchema, CompanyOutItemsSchema, UserOutItemsSchema
from services.user.user import UserService

router = APIRouter(prefix='/users')


@router.post('/inviteNewUser', response_model=SuccessSchema)
async def invite_new_user(user: UserInviteSchema, session: Session = Depends(get_db_session),
                          authorized_user=Depends(Authorize(RoleEnum.admin))):
    UserService(session=session).invite_new_user(user=user, authorized_user=authorized_user)
    return SuccessSchema()


@router.post('/verifyInvitation', response_model=InvitationVerifySchema)
async def verify_by_token(invitation_token=Body(..., embed=True, alias="invitationToken"),
                          session: Session = Depends(get_db_session)):
    response_schema = UserService(session=session).get_user_by_token(invitation_token)
    return response_schema


@router.post('/signUp', response_model=SuccessSchema)
async def create_user(user: UserUnprotectedSchema, session: Session = Depends(get_db_session)):
    UserService(session=session).create_user(user_in=user)
    return SuccessSchema()


@router.get('/{id}', response_model=UserOutDetailSchema)
async def get_user_by_id(id: UUID, session: Session = Depends(get_db_session),
                         authorized_user: AuthorizedUser = Depends(Authorize())):
    user = UserService(session=session).get_user_by_id(id)
    return user


@router.get('/{id}/agents', response_model=UserOutItemsSchema)
async def get_agents_for_user(id: UUID, session: Session = Depends(get_db_session),
                              authorized_user: AuthorizedUser = Depends(Authorize())):
    users = UserService(session=session).get_agents_for_user(id)

    return UserOutItemsSchema(items=users)


@router.get('/{id}/companies', response_model=CompanyOutItemsSchema)
async def get_companies_for_user(id: UUID, session: Session = Depends(get_db_session),
                                 authorized_user: AuthorizedUser = Depends(Authorize())):
    companies = UserService(session=session).get_companies_for_user(id)
    return CompanyOutItemsSchema(items=companies)


@router.get('', response_model=UserPaginationSchema)
async def list_users(pagination_in: PaginationInSchema = Depends(), session: Session = Depends(get_db_session),
                     authorized_user: AuthorizedUser = Depends(Authorize())):
    users = UserService(session=session).list_users(pagination_in, authorized_user)
    return users


@router.put('/{id}', response_model=UserOutDetailSchema)
async def update_user(id: UUID, user: UserUpdateSchema, session: Session = Depends(get_db_session),
                      authorized_user: AuthorizedUser = Depends(Authorize())):
    user = UserService(session=session).update_user(id, user)
    return user


@router.put('/{id}/status', response_model=SuccessSchema)
async def change_user_status(id: UUID, status: StatusEnum = Body(..., embed=True),
                             session: Session = Depends(get_db_session),
                             authorized_user: AuthorizedUser = Depends(Authorize())):
    UserService(session=session).change_user_status(id, status)
    return SuccessSchema()


@router.put('/{id}/password', response_model=SuccessSchema)
async def change_user_password(id: UUID, password_schema: ChangePasswordSchema,
                               session: Session = Depends(get_db_session),
                               authorized_user: AuthorizedUser = Depends(Authorize())):
    UserService(session=session).change_user_password(id, authorized_user, password_schema)
    return SuccessSchema()
