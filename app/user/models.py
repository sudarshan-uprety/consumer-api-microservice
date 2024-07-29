from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    UniqueConstraint,
    DateTime,
    PrimaryKeyConstraint
)
from sqlalchemy_serializer import SerializerMixin

from utils.database import Base
from app.common.models import Common


class Users(Base, Common, SerializerMixin):
    """Models a user table"""
    __tablename__ = "Users"
    serialize_only = ('id', 'email', 'full_name', 'phone', 'address')
    id = Column(Integer, nullable=False, primary_key=True)
    phone = Column(String(15), nullable=False, unique=True)
    full_name = Column(String(225), nullable=False)
    email = Column(String(225), nullable=False, unique=True)
    password = Column(String, nullable=False)
    address = Column(String(225), nullable=False)
    is_active = Column(Boolean, default=False)

    UniqueConstraint("email", name="uq_user_email")
    PrimaryKeyConstraint("id", name="pk_user_id")

    class Config:
        orm_mode = True


class UsedToken(Base):
    __tablename__ = "used_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    used_at = Column(DateTime)
