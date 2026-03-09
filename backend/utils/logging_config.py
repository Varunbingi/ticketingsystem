from utils.settings import config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "default": {
            "format": (
                "%(asctime)s %(levelname)s "
                "file=%(filename)s line=%(lineno)d "
                "path=%(path)s method=%(method)s "
                "user_id=%(user_id)s "
                "request_id=%(request_id)s trace_id=%(trace_id)s span_id=%(span_id)s span_name=%(span_name)s "
                "duration_ms=%(duration_ms)s "
                "message=%(message)s"
            )
        }
    },

    "filters": {
        "context": {
            "()": "logging_system.logging_filter.RequestContextFilter"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "filters": ["context"],
            "level": "INFO"
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filters": ["context"],
            "level": "INFO",
            "filename": "logs/app.log"
        },
        "betterstack": {
            "class": "logtail.LogtailHandler",
            "formatter": "default",
            "filters": ["context"],
            "level": "INFO",
            "source_token": config.BETTERSTACK_SOURCE_TOKEN
        },
        "db": {
            "class": "logging_system.db_log_handler.DBLogHandler",
            "level": "INFO",
            "filters": ["context"]
        }
    },

    "loggers": {
        "app": {
            "handlers": ["console", "file", "betterstack", "db"],
            "level": "INFO",
            "propagate": False
        }
    }
}