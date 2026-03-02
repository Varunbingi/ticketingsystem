from .base_strategy import BaseStrategy

class DirectStrategy(BaseStrategy):
    async def resolve(self, payload: dict):
        # Expects payload: {"user_id": 1}
        user_id = payload.get("user_id")
        return [user_id] if user_id else []