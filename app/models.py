from sqlalchemy import (
    LargeBinary,
    Column,
    String,
    Integer,
    Boolean,
    UniqueConstraint,
    PrimaryKeyConstraint,
    DateTime,
    func
)
from app.database.database import Base


class Common(object):
    __abstract__ = True  # Set this class as an abstract base class
    __tablename__ = "common"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), nullable=False, onupdate=func.now())


class User(Base, Common):
    """Models a user table"""
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True)
    phone = Column(String(15), nullable=False, unique=True)
    full_name = Column(String(225), nullable=False)
    email = Column(String(225), nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    UniqueConstraint("email", name="uq_user_email")
    PrimaryKeyConstraint("id", name="pk_user_id")
