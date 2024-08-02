from app.payments.models import UserPayment
from app.payments.schema import TransactionDetails
from app.user.models import Users
from utils import store


def create_payment(payment: TransactionDetails, user: Users) -> UserPayment:
    payment = payment.dict()
    payment['user_id'] = user.id
    payment_obj = UserPayment(**payment)
    store.session.add(payment_obj)
    store.session.commit()
    return payment_obj
