from fastapi import Request, status
from fastapi.exceptions import RequestValidationError

from sqlalchemy.orm.exc import NoResultFound
from pydantic import ValidationError

from app.others.custom_exception import ServerError, CustomException
from app.others import helpers
from app.utils import response


def exception_handlers(app):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        return response.error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message='Invalid input data.',
            errors=helpers.pydantic_error(exc.errors()).get('body')
        )

    @app.exception_handler(NoResultFound)
    async def not_found_exception_handler(request: Request, exc: NoResultFound):
        return response.error_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message='Not Found',
            errors=str(exc)
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return response.error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message='Bad Request',
            errors=str(exc)
        )

    @app.exception_handler(ServerError)
    async def server_error_handler(request: Request, exc: ServerError):
        return response.error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message='Internal Server Error',
            errors=str(exc)
        )

    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return response.error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message='Something went wrong.',
            errors=str(exc)
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return response.error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message='Something went wrong.',
            errors=str(exc)
        )
