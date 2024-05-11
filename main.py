from fastapi import FastAPI, Request, HTTPException, status
from app.routers import login_router, password_router, signup_router, verify_router, user_detail_router
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


app = FastAPI()

app.include_router(login_router.router)
app.include_router(signup_router.router)
app.include_router(password_router.router)
app.include_router(verify_router.router)
app.include_router(user_detail_router.router)


@app.exception_handler(RequestValidationError)
async def standard_validation_exception_handler(request: Request, exc: RequestValidationError):
    missing_fields = [err["loc"][1] for err in exc.errors() if err["type"] == "missing"]
    return JSONResponse(
        status_code=422,
        content={"message": "Missing fields", "fields": missing_fields},
    )
