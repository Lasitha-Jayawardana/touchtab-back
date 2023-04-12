import datetime
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.params import Body, Query, Path
from sqlalchemy.orm import Session

from constants.custom_types import RoleEnum, RoomTypeEnum
from routes import get_db_session, Authorize, AuthorizedUser
from schemas.common import SuccessSchema, MetaSchema
from schemas.hotel import HotelSchema
from schemas.partner import PartnerSchema
from schemas.room import RoomSchema, CheckInSchema
from schemas.user import UserSchema, AdminSchema
from services.hotel import HotelService
from services.room import RoomService

router = APIRouter(prefix='/hotels/{id}/rooms')


#
# @router.post('', response_model=SuccessSchema)
# async def create_hotel(hotel: HotelSchema,
#                        session: Session = Depends(get_db_session),
#                        # authorized_user=Depends(Authorize())
#                        ):
#     HotelService(session=session).add_hotel(hotel)
#     return SuccessSchema()
#
#
@router.post('/{roomId}/checkIn', response_model=SuccessSchema)
async def create_hotel_admin(id: int, data: CheckInSchema, room_id: int = Path(..., alias="roomId"),
                             session: Session = Depends(get_db_session)):
    RoomService(session=session).check_in(id, room_id, data)
    return SuccessSchema()


@router.get('', response_model=List[RoomSchema])
async def get_rooms(
        id: int,
        check_in: datetime.date = Query(None, alias="checkIn"),
        check_out: datetime.date = Query(None, alias="checkOut"),
        room_type: RoomTypeEnum = Query(None, alias="roomType"),
        session: Session = Depends(get_db_session),
        # authorized_user: AuthorizedUser = Depends(Authorize())
):
    user = RoomService(session=session).get_rooms(id, check_in, check_out, room_type)
    return user

#
# @router.get('/{id}/admins', response_model=List[AdminSchema])
# async def get_hotel_admins(id: int, session: Session = Depends(get_db_session),
#                            # authorized_user: AuthorizedUser = Depends(Authorize())
#                            ):
#     user = HotelService(session=session).get_hotel_admins(id)
#     return user

# @router.post('/{id}/partners', response_model=SuccessSchema)
# async def create_partner(id: int, data: PartnerSchema,
#                              session: Session = Depends(get_db_session)):
#     HotelService(session=session).create_partner(id, data)
#     return SuccessSchema()

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
