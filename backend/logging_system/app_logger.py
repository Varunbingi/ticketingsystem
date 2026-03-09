import logging
from logging_system.base import BaseLogger


class AppLogger(BaseLogger):
    def __init__(self):
        self.logger = logging.getLogger("app")

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
        log_func(message, extra=extra, stacklevel=4)

    # Extra builder
    def _build_extra(self, data: dict) -> dict:
        """
        Ensure all required formatter fields always exist.
        Prevents KeyError from logging formatter.
        """
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