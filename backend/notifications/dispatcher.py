from sqlalchemy import select
from db.db import async_session
from db.models.notifications import NotificationPreference
from notifications.strategies.direct_strategy import DirectStrategy
from notifications.strategies.multiple_strategy import MultipleStrategy
from notifications.channels.email_channel import EmailChannel
from notifications.channels.inapp_channel import InAppChannel
from notifications.channels.sms_channel import SmsChannel


STRATEGY_REGISTRY = {
    "DIRECT": DirectStrategy(),
    "MULTIPLE": MultipleStrategy(),
}

async def emit_event(event_name: str, strategy: str, payload: dict):
    """
    Core function to trigger notifications across multiple channels 
    based on user-defined preferences.
    """
   
    resolver = STRATEGY_REGISTRY.get(strategy)
    if not resolver:
        raise ValueError(f"Invalid strategy: {strategy}")
    
    user_ids = await resolver.resolve(payload)
    

    inapp = InAppChannel()
    email = EmailChannel()
    sms = SmsChannel()
    

    async with async_session() as session:
        for user_id in user_ids:

            result = await session.execute(
                select(NotificationPreference).where(NotificationPreference.user_id == user_id)
            )
            prefs = result.scalar_one_or_none()

      
            if not prefs:
                await inapp.send(user_id, payload.get("message"), event_name)
                await email.send(user_id, payload.get("message"), event_name)
                continue

            if prefs.inapp_enabled:
                await inapp.send(user_id, payload.get("message"), event_name)
            
            if prefs.email_enabled:
                await email.send(user_id, payload.get("message"), event_name)
                
            if prefs.sms_enabled:
                await sms.send(user_id, payload.get("message"), event_name)