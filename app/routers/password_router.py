from fastapi import Depends, APIRouter, BackgroundTasks
from sqlalchemy.orm import Session

from app.models import User
from app.utils.OAuth2 import get_current_user
from app.schemas import EmailSchema
from app.database.database import get_db
from app import api
from app.usecase import get_user_or_404

router = APIRouter(
    prefix="/password",
    tags=['accounts']
)


@router.post('/forget/password')
async def forget_password(email: EmailSchema, db: Session = Depends(get_db), background_tasks: BackgroundTasks =
                          BackgroundTasks()) -> str:
    # forget password API with email verification
    api.forgert_password_api(email=email.email, db=db, bg_task=background_tasks)
    return "Hello from login"


@router.get('/me', summary='Get details of currently logged in user')
async def get_me(user: User = Depends(get_current_user)) -> str:
    print(user)
    return 'hey'