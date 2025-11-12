import logging, sys, json, time, uuid
from typing import Optional

def _json_formatter(record: logging.LogRecord) -> str:
    payload = {
        "time": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(record.created)),
        "level": record.levelname,
        "name": record.name,
        "msg": record.getMessage(),
    }
    if record.exc_info:
        payload["exc_info"] = logging.Formatter().formatException(record.exc_info)
    return json.dumps(payload)

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return _json_formatter(record)

def configure_logging(level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger("eprda")
    if logger.handlers:
        return logger
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger

def new_run_id() -> str:
    return uuid.uuid4().hex[:12]
