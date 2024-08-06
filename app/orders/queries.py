from app.orders.models import Orders
from app.orders.schemas import ProductOrder
from app.payments.models import UserPayment
from utils import store


def create_order(orders: ProductOrder, payment: UserPayment):
    order_details = orders.dict()['order_details']
    delivery_address = order_details['delivery_address']
    order_notes = order_details['order_notes']
    products = order_details['products']

    for product in products:
        order = Orders(
            user_id=payment.user_id,
            product_id=product['product_id'],
            quantity=product['quantity'],
            price_per_item=product['price_per_item'],
            delivery_address=delivery_address,
            payment_id=payment.id,
            status=payment.payment_status,
            order_note=order_notes
        )
        store.session.add(order)
        store.session.commit()
    return None
