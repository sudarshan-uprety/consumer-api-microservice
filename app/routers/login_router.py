from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, BackgroundTasks
from sqlalchemy.orm import Session

from app.database.database import get_db
from app import schemas, api, validation
from app.utils.jwt_token import create_refresh_token, create_access_token

router = APIRouter(
    prefix="/accounts",
    tags=['logins']
)


@router.post('/login', status_code=status.HTTP_200_OK, response_model=schemas.LoginResponse)
async def login(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
    try:
        user = await api.login_user_api(user_in=user_in, db=db)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post('/access/token/new', status_code=status.HTTP_201_CREATED, response_model=schemas.TokenResponse)
async def refresh_token(request: schemas.RefreshTokenRequest):
    try:
        user_email = validation.verify_refresh_token(refresh_token=request.refresh_token)

        access_token = create_access_token(user_email)
        refresh_token = create_refresh_token(user_email)

        # Return the new access token
        return schemas.TokenResponse(access_token=access_token, refresh_token=refresh_token)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
