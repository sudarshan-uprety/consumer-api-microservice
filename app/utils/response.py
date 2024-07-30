from typing import Dict, List, Optional, Union

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from utils.constant import ERROR_BAD_REQUEST, SUCCESS

headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Credentials': 'true',
}


def response(data: Optional[Union[Dict, List]], success: bool, message: str, status_code: int, **kwargs) -> JSONResponse:
    content = {
        "message": message,
        "success": success,
        "data": data
    }

    return JSONResponse(
        content=jsonable_encoder(content, **kwargs),
        status_code=status_code,
        headers=headers
    )


def success(status_code=SUCCESS, message=None, data=None, **kwargs):
    return response(data=data, success=True, message=message, status_code=status_code, **kwargs)


def error(status_code=ERROR_BAD_REQUEST, message=None):
    return response(data=None, success=False, message=message, status_code=status_code)
