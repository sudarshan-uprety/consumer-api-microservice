from app.payments.models import UserPayment
from app.payments.schema import TransactionDetails
from app.user.models import Users


def create_payment(payment: TransactionDetails, user: Users) -> UserPayment:
    print('payment is', payment.order_details)
