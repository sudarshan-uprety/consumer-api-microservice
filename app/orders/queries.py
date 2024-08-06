from app.orders.models import Orders, OrderItem
from app.orders.schemas import OrderBase
from app.payments.models import UserPayment
from utils import store


def create_order(orders: OrderBase, payment: UserPayment):
    order = Orders(
        user_id=payment.user_id,
        delivery_address=orders.delivery_address,
        payment_id=payment.id,
        status=payment.payment_status,
        order_note=orders.order_notes
    )
    store.session.add(order)
    store.session.commit()

    for product in orders.products:
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.product_id,
            quantity=product.quantity,
            price_per_item=product.price_per_item
        )
        store.session.add(order_item)
        store.session.commit()
    return order
    # order_details = orders.dict()['order_details']
    # delivery_address = order_details['delivery_address']
    # order_notes = order_details['order_notes']
    # products = order_details['products']
    #
    # for product in products:
    #     order = Orders(
    #         user_id=payment.user_id,
    #         delivery_address=orders.delivery_address,
    #         payment_id=payment.id,
    #         status=payment.payment_status,
    #         order_note=orders.order_notes
    #     )
    #     store.session.add(order)
    #     store.session.commit()
    # return None
