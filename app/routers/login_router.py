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
    user = await api.login_user_api(user_in=user_in, db=db)
    return user


@router.post('/access/token/new', status_code=status.HTTP_201_CREATED, response_model=schemas.TokenResponse)
async def refresh_token(request: schemas.RefreshTokenRequest) -> schemas.TokenResponse:
    token_response = await api.new_token_api(refresh_token=request.refresh_token)
    return token_response
