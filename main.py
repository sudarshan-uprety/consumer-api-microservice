from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.routers import login_router, password_router, signup_router, verify_router, user_detail_router
from app import exception


app = FastAPI(
    title="Authentication backend",
    description="This is a service which is responsible for authenticating users",
    docs_url="/api/docs/",
)

# add routers in app
app.include_router(login_router.router)
app.include_router(signup_router.router)
app.include_router(password_router.router)
app.include_router(verify_router.router)
app.include_router(user_detail_router.router)


# add custom exception in app
app.add_exception_handler(RequestValidationError, exception.standard_validation_exception_handler)
