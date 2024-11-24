import enum
from datetime import datetime, timedelta

from pydantic import Extra

from ..main import Base

from sqlalchemy import Column, Integer, String,  ForeignKey, BOOLEAN
from .mixin import Timestamp, UserBasic
from sqlalchemy.orm import relationship, Relationship



class Role(Timestamp, Base):
    __tablename__ = "roles"
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name: str = Column(String(100), nullable=False)
    created_by: int = Column(Integer, ForeignKey("users.id", ))
    staffs = Relationship("Staff", secondary="staffs_roles", back_populates="roles")


class ResidentialAddress(Timestamp, Base):
    __tablename__ = "staff_resident"
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    house_no: int = Column(Integer)
    street_name: str = Column(String(100), nullable=False)
    lga: str = Column(String(100), nullable=False)
    state_of_origin: str = Column(String(100), nullable=False)
    staff = Relationship("Staff", back_populates="resident_info")
    account_id = Column(Integer, ForeignKey("staff.id"))


class Staff(Base,UserBasic, Timestamp):
    __tablename__ = "staff"
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    resident_info = relationship("ResidentialAddress", uselist=False, back_populates="staff", cascade="all, delete")
    roles = Relationship("Role", secondary="staffs_roles", back_populates="staffs")

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class StaffRole(Timestamp, Base):
    __tablename__ = "staffs_roles"
    staff_id: int = Column(Integer, ForeignKey("staff.id"), nullable=False, primary_key=True)
    role_id: int = Column(Integer, ForeignKey("roles.id"), nullable=False, primary_key=True)
