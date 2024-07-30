from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import (HTTPException, RequestValidationError,
                                WebSocketRequestValidationError)
from sqlalchemy.exc import OperationalError, PendingRollbackError

from app.routers import password_router, user_detail_router, order_router
from app.utils import middleware
from utils.database import connect_to_database, disconnect_from_database, rollback_session
from app.user.routers import router
from app.utils import response, constant
from app.others import exceptions


def register_routes(server):
    # server.include_router(login_router.router)
    server.include_router(router)
    server.include_router(password_router.router)
    server.include_router(user_detail_router.router)
    server.include_router(order_router.router)


def register_middlewares(server):

    # Initialize CORS
    server.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True
    )


server = FastAPI(
    title="Authentication backend",
    description="This is a service which is responsible for authenticating users",
    docs_url="/api/docs/",
)


# Startup Events
@server.on_event("startup")
async def startup_event():
    connect_to_database()


# Shutdown Events
@server.on_event("shutdown")
async def shutdown_event():
    disconnect_from_database()

# Register Routes
register_routes(server)

# Registrer Middlewares
register_middlewares(server)

# add logging middleware
server.add_middleware(BaseHTTPMiddleware, dispatch=middleware.log_middleware)

# add custom exception handler.
# exception_handlers(server)


@server.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exception):
    return response.error(constant.UNPROCESSABLE_ENTITY, exception.errors())


@server.exception_handler(OperationalError)
async def database_operational_exception_handler(_, exception):
    conn = exceptions.DatabaseConnectionProblem()
    return response.error(conn.status_code, conn.message)


@server.exception_handler(PendingRollbackError)
async def database_rollback_exception_handler(_, exception):
    rollback_session()


@server.exception_handler(exceptions.DatabaseConnectionProblem)
async def database_connection_exception_handler(_, exception):
    return response.error(exception.status_code, exception.message)


@server.exception_handler(exceptions.GenericError)
async def generic_exception_handler(_, exception):
    return response.error(message=exception.message, status_code=exception.status_code)


@server.exception_handler(exceptions.InternalError)
async def internal_exception_handler(_, exception):
    rollback_session()
    return response.error(exception.status_code, exception.message)


@server.exception_handler(HTTPException)
async def http_exception_handler(_, exception):
    rollback_session()
    return response.error(exception.status_code, exception.detail)


@server.exception_handler(Exception)
async def exception_handler(_, exception):
    rollback_session()
    return response.error(constant.ERROR_INTERNAL_SERVER_ERROR, str(exception))
