from abc import ABC, abstractmethod

class BaseChannel(ABC):
    @abstractmethod
    async def send(self, user_id: int, message: str, title: str = None):
        """Logic to deliver the message via a specific medium."""
        pass