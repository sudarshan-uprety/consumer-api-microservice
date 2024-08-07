from typing import List

from fastapi import status, APIRouter, Depends
from pydantic import parse_obj_as

from app.orders.queries import get_user_orders
from app.orders.schemas import OrderResponse
from app.user.models import Users
from utils import OAuth2, response

router = APIRouter(
    prefix="/orders",
    tags=["order endpoints"],
)


@router.get("/list", status_code=status.HTTP_200_OK)
async def get_order_list(user: Users = Depends(OAuth2.get_current_user)) -> List[OrderResponse]:
    orders = get_user_orders(user)
    order_responses = parse_obj_as(List[OrderResponse], orders)
    return response.success(
        status_code=200,
        message="Successfully fetched orders",
        data=order_responses,
        warning=None
    )
