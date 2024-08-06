from app.orders.schemas import ProductOrder
from app.payments.models import UserPayment


def create_order(orders: ProductOrder, payment: UserPayment):
    print(orders)
    for order in orders:
        print('order is', order)
    return None
