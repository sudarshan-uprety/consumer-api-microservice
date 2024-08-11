import json
import time
import uuid

from fastapi import Request
from fastapi.responses import JSONResponse

from utils.log import get_logger, trace_id_var

# Create a logger instance
logger = get_logger("auth_and_order_service")

# List of sensitive fields to redact
SENSITIVE_FIELDS = [
    "password", "confirm_password", "new_password", "current_password",
    "access_token", "refresh_token"
]


def sanitize_payload(payload):
    if isinstance(payload, bytes):
        try:
            payload = json.loads(payload.decode())
        except json.JSONDecodeError:
            return payload

    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            return payload

    if isinstance(payload, dict):
        return {k: '******' if k in SENSITIVE_FIELDS else
        (sanitize_payload(v) if isinstance(v, (dict, list)) else v)
                for k, v in payload.items()}
    elif isinstance(payload, list):
        return [sanitize_payload(item) for item in payload]
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

    logger.info(f"Received request: {request.method} {request.url.path} from {client_ip}")

    async def capture_response(request):
        response = await call_next(request)
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        return JSONResponse(
            content=json.loads(response_body),
            status_code=response.status_code,
            headers=dict(response.headers)
        )

    try:
        response = await capture_response(request)
        process_time = time.time() - start_time

        status_code = response.status_code

        # Redact sensitive data from response payload
        response_content = json.loads(response.body)
        response_payload = sanitize_payload(response_content)

        log_dict = {
            "url": request.url.path,
            "method": request.method,
            "process_time": f"{process_time:.4f}",
            "status_code": status_code,
            "trace_id": trace_id,
            "client_ip": client_ip,
            "request_payload": request_body,
            "response_payload": json.dumps(response_payload)  # Convert back to JSON string
        }

        if status_code >= 500:
            logger.error(f"Request failed: {log_dict}")
        elif status_code >= 400:
            logger.warning(f"Request resulted in client error: {log_dict}")
        else:
            logger.info(f"Request completed successfully: {log_dict}")

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
