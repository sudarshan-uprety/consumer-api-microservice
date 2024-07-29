from fastapi import FastAPI, Request, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.routers import login_router, password_router, signup_router, verify_router, user_detail_router, order_router
from app.utils import middleware


from fastapi.responses import JSONResponse
from sqlalchemy.orm.exc import NoResultFound
from app.others.exception import ServerError, CustomException
from app.utils import constant
from app.others import helpers
from app.utils import response
from fastapi.exceptions import RequestValidationError



app = FastAPI(
    title="Authentication backend",
    description="This is a service which is responsible for authenticating users",
    docs_url="/api/docs/",
)

# add logging middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=middleware.log_middleware)

# add routers in app
app.include_router(login_router.router)
app.include_router(signup_router.router)
app.include_router(password_router.router)
app.include_router(verify_router.router)
app.include_router(user_detail_router.router)
app.include_router(order_router.router)

# add custom exception in app
# app.add_exception_handler(RequestValidationError, exception.custom_validation_exception_handler)
# app.add_exception_handler(HTTPException, exception.custom_http_exception_handler)


# if __name__ == '__main__':
#     run(app, host="0.0.0.0", port=9000)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return response.error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message='Validation error',
        errors=helpers.pydantic_error(exc.errors())
    )


@app.exception_handler(NoResultFound)
async def not_found_exception_handler(request: Request, exc: NoResultFound):
    return JSONResponse(
        status_code=constant.ERROR_NOT_FOUND,
        content={"message": str(exc), "errors": str(exc)}
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=constant.ERROR_BAD_REQUEST,
        content={"message": str(exc), "errors": str(exc)}
    )


@app.exception_handler(ServerError)
async def server_error_handler(request: Request, exc: ServerError):
    return JSONResponse(
        status_code=constant.ERROR_INTERNAL_SERVER_ERROR,
        content={"message": constant.ERROR_SERVER_DOWN, "errors": str(exc.args)}
    )


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=constant.ERROR_INTERNAL_SERVER_ERROR,
        content={"message": str(exc), "errors": "Something went wrong"}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=constant.ERROR_INTERNAL_SERVER_ERROR,
        content={"message": str(exc), "errors": str(exc)}
    )
