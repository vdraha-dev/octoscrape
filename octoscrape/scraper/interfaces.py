from abc import ABC, abstractmethod

from ..config import ScraperConfig


class IAsyncScraper(ABC):
    """
    Abstract base class for asynchronous scrapers.

    This interface defines the common properties and state management
    for all scrapers, including identification and stopped status.
    """

    def __init__(self, config: ScraperConfig):
        """
        Initialize the scraper with a given configuration.

        Args:
            config: ScraperConfig instance containing scraper settings.
        """
        self._config: ScraperConfig = config
        self._is_stopped: bool = True

    @property
    def name(self):
        """
        Get the internal name of the scraper.

        Returns:
            The unique name of the scraper.
        """
        return self._config.name

    @property
    def human_name(self):
        """
        Get the human-readable name of the scraper.

        Returns:
            A user-friendly display name for the scraper.
        """
        return self._config.human_name

    @property
    def full_name(self):
        """
        Get the full descriptive name of the scraper.

        Combines the key, internal name, and human-readable name.

        Returns:
            Full name string, formatted as "key.name | human_name" if
            key and human name exist, otherwise just the internal name.
        """

        key = self._config.key
        if len(key) > 0:
            key += "."

        human_name = self._config.human_name
        if len(human_name) > 0:
            human_name = f" | {human_name}"

        return f"{key}{self._config.name}{human_name}"

    @property
    def is_stopped(self) -> bool:
        """
        Check whether the scraper is currently stopped.

        Returns:
            True if the scraper is stopped, False otherwise.
        """
        return self._is_stopped

    @abstractmethod
    async def async_start(self): ...

    @abstractmethod
    async def async_stop(self): ...
