from octoscrape.scraper import IAsyncScraper
from octoscrape.config import ScraperConfig
from octoscrape.concurrency import AsyncPool
from httpx import AsyncClient
import asyncio
import bs4
from typing import Generator
from .writer_services import write_to_csv


class Q2S(IAsyncScraper):
    '''Scraper for site "Quotes to Scrape"'''

    def __init__(self, scraper_config: ScraperConfig):
        super().__init__(scraper_config)
        self.__cached_quotes = set()
        self.__pool = AsyncPool(self._config.PoolSize)


    async def async_stop(self):...


    async def async_start(self):
        await self.__pool.start()
        async with AsyncClient() as client:
            await self.__pool.submit(self.__start_crawle(client, self._config.Url))
            await self.__pool.drain()
        await self.__pool.stop()


    async def __start_crawle(self, client:AsyncClient, url:str ):
        try:
            response = await client.get(url)
            response.raise_for_status()
        except:
            await asyncio.sleep(3)
            await self.__pool.submit(self.__start_crawle(client, url))
            return

        soup = bs4.BeautifulSoup(response.text, "lxml")
        paths = soup.find(class_="col-md-4 tags-box").find_all("a")

        if not paths:
            raise ValueError("No tag links found")
        
        for path in paths:
            await self.__pool.submit(self.__scrape_quotes(client, self._config.Url + path.get("href")))
    

    async def __scrape_quotes(self, client: AsyncClient, url: str):
        try:
            response = await client.get(url)
            response.raise_for_status()
        except Exception:
            # if no response is received, 
            # we place this task at the end of the queue for a retry
            self.__pool.submit(self.__scrape_quotes(client, url))
            return

        soup = bs4.BeautifulSoup(response.text, "lxml")
        quotes_div = soup.find_all("div", class_="quote")

        await write_to_csv(self._config.Name, self.__filtered_quotes(quotes_div), delimiter="|")

        next_url = soup.find("li", class_="next")
        if not next_url is None:
            await self.__pool.submit(self.__scrape_quotes(client, self._config.Url + next_url.find("a").get("href")))


    def __filtered_quotes(self, quotes_div) -> Generator[dict[str, str], None, None]:
        for qt in quotes_div:
            quote = qt.find("span", class_="text").get_text(strip=True)
            h = hash(quote)

            if h in self.__cached_quotes:
                continue

            self.__cached_quotes.add(h)
            yield {
                "quote": quote,
                "author": qt.find(class_="author").get_text(strip=True),
                "tags": ",".join(
                    tag.get_text(strip=True) 
                    for tag in qt.find("div", class_="tags").find_all("a")
                ),
            }