from fastapi import HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime

from app import models, schemas
from app.utils.email import send_register_mail
from app.utils.jwt_token import get_hashed_password, create_refresh_token, create_access_token
from app.utils.OAuth2 import get_current_user
from app.utils.email import send_forget_password_mail
from app.usecase import get_user_or_404, check_used_token


async def login_user_api(email: str, db: Session) -> schemas.LoginResponse:
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        user_out = schemas.UserOut(**user.__dict__)
        response = schemas.LoginResponse(access_token=create_access_token(user.email),
                                         refresh_token=create_refresh_token(user.email), user=user_out)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


async def create_user_api(user: schemas.UserCreate, db: Session, bg_task: BackgroundTasks) -> models.User:
    try:
        user_dict = user.dict()
        del user_dict['confirm_password']
        user_dict['password'] = get_hashed_password(user_dict['password'])
        user = models.User(**user_dict)
        db.add(user)
        db.commit()
        bg_task.add_task(send_register_mail, user=user, token=create_access_token(user.email))
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


async def verify_user_email_api(token: str, db: Session) -> models.User:
    try:
        check_used_token(token=token)
        get_user = await get_current_user(token=token, db=db)
        user = db.query(models.User).filter(models.User.email == get_user.email).first()
        if user.is_active == True:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User {get_user.email} already active')
        user.is_active = True
        db.commit()
        db.refresh(user)
        # now save the used token to the table
        used_token = models.UsedToken(token=token, used_at=datetime.utcnow())
        db.add(used_token)
        db.commit()
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


async def forgert_password_api(email: str, db: Session, bg_task: BackgroundTasks) -> None:
    try:
        user = get_user_or_404(email=email)
        token = create_access_token(user.email)
        bg_task.add_task(send_forget_password_mail, user=user, token=token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


async def forget_password_validate_api(data: schemas.ForgetPasswordRequest, db: Session):
    try:
        check_used_token(data.token)
        get_user = await get_current_user(token=data.token, db=db)
        user = db.query(models.User).filter(models.User.email == get_user.email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User {get_user.email} not found')
        user.password = get_hashed_password(data.password)
        db.commit()
        db.refresh(user)
        # save used token to db
        used_token = models.UsedToken(token=data.token, used_at=datetime.utcnow())
        db.add(used_token)
        db.commit()
        return {'success': "Password changed successfully"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


async def get_user_api(email: str, db: Session) -> models.User:
    try:
        user = get_user_or_404(email=email)
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))