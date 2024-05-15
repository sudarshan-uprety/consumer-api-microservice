from fastapi import Depends, APIRouter

from app.models import User
from app.utils.OAuth2 import get_current_user
from app.schemas import UserDetails

router = APIRouter(
    prefix="/accounts",
    tags=['user_details'],
)


@router.get('/me', summary='Get details of currently logged in user', response_model=UserDetails)
async def get_me(user: User = Depends(get_current_user)) -> UserDetails:
    return UserDetails(**user.__dict__)
