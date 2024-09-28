from datetime import datetime

from fastapi import status, APIRouter, Depends, BackgroundTasks

from app.events.producer import produce
from app.events.schema import ReduceQuantityEvent, ProductItem
from app.payments.schema import TransactionDetails, PaymentResponseSchema, OrderConfirmationEmailEvent, OrderProductItem
from app.payments.utils import validate_payment, get_product_data, validate_order
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
    validate_order(data=data.order_details.products)
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
        event_name=variables.DECREASE_PRODUCT_QUANTITY_EVENT,
        product=[ProductItem(product_id=product.product_id, quantity=product.quantity, size=product.size,
                             color=product.color)
                 for product in orders.order_items]
    ).json()

    order_confirmation_event = OrderConfirmationEmailEvent(
        trace_id=log.trace_id_var.get(),
        event_name=variables.ORDER_CONFIRMATION_EMAIL,
        to=user.email,
        order_id=str(orders.id),
        full_name=user.full_name,
        customer_phone=user.phone,
        delivery_address=data.order_details.delivery_address,
        products=[
            OrderProductItem(
                product_id=item.product_id,
                name=get_product_data(item.product_id),
                quantity=item.quantity,
                price=item.price_per_item,
                total=item.quantity * item.price_per_item,
                size=item.size,
                color=item.color
            ) for item in data.order_details.products
        ],
        total_price=data.total_amount,
        payment_id=str(payment.id),
        payment_amount=payment.payment_amount,
        payment_method=payment.payment_method,
        payment_status=payment.payment_status,
        order_date=datetime.now()
    ).json()

    background_tasks.add_task(produce, event_data, variables.INVENTORY_QUEUE)
    background_tasks.add_task(produce, order_confirmation_event, variables.EMAIL_QUEUE)
    return response.success(
        message='Payment created successfully',
        data=response_data.dict(),
        status_code=status.HTTP_201_CREATED,
        warning=None
    )
