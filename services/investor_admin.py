from typing import Union, Type, List

from sqlalchemy import select

from constants.custom_types import RoleEnum
from constants.exceptions import ErrorMessages
from models.user import User, Department, AssetClass, Strategy, Fund, InvestmentVehicle, LP

from schemas.investor_admin import BeneficialOwnersSchema, InvestmentVehicleSchema
from schemas.fund_admin import OnboardingSchema, FundStructureSchema
from utilities.exceptions import HTTPException
from utilities.helper import split_full_name
from utilities.logger import logger


class InvestorAdminService:
    def __init__(self, session):
        self.session = session
        # self.admin_service = AdminService()
        # self.agent_service = AgentService(session)
        # self.customer_service = CustomerService()
        # self.shared_service = SharedService(session)
        # self.email_service = EmailService()

    def add_beneficial_owners(self, investor_admin_id, data_in: BeneficialOwnersSchema,role:RoleEnum):
        stmt = select(User).where(User.id == investor_admin_id)
        investor_admin: User = self.session.execute(stmt).scalars().first()
        if not investor_admin:
            raise HTTPException(status_code=401, message=ErrorMessages.USER_NOT_EXISTING)

        try:

            investor = User(email=data_in.email,
                            role=role,
                            role_type=data_in.type,
                            first_name=split_full_name(data_in.contact_person)[0],
                            last_name=split_full_name(data_in.contact_person)[1],
                            phone=data_in.phone,
                            investment_vehicle_id=data_in.investment_vehicle_id
                            )
            self.session.add(investor)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)

    def get_beneficial_owners(self, investor_admin_id: int,role:RoleEnum):
        stmt = select(User).where(User.id == investor_admin_id)
        investor_admin: User = self.session.execute(stmt).scalars().first()



        res = []
        for _investment_vehicle in investor_admin.lp.investment_vehicles:
            _users = _investment_vehicle.users
            for _user in _users:
                if _user.role ==role:
                    res.append(BeneficialOwnersSchema(id=_user.id,
                                              type=_user.role_type,
                                              investment_vehicle=_investment_vehicle.company_name,
                                              investment_vehicle_id=_investment_vehicle.id,
                                              contact_person=f'{_user.first_name} {_user.last_name}',
                                              email=_user.email,
                                              phone=_user.phone))
        return res


    # def del_beneficial_owners(self, id: int):
    #     stmt = select(BeneficialOwner).where(BeneficialOwner.id == id)
    #     beneficial_owners: BeneficialOwner = self.session.execute(stmt).scalars().first()
    #     if not beneficial_owners:
    #         raise HTTPException(status_code=401, message=ErrorMessages.NOT_EXIST)
    #
    #     self.session.delete(beneficial_owners)
    #     self.session.commit()

    def add_investment_vehicle(self, investor_admin_id, data_in: InvestmentVehicleSchema):
        stmt = select(User).where(User.id == investor_admin_id)
        investor_admin: User = self.session.execute(stmt).scalars().first()
        if not investor_admin:
            raise HTTPException(status_code=401, message=ErrorMessages.USER_NOT_EXISTING)

        try:
            investment_vehicle = InvestmentVehicle(company_name=data_in.name,
                                                   siren=data_in.siren,
                                                   commitment=data_in.commitment,
                                                   lp=investor_admin.lp)
            investor = User(email=data_in.email,
                            role=RoleEnum.investor,
                            first_name=split_full_name(data_in.contact_person)[0],
                            last_name=split_full_name(data_in.contact_person)[1],
                            phone=data_in.phone,
                            investment_vehicle=investment_vehicle
                            )
            self.session.add(investor)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)

    def del_investment_vehicle(self, id: int):
        stmt = select(InvestmentVehicle).where(InvestmentVehicle.id == id)
        investment_vehicle: InvestmentVehicle = self.session.execute(stmt).scalars().first()
        if not investment_vehicle:
            raise HTTPException(status_code=401, message=ErrorMessages.NOT_EXIST)

        self.session.delete(investment_vehicle)
        self.session.commit()

    def get_investment_vehicle(self, investor_admin_id: int):
        stmt = select(InvestmentVehicle).join(LP).join(User).where(User.id == investor_admin_id)
        data: List[InvestmentVehicle] = self.session.execute(stmt).scalars().all()
        res = []
        for _investment_vehicle in data:
            for user in _investment_vehicle.users:  # User
                if user.role == RoleEnum.investor:
                    res.append(InvestmentVehicleSchema(id=_investment_vehicle.id,
                                                       name=_investment_vehicle.company_name,
                                                       siren=_investment_vehicle.siren,
                                                       commitment=_investment_vehicle.commitment,
                                                       contact_person=f'{user.first_name} {user.last_name}',
                                                       email=user.email,
                                                       phone=user.phone))
        return res
    #
    # def add_legal_representative(self, data_in: LegalRepresentativeSchema):
    #     stmt = select(User).where(User.id == data_in.investor_admin_id)
    #     investor_admin: User = self.session.execute(stmt).scalars().first()
    #     if not investor_admin:
    #         raise HTTPException(status_code=401, message=ErrorMessages.USER_NOT_EXISTING)
    #
    #     try:
    #         investor_admin.legal_representatives.append(LegalRepresentative(type=data_in.type,
    #                                                                         name=data_in.name,
    #                                                                         contact_person=data_in.contact_person,
    #                                                                         email=data_in.email,
    #                                                                         phone=data_in.phone))
    #
    #         self.session.add(investor_admin)
    #         self.session.commit()
    #     except Exception as exc:
    #         logger.debug(exc)
    #
    # def del_legal_representative(self, id: int):
    #     stmt = select(LegalRepresentative).where(LegalRepresentative.id == id)
    #     legal_representative: LegalRepresentative = self.session.execute(stmt).scalars().first()
    #     if not legal_representative:
    #         raise HTTPException(status_code=401, message=ErrorMessages.NOT_EXIST)
    #
    #     self.session.delete(legal_representative)
    #     self.session.commit()
    #
    # def get_legal_representative(self, investor_admin_id: int):
    #     stmt = select(LegalRepresentative).where(LegalRepresentative.investor_admin_id == investor_admin_id)
    #     data: List[BeneficialOwner] = self.session.execute(stmt).scalars().all()
    #     res = LegalRepresentativeSchema.from_orm_list(data)
    #     return res
