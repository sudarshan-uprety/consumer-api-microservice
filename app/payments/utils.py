import requests

from utils.exceptions import GenericError


def validate_payment_id(*args, **kwargs):
    request_url = (f"https://uat.esewa.com.np/api/epay/transaction/status/"
                   f"?product_code={product_code}&total_amount={total_amount}&transaction_uuid={transaction_uuid}")
    response_data = requests.get(request_url)
    if response_data.status_code == 200:
        data = response_data.json()
    else:
        raise GenericError(
            message="Invalid payment.",
            status_code=response_data.status_code,
            data=response_data.json(),
            errors=response_data.json()
        )
