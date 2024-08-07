from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    ForeignKey,
    PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from app.common.models import Common
from utils.database import Base


class UserPayment(Base, Common, SerializerMixin):
    """Models a user payment table"""
    __tablename__ = "Payment"
    serialize_only = ('id', 'user_id', 'payment_id', 'payment_method', 'order_id')
    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    payment_uuid = Column(String, nullable=False)
    payment_method = Column(String, nullable=False)
    payment_amount = Column(Float, nullable=False)
    payment_status = Column(String, nullable=False)
    product_code = Column(String, nullable=False)
    ref_id = Column(String, nullable=False)

    PrimaryKeyConstraint("id", name="pk_payment_id")

    user = relationship("Users", back_populates="payments")
    orders = relationship("Orders", back_populates="payment")

    class Config:
        orm_mode = True
