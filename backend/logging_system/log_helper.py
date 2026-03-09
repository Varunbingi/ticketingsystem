from fastapi import Request
import uuid
import time
from typing import Optional
from logging_system.app_logger import AppLogger

logger = AppLogger()


def new_span(request: Request, span_name: str = "span") -> None:
    """
    Start a new tracing span.
    Supports nested spans.
    """
    if not hasattr(request.state, "span_stack"):
        request.state.span_stack = []

    span = {
        "span_id": str(uuid.uuid4()),
        "span_name": span_name,
        "start_time": time.perf_counter(),
    }

    request.state.span_stack.append(span)
    request.state.span_id = span["span_id"]
    request.state.span_name = span["span_name"]


def end_span(request: Request) -> tuple[float, str]:
    """
    End the current span, calculate duration in milliseconds,
    and return both duration and span name.
    """
    if not hasattr(request.state, "span_stack") or not request.state.span_stack:
        return 0.0, "-"

    # Pop current span
    span = request.state.span_stack.pop()
    duration = round((time.perf_counter() - span["start_time"]) * 1000, 2)
    span_name = span["span_name"]

    # Store duration in request.state
    request.state.duration = duration

    # Restore parent span if exists
    if request.state.span_stack:
        parent = request.state.span_stack[-1]
        request.state.span_id = parent["span_id"]
        request.state.span_name = parent["span_name"]
    else:
        request.state.span_id = "-"
        request.state.span_name = "-"

    return duration, span_name


def extract_user_id(request: Request) -> Optional[int]:
    """
    Safely extract the user_id from request.state.
    Returns None if not set.
    """
    user_id = getattr(request.state, "user_id", None)
    if user_id in ("-", None):
        return None
    return user_id


def log_with_span(request: Request, message: str, level: str = "info", **kwargs):
    """
    Logs a message and automatically attaches current span_id, span_name, trace_id.
    """
    kwargs["span_id"] = getattr(request.state, "span_id", "-")
    kwargs["span_name"] = getattr(request.state, "span_name", "-")
    kwargs["trace_id"] = getattr(request.state, "trace_id", "-")

    if level.lower() == "info":
        log_info(request, message, **kwargs)
    elif level.lower() == "warning":
        log_warning(request, message, **kwargs)
    elif level.lower() == "error":
        log_exception(request, message, **kwargs)


def _common_fields(request: Request):
    return {
        "path": request.url.path,
        "method": request.method,
        "user_id": getattr(request.state, "user_id", "-"),
        "request_id": getattr(request.state, "request_id", "-"),
        "trace_id": getattr(request.state, "trace_id", "-"),
        "span_id": getattr(request.state, "span_id", "-"),
        "span_name": getattr(request.state, "span_name", "-"),
        "duration_ms": getattr(request.state, "duration", 0),
    }


def log_info(request: Request, message: str) -> None:
    logger.info(message, **_common_fields(request))


def log_warning(request: Request, message: str) -> None:
    logger.warning(message, **_common_fields(request))


def log_error(request: Request, message: str) -> None:
    logger.error(message, **_common_fields(request))


def log_exception(request: Request, message: str) -> None:
    logger.exception(message, **_common_fields(request))