from fastapi import Depends, APIRouter, BackgroundTasks, HTTPException, status, Path
from sqlalchemy.orm import Session

from app.models import User
from app.utils.OAuth2 import get_current_user
from app.schemas import EmailSchema, ForgetPasswordRequest, UserDetails
from app.database.database import get_db
from app import api
from app.usecase import get_user_or_404

router = APIRouter(
    prefix="/accounts",
    tags=['password']
)


@router.post('/forget/password')
async def forget_password(email: EmailSchema, db: Session = Depends(get_db), background_tasks: BackgroundTasks =
                          BackgroundTasks()) -> dict:
    try:
        # forget password API with email verification
        await api.forgert_password_api(email=email.email, db=db, bg_task=background_tasks)
        return {"message": "Password reset mail has been sent."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': str(e)})


@router.post('/forget/password/validate')
async def forget_password_validate(data: ForgetPasswordRequest, db: Session = Depends(get_db)):
    try:
        data = await api.forget_password_validate_api(data=data, db=db)
        return data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': str(e)})


@router.get('/me', summary='Get details of currently logged in user', response_model=UserDetails)
async def get_me(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        user = await api.get_user_api(email=user.email, db=db)
        return UserDetails(**user.__dict__)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': str(e)})