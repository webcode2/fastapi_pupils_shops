import enum
from datetime import datetime, timedelta
from ..main import Base

from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, BOOLEAN, Enum, TEXT
from .mixin import Timestamp
from sqlalchemy.orm import relationship


class Role(enum.IntEnum):
    superuser = 1
    staff = 2
    resident = 3
    security = 4


class User(Timestamp, Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name: str = Column(String(100), nullable=False)
    last_name: str = Column(String(100), nullable=False)
    email: str = Column(String(255), unique=True, nullable=False)
    phone: str = Column(String(10), unique=True, nullable=False)
    hashed_password: str = Column(String(128), nullable=False)
    disabled: bool = Column(BOOLEAN, default=False)
    role = Column(Enum(Role), default=Role.resident, nullable=False)

    # # Relationship with other models (optional)
    tokens = relationship("Token", back_populates="owner",cascade="all, delete")
    resident_info = relationship("Resident", uselist=False, back_populates="resident",cascade="all, delete")
    user_complaint = relationship("Complaint", back_populates="complaint_owner",cascade="all, delete")

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class Token(Timestamp, Base):
    __tablename__ = "tokens"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code: str = Column(String(5),index=True)
    verified: bool = Column(BOOLEAN, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tokens")



#
class Resident(Timestamp, Base):
    __tablename__ = "residents"
    id: int = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    house_num: int = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resident = relationship('User', back_populates="resident_info")


class Complaint(Timestamp, Base):
    __tablename__ = "complaints"

    message: str = Column(TEXT, nullable=False)
    title:str=Column(String(100),nullable=False,)
    id: int = Column(BigInteger, index=True, autoincrement=True, primary_key=True)
    created_date = Column(String, default=datetime.now())

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    complaint_owner = relationship("User", back_populates="user_complaint")

    def __str__(self):
        return f"{self.complaint_owner.get_full_name()} - {self.title}"
