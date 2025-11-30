from typing import Type
from multiprocessing.managers import BaseManager

from .IScraper import IScraper
from .scraper_factory import ScraperFactory


class Manager(BaseManager):

    @staticmethod
    def register_scrapers(factory_dict: dict[str, Type[IScraper]]):
        Manager.register("Worker", ScraperFactory(factory_dict))