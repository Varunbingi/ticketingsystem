from .base_channel import BaseChannel
from db.models.notifications import Notification 
from db.db import async_session

class InAppChannel(BaseChannel):
    async def send(self, user_id: int, message: str, title: str = "New Notification"):
        async with async_session() as session:
            new_notif = Notification(
                user_id=user_id,
                title=title,
                message=message,
                channel="INAPP"
            )
            session.add(new_notif)
            await session.commit()