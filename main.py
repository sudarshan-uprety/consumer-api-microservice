from fastapi import FastAPI

from app.routers import login_router, password_router, signup_router, verify_router, user_detail_router, order_router
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils import middleware
from app.others.exception import exception_handlers


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


# add custom exception handler.
exception_handlers(app)
