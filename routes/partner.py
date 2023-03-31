from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from routes import get_db_session, Authorize, AuthorizedUser
from schemas.common import SuccessSchema
from schemas.partner import PartnerSchema
from schemas.user import UserSchema, AdminSchema
from services.partner import PartnerService

router = APIRouter(prefix='/partners')


@router.post('', response_model=SuccessSchema)
async def create_partner(data: PartnerSchema,
                         session: Session = Depends(get_db_session)):
    PartnerService(session=session).create_partner(data)
    return SuccessSchema()


@router.post('/{id}/admin', response_model=SuccessSchema)
async def create_partner_admin(id: int, data: UserSchema,
                               session: Session = Depends(get_db_session)):
    PartnerService(session=session).create_partner_admin(id, data)
    return SuccessSchema()


@router.get('', response_model=List[PartnerSchema])
async def get_hotels(session: Session = Depends(get_db_session),
                     # authorized_user: AuthorizedUser = Depends(Authorize())
                     ):
    user = PartnerService(session=session).get_partners()
    return user

# @router.post('/signUp', response_model=SuccessSchema)
# async def create_user(user: UserUnprotectedSchema, session: Session = Depends(get_db_session)):
#     UserService(session=session).create_user(user_in=user)
#     return SuccessSchema()
#
#
#
# @router.get('/{id}/agents', response_model=UserOutItemsSchema)
# async def get_agents_for_user(id: UUID, session: Session = Depends(get_db_session),
#                               authorized_user: AuthorizedUser = Depends(Authorize())):
#     users = UserService(session=session).get_agents_for_user(id)
#
#     return UserOutItemsSchema(items=users)
#
#
# @router.get('/{id}/companies', response_model=CompanyOutItemsSchema)
# async def get_companies_for_user(id: UUID, session: Session = Depends(get_db_session),
#                                  authorized_user: AuthorizedUser = Depends(Authorize())):
#     companies = UserService(session=session).get_companies_for_user(id)
#     return CompanyOutItemsSchema(items=companies)
#
#
# @router.get('', response_model=UserPaginationSchema)
# async def list_users(pagination_in: PaginationInSchema = Depends(), session: Session = Depends(get_db_session),
#                      authorized_user: AuthorizedUser = Depends(Authorize())):
#     users = UserService(session=session).list_users(pagination_in, authorized_user)
#     return users
#
#
# @router.put('/{id}', response_model=UserOutDetailSchema)
# async def update_user(id: UUID, user: UserUpdateSchema, session: Session = Depends(get_db_session),
#                       authorized_user: AuthorizedUser = Depends(Authorize())):
#     user = UserService(session=session).update_user(id, user)
#     return user
#
#
# @router.put('/{id}/status', response_model=SuccessSchema)
# async def change_user_status(id: UUID, status: StatusEnum = Body(..., embed=True),
#                              session: Session = Depends(get_db_session),
#                              authorized_user: AuthorizedUser = Depends(Authorize())):
#     UserService(session=session).change_user_status(id, status)
#     return SuccessSchema()
#
#
# @router.put('/{id}/password', response_model=SuccessSchema)
# async def change_user_password(id: UUID, password_schema: ChangePasswordSchema,
#                                session: Session = Depends(get_db_session),
#                                authorized_user: AuthorizedUser = Depends(Authorize())):
#     UserService(session=session).change_user_password(id, authorized_user, password_schema)
#     return SuccessSchema()
