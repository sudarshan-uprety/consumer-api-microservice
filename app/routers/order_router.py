from fastapi import status, Depends, APIRouter, BackgroundTasks
from sqlalchemy.orm import Session

from app.database.database import get_db
from app import api
from app.models import UserOrder, User
from app.schemas import UserOrderList
from app.utils.OAuth2 import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=['Orders and Payment']
)


@router.get('/order/list', summary='Get list of order of the user.', response_model=UserOrderList)
async def get_orders(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> UserOrderList:
    data = await api.get_orders_api(current_user=user, db=db)
    order_dicts = [
        {
            "id": order.id,
            "product": order.product,
            "quantity": order.quantity,
            "price": order.price,
            "is_delivered": order.is_delivered
        }
        for order in data
    ]
    return UserOrderList(orders=[UserOrder(**order_dict) for order_dict in order_dicts])

