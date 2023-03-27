from typing import Union, Type, List

from sqlalchemy import select

from constants.custom_types import RoleEnum
from constants.exceptions import ErrorMessages
from models.user import User, Department, AssetClass, Strategy, Fund, InvestmentVehicle, \
    TempUser, InvestmentFund
from schemas.investor_admin import BeneficialOwnersSchema, InvestmentVehicleSchema
from schemas.fund_admin import OnboardingSchema, FundStructureSchema
from schemas.super_admin import TempUsersSchema, InvestmentFundSchema
from utilities.exceptions import HTTPException
from utilities.helper import split_full_name
from utilities.logger import logger


class SuperAdminService:
    def __init__(self, session):
        self.session = session
        # self.admin_service = AdminService()
        # self.agent_service = AgentService(session)
        # self.customer_service = CustomerService()
        # self.shared_service = SharedService(session)
        # self.email_service = EmailService()

    def add_temp_users(self, data_in: TempUsersSchema):
        stmt = select(User).where(User.id == data_in.super_admin_id)
        super_admin: User = self.session.execute(stmt).scalars().first()
        if not super_admin:
            raise HTTPException(status_code=401, message=ErrorMessages.USER_NOT_EXISTING)

        try:
            super_admin.temp_users.append(TempUser(
                name=data_in.name,
                department=data_in.department,
                email=data_in.email,
            ))

            self.session.add(super_admin)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)

    def del_temp_users(self, id: int):
        stmt = select(TempUser).where(TempUser.id == id)
        temp_user: TempUser = self.session.execute(stmt).scalars().first()
        if not temp_user:
            raise HTTPException(status_code=401, message=ErrorMessages.NOT_EXIST)

        self.session.delete(temp_user)
        self.session.commit()

    def get_temp_users(self, super_admin_id: int):
        stmt = select(TempUser).where(TempUser.super_admin_id == super_admin_id)
        data: List[TempUser] = self.session.execute(stmt).scalars().all()
        res = TempUsersSchema.from_orm_list(data)
        return res

    def add_investment_vehicle(self, data_in: InvestmentVehicleSchema):
        stmt = select(User).where(User.id == data_in.investor_admin_id)
        investor_admin: User = self.session.execute(stmt).scalars().first()
        if not investor_admin:
            raise HTTPException(status_code=401, message=ErrorMessages.USER_NOT_EXISTING)

        try:
            investor_admin.investment_vehicles.append(InvestmentVehicle(
                siren=data_in.siren,
                contact_person=data_in.contact_person,
                email=data_in.email,
                phone=data_in.phone))

            self.session.add(investor_admin)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)
            raise HTTPException(status_code=500, message=ErrorMessages.SERVER_ERROR)

    def del_investment_vehicle(self, id: int):
        stmt = select(InvestmentVehicle).where(InvestmentVehicle.id == id)
        investment_vehicle: InvestmentVehicle = self.session.execute(stmt).scalars().first()
        if not investment_vehicle:
            raise HTTPException(status_code=401, message=ErrorMessages.NOT_EXIST)

        self.session.delete(investment_vehicle)
        self.session.commit()

    def get_investment_vehicle(self, investor_admin_id: int):
        stmt = select(InvestmentVehicle).where(InvestmentVehicle.investor_admin_id == investor_admin_id)
        data: List[InvestmentVehicle] = self.session.execute(stmt).scalars().all()
        res = InvestmentVehicleSchema.from_orm_list(data)
        return res

    def add_investment_fund(self, data_in: InvestmentFundSchema):
        try:
            investment_fund = InvestmentFund(siren=data_in.siren,
                                             name=data_in.name)
            fund_admin = User(email=data_in.email,
                              role=RoleEnum.fund_admin,
                              first_name=split_full_name(data_in.contact_person)[0],
                              last_name=split_full_name(data_in.contact_person)[1],
                              phone=data_in.phone,
                              investment_fund=investment_fund
                              )

            self.session.add(fund_admin)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)

    def del_investment_fund(self, id: int):
        stmt = select(InvestmentFund).where(InvestmentFund.id == id)
        investment_fund: InvestmentFund = self.session.execute(stmt).scalars().first()
        if not investment_fund:
            raise HTTPException(status_code=401, message=ErrorMessages.NOT_EXIST)

        self.session.delete(investment_fund)
        self.session.commit()

    def get_investment_fund(self):
        stmt = select(InvestmentFund)
        data: List[InvestmentFund] = self.session.execute(stmt).scalars().all()
        res = []
        for _investment_fund in data:
            for user in _investment_fund.fund_admins:
                res.append(InvestmentFundSchema(id=_investment_fund.id,
                                                name=_investment_fund.name,
                                                siren=_investment_fund.siren,
                                                contact_person=f'{user.first_name} {user.last_name}',
                                                email=user.email,
                                                phone=user.phone))
        return res
