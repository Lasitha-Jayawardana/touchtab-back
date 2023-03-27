from typing import Union, Type, List

from sqlalchemy import select

from constants.custom_types import RoleEnum
from constants.exceptions import ErrorMessages
from models.user import User, Department, AssetClass, Strategy, Fund, ManagementCompany, InvestmentFund, LP
from schemas.fund_admin import OnboardingSchema, FundStructureSchema, ManagementCompanySchema, TeamSchema, \
    DepartmentSchema, AssetClassSchema, StrategySchema
from schemas.fund_user import LPSchema, FundUserSchema
from utilities.exceptions import HTTPException
from utilities.helper import split_full_name
from utilities.logger import logger


class FundUserService:
    def __init__(self, session):
        self.session = session

    def get_fund_users(self):
        stmt = select(User).where(User.role == RoleEnum.fund_user)
        fund_users: User = self.session.execute(stmt).scalars().all()
        users = []
        for fund_user in fund_users:
            user = FundUserSchema.from_orm(fund_user)
            if fund_user.department:
                user.department_name = fund_user.department.name
            users.append(user)
        return users

    def add_lp(self, fund_user_id, data_in: LPSchema):
        stmt = select(User).where(User.id == fund_user_id)
        fund_user: User = self.session.execute(stmt).scalars().first()
        if not fund_user:
            raise HTTPException(status_code=401, message=ErrorMessages.USER_NOT_EXISTING)

        try:
            lp = LP(company_name=data_in.name,
                    siren=data_in.siren,
                    commitment=data_in.commitment,
                    department=fund_user.department)
            investor_admin = User(email=data_in.email,
                                  role=RoleEnum.fund_user,
                                  first_name=split_full_name(data_in.contact_person)[0],
                                  last_name=split_full_name(data_in.contact_person)[1],
                                  phone=data_in.phone,
                                  lp=lp
                                  )
            self.session.add(investor_admin)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)


    def get_lps(self, fund_user_id):
        stmt = select(LP).join(Department).join(User).where(
            User.id == fund_user_id)
        data: List[LP] = self.session.execute(stmt).scalars().all()
        res = []
        for _lp in data:
            for user in _lp.investor_admins:
                res.append(LPSchema(id=_lp.id,
                                    name=_lp.name,
                                    siren=_lp.siren,
                                    commitment=_lp.commitment,
                                    contact_person=f'{user.first_name} {user.last_name}',
                                    email=user.email,
                                    phone=user.phone))
        return res
