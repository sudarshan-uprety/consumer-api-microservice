from fastapi import status, APIRouter, Depends

from app.payments.schema import TransactionDetails, PaymentResponseSchema
from app.payments.utils import validate_payment
from app.user.models import Users
from utils import OAuth2, response

router = APIRouter(
    prefix="/payments",
    tags=['payment endpoints'],
)


@router.post('/create', status_code=status.HTTP_200_OK)
async def create_user_payment(data: TransactionDetails, user: Users = Depends(OAuth2.get_current_user)):
    orders, payment = validate_payment(data=data, user=user)
    response_data = PaymentResponseSchema(
        id=orders.id,
        payment_id=payment.id,
        payment_method=payment.payment_method,
        payment_amount=payment.payment_amount,
        payment_status=payment.payment_status,
        order_id=orders.id,
        delivery_address=orders.delivery_address,
        email=orders.user.email,
        phone_number=orders.user.phone,
    )
    return response.success(
        message='Payment created successfully',
        data=response_data.dict(),
        status_code=status.HTTP_201_CREATED,
        warning=None
    )
