import asyncio
from octoscrape.scraper import IAsyncScraper


class DummiesScraper(IAsyncScraper):
    async def async_start(self):
        self._is_stopped = False
        while not self.is_stopped:
            await asyncio.sleep(0.05)
            print("dumimes")


    async def async_stop(self):
        self._is_stopped = True