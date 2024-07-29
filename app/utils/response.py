import json
import math
from fastapi.responses import JSONResponse


headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": True,
}


def success_response(status_code, message, data, warning: str = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "data": data,
            "success": True,
            "message": message,
            "status_code": status_code,
            'warning': warning
        }
    )


def error_response(status_code, message, errors=[]):
    return JSONResponse(
        status_code=status_code,
        content={
            "data": None,
            "success": False,
            "message": message,
            "errors": errors
        }
    )


# def respond_error(data, success, message, status_code, errors=[]):
#     body = {"message": message, "success": success, "data": data, "errors": errors}
#     return {"statusCode": status_code, "headers": headers, "body": json.dumps(body)}
#
#
# def respond_success(data, success, message, status_code, warning=None, total_page=None, current_page=None):
#     if total_page and current_page:
#         data = {
#             "total_pages": math.ceil(total_page),
#             "current_page": current_page,
#             "data": data,
#         }
#     body = {"message": message, "success": success, "data": data, "warning": warning}
#     return {"statusCode": status_code, "headers": headers, "body": json.dumps(body)}
