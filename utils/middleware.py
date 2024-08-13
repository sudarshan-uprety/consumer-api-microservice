import json
import time
import uuid

from fastapi import Request

from utils.log import get_logger, trace_id_var

# Create a logger instance
logger = get_logger("auth_and_order_service")

# List of sensitive fields to redact
SENSITIVE_FIELDS = [
    "password", "confirm_password", "new_password", "current_password",
    "access_token", "refresh_token"
]


def sanitize_payload(payload):
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            return payload

    if isinstance(payload, dict):
        sanitized = {}
        for key, value in payload.items():
            if key in SENSITIVE_FIELDS:
                sanitized[key] = "******"
            elif isinstance(value, (dict, list)):
                sanitized[key] = sanitize_payload(value)
            else:
                sanitized[key] = value
        return sanitized
    elif isinstance(payload, list):
        return [sanitize_payload(item) for item in payload]
    else:
        return payload


async def log_middleware(request: Request, call_next):
    trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
    trace_id_var.set(trace_id)

    start_time = time.time()
    client_ip = request.client.host

    # Get and redact the request body
    try:
        request_body = await request.json()
        request_body = sanitize_payload(request_body)
    except json.JSONDecodeError:
        request_body = await request.body()
        request_body = request_body.decode() if request_body else ""

    try:
        response = await call_next(request)
        process_time = time.time() - start_time

        status_code = response.status_code

        log_dict = {
            "url": request.url.path,
            "method": request.method,
            "process_time": f"{process_time:.4f}",
            "status_code": status_code,
            "trace_id": trace_id,
            "client_ip": client_ip,
            "request_payload": request_body
        }

        if status_code >= 500:
            logger.error(f"Request failed: {json.dumps(log_dict)}")
        elif status_code >= 400:
            logger.warning(f"Request resulted in client error: {json.dumps(log_dict)}")
        else:
            logger.info(f"Request completed successfully: {json.dumps(log_dict)}")

    except Exception as e:
        process_time = time.time() - start_time
        logger.exception(f"Request failed with exception: {str(e)}", extra={
            "url": request.url.path,
            "method": request.method,
            "process_time": f"{process_time:.4f}",
            "trace_id": trace_id,
            "client_ip": client_ip,
            "request_payload": request_body
        })
        raise

    return response
