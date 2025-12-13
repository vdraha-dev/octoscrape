from typing import Iterable

from ..config import ScraperConfig
from .interfaces import IAsyncScraper


class ScraperFactory:
    """
    Factory for IAsyncScraper implementations.

    Args:
        scrapers: Iterable of scraper classes.

    Example:
        ScraperFactory([Scraper1, Scraper2, Scraper3])

    Raises:
        KeyError: if scraper not found
    """

    def __init__(self, scrapers: Iterable[type[IAsyncScraper]]):
        self.__scrapers = {s.__name__: s for s in scrapers}

    def __call__(self, config: ScraperConfig, *args, **kwargs) -> IAsyncScraper:
        cls = self.__scrapers.get(config.Scraper, None)
        if cls is None:
            raise KeyError(f"Scraper '{config.Scraper}' not found")
        return cls(config, *args, **kwargs)
