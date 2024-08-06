from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from app.common.models import Common
from utils.database import Base


class Orders(Common, Base, SerializerMixin):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    product_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_item = Column(Float, nullable=False)
    payment_id = Column(Integer, ForeignKey('Payment.id'), nullable=False)
    delivery_address = Column(String, nullable=False)
    status = Column(String, nullable=True)
    order_note = Column(String, nullable=True)
    user = relationship("Users", back_populates="orders")

    # payment = relationship("UserPayment", back_populates="orders")

    class Config:
        orm_mode = True
