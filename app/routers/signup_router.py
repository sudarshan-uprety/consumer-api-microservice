from fastapi import status, Depends, APIRouter, BackgroundTasks
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.api import api
from app.schema import register_schema
from app.models.models import User

router = APIRouter(
    prefix="/accounts",
    tags=['signup']
)


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=register_schema.UserRegisterResponse)
async def signup(user: register_schema.UserRegister, db: Session = Depends(get_db), background_tasks: BackgroundTasks
                 = BackgroundTasks()) -> User:
    user_create = await api.create_user_api(user=user, db=db, bg_task=background_tasks)
    return user_create
