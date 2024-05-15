from fastapi import HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app import models, schemas, usecase, validation
from app.utils import jwt_token, OAuth2, email
from app.utils.email import send_forget_password_mail


async def login_user_api(user_in: schemas.UserLogin, db: Session) -> schemas.LoginResponse:
    try:
        user = await validation.login_user_verification(email=user_in.email, password=user_in.password, db=db)
        user_out = schemas.UserOut(**user)
        response = schemas.LoginResponse(access_token=jwt_token.create_access_token(user.email),
                                         refresh_token=jwt_token.create_refresh_token(user.email), user=user_out)
        return response
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code,
                            detail=e.detail)  # Re-raise the HTTPException without wrapping it
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def create_user_api(user: schemas.UserCreate, db: Session, bg_task: BackgroundTasks) -> models.User:
    try:
        await validation.password_validation(password=user.password, confirm_password=user.confirm_password)
        await validation.signup_user_verification(email=user.email, phone=user.phone, db=db)
        user_dict = user.dict(exclude={'confirm_password'})
        user_dict['password'] = jwt_token.get_hashed_password(user_dict['password'])
        user = models.User(**user_dict)
        db.add(user)
        db.commit()
        bg_task.add_task(email.send_register_mail, user=user, token=jwt_token.create_access_token(user.email))
        return user
    except HTTPException as e:
        raise e  # Re-raise the HTTPException without wrapping it
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def verify_user_email_api(token: str, db: Session) -> models.User:
    try:
        await validation.check_used_token(token=token, db=db)
        current_user = await OAuth2.get_current_user(token=token, db=db)
        user = await usecase.check_user_active(email=current_user.email, db=db)
        user.is_active = True
        db.commit()
        db.refresh(user)
        # now save the used token to the table
        used_token = models.UsedToken(token=token, used_at=datetime.utcnow())
        db.add(used_token)
        db.commit()
        return user
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code,
                            detail=e.detail)  # Re-raise the HTTPException without wrapping it
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def forgert_password_api(email: str, db: Session, bg_task: BackgroundTasks) -> None:
    try:
        user = await usecase.get_user_or_404(email=email, db=db)
        token = jwt_token.create_access_token(user.email)
        bg_task.add_task(send_forget_password_mail, user=user, token=token)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code,
                            detail=e.detail)  # Re-raise the HTTPException without wrapping it
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def forget_password_validate_api(data: schemas.ForgetPasswordRequest, db: Session):
    try:
        get_user = await OAuth2.get_current_user(token=data.token, db=db)
        await validation.password_validation(password=data.password, confirm_password=data.confirm_password)
        await validation.check_used_token(data.token, db=db)
        user = await usecase.get_user_or_404(email=get_user.email, db=db)
        user.password = jwt_token.get_hashed_password(data.password)
        db.commit()
        db.refresh(user)
        # save used token to db
        used_token = models.UsedToken(token=data.token, used_at=datetime.utcnow())
        db.add(used_token)
        db.commit()
        return JSONResponse(status_code=200, content={'success': "Password changed successfully"})
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code,
                            detail=e.detail)  # Re-raise the HTTPException without wrapping it
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_user_api(email: str, db: Session) -> schemas.UserDetails:
    try:
        user = await usecase.get_user_or_404(email=email, db=db)
        return user
    except HTTPException as e:
        raise e  # Re-raise the HTTPException without wrapping it
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def new_token_api(refresh_token: str) -> schemas.TokenResponse:
    try:
        user_email = await validation.verify_refresh_token(refresh_token=refresh_token)

        access_token = jwt_token.create_access_token(user_email)
        refresh_token = jwt_token.create_refresh_token(user_email)

        return schemas.TokenResponse(access_token=access_token, refresh_token=refresh_token)
    except HTTPException as e:
        raise e  # Re-raise the HTTPException without wrapping it
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def change_password_api(data: schemas.ChangePasswordRequest, user: models.User, db: Session):
    try:
        await validation.password_validation(password=data.new_password, confirm_password=data.confirm_password)
        await jwt_token.verify_password(password=data.current_password, hashed_pass=user.password)
        await jwt_token.compare_passwords(new_password=data.confirm_password, old_hashed_password=user.password)
        await usecase.change_password(user=user, password=data.confirm_password, db=db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))