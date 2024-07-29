from datetime import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    ForeignKey,
    Column,
    String,
    Integer,
    Boolean,
    UniqueConstraint,
    PrimaryKeyConstraint,
    DateTime,
    func
)
from sqlalchemy.orm import relationship

from app.database.database import SessionLocal

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def get(cls, db: SessionLocal, id: int):
        return db.query(cls).filter(cls.id == id).first()

    @classmethod
    def filter(cls, db: SessionLocal, **kwargs):
        return db.query(cls).filter_by(**kwargs)

    @classmethod
    def create(cls, db: SessionLocal, **kwargs):
        instance = cls(**kwargs)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    def update(self, db: SessionLocal, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.commit()
        db.refresh(self)
        return self

    def delete(self, db: SessionLocal):
        db.delete(self)
        db.commit()


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
    payments = relationship("UserPayment", back_populates="user")
    orders = relationship("UserOrder", back_populates="user")

    UniqueConstraint("email", name="uq_user_email")
    PrimaryKeyConstraint("id", name="pk_user_id")


class UsedToken(Base):
    __tablename__ = "used_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    used_at = Column(DateTime)


class UserPayment(Base, Common):
    __tablename__ = "user_payments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    payment_id = Column(String, index=True, unique=True)
    payment_method = Column(String, index=True)
    amount_paid = Column(String, index=True)
    user = relationship("User", back_populates="payments")
    order = relationship("UserOrder", back_populates="payment", uselist=False)


class UserOrder(Base, Common):
    __tablename__ = "user_orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="orders")
    payment_id = Column(Integer, ForeignKey("user_payments.id"), nullable=True)
    payment = relationship("UserPayment", back_populates="order")
    product = Column(String, index=True)
    quantity = Column(Integer, index=True)
    price = Column(String, index=True)
    address = Column(String, index=True)
    is_delivered = Column(Boolean, default=False)
