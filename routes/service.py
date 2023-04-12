from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.params import Body, Query
from sqlalchemy.orm import Session

from constants.custom_types import RoleEnum
from routes import get_db_session, Authorize, AuthorizedUser
from schemas.common import SuccessSchema
from schemas.service import MeetingRoomSchema, RestaurantSchema, FoodSchema, BabySitterSchema, BoatSchema
from services.service import ServiceService

router = APIRouter(prefix='/hotels/{id}')


@router.post('/meetingRooms', response_model=SuccessSchema)
async def create_meeting_room(id: int, data: MeetingRoomSchema,
                              session: Session = Depends(get_db_session),
                              # authorized_user=Depends(Authorize())
                              ):
    ServiceService(session=session).add_meeting_room(id, data)
    return SuccessSchema()


@router.post('/restaurants', response_model=SuccessSchema)
async def create_meeting_room(id: int, data: RestaurantSchema,
                              session: Session = Depends(get_db_session),
                              # authorized_user=Depends(Authorize())
                              ):
    ServiceService(session=session).add_restaurant(id, data)
    return SuccessSchema()


@router.post('/foodMenu', response_model=SuccessSchema)
async def create_meeting_room(id: int, data: FoodSchema,
                              restaurant_id=Query(alias="restaurantId"),
                              session: Session = Depends(get_db_session),
                              # authorized_user=Depends(Authorize())
                              ):
    ServiceService(session=session).add_food(id, restaurant_id, data)
    return SuccessSchema()


@router.get('/foodMenu', response_model=List[FoodSchema])
async def get_hotels(id: int,
                     restaurant_id=Query(alias="restaurantId"),
                     food_category_id=Query(default=None, alias="foodCategoryId"),
                     session: Session = Depends(get_db_session),
                     # authorized_user: AuthorizedUser = Depends(Authorize())
                     ):
    user = ServiceService(session=session).get_foods(id, restaurant_id, food_category_id)
    return user


#
# @router.post('/{id}/admin', response_model=SuccessSchema)
# async def create_hotel_admin(id: int, data: UserSchema,
#                              session: Session = Depends(get_db_session)):
#     HotelService(session=session).create_hotel_admin(id, data)
#     return SuccessSchema()
#

@router.get('/meetingRooms', response_model=List[MeetingRoomSchema])
async def get_hotels(id: int, session: Session = Depends(get_db_session),
                     # authorized_user: AuthorizedUser = Depends(Authorize())
                     ):
    user = ServiceService(session=session).get_meeting_room(id)
    return user


@router.get('/restaurants', response_model=List[RestaurantSchema])
async def get_hotels(id: int, session: Session = Depends(get_db_session),
                     # authorized_user: AuthorizedUser = Depends(Authorize())
                     ):
    user = ServiceService(session=session).get_restaurants(id)
    return user

@router.get('/babySitters', response_model=List[BabySitterSchema])
async def get_hotels(id: int, session: Session = Depends(get_db_session),
                     # authorized_user: AuthorizedUser = Depends(Authorize())
                     ):
    user = ServiceService(session=session).get_baby_sitters(id)
    return user

@router.get('/boats', response_model=List[BoatSchema])
async def get_hotels(id: int, session: Session = Depends(get_db_session),
                     # authorized_user: AuthorizedUser = Depends(Authorize())
                     ):
    user = ServiceService(session=session).get_boats(id)
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
