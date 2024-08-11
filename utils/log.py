import asyncio
import logging
import os
from contextvars import ContextVar
from logging.handlers import RotatingFileHandler

import httpx

from utils.variables import ENV, LOG_PATH, LOKI_URL

# ContextVar to store the trace ID for the current context
trace_id_var = ContextVar("trace_id", default="")

LOG_PATH = LOG_PATH
os.makedirs(LOG_PATH, exist_ok=True)


class CustomFormatter(logging.Formatter):
    def format(self, record):
        trace_id = trace_id_var.get()
        record.trace_id = trace_id
        return super().format(record)


class AsyncLokiHandler(logging.Handler):
    def __init__(self, url, labels=None):
        super().__init__()
        self.url = url
        self.labels = labels if labels else {}
        self.queue = asyncio.Queue()
        self.task = asyncio.create_task(self.sender())

    async def sender(self):
        async with httpx.AsyncClient() as client:
            while True:
                record = await self.queue.get()
                try:
                    await self.send_log(client, record)
                except Exception as e:
                    print(f"Failed to send log to Loki: {e}")
                finally:
                    self.queue.task_done()

    async def send_log(self, client, record):
        log_entry = self.format(record)
        payload = {
            "streams": [
                {
                    "stream": self.labels,
                    "values": [[str(int(record.created * 1e9)), log_entry]]
                }
            ]
        }
        headers = {'Content-type': 'application/json'}
        response = await client.post(self.url, json=payload, headers=headers)
        response.raise_for_status()

    def emit(self, record):
        asyncio.create_task(self.queue.put(record))

    def format_labels(self, labels):
        return ''.join([f'{k}="{v}",' for k, v in labels.items()])[:-1]

    def format_timestamp(self, created_time):
        return f"{int(created_time * 1e9)}"  # Convert to nanoseconds


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # File handler
    file_handler = RotatingFileHandler(
        os.path.join(LOG_PATH, f"{name}.log"),
        maxBytes=10485760,
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(trace_id)s - %(message)s'))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(trace_id)s - %(message)s'))

    # Loki handler
    loki_handler = AsyncLokiHandler(
        url=LOKI_URL,
        labels={"service": "login-auth", "env": ENV}
    )
    loki_handler.setLevel(logging.DEBUG)
    loki_handler.setFormatter(CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(trace_id)s - %(message)s'))

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.addHandler(loki_handler)

    return logger


# Example usage
logger = get_logger("my_app")


# To set a trace ID for a request
async def some_request_handler():
    trace_id = "unique_trace_id"  # Generate or get this from the request
    trace_id_var.set(trace_id)
    logger.info("Processing request")
    # Your request handling logic here


# To use the logger in an async context
async def main():
    logger.info("Starting application")
    await some_request_handler()
    logger.info("Application finished")
