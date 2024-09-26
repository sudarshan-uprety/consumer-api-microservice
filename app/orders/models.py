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
    delivery_address = Column(String, nullable=False)
    status = Column(String, nullable=True)
    order_note = Column(String, nullable=True)
    payment_id = Column(Integer, ForeignKey('Payment.id'), nullable=False)

    user = relationship("Users", back_populates="orders")
    payment = relationship("UserPayment", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    class Config:
        orm_mode = True


class OrderItem(Common, Base, SerializerMixin):
    __tablename__ = 'OrderItems'
    id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey('Orders.id'), nullable=False)
    product_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_item = Column(Float, nullable=False)
    color = Column(String, nullable=True)
    size = Column(String, nullable=True)
    total_amount = Column(Float, nullable=False)
    order = relationship("Orders", back_populates="order_items")

    class Config:
        orm_mode = True
