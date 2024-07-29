import json

from mongoengine.errors import DoesNotExist, FieldDoesNotExist, ValidationError, NotRegistered
from pydantic import ValidationError as PydanticError
from aws_lambda_powertools.event_handler.exceptions import UnauthorizedError
import botocore.exceptions

from app.utils import constant, response
from app.others import helpers
from app.others.custom_exception import ServerError, CustomException


def error_handler(func):
    def validate(*args, **kwargs):
        try:
            to_return = func(*args, **kwargs)
        except DoesNotExist as err:
            return response.error_response(
                status_code=constant.ERROR_NOT_FOUND, message=err.args[0], errors=err.args[0]
            )
        except FieldDoesNotExist as err:
            return response.error_response(
                status_code=constant.ERROR_FOUND, message=err.args[0], errors=err.args[0]
            )
        except ValidationError as err:
            return response.error_response(
                status_code=constant.ERROR_FOUND, message=err.args[0], errors=err.args[0]
            )
        except ServerError as err:
            return response.error_response(
                status_code=constant.ERROR_INTERNAL_SERVER_ERROR, message=constant.ERROR_SERVER_DOWN, errors=err.args
            )
        except CustomException as err:
            return response.error_response(
                status_code=constant.ERROR_INTERNAL_SERVER_ERROR, message=err, errors="Something went wrong"
            )
        except PydanticError as err:
            msg = helpers.pydantic_error(err)
            return response.error_response(
                status_code=constant.ERROR_BAD_REQUEST, message="Invalid data", errors=msg
            )
        except botocore.exceptions.ClientError as err:
            return response.error_response(
                status_code=constant.ERROR_BAD_REQUEST,
                message=str(err.response["Error"]["Message"]),
                errors=str(err.response["Error"]["Message"])
            )
        except UnauthorizedError as err:
            return response.error_response(
                status_code=constant.ERROR_BAD_REQUEST,
                message=str(err),
                errors=str(err)
            )
        except ValueError as err:
            return response.error_response(
                status_code=constant.ERROR_BAD_REQUEST,
                message=str(err),
                errors=str(err)
            )
        except Exception as err:
            return response.error_response(
                status_code=constant.ERROR_INTERNAL_SERVER_ERROR,
                message=str(err),
                errors=str(err)
            )
        return to_return
    return validate
