from abc import ABC, abstractmethod
from typing import Any


class BaseLogger(ABC):
    """
    Base contract for all loggers in the system.
    Ensures consistent structured logging interface.
    """

    @abstractmethod
    def debug(self, message: str, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def info(self, message: str, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def error(self, message: str, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def exception(self, message: str, **kwargs: Any) -> None:
        """
        Log an error message including the current exception stack trace.
        """
        pass