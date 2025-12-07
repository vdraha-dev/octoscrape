import pytest
import asyncio
from octoscrape.config import ScraperConfig
from octoscrape.scraper.interfaces import IAsyncScraper
from octoscrape.scraper.factory import ScraperFactory
from octoscrape.scraper.mixins import MixinContextCreator, MixinSync

############################
# Fixctures for Interfaces #
############################

class AsyncScraper(IAsyncScraper):
    async def async_start(self):
        await asyncio.sleep(.01)

    async def async_stop(self):
        await asyncio.sleep(.01)


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
        await asyncio.sleep(.01)

    async def async_stop(self):
        await asyncio.sleep(.01)


class SyncScraper(IAsyncScraper, MixinSync):
    async def async_start(self):
        await asyncio.sleep(.01)

    async def async_stop(self):
        await asyncio.sleep(.01)


@pytest.fixture(scope="session")
def sync_scraper(scraper_config):
    return SyncScraper(scraper_config)


@pytest.fixture(scope="session")
def context_creator_scraper(scraper_config):
    return AsyncScraperWithContextCreator(scraper_config)




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