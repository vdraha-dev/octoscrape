import pytest 
import asyncio
from octoscrape.scraper.interfaces import IScraper
from octoscrape.scraper.factory import ScraperFactory
from octoscrape.config import ScraperConfig, CommonConfig

class MockScraper(IScraper):
    async def async_start(self):
        await asyncio.sleep(.1)
        while not self._stop_event.is_set():
            await asyncio.sleep(.1)

    async def async_stop(self):...


class FailingScraper(IScraper):
    async def async_start(self):
        await asyncio.sleep(.1)
        raise RuntimeError("FailingScraper")

    async def async_stop(self):...


@pytest.fixture(scope="session")
def scraper_config_dict():
    return {}


@pytest.fixture(scope="session")
def common_config_dict():
    return {}


@pytest.fixture(scope="session")
def scraper_config(scraper_config_dict):
    return ScraperConfig(scraper_config_dict)


@pytest.fixture(scope="session")
def common_config(common_config_dict):
    return CommonConfig(common_config_dict)


@pytest.fixture(scope="session")
def scraper_dict():
    return {
        "scraper": MockScraper,
        "failing_scraper": FailingScraper
    }


@pytest.fixture(scope="session")
def factory(scraper_dict):
    return ScraperFactory(scraper_dict)


@pytest.fixture(scope="function")
def runner(factory):
    return MultiRunner(factory, pool_size=2)