from typing import Union, Type

from sqlalchemy import select

from constants.custom_types import RoleEnum
from constants.exceptions import ErrorMessages
from models.user import User, Department, AssetClass, Strategy, Fund
from schemas.fund_admin import OnboardingSchema, FundStructureSchema
from schemas.investor import InvestorOutSchema
from utilities.exceptions import HTTPException
from utilities.logger import logger


class InvestorService:
    def __init__(self, session):
        self.session = session
        # self.admin_service = AdminService()
        # self.agent_service = AgentService(session)
        # self.customer_service = CustomerService()
        # self.shared_service = SharedService(session)
        # self.email_service = EmailService()

    def getInvestor(self, id):
        stmt = select(User).where(User.id == id).where(User.role == RoleEnum.investor)
        investor: User = self.session.execute(stmt).scalars().first()
        res = InvestorOutSchema.from_orm(investor)
        return res

    def onboarding(self, id):
        stmt = select(User).where(User.id == id).where(User.role == RoleEnum.investor)
        fund_admin: User = self.session.execute(stmt).scalars().first()
        # if not fund_admin:
        #     raise HTTPException(status_code=401, message=ErrorMessages.USER_NOT_EXISTING)
        #
        # try:
        #
        #     if data_in.departments:
        #         for _department in data_in.departments:
        #             fund_admin.departments.append(Department(name=_department.name))
        #
        #     if data_in.asset_classes:
        #         for _item in data_in.asset_classes:
        #             fund_admin.asset_classes.append(AssetClass(name=_item.name))
        #
        #     if data_in.strategies:
        #         for _item in data_in.strategies:
        #             fund_admin.strategies.append(Strategy(name=_item.name))
        #
        #     if data_in.funds:
        #         for _item in data_in.funds:
        #             fund_admin.funds.append(Fund(name=_item.name))
        #
        #     if data_in.source_of_funds:
        #         for _item in data_in.source_of_funds:
        #             fund_admin.source_of_funds.append(SourceOfFund(name=_item.name, email=_item.email, team=_item.team))
        #
        #     self.session.add(fund_admin)
        #     self.session.commit()
        # except Exception as exc:
        #     logger.debug(exc)

    def get_fund_structure(self, fund_admin_id, structure: Union[
        Type[Department], Type[AssetClass], Type[Fund], Type[Strategy]],
                           schema_out: Union[
                               Type[FundStructureSchema], ] = FundStructureSchema):
        stmt = select(structure).where(structure.fund_admin_id == fund_admin_id)
        data: structure = self.session.execute(stmt).scalars().all()
        res = schema_out.from_orm_list(data)
        return res
