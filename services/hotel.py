from typing import Union, Type, List

from sqlalchemy import select

from constants.custom_types import RoleEnum
from constants.exceptions import ErrorMessages
from models.user import Hotel, User, Admin, Partner
from schemas.hotel import HotelSchema
from schemas.partner import PartnerSchema
from schemas.user import UserSchema, AdminSchema
from services.user import UserService

from utilities.exceptions import HTTPException
from utilities.logger import logger


class HotelService:
    def __init__(self, session):
        self.session = session
        self.user_service = UserService(session)
        # self.agent_service = AgentService(session)
        # self.customer_service = CustomerService()
        # self.shared_service = SharedService(session)
        # self.email_service = EmailService()

    def add_hotel(self, data_in: HotelSchema):
        stmt = select(Hotel).where(Hotel.name == data_in.name)
        orm = self.session.execute(stmt).scalars().first()
        if orm:
            raise HTTPException(status_code=401, message=ErrorMessages.EXISTING_ITEM)

        try:
            orm = Hotel(name=data_in.name,
                        location=data_in.location,
                        image_url=data_in.image_url,
                        wifi_password=data_in.wifi_password)

            self.session.add(orm)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)

    def create_hotel_admin(self, id, data: UserSchema):
        stmt = select(Hotel).where(Hotel.id == id)
        hotel = self.session.execute(stmt).scalars().first()
        if not hotel:
            raise HTTPException(status_code=401, message='Hotel not found')

        try:
            data.role = RoleEnum.hotel_admin
            user: User = self.user_service.create_user(data)
            if user and (not user.admin):
                user.admin = Admin(hotel=hotel)
            self.session.add(user)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)


    def get_hotels(self):
        stmt = select(Hotel)
        data: List[Hotel] = self.session.execute(stmt).scalars().all()
        res = HotelSchema.from_orm_list(data)
        return res

    def get_hotel_admins(self, id):
        stmt = select(Admin).where(Admin.hotel_id == id)
        data: List[Admin] = self.session.execute(stmt).scalars().all()
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
    #
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
