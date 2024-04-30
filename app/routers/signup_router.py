from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.database.database import get_db
from app import schemas, api
from app.models import User

router = APIRouter(
    prefix="/accounts",
    tags=['accounts']
)


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def signup(user: schemas.UserCreate, db: Session = Depends(get_db)) -> User:
    try:
        user_create = api.create_user_api(user=user, db=db)
        return user_create
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
