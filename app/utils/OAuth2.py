from datetime import datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app.schema.schemas import TokenPayload
from app.user.models import Users
from utils.variables import ALGORITHM, JWT_SECRET_KEY

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


def get_current_user(token: str = Depends(reusable_oauth)) -> Users:
    payload = jwt.decode(
        token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
    )
    token_data = TokenPayload(**payload)
    if datetime.fromtimestamp(token_data.exp) < datetime.now():
        raise ValidationError("Token is expired")

    user = Users.query.filter_by(email=token_data.sub).first()

    if user is None:
        raise ValidationError("User not found")
    return user
