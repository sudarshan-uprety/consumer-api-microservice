from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.models import User
from app.utils.OAuth2 import get_current_user
from app.schemas import UserDetails
from app.database.database import get_db
from app import api

router = APIRouter(
    prefix="/accounts",
    tags=['user_details'],
)


@router.get('/me', summary='Get details of currently logged in user', response_model=UserDetails)
async def get_me(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> UserDetails:
    try:
        user = await api.get_user_api(email=user.email, db=db)
        return UserDetails(**user.__dict__)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
