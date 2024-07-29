from app.user.models import Users
from app.utils.response import error_response


def get_user_or_404(user_id):
    user = Users.query.get(user_id)

    if user and not user.is_deleted:
        return user

    else:
        return error_response(
            status_code=404,
            message='User not found'
        )
