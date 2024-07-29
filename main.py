from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import login_router, password_router, user_detail_router, order_router
from app.utils import middleware
from app.others.exception import exception_handlers
from utils.database import connect_to_database, disconnect_from_database
from app.user.routers import router


def register_routes(server):
    server.include_router(login_router.router)
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
exception_handlers(server)
