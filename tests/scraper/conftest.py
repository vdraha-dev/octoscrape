import pytest
import asyncio
from octoscrape.config import ScraperConfig
from octoscrape.scraper.interfaces import IAsyncScraper
from octoscrape.scraper.factory import ScraperFactory
from octoscrape.scraper.mixins import MixinContextCreator

############################
# Fixctures for Interfaces #
############################


class AsyncScraper(IAsyncScraper):
    async def async_start(self):
        await asyncio.sleep(0.01)

    async def async_stop(self):
        await asyncio.sleep(0.01)


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
def async_scraper(scraper_config):
    return AsyncScraper(scraper_config)


#######################
# Fixtures for mixins #
#######################


class AsyncScraperWithContextCreator(IAsyncScraper, MixinContextCreator):
    async def async_start(self):
        await asyncio.sleep(0.01)

    async def async_stop(self):
        await asyncio.sleep(0.01)


@pytest.fixture(scope="session")
def context_creator_scraper(scraper_config):
    return AsyncScraperWithContextCreator(scraper_config)


########################
# Fixtures for factory #
########################


class Scraper2(AsyncScraper): ...


class Scraper3(AsyncScraper): ...


@pytest.fixture(scope="session")
def factory_list():
    return [AsyncScraper, Scraper2, Scraper3]


@pytest.fixture(scope="session")
def factory(factory_list):
    return ScraperFactory(factory_list)


@pytest.fixture(scope="function")
def exist_config_1():
    return ScraperConfig({"scraper": "AsyncScraper"})


@pytest.fixture(scope="function")
def exist_config_2():
    return ScraperConfig({"scraper": "Scraper2"})


@pytest.fixture(scope="function")
def exist_config_3():
    return ScraperConfig({"scraper": "Scraper3"})


@pytest.fixture(scope="function")
def not_exist_config():
    return ScraperConfig({"scraper": "is_not_exist"})
