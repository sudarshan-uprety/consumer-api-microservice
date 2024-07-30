from datetime import datetime
from http import HTTPStatus

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app.others import exceptions
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
        raise exceptions.GenericError(
            message="Token is expired",
            status_code=HTTPStatus.UNAUTHORIZED
        )

    user = Users.query.filter_by(email=token_data.sub).first()
    # user = get_user_by_email_or_404(email=token_data.sub)
    if user is None:
        raise exceptions.GenericError(
            message="User not found",
            status_code=HTTPStatus.NOT_FOUND
        )
    return user
