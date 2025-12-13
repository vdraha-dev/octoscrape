from abc import ABC, abstractmethod
from contextlib import asynccontextmanager

from playwright.async_api import Browser


class IBrowserManager(ABC):
    """
    Interface for singleton browser lifecycle management.

    Defines the contract for creating, accessing, and destroying
    a single browser instance in an asynchronous environment.
    """

    @property
    @abstractmethod
    def browser(self) -> Browser:
        """
        Return existing browser instance.

        Raises:
            RuntimeError: If the browser has not been created yet.
        """

    @property
    @abstractmethod
    def initialized(self) -> bool:
        """Indicates whether the browser has been initialized."""

    @abstractmethod
    @asynccontextmanager
    async def create_browser(self):
        """
        Creates a browser instance.

        Raises:
            RuntimeError: if browser almost exists
        """
