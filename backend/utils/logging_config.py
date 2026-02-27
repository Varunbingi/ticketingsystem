import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
        "simple": {
            "format": "[%(levelname)s] %(message)s"
        },
    },

    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": "logs/app.log",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
        },
    },

    "loggers": {
        "": {  # This is the 'root' logger: every logger in the app inherits from this
            "handlers": ["console", "file"], # Send root logs to both destinations
            "level": "INFO",
            "propagate": True
        },
        "uvicorn.access": { # Explicitly configure uvicorn's web server logs
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    }
}