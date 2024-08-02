from app.orders.models import Order
from app.payments.models import UserPayment
from app.payments.schema import TransactionDetails
from app.user.models import Users
from utils import store


def create_payment(payment: TransactionDetails, user: Users) -> UserPayment:
    data = payment.dict()
    order_data = data.pop('order_details')
    payment_data = data
    payment_obj = UserPayment(**payment_data)
    order_obj = Order(**order_data)
    store.session.add(payment_obj, order_obj)
    store.session.commit()
    return payment_obj
