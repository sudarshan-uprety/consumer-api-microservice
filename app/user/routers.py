from fastapi import status, APIRouter, BackgroundTasks, Path
from app.user.schema import UserRegister, UserRegisterResponse
from app.user.models import Users
from app.utils import jwt_token
from app.utils import email, response
from app.user.queries import create_user, verify_user

router = APIRouter(
    prefix="/accounts",
    tags=['signup']
)


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserRegisterResponse)
async def signup(user: UserRegister, background_tasks: BackgroundTasks
                 = BackgroundTasks()) -> Users:
    user = create_user(user=user)
    background_tasks.add_task(email.send_register_mail, user=user, token=jwt_token.create_access_token(user.email))
    data = UserRegisterResponse.from_orm(user)
    return response.success_response(
        status_code=status.HTTP_201_CREATED,
        message='User created successfully, please check your email for verification.',
        data=data.dict(),
        warning=None
    )


@router.get('/verify/user/{token}', status_code=status.HTTP_200_OK)
async def verify_email(token: str = Path(..., description="Verification token")):
    verify = verify_user(token=token)
    return response.success_response(
        status_code=status.HTTP_200_OK,
        message='Email verified successfully.',
        data=None,
        warning=None
    )
