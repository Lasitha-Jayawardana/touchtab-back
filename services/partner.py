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


class PartnerService:
    def __init__(self, session):
        self.session = session
        self.user_service = UserService(session)
        # self.agent_service = AgentService(session)
        # self.customer_service = CustomerService()
        # self.shared_service = SharedService(session)
        # self.email_service = EmailService()

    def create_partner(self, data_in: PartnerSchema):
        stmt = select(Partner).where(Partner.name == data_in.name)
        partner = self.session.execute(stmt).scalars().first()
        if partner:
            raise HTTPException(status_code=401, message=ErrorMessages.EXISTING_ITEM)

        try:
            orm = Partner(name=data_in.name,
                          location=data_in.location,
                          )

            self.session.add(orm)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)

    def create_partner_admin(self, id, data: UserSchema):
        stmt = select(Partner).where(Partner.id == id)
        partner = self.session.execute(stmt).scalars().first()
        if not partner:
            raise HTTPException(status_code=401, message='Hotel not found')

        try:
            data.role = RoleEnum.partner_admin
            user: User = self.user_service.create_user(data)
            if user and (not user.admin):
                user.admin = Admin(partner=partner)
            self.session.add(user)
            self.session.commit()
        except Exception as exc:
            logger.debug(exc)

    def get_partners(self):
        stmt = select(Partner)
        data: List[Partner] = self.session.execute(stmt).scalars().all()
        res = PartnerSchema.from_orm_list(data)
        return res
