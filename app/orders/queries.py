from app.orders.models import Orders
from app.orders.schemas import ProductOrder
from app.user.models import Users
from utils import store


def create_order(orders: ProductOrder, user: Users):
    for order in orders:
        order_data = order.dict()
        order_data['user_id'] = user.id
        order_obj = Orders(**order_data)
        store.session.add(order_obj)
        store.session.commit()
    return None
