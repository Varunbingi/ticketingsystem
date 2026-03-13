from fastapi import FastAPI,Request
from utils.settings import config
from utils.initialize import lifespan
from api.routes import api_router
import logging.config
from utils.logging_config import LOGGING_CONFIG
from fastapi.middleware.cors import CORSMiddleware
from middleware import origins
import utils.cloudinary_config 
import uuid 
from logging_system.log_helper import log_info,log_error,log_warning,log_exception,new_span,end_span,extract_user_id
from http import HTTPStatus
from jose import jwt # for decoding JWT (if you use it)
from i18n.language_middleware import LanguageMiddleware

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)

app.add_middleware(LanguageMiddleware)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Setup request context
    request.state.request_id = str(uuid.uuid4())
    request.state.trace_id = request.headers.get("x-trace-id") or str(uuid.uuid4())
    request.state.user_id = None

    # Extract user_id from JWT if present
    auth_header = request.headers.get("authorization")
    if auth_header:
        try:
            parts = auth_header.split(" ")
            if len(parts) == 2:
                token = parts[1]
                payload = jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
                request.state.user_id = payload.get("user_id")
        except Exception:
            request.state.user_id = None

    # Start top-level span for the entire request
    new_span(request, "http.request")

    try:
        response = await call_next(request)
    except Exception as e:
        # Log exception BEFORE ending span
        log_exception(request, f"Unhandled server exception: {str(e)}")
        end_span(request)  # end top-level span
        raise

    # Log middleware request AFTER route executes, BEFORE ending span
    status = response.status_code
    reason = HTTPStatus(status).phrase
    message = f"{request.method} {request.url.path} → {status} {reason}"

    if status >= 500:
        log_error(request, message)
    elif status >= 400:
        log_warning(request, message)
    else:
        log_info(request, message)

    # End top-level span AFTER logging
    duration, span_name = end_span(request)
    request.state.duration = duration  # optional: store duration in state

    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # List of allowed origins
    allow_credentials=True,         # Allow cookies and auth headers
    allow_methods=["*"],            # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],            # Allow all headers
)

app.include_router(api_router)
