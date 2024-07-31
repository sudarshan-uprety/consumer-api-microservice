from fastapi import status, APIRouter, BackgroundTasks, Depends

from app.user.queries import *
from app.user.schema import *
from app.user.utils import verify_signup_otp, verify_forget_password_otp
from utils import response, jwt_token, OAuth2, email
from utils.otp import otp

router = APIRouter(
    prefix="/accounts",
    tags=['authentication and authorization']
)


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserRegisterResponse)
async def signup(user: UserRegister, background_tasks: BackgroundTasks = BackgroundTasks()) -> UserRegisterResponse:
    user = create_user(user=user)
    background_tasks.add_task(email.send_register_mail, user=user, otp=otp.generate_otp(user_email=user.email))
    data = UserRegisterResponse.from_orm(user)
    return response.success(
        status_code=status.HTTP_201_CREATED,
        message='User created successfully, please check your email for verification.',
        data=data.dict(),
        warning=None
    )


@router.post('/verify/top/', status_code=status.HTTP_200_OK)
async def verify_email(data: OTPVerification) -> dict:
    verify_signup_otp(code=data.otp, email=data.email)
    return response.success(
        status_code=status.HTTP_200_OK,
        message='Email verified successfully.',
        data=None,
        warning=None
    )


@router.post('/login', status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def login(user_in: UserLogin) -> LoginResponse:
    user = get_user_by_email_or_404(user_in.email)
    jwt_token.verify_password(
        password=user_in.password,
        hashed_pass=user.password
    )
    login_response = LoginResponse(access_token=jwt_token.create_access_token(user.email),
                                   refresh_token=jwt_token.create_refresh_token(user.email),
                                   user=UserRegisterResponse.from_orm(user))
    return response.success(
        status_code=status.HTTP_200_OK,
        message='Login successful',
        data=login_response.dict(),
        warning=None
    )


@router.post('/access/token/new', status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
async def refresh_token(token: RefreshTokenRequest) -> TokenResponse:
    user_email = jwt_token.verify_refresh_token(refresh_token=token.refresh_token)
    access_token = jwt_token.create_access_token(user_email)
    response_token = TokenResponse(access_token=access_token)
    return response.success(
        status_code=status.HTTP_200_OK,
        message='Token created successfully',
        data=response_token.dict(),
        warning=None
    )


@router.get('/me', summary='Get details of currently logged in user', response_model=UserDetails)
async def get_me(user: Users = Depends(OAuth2.get_current_user)) -> UserDetails:
    response_detail = UserDetails.from_orm(user)
    return response.success(
        status_code=status.HTTP_200_OK,
        message="User details retrieved successfully.",
        data=response_detail.dict(),
        warning=None
    )


@router.post('/forget/password')
async def forget_password(user_email: EmailSchema, background_tasks: BackgroundTasks = BackgroundTasks()) -> dict:
    user = get_user_by_email_or_404(user_email.email)
    code = otp.generate_otp(user_email=user.email)
    background_tasks.add_task(email.send_forget_password_mail, user=user, code=code)
    return response.success(
        status_code=status.HTTP_200_OK,
        message='Forget password email with OTP has been sent.',
        data=None,
        warning=None
    )


@router.post('/validate/forget/password')
async def forget_password_validate(data: ForgetPasswordRequest):
    user = get_user_by_email_or_404(data.email)
    verify_forget_password_otp(code=data.otp, email=data.email)
    change_password(user=user, password=data.password)
    return response.success(
        status_code=status.HTTP_200_OK,
        message='Password changed successfully',
        data=None,
        warning=f"Password changed successfully for user {user.email}"
    )


@router.post('/change/password')
async def change_user_password(data: ChangePasswordRequest,
                               current_user: Users = Depends(OAuth2.get_current_user)) -> dict:
    jwt_token.verify_password(password=data.current_password, hashed_pass=current_user.password)
    jwt_token.compare_passwords(new_password=data.new_password, old_hashed_password=current_user.password)
    change_password(user=current_user, password=data.new_password)
    return response.success(
        status_code=status.HTTP_200_OK,
        message='Password changed successfully',
        data=None,
        warning=None
    )
