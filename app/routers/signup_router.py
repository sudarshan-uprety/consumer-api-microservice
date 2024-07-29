from fastapi import status, APIRouter, BackgroundTasks
from app.user.schema import UserRegister, UserRegisterResponse
from app.user.models import Users
from app.utils import jwt_token

router = APIRouter(
    prefix="/accounts",
    tags=['signup']
)


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserRegisterResponse)
async def signup(user: UserRegister, background_tasks: BackgroundTasks
                 = BackgroundTasks()) -> Users:
    hashed_password = jwt_token.get_hashed_password(user.password)
    user_data = user.dict()
    user_data['password'] = hashed_password
    user_data.pop('confirm_password', None)  # Remove 'confirm_password' key if it exists
    new_user = Users(**user_data)  # Unpack the remaining dictionary
    new_user.save()
    print('ok'*100)
