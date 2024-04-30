from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from app.models import User
from app.OAuth2 import get_current_user
from app.schemas import UserOut
router = APIRouter(
    prefix="/password",
    tags=['accounts']
)


@router.post('/forget')
async def forget_password() -> str:
    # need to create a forget password API with email verification
    return "Hello from login"


@router.get('/me', summary='Get details of currently logged in user')
async def get_me(user: User = Depends(get_current_user)) -> str:
    print(user)
    return 'hey'