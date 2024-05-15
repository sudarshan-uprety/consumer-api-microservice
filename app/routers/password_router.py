from fastapi import Depends, APIRouter, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.schemas import EmailSchema, ForgetPasswordRequest, ChangePasswordRequest
from app.database.database import get_db
from app import api, models
from app.utils.OAuth2 import get_current_user

router = APIRouter(
    prefix="/accounts",
    tags=['password']
)


@router.post('/forget/password')
async def forget_password(email: EmailSchema, db: Session = Depends(get_db), background_tasks: BackgroundTasks =
                          BackgroundTasks()) -> JSONResponse:
    await api.forgert_password_api(email=email.email, db=db, bg_task=background_tasks)
    return JSONResponse(status_code=200, content={'message': 'Password reset mail has been sent to your email.'})


@router.post('/validate/forget/password')
async def forget_password_validate(data: ForgetPasswordRequest, db: Session = Depends(get_db)):
    data = await api.forget_password_validate_api(data=data, db=db)
    return data


@router.post('/change/password')
async def change_password(data: ChangePasswordRequest, current_user: models.User = Depends(get_current_user),
                          db: Session = Depends(get_db)) -> JSONResponse:
    await api.change_password_api(data=data, user=current_user, db=db)
    return JSONResponse(status_code=200, content={"detail": "Password changed successfully."})
