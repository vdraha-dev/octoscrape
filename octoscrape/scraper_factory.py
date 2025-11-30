from typing import Type
from .IScraper import IScraper


class ScraperFactory:
    def __init__(self, scrapers: dict[str, Type[IScraper]]):
        self.__scrapers = scrapers


    def __call__(self, label, *args, **kwargs) -> IScraper:
        cls = self.__scrapers.get(label, None)
        if cls is None:
            raise KeyError(f"Scraper '{label}' not found") 
        return cls(*args, **kwargs)