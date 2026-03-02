from .base_strategy import BaseStrategy

class MultipleStrategy(BaseStrategy):
    async def resolve(self, payload: dict):
        # Expects payload: {"user_ids": [1, 2, 3]}
        return payload.get("user_ids", [])