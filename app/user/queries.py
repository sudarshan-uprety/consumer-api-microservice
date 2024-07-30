from pydantic import ValidationError
from datetime import datetime

from app.user.models import Users, UsedToken
from app.utils import jwt_token, OAuth2
from utils import store
from app.others.exceptions import GenericError


def get_user_or_404(user_id):
    user = Users.query.get(user_id)

    if user and not user.is_deleted:
        return user

    else:
        raise GenericError(
            status_code=404,
            message='User not found'
        )


def get_user_by_email_or_404(email):
    user = Users.query.filter_by(email=email).first()

    if user is None:
        raise GenericError(
            status_code=404,
            message="User not found",
            errors={'email': f'{email} not found'}
        )

    else:
        return user


def create_user(user):
    hashed_password = jwt_token.get_hashed_password(user.password)
    user_data = user.dict()
    user_data['password'] = hashed_password
    user_data.pop('confirm_password', None)
    new_user = Users(**user_data)
    store.session.add(new_user)
    store.session.commit()
    return new_user


def check_used_token(token):
    token = UsedToken.query.filter_by(token=token).first()
    if token is not None:
        raise ValueError("Token already used.")


def verify_user(token):
    check_used_token(token=token)
    user = OAuth2.get_current_user(token=token)
    if user.is_active:
        raise ValidationError('User is already active.')
    user.is_active = True
    store.session.commit()
    store.session.refresh(user)

    # now save the used token to the table
    token_data = {
        'token': token,
        'used_at': datetime.utcnow()
    }
    used_token = UsedToken(**token_data)
    store.session.add(used_token)
    store.session.commit()

