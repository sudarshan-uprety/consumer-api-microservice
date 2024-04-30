from fastapi import FastAPI
from app.routers import login_router, password_router, signup_router, verify_router

app = FastAPI()

app.include_router(login_router.router)
app.include_router(signup_router.router)
app.include_router(password_router.router)
app.include_router(verify_router.router)
