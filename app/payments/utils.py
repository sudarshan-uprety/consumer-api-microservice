from typing import List

import httpx

from app.orders.queries import create_order
from app.orders.schemas import ProductOrder
from app.payments.queries import create_payment
from app.payments.schema import TransactionDetails
from app.user.models import Users
from utils.exceptions import GenericError, ValidationError
from utils.variables import GET_PRODUCT_API


def validate_payment(data: TransactionDetails, user: Users):
    request_url = (
        f"https://uat.esewa.com.np/api/epay/transaction/status/"
        f"?product_code={data.product_code}&"
        f"total_amount={data.total_amount}&"
        f"transaction_uuid={data.transaction_uuid}"
    )
    with httpx.Client(timeout=20) as client:
        response_data = client.get(request_url).json()

        # response format example
        # response_data = {"product_code": "EPAYTEST", "transaction_uuid": "123", "total_amount": 100.0,
        #                  "status": "COMPLETE", "ref_id": "0001TS9"}

    if response_data['status'] == 'COMPLETE':
        # if transaction is valid create the order and payment object in database.
        payment_obj = create_payment(payment=response_data, user=user)
        orders = create_order(orders=data.order_details, payment=payment_obj)
        return orders, payment_obj
    else:
        raise GenericError(
            message="Invalid payment.",
            status_code=400,
            data=response_data['status'],
            errors={'error': 'Something went wrong.'}
        )


def get_product_data(product_code) -> str:
    url = GET_PRODUCT_API + product_code
    with httpx.Client(timeout=20) as client:
        response_data = client.get(url).json()
    return response_data['data']['name']


def validate_order(data: List[ProductOrder]):
    for order in data:
        product_id = order.product_id
        size = order.size
        color = order.color
        quantity = order.quantity

        url = GET_PRODUCT_API + product_id
        with httpx.Client(timeout=20) as client:
            response_data = client.get(url).json()['data']

        variant_found = False
        for variant in response_data['variants']:
            if variant['size'].lower() == size.lower() and variant['color'].lower() == color.lower():
                variant_found = True
                if variant['stock'] < quantity:
                    raise ValidationError(
                        message=f"Product {product_id} is out of stock.",
                        status_code=400
                    )
                break

        if not variant_found:
            raise ValidationError(
                message=f"Product with {size} and {color} not available.",
                status_code=400
            )
