from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.exc import NoResultFound
from pydantic import ValidationError as PydanticError

from app.utils import constant, response
from app.others import helpers
from app.others.custom_exception import ServerError, CustomException


def error_handler(func):
    def validate(*args, **kwargs):
        try:
            to_return = func(*args, **kwargs)
        except NoResultFound as err:
            raise HTTPException(
                status_code=constant.ERROR_NOT_FOUND,
                detail=jsonable_encoder({"message": str(err), "errors": str(err)}),
            )
        except PydanticError as err:
            msg = helpers.pydantic_error(err)
            return response.error_response(
                status_code=constant.ERROR_BAD_REQUEST, message="Invalid data", errors=msg
            )
        except ValueError as err:
            raise HTTPException(
                status_code=constant.ERROR_BAD_REQUEST,
                detail=jsonable_encoder({"message": str(err), "errors": str(err)}),
            )
        except ServerError as err:
            raise HTTPException(
                status_code=constant.ERROR_INTERNAL_SERVER_ERROR,
                detail=jsonable_encoder({
                    "message": constant.ERROR_SERVER_DOWN,
                    "errors": str(err.args),
                }),
            )
        except CustomException as err:
            raise HTTPException(
                status_code=constant.ERROR_INTERNAL_SERVER_ERROR,
                detail=jsonable_encoder({"message": str(err), "errors": "Something went wrong"}),
            )
        except Exception as err:
            raise HTTPException(
                status_code=constant.ERROR_INTERNAL_SERVER_ERROR,
                detail=jsonable_encoder({"message": str(err), "errors": str(err)}),
            )
        return to_return
    return validate
