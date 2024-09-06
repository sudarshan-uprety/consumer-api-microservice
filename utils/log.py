import asyncio
import logging
import os
from contextvars import ContextVar
from logging.handlers import RotatingFileHandler

import httpx

from utils.variables import ENV, LOG_PATH, LOKI_URL

# ContextVar to store the trace ID for the current context
trace_id_var = ContextVar("trace_id", default="")

os.makedirs(LOG_PATH, exist_ok=True)


class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.trace_id = trace_id_var.get()
        return super().format(record)


class AsyncLokiHandler(logging.Handler):
    def __init__(self, url, labels=None):
        super().__init__()
        self.url = url
        self.labels = labels or {}
        self.queue = asyncio.Queue()
        self.client = httpx.AsyncClient()
        self.task = asyncio.create_task(self.sender())

    async def sender(self):
        while True:
            record = await self.queue.get()
            try:
                await self.send_log(record)
            except Exception as e:
                print(f"Failed to send log to Loki: {e}")
            finally:
                self.queue.task_done()

    async def send_log(self, record):
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
        response = await self.client.post(self.url, json=payload, headers=headers)
        response.raise_for_status()

    def emit(self, record):
        asyncio.create_task(self.queue.put(record))

    async def close(self):
        await self.client.aclose()
        await self.queue.join()


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
    file_formatter = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - [%(trace_id)s] - %(message)s')
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - [%(trace_id)s] - %(message)s')
    console_handler.setFormatter(console_formatter)

    # Loki handler
    loki_handler = AsyncLokiHandler(
        url=LOKI_URL,
        labels={"service": "login-auth", "env": ENV}
    )
    loki_handler.setLevel(logging.DEBUG)
    loki_formatter = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - [%(trace_id)s] - %(message)s')
    loki_handler.setFormatter(loki_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.addHandler(loki_handler)

    return logger


# Create a global logger instance
logger = get_logger("auth_and_order_service")
