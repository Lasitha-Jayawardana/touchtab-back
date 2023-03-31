from typing import Union, Type, List

from sqlalchemy import select

from constants.custom_types import RoleEnum, ServiceCategoryEnum
from constants.exceptions import ErrorMessages
from models.user import Hotel, User, Admin, Partner, MeetingRoom, Service, Restaurant, FoodMenu
from schemas.hotel import HotelSchema
from schemas.partner import PartnerSchema
from schemas.service import MeetingRoomSchema, RestaurantSchema, FoodSchema
from schemas.user import UserSchema, AdminSchema
from services.user import UserService

from utilities.exceptions import HTTPException
from utilities.logger import logger


class ServiceService:
    def __init__(self, session):
        self.session = session
        self.user_service = UserService(session)
        # self.agent_service = AgentService(session)
        # self.customer_service = CustomerService()
        # self.shared_service = SharedService(session)
        # self.email_service = EmailService()

    def add_meeting_room(self, id, data: MeetingRoomSchema):
        stmt = select(Hotel).where(Hotel.id == id)
        hotel: Hotel = self.session.execute(stmt).scalars().first()
        if not hotel:
            raise HTTPException(status_code=401, message='Hotel not found')

        try:
            meeting_room = MeetingRoom(name=data.name,
                                       place=data.place,
                                       price=data.price,
                                       capacity=data.capacity,
                                       image_url=data.image_url)
            service = Service(service_category=ServiceCategoryEnum.meeting_room,
                              meeting_room=meeting_room,
                              partner_id=data.partner.id if data.partner else None)

            hotel.services.append(service)
            self.session.add(hotel)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)

    def get_meeting_room(self, id):
        stmt = select(Service).join(Hotel).where(Service.service_category == ServiceCategoryEnum.meeting_room).where(
            Hotel.id == id)
        services: List[Service] = self.session.execute(stmt).scalars().all()

        res = []
        for service in services:
            if service.meeting_room:
                schema = MeetingRoomSchema.from_orm(service.meeting_room)
                if service.partner:
                    schema.partner = PartnerSchema.from_orm(service.partner)
                res.append(schema)
        return res

    def add_restaurant(self, id, data: RestaurantSchema):
        stmt = select(Hotel).where(Hotel.id == id)
        hotel: Hotel = self.session.execute(stmt).scalars().first()
        if not hotel:
            raise HTTPException(status_code=401, message='Hotel not found')

        try:
            restaurant = Restaurant(name=data.name,
                                    place=data.place,
                                    open_time=data.open_time,
                                    close_time=data.close_time,
                                    cuisine_type=data.cuisine_type,
                                    description=data.description,
                                    image_url=data.image_url)
            service = Service(service_category=ServiceCategoryEnum.restaurant,
                              restaurant=restaurant,
                              partner_id=data.partner.id if data.partner else None)

            hotel.services.append(service)
            self.session.add(hotel)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)

    def add_food(self, id, restaurant_id, data: FoodSchema):
        stmt = select(Restaurant).where(Restaurant.id == restaurant_id)
        restaurant: Restaurant = self.session.execute(stmt).scalars().first()
        if not restaurant:
            raise HTTPException(status_code=401, message='Hotel not found')

        try:
            food = FoodMenu(name=data.name,
                            description=data.description,
                            price=data.price,
                            type=data.type,
                            food_category_id=data.food_category.id,
                            restaurant=restaurant,
                            image_url=data.image_url)

            self.session.add(food)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)

    def get_foods(self, id, restaurant_id, food_category_id):
        stmt = select(FoodMenu).where(FoodMenu.restaurant_id == restaurant_id)
        if food_category_id:
            stmt = stmt.where(FoodMenu.food_category_id == food_category_id)

        foods: List[FoodMenu] = self.session.execute(stmt).scalars().all()

        res = FoodSchema.from_orm_list(foods)
        # for food in foods:
        #     schema = FoodSchema.from_orm(food)
        #     res.append(schema)
        return res

    def get_restaurants(self, id):
        stmt = select(Service).join(Hotel).where(Service.service_category == ServiceCategoryEnum.restaurant).where(
            Hotel.id == id)
        services: List[Service] = self.session.execute(stmt).scalars().all()

        res = []
        for service in services:
            if service.restaurant:
                schema = RestaurantSchema.from_orm(service.restaurant)
                if service.partner:
                    schema.partner = PartnerSchema.from_orm(service.partner)
                res.append(schema)
        return res

    # def del_temp_users(self, id: int):
    #     stmt = select(TempUser).where(TempUser.id == id)
    #     temp_user: TempUser = self.session.execute(stmt).scalars().first()
    #     if not temp_user:
    #         raise HTTPException(status_code=401, message=ErrorMessages.NOT_EXIST)
    #
    #     self.session.delete(temp_user)
    #     self.session.commit()
    #
    # def get_temp_users(self, super_admin_id: int):
    #     stmt = select(TempUser).where(TempUser.super_admin_id == super_admin_id)
    #     data: List[TempUser] = self.session.execute(stmt).scalars().all()
    #     res = TempUsersSchema.from_orm_list(data)
    #     return res
    #
    # def add_investment_vehicle(self, data_in: InvestmentVehicleSchema):
    #     stmt = select(User).where(User.id == data_in.investor_admin_id)
    #     investor_admin: User = self.session.execute(stmt).scalars().first()
    #     if not investor_admin:
    #         raise HTTPException(status_code=401, message=ErrorMessages.USER_NOT_EXISTING)
    #
    #     try:
    #         investor_admin.investment_vehicles.append(InvestmentVehicle(
    #             siren=data_in.siren,
    #             contact_person=data_in.contact_person,
    #             email=data_in.email,
    #             phone=data_in.phone))
    #
    #         self.session.add(investor_admin)
    #         self.session.commit()
    #     except Exception as exc:
    #         logger.debug(exc)
    #         raise HTTPException(status_code=500, message=ErrorMessages.SERVER_ERROR)
    #
    # def del_investment_vehicle(self, id: int):
    #     stmt = select(InvestmentVehicle).where(InvestmentVehicle.id == id)
    #     investment_vehicle: InvestmentVehicle = self.session.execute(stmt).scalars().first()
    #     if not investment_vehicle:
    #         raise HTTPException(status_code=401, message=ErrorMessages.NOT_EXIST)
    #
    #     self.session.delete(investment_vehicle)
    #     self.session.commit()
    #
    # def get_investment_vehicle(self, investor_admin_id: int):
    #     stmt = select(InvestmentVehicle).where(InvestmentVehicle.investor_admin_id == investor_admin_id)
    #     data: List[InvestmentVehicle] = self.session.execute(stmt).scalars().all()
    #     res = InvestmentVehicleSchema.from_orm_list(data)
    #     return res
    #
    # def add_investment_fund(self, data_in: InvestmentFundSchema):
    #     try:
    #         investment_fund = InvestmentFund(siren=data_in.siren,
    #                                          name=data_in.name)
    #         fund_admin = User(email=data_in.email,
    #                           role=RoleEnum.fund_admin,
    #                           first_name=split_full_name(data_in.contact_person)[0],
    #                           last_name=split_full_name(data_in.contact_person)[1],
    #                           phone=data_in.phone,
    #                           investment_fund=investment_fund
    #                           )
    #
    #         self.session.add(fund_admin)
    #         self.session.commit()
    #     except Exception as exc:
    #         logger.debug(exc)
    #
    # def del_investment_fund(self, id: int):
    #     stmt = select(InvestmentFund).where(InvestmentFund.id == id)
    #     investment_fund: InvestmentFund = self.session.execute(stmt).scalars().first()
    #     if not investment_fund:
    #         raise HTTPException(status_code=401, message=ErrorMessages.NOT_EXIST)
    #
    #     self.session.delete(investment_fund)
    #     self.session.commit()
    #
    # def get_investment_fund(self):
    #     stmt = select(InvestmentFund)
    #     data: List[InvestmentFund] = self.session.execute(stmt).scalars().all()
    #     res = []
    #     for _investment_fund in data:
    #         for user in _investment_fund.fund_admins:
    #             res.append(InvestmentFundSchema(id=_investment_fund.id,
    #                                             name=_investment_fund.name,
    #                                             siren=_investment_fund.siren,
    #                                             contact_person=f'{user.first_name} {user.last_name}',
    #                                             email=user.email,
    #                                             phone=user.phone))
    #     return res
