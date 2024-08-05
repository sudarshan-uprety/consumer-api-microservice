import requests

from app.orders.queries import create_order
from app.payments.schema import TransactionDetails
from app.user.models import Users
from utils.exceptions import GenericError


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
        create_order(data.order_details.products, user=user)
    else:
        raise GenericError(
            message="Invalid payment.",
            status_code=response_data.status_code,
            data=response_data['status'],
            errors={'error': 'Something went wrong.'}
        )
