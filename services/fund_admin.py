from typing import Union, Type, List

from sqlalchemy import select

from constants.custom_types import RoleEnum
from constants.exceptions import ErrorMessages
from models.user import User, Department, AssetClass, Strategy, Fund, ManagementCompany, InvestmentFund
from schemas.fund_admin import OnboardingSchema, FundStructureSchema, ManagementCompanySchema, TeamSchema, \
    DepartmentSchema, AssetClassSchema, StrategySchema
from utilities.exceptions import HTTPException
from utilities.helper import split_full_name
from utilities.logger import logger


class FundAdminService:
    def __init__(self, session):
        self.session = session
        # self.admin_service = AdminService()
        # self.agent_service = AgentService(session)
        # self.customer_service = CustomerService()
        # self.shared_service = SharedService(session)
        # self.email_service = EmailService()

    def onboarding(self, data_in: OnboardingSchema):
        stmt = select(User).where(User.id == data_in.fund_admin_id)
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

    def add_management_company(self, fund_admin_id, data_in: ManagementCompanySchema):
        stmt = select(User).where(User.id == fund_admin_id)
        fund_admin: User = self.session.execute(stmt).scalars().first()
        if not fund_admin:
            raise HTTPException(status_code=401, message=ErrorMessages.USER_NOT_EXISTING)
        if not fund_admin.investment_fund:
            raise HTTPException(status_code=401, message=ErrorMessages.INVESTMENT_FUND_NOT_DEFINED)

        try:
            management_company = ManagementCompany(name=data_in.name,
                                                   siren=data_in.siren,
                                                   investment_fund_id=fund_admin.investment_fund.id)

            self.session.add(management_company)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)

    def get_management_companies(self, fund_admin_id):
        stmt = select(ManagementCompany).join(InvestmentFund).join(User).where(User.id == fund_admin_id)
        data: List[ManagementCompany] = self.session.execute(stmt).scalars().all()
        res = ManagementCompanySchema.from_orm_list(data)
        return res

    def add_asset_class(self, fund_admin_id, data_in: AssetClassSchema):
        stmt = select(User).where(User.id == fund_admin_id)
        fund_admin: User = self.session.execute(stmt).scalars().first()
        if not fund_admin:
            raise HTTPException(status_code=401, message=ErrorMessages.USER_NOT_EXISTING)
        if not fund_admin.investment_fund:
            raise HTTPException(status_code=401, message=ErrorMessages.INVESTMENT_FUND_NOT_DEFINED)

        try:
            asset_class = AssetClass(name=data_in.name,
                                     management_company_id=data_in.management_company_id)
            self.session.add(asset_class)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)

    def get_asset_classes(self, fund_admin_id):
        stmt = select(AssetClass).join(ManagementCompany).join(InvestmentFund).join(User).where(
            User.id == fund_admin_id)
        data: List[AssetClass] = self.session.execute(stmt).scalars().all()
        res = []
        for _asset_class in data:
            res.append(AssetClassSchema(id=_asset_class.id,
                                        name=_asset_class.name,
                                        management_company_id=_asset_class.management_company_id,
                                        management_company=_asset_class.management_company.name,
                                        ))
        return res

    def add_strategy(self, fund_admin_id, data_in: StrategySchema):
        stmt = select(User).where(User.id == fund_admin_id)
        fund_admin: User = self.session.execute(stmt).scalars().first()

        if not fund_admin:
            raise HTTPException(status_code=401, message=ErrorMessages.USER_NOT_EXISTING)
        if not fund_admin.investment_fund:
            raise HTTPException(status_code=401, message=ErrorMessages.INVESTMENT_FUND_NOT_DEFINED)

        try:
            strategy = Strategy(name=data_in.name,
                                asset_class_id=data_in.asset_class_id)
            self.session.add(strategy)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)

    def get_strategies(self, fund_admin_id):
        stmt = select(Strategy).join( AssetClass).join(ManagementCompany).join(InvestmentFund).join(User).where(
            User.id == fund_admin_id)
        data: List[Strategy] = self.session.execute(stmt).scalars().all()
        res = []
        for _strategy in data:
            res.append(StrategySchema(id=_strategy.id,
                                      name=_strategy.name,
                                      asset_class_id=_strategy.asset_class_id,
                                      asset_class=_strategy.asset_class.name,
                                      ))
        return res

    def add_department(self, fund_admin_id, data_in: DepartmentSchema):
        stmt = select(User).where(User.id == fund_admin_id)
        fund_admin: User = self.session.execute(stmt).scalars().first()
        if not fund_admin:
            raise HTTPException(status_code=401, message=ErrorMessages.USER_NOT_EXISTING)

        try:
            department = Department(name=data_in.name,
                                    management_company_id=data_in.management_company_id)
            fund_user = User(email=data_in.email,
                             role=RoleEnum.fund_user,
                             first_name=split_full_name(data_in.contact_person)[0],
                             last_name=split_full_name(data_in.contact_person)[1],
                             phone=data_in.phone,
                             department=department
                             )
            self.session.add(fund_user)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)

    def get_departments(self, fund_admin_id):
        stmt = select(Department).join(ManagementCompany).join(InvestmentFund).join(User).where(
            User.id == fund_admin_id)
        data: List[Department] = self.session.execute(stmt).scalars().all()
        res = []
        for _department in data:
            for user in _department.fund_users:
                res.append(DepartmentSchema(id=_department.id,
                                            name=_department.name,
                                            management_company_id=_department.management_company_id,
                                            management_company=_department.management_company.name,
                                            contact_person=f'{user.first_name} {user.last_name}',
                                            email=user.email,
                                            phone=user.phone))
        return res

    def get_fund_structure(self, fund_admin_id, structure: Union[
        Type[Department], Type[AssetClass], Type[Fund], Type[ManagementCompany], Type[Strategy]],
                           schema_out: Union[
                               Type[FundStructureSchema], Type[ManagementCompanySchema]] = FundStructureSchema):
        stmt = select(structure).join(InvestmentFund).where(InvestmentFund.fund_admin_id == fund_admin_id)
        data: structure = self.session.execute(stmt).scalars().all()
        res = schema_out.from_orm_list(data)
        return res

    def add_fund_structure(self, fund_admin_id, data_in: Union[
        Type[ManagementCompanySchema], Type[FundStructureSchema],], Structure: Union[
        Type[Department], Type[AssetClass], Type[Fund], Type[ManagementCompany], Type[Strategy]]):

        stmt = select(User).where(User.id == fund_admin_id)
        fund_admin: User = self.session.execute(stmt).scalars().first()
        if not fund_admin:
            raise HTTPException(status_code=401, message=ErrorMessages.USER_NOT_EXISTING)

        try:
            if Structure == ManagementCompany:
                structure_orm = Structure(name=data_in.name,
                                          siren=data_in.siren,
                                          contact_person=data_in.contact_person,
                                          email=data_in.email,
                                          phone=data_in.phone,
                                          investment_fund_id=fund_admin.investment_fund.id)
            else:
                structure_orm = Structure(name=data_in.name, investment_fund_id=fund_admin.investment_fund.id)

            self.session.add(structure_orm)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)

    def del_structure(self, id: int, Structure: Union[
        Type[Department], Type[AssetClass], Type[Fund], Type[ManagementCompany], Type[Strategy]]):

        stmt = select(Structure).where(Structure.id == id)
        structure = self.session.execute(stmt).scalars().first()
        if not structure:
            raise HTTPException(status_code=401, message=ErrorMessages.NOT_EXIST)

        self.session.delete(structure)
        self.session.commit()

    def add_team(self, data_in: TeamSchema):
        stmt = select(User).where(User.id == data_in.email)
        fund_user: User = self.session.execute(stmt).scalars().first()

        try:
            if not fund_user:
                fund_user = User(email=data_in.email,
                                 role=RoleEnum.fund_user,
                                 first_name=split_full_name(data_in.contact_person)[0],
                                 last_name=split_full_name(data_in.contact_person)[1],
                                 phone=data_in.phone,
                                 )
            fund_user.department_id = data_in.department_id

            self.session.add(fund_user)
            self.session.commit()


        except Exception as exc:
            logger.debug(exc)

    def get_teams(self, fund_admin_id):
        stmt = select(User).where(User.id == fund_admin_id)
        fund_admin: User = self.session.execute(stmt).scalars().first()
        if not fund_admin:
            raise HTTPException(status_code=401, message=ErrorMessages.USER_NOT_EXISTING)

        departments = fund_admin.investment_fund.departments
        teams = []
        for department in departments:
            for fund_user in department.fund_users:
                teams.append(TeamSchema(email=fund_user.email,
                                        department=department.name,
                                        department_id=department.id,
                                        contact_person=fund_user.first_name,
                                        phone=fund_user.phone,
                                        ))

        return teams

    def del_team(self, email):
        stmt = select(User).where(User.email == email)
        fund_user = self.session.execute(stmt).scalars().first()
        if not fund_user:
            raise HTTPException(status_code=401, message=ErrorMessages.NOT_EXIST)

        self.session.delete(fund_user)
        self.session.commit()
