from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    @abstractmethod
    async def resolve(self, payload: dict):
        """Returns a list of user IDs based on the payload."""
        pass