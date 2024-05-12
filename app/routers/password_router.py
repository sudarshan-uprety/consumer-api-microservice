from fastapi import Depends, APIRouter, BackgroundTasks, HTTPException, status, Path
from sqlalchemy.orm import Session

from app.schemas import EmailSchema, ForgetPasswordRequest
from app.database.database import get_db
from app import api

router = APIRouter(
    prefix="/accounts",
    tags=['password']
)


@router.post('/forget/password')
async def forget_password(email: EmailSchema, db: Session = Depends(get_db), background_tasks: BackgroundTasks =
                          BackgroundTasks()) -> dict:
    await api.forgert_password_api(email=email.email, db=db, bg_task=background_tasks)
    return {"message": "Password reset mail has been sent."}


@router.post('/validate/forget/password')
async def forget_password_validate(data: ForgetPasswordRequest, db: Session = Depends(get_db)):
    data = await api.forget_password_validate_api(data=data, db=db)
    return data
