from enum import Enum


class RoleEnum(Enum):
    super_admin = 'super_admin'
    hotel_admin = 'hotel_admin'
    partner_admin = 'partner_admin'
    guest = 'guest'


class RoomTypeEnum(Enum):
    presidential = 'presidential'
    junior = 'junior'
    standard = 'standard'
    honeymoon = 'honeymoon'
    bridal = 'bridal'
    penthouse = 'penthouse'


class ServiceCategoryEnum(Enum):
    restaurant = 'restaurant'
    baby_sitter = 'baby_sitter'
    meeting_room = 'meeting_room'
    boat = 'boat'


class FoodTypeEnum(Enum):
    starters = 'starters'
    main_course = 'main_course'
    desserts = 'desserts'
    drinks = 'drinks'


class TokenIssuerEnum(Enum):
    refresh = 'refresh'
    access = 'access'
    reset = 'reset'
