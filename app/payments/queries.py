from app.payments.models import UserPayment
from app.user.models import Users
from utils import store


def create_payment(payment, user: Users) -> UserPayment:
    payment_obj = UserPayment(
        user_id=user.id,
        payment_status=payment['status'],
        payment_amount=payment['total_amount'],
        payment_uuid=payment['transaction_uuid'],
        payment_method='ESEWA',
        product_code=payment['product_code'],
        ref_id=payment['ref_id']
    )
    store.session.add(payment_obj)
    store.session.commit()
    return payment_obj
