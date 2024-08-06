from fastapi import status, APIRouter, Depends

from app.payments.schema import TransactionDetails
from app.payments.utils import validate_payment
from app.user.models import Users
from utils import OAuth2, response

router = APIRouter(
    prefix="/payments",
    tags=['payment endpoints'],
)


@router.post('/create', status_code=status.HTTP_200_OK)
async def create_user_payment(data: TransactionDetails, user: Users = Depends(OAuth2.get_current_user)):
    validate_payment(data=data, user=user)
    return response.success(
        message='Payment created successfully',
        data=None,
        status_code=status.HTTP_201_CREATED,
        warning=None
    )
