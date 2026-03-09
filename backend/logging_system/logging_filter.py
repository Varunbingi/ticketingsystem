import logging


class RequestContextFilter(logging.Filter):
    """
    Ensures all required structured logging fields exist
    to prevent formatter KeyError and maintain schema consistency.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        # Text fields
        record.path = getattr(record, "path", "-")
        record.method = getattr(record, "method", "-")
        record.user_id = getattr(record, "user_id", "-")
        record.request_id = getattr(record, "request_id", "-")
        record.trace_id = getattr(record, "trace_id", "-")
        record.span_id = getattr(record, "span_id", "-")
        record.span_name = getattr(record, "span_name", "-")

        # Duration must be numeric
        duration = getattr(record, "duration_ms", None)
        record.duration_ms = duration if isinstance(duration, (int, float)) else 0

        return True