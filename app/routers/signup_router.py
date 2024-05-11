from fastapi import status, HTTPException, Depends, APIRouter, BackgroundTasks
from sqlalchemy.orm import Session

from app.database.database import get_db
from app import schemas, api
from app.models import User

router = APIRouter(
    prefix="/accounts",
    tags=['signup']
)


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def signup(user: schemas.UserCreate, db: Session = Depends(get_db), background_tasks: BackgroundTasks
                 = BackgroundTasks()) -> User:
    try:
        user_create = await api.create_user_api(user=user, db=db, bg_task=background_tasks)
        return user_create
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
