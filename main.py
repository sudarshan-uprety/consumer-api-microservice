from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app.routers import login_router, password_router, signup_router, verify_router, user_detail_router
from app import exception, middleware
from uvicorn import run


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

# add custom exception in app
app.add_exception_handler(RequestValidationError, exception.custom_validation_exception_handler)
app.add_exception_handler(HTTPException, exception.custom_http_exception_handler)


# if __name__ == '__main__':
#     run(app, host="0.0.0.0", port=9000)
