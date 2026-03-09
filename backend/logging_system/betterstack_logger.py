# logging_system/betterstack_logger.py

import logging
from logtail import LogtailHandler
from .base import BaseLogger


class BetterStackLogger(BaseLogger):
    def __init__(self, source_token: str, name: str = "betterstack"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        if not self.logger.handlers:
            handler = LogtailHandler(source_token=source_token)
            self.logger.addHandler(handler)

    # Public methods

    def debug(self, message: str, **kwargs):
        self._log(self.logger.debug, message, **kwargs)

    def info(self, message: str, **kwargs):
        self._log(self.logger.info, message, **kwargs)

    def warning(self, message: str, **kwargs):
        self._log(self.logger.warning, message, **kwargs)

    def error(self, message: str, **kwargs):
        self._log(self.logger.error, message, **kwargs)

    def exception(self, message: str, **kwargs):
        self._log(self.logger.exception, message, **kwargs)

    # Core logger

    def _log(self, log_func, message: str, **kwargs):
        extra = self._build_extra(kwargs)
        log_func(message, extra=extra, stacklevel=3)

    # Extra builder

    def _build_extra(self, data: dict) -> dict:
        return {
            "path": data.get("path") if data.get("path") is not None else "-",
            "method": data.get("method") if data.get("method") is not None else "-",
            "user_id": data.get("user_id") if data.get("user_id") is not None else "-",
            "request_id": data.get("request_id") if data.get("request_id") is not None else "-",
            "trace_id": data.get("trace_id") if data.get("trace_id") is not None else "-",
            "span_id": data.get("span_id") if data.get("span_id") is not None else "-",
            "span_name": data.get("span_name") if data.get("span_name") is not None else "-",
            "duration_ms": data.get("duration_ms") if data.get("duration_ms") is not None else 0,
        }