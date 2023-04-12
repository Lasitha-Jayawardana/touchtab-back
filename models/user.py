from datetime import datetime

from sqlalchemy import Column, String, Enum, Unicode, ForeignKey, DateTime, Integer, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils import PasswordType

from constants.custom_types import RoleEnum, RoomTypeEnum, FoodTypeEnum, ServiceCategoryEnum
from database import Base
from constants.commons import Constant
from sqlalchemy.orm import relationship, backref


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String(Constant.DB_STRING_MEDIUM, collation="utf8mb4_bin"), unique=True)
    password = Column(PasswordType(Constant.DB_STRING_SIZE, schemes=["bcrypt"]))

    role = Column(Enum(RoleEnum))
    name = Column(String(Constant.DB_STRING_SHORT, collation="utf8mb4_bin"))
    phone = Column(String(Constant.DB_STRING_SHORT, collation="utf8mb4_bin"))
    image_url = Column(Unicode(Constant.DB_STRING_TEXT, collation="utf8mb4_bin"))

    admin = relationship("Admin", back_populates="user", uselist=False)
    guest = relationship("Guest", back_populates="user", uselist=False)

    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="admin")
    hotel = relationship("Hotel", back_populates="hotel_admins")
    hotel_id = Column(Integer, ForeignKey("hotel.id"))

    partner_id = Column(Integer, ForeignKey("partner.id"))
    partner = relationship("Partner", back_populates="partner_admins")


class Guest(Base):
    __tablename__ = "guest"
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="guest")

    hotel = relationship("Hotel", back_populates="guests")
    hotel_id = Column(Integer, ForeignKey("hotel.id"))

    reservation = relationship("Reservation", back_populates="guest", uselist=False)


class Hotel(Base):
    __tablename__ = "hotel"
    id = Column(Integer, primary_key=True)
    name = Column(String(Constant.DB_STRING_SHORT, collation="utf8mb4_bin"), unique=True)
    location = Column(String(Constant.DB_STRING_SIZE, collation="utf8mb4_bin"))
    image_url = Column(Unicode(Constant.DB_STRING_TEXT, collation="utf8mb4_bin"))
    wifi_password = Column(String(Constant.DB_STRING_SHORT, collation="utf8mb4_bin"))

    hotel_admins = relationship("Admin", back_populates="hotel")
    guests = relationship("Guest", back_populates="hotel")
    rooms = relationship("Room", back_populates="hotel")
    services = relationship("Service", back_populates="hotel")


class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True)
    number = Column(String(Constant.DB_STRING_SHORT, collation="utf8mb4_bin"))
    type = Column(Enum(RoomTypeEnum))
    price = Column(Float)
    capacity = Column(Integer)

    availability = Column(Boolean, default=False)

    image_url = Column(Unicode(Constant.DB_STRING_TEXT, collation="utf8mb4_bin"))

    hotel_id = Column(Integer, ForeignKey("hotel.id"))
    hotel = relationship("Hotel", back_populates="rooms")

    reservation = relationship("Reservation", back_populates="room", uselist=False)


class Reservation(Base):
    __tablename__ = "reservation"
    id = Column(Integer, primary_key=True)

    check_in = Column(DateTime)
    check_out = Column(DateTime)

    guest_id = Column(Integer, ForeignKey("guest.id"))
    room_id = Column(Integer, ForeignKey("room.id"))

    guest = relationship("Guest", back_populates="reservation")
    room = relationship("Room", back_populates="reservation")


class Service(Base):
    __tablename__ = "service"
    id = Column(Integer, primary_key=True)
    name = Column(String(Constant.DB_STRING_SHORT, collation="utf8mb4_bin"))
    description = Column(String(Constant.DB_STRING_SIZE, collation="utf8mb4_bin"))

    service_category = Column(Enum(ServiceCategoryEnum))

    hotel_id = Column(Integer, ForeignKey("hotel.id"))
    hotel = relationship("Hotel", back_populates="services")

    partner_id = Column(Integer, ForeignKey("partner.id"))
    partner = relationship("Partner", back_populates="services")

    meeting_room = relationship("MeetingRoom", back_populates="service", uselist=False)
    baby_sitter = relationship("BabySitter", back_populates="service", uselist=False)
    boat = relationship("Boat", back_populates="service", uselist=False)
    restaurant = relationship("Restaurant", back_populates="service", uselist=False)


class Partner(Base):
    __tablename__ = "partner"
    id = Column(Integer, primary_key=True)
    name = Column(String(Constant.DB_STRING_SHORT, collation="utf8mb4_bin"))
    location = Column(String(Constant.DB_STRING_SIZE, collation="utf8mb4_bin"))

    services = relationship("Service", back_populates="partner")

    partner_admins = relationship("Admin", back_populates="partner")


class MeetingRoom(Base):
    __tablename__ = "meeting_room"
    id = Column(Integer, primary_key=True)
    name = Column(String(Constant.DB_STRING_SHORT, collation="utf8mb4_bin"))
    place = Column(String(Constant.DB_STRING_SIZE, collation="utf8mb4_bin"))
    price = Column(Float)
    rate = Column(Float)
    capacity = Column(Integer)

    image_url = Column(Unicode(Constant.DB_STRING_TEXT, collation="utf8mb4_bin"))
    availability = Column(Boolean, default=False)

    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service", back_populates="meeting_room")


class BabySitter(Base):
    __tablename__ = "baby_sitter"
    id = Column(Integer, primary_key=True)
    name = Column(String(Constant.DB_STRING_SHORT, collation="utf8mb4_bin"))
    place = Column(String(Constant.DB_STRING_SIZE, collation="utf8mb4_bin"))
    capacity = Column(Integer)

    price = Column(Float)
    rate = Column(Float)
    image_url = Column(Unicode(Constant.DB_STRING_TEXT, collation="utf8mb4_bin"))
    reserved = Column(Integer,default=0)

    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service", back_populates="baby_sitter")


class Boat(Base):
    __tablename__ = "boat"
    id = Column(Integer, primary_key=True)
    name = Column(String(Constant.DB_STRING_SHORT, collation="utf8mb4_bin"))
    place = Column(String(Constant.DB_STRING_SIZE, collation="utf8mb4_bin"))
    description = Column(String(Constant.DB_STRING_SIZE, collation="utf8mb4_bin"))
    seats = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    price = Column(Float)
    rate = Column(Float)
    image_url = Column(Unicode(Constant.DB_STRING_TEXT, collation="utf8mb4_bin"))
    reserved = Column(Integer)

    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service", back_populates="boat")


class Restaurant(Base):
    __tablename__ = "restaurant"
    id = Column(Integer, primary_key=True)
    name = Column(String(Constant.DB_STRING_SHORT, collation="utf8mb4_bin"))
    cuisine_type = Column(String(Constant.DB_STRING_SHORT, collation="utf8mb4_bin"))

    place = Column(String(Constant.DB_STRING_SIZE, collation="utf8mb4_bin"))
    description = Column(String(Constant.DB_STRING_SIZE, collation="utf8mb4_bin"))
    # open_time = Column(DateTime)
    # close_time = Column(DateTime)
    open_time = Column(String(Constant.DB_STRING_SHORT, collation="utf8mb4_bin"))
    close_time = Column(String(Constant.DB_STRING_SHORT, collation="utf8mb4_bin"))

    image_url = Column(Unicode(Constant.DB_STRING_TEXT, collation="utf8mb4_bin"))

    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service", back_populates="restaurant")
    capacity = Column(Integer)

    food_menus = relationship("FoodMenu", back_populates="restaurant")


class FoodMenu(Base):
    __tablename__ = "food_menu"
    id = Column(Integer, primary_key=True)
    name = Column(String(Constant.DB_STRING_SHORT, collation="utf8mb4_bin"))
    description = Column(String(Constant.DB_STRING_SIZE, collation="utf8mb4_bin"))

    price = Column(Float)
    rate = Column(Float)
    image_url = Column(Unicode(Constant.DB_STRING_TEXT, collation="utf8mb4_bin"))
    type = Column(Enum(FoodTypeEnum))

    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))
    restaurant = relationship("Restaurant", back_populates="food_menus")

    food_category_id = Column(Integer, ForeignKey("food_category.id"))
    food_category = relationship("FoodCategory", back_populates="food_menus")


class FoodCategory(Base):
    __tablename__ = "food_category"
    id = Column(Integer, primary_key=True)
    name = Column(String(Constant.DB_STRING_SHORT, collation="utf8mb4_bin"))

    food_menus = relationship("FoodMenu", back_populates="food_category")
