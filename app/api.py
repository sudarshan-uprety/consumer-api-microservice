from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.utils.jwt_token import get_hashed_password, create_refresh_token, create_access_token


def login_user_api(email: str, db: Session) -> schemas.LoginResponse:
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        user_out = schemas.UserOut(**user.__dict__)
        response = schemas.LoginResponse(access_token=create_access_token(user.email),
                                         refresh_token=create_refresh_token(user.email), user=user_out)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


def create_user_api(user: schemas.UserCreate, db: Session) -> models.User:
    user_dict = user.dict()
    del user_dict['confirm_password']
    user_dict['password'] = get_hashed_password(user_dict['password'])
    user = models.User(**user_dict)
    db.add(user)
    db.commit()
    return user
