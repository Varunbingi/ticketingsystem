import logging
import asyncio
from db.models.log import AppLog
from db.db import async_session
from datetime import datetime


class DBLogHandler(logging.Handler):
    """
    Async-safe DB logging handler for FastAPI.
    Uses async_session internally to insert log rows in the background.
    """

    def emit(self, record: logging.LogRecord):
        try:
            # Schedule the async insert in the background
            asyncio.create_task(self._write_log(record))
        except Exception:
            self.handleError(record)

    async def _write_log(self, record: logging.LogRecord):
        try:
            async with async_session() as session:
                async with session.begin():
                    # Safely convert integer fields
                    lineno_val = self._safe_int(getattr(record, "lineno", 0))
                    user_id_val = self._safe_int(getattr(record, "user_id", None))

                    log_entry = AppLog(
                        level=str(getattr(record, "levelname", "-")),
                        filename=str(getattr(record, "filename", "-")),
                        lineno=lineno_val,
                        user_id=user_id_val,
                        path=str(getattr(record, "path", "-")),
                        method=str(getattr(record, "method", "-")),
                        request_id=str(getattr(record, "request_id", "-")),
                        trace_id=str(getattr(record, "trace_id", "-")),
                        span_id=str(getattr(record, "span_id", "-")),
                        span_name=str(getattr(record, "span_name", "-")),
                        duration_ms=float(getattr(record, "duration_ms", 0.0)),
                        message=str(record.getMessage()),
                        created_at=datetime.utcnow()
                    )
                    session.add(log_entry)
        except Exception:
            self.handleError(record)

    @staticmethod
    def _safe_int(value):
        """
        Safely convert a value to integer, return None if not possible.
        """
        if value is None:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None