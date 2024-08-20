import requests

from app.orders.queries import create_order
from app.payments.queries import create_payment
from app.payments.schema import TransactionDetails
from app.user.models import Users
from utils.exceptions import GenericError
from utils.variables import GET_PRODUCT_API


def validate_payment(data: TransactionDetails, user: Users):
    request_url = (
        f"https://uat.esewa.com.np/api/epay/transaction/status/"
        f"?product_code={data.product_code}&"
        f"total_amount={data.total_amount}&"
        f"transaction_uuid={data.transaction_uuid}"
    )
    response_data = requests.get(request_url).json()
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
    response_data = requests.get(url).json()
    return response_data['data']['name']
