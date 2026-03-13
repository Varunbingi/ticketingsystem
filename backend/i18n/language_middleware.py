from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from .translator import get_translator

class LanguageMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        lang = request.headers.get("Accept-Language", "en")

        translator = get_translator(lang)

        request.state.translate = translator

        response = await call_next(request)

        return response