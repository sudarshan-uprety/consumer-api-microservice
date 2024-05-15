from urllib.request import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import ValidationException, HTTPException
from app.utils.log import logger


def custom_validation_exception_handler(request, exc: ValidationException) -> JSONResponse:
    print('hey', exc)
    missing_fields = []
    for err in exc.errors():
        if err["type"] == "missing":
            if err["loc"]:
                missing_fields.append(err["loc"][-1])
            else:
                missing_fields.append("payload")
        elif err["type"] == "json_invalid":
            return JSONResponse(
                    status_code=400,
                    content={"message": "Invalid JSON payload"}
                )

    if missing_fields:
        return JSONResponse(
            status_code=422,
            content={"message": "Missing fields", "fields": missing_fields},
        )
    else:
        return JSONResponse(
            status_code=422,
            content={"message": "Validation error", "details": exc.errors()},
        )


def custom_http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.exception(msg=f'Http exception with f{exc.detail}, status_code: {exc.status_code}')
    return JSONResponse(status_code=exc.status_code, content={"detail": str(exc.detail)})
