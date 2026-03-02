from .base_channel import BaseChannel
from ..providers.email import send_email 
from db.db import async_session
from db.models.user import User
from sqlalchemy import select

class EmailChannel(BaseChannel):
    async def send(self, user_id: int, message: str, title: str = "Notification"):
        print
        template_map = {
            "WELCOME": "user_registration.html",
            "TICKET_CREATED": "ticket_confirmation.html",
            "DEFAULT": "notification_template.html",
            "VERIFICATION": "verification.html"
        }
        target_template = template_map.get(title, template_map["DEFAULT"])
        # Fetch actual user email from DB
        async with async_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            
            if user and user.email:
                email_context = {
                    "message": message, 
                    "firstname": user.firstname
                }
                if title == "VERIFICATION":
                    email_context["verification_link"] = message
                await send_email(
                    subject=title,
                    recipient_email=[user.email],
                    template_name=target_template,
                    context=email_context
                )