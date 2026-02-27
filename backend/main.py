from fastapi import FastAPI
from utils.settings import config
from utils.initialize import lifespan
from api.routes import api_router
import logging.config
from utils.logging_config import LOGGING_CONFIG
from fastapi.middleware.cors import CORSMiddleware
from middleware import origins
import utils.cloudinary_config  

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # List of allowed origins
    allow_credentials=True,         # Allow cookies and auth headers
    allow_methods=["*"],            # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],            # Allow all headers
)

app.include_router(api_router)
