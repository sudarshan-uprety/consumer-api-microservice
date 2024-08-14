from fastapi import status, APIRouter, Depends, BackgroundTasks

from app.events.producer import produce
from app.events.schema import ReduceQuantityEvent, ProductItem
from app.payments.schema import TransactionDetails, PaymentResponseSchema
from app.payments.utils import validate_payment
from app.user.models import Users
from utils import OAuth2, response, log, variables

router = APIRouter(
    prefix="/payments",
    tags=['payment endpoints'],
)


@router.post('/create', status_code=status.HTTP_200_OK)
async def create_user_payment(
        data: TransactionDetails,
        background_tasks: BackgroundTasks,
        user: Users = Depends(OAuth2.get_current_user)
):
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

    event_data = ReduceQuantityEvent(
        trace_id=log.trace_id_var.get(),
        operation='decrease',
        product=[ProductItem(product_id=product.product_id, quantity=product.quantity)
                 for product in orders.order_items]
    ).json()
    background_tasks.add_task(produce, event_data, variables.INVENTORY_QUEUE)
    return response.success(
        message='Payment created successfully',
        data=response_data.dict(),
        status_code=status.HTTP_201_CREATED,
        warning=None
    )
