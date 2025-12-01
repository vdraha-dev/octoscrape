from typing import Type
from multiprocessing.managers import BaseManager

from .interfaces import IScraper
from .factory import ScraperFactory


class Manager(BaseManager):

    @staticmethod
    def register_scrapers(factory_dict: dict[str, Type[IScraper]]):
        Manager.register("Worker", ScraperFactory(factory_dict))