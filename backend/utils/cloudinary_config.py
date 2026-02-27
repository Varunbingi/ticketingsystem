import cloudinary
import cloudinary.uploader
from utils.settings import config


cloudinary.config(
    cloud_name=config.cloud_name,
    api_key=config.api_key,
    api_secret=config.api_secret,
    secure=True
)
