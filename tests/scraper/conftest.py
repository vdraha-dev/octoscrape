import pytest
import asyncio
import copy
from octoscrape.config import ScraperConfig
from octoscrape.scraper.interfaces import IAsyncScraper, IScraper
from octoscrape.scraper.factory import ScraperFactory


############################
# Fixctures for Interfaces #
############################

class AsyncScraper(IAsyncScraper):
    async def async_start(self):
        await asyncio.sleep(.01)

    async def async_stop(self):
        await asyncio.sleep(.01)


class SyncScraper(IScraper):
    async def async_start(self):
        await asyncio.sleep(.01)

    async def async_stop(self):
        await asyncio.sleep(.01)


@pytest.fixture(scope="session")
def scraper_config_dict():
    return {
        "human_name": "like a human",
        "name": "qwerty",
        "url": "urllll",
        "headless": True
    }


@pytest.fixture(scope="function")
def fresh_scraper_config_dict(scraper_config_dict):
    return copy.deepcopy(scraper_config_dict)


@pytest.fixture(scope="function")
def create_fresh_async_scraper():
    def inner(*args, **kwargs):
        return AsyncScraper(*args, **kwargs) 
    return inner


@pytest.fixture(scope="function")
def create_fresh_scraper_config():
    def inner(*args, **kwargs):
        return ScraperConfig(*args, **kwargs) 
    return inner


@pytest.fixture(scope="session")
def scraper_config(scraper_config_dict):
    return ScraperConfig(scraper_config_dict, "Key")


@pytest.fixture(scope="session")
def async_scraper(scraper_config):
    return AsyncScraper(scraper_config)


@pytest.fixture(scope="session")
def sync_scraper(scraper_config):
    return SyncScraper(scraper_config)



########################
# Fixtures for factory #
########################

class SyncScraper2(SyncScraper):...
class SyncScraper3(SyncScraper):...

@pytest.fixture(scope="session")
def factory_dict():
    return {
        "label1": SyncScraper,
        "label2": SyncScraper2,
        "label3": SyncScraper3
    }

@pytest.fixture(scope="session")
def factory(factory_dict):
    return ScraperFactory(factory_dict)