from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)
from sqlalchemy_serializer import SerializerMixin

from app.common.models import Common
from utils.database import Base


class Order(Common, Base, SerializerMixin):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('Products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
