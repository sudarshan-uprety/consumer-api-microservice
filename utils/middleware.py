import time
import uuid

from fastapi import Request

from utils.log import get_logger, trace_id_var

# Create a logger instance
logger = get_logger("auth_and_order_service")


async def log_middleware(request: Request, call_next):
    # Generate a unique trace ID for each request
    trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
    trace_id_var.set(trace_id)

    start_time = time.time()

    # Log the incoming request
    logger.info(f"Received request: {request.method} {request.url.path}")

    try:
        response = await call_next(request)
        process_time = time.time() - start_time

        status_code = response.status_code
        log_dict = {
            "url": request.url.path,
            "method": request.method,
            "process_time": f"{process_time:.4f}",
            "status_code": status_code,
            "trace_id": trace_id
        }

        # Log based on the response status
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
            "trace_id": trace_id
        })
        raise

    return response
