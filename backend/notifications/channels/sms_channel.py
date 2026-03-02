from .base_channel import BaseChannel

class SmsChannel(BaseChannel):
    async def send(self, user_id: int, message: str, title: str = None):
        # Placeholder for SMS Gateway (Twilio, etc.)
        print(f"Sending SMS to User {user_id}: {message}")