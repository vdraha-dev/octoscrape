import asyncio
import logging
import threading
import time
from typing import Iterable

from ..concurrency import AsyncPool
from ..config import common_config, scrappers_configs
from .factory import ScraperFactory
from .interfaces import IAsyncScraper

logger = logging.getLogger(__name__)


class MultiRunner:
    """
    Manager for running multiple asynchronous scrapers in a controlled thread loop.

    This class handles:
    - creating and managing an asyncio event loop in a separate thread
    - starting and stopping an AsyncPool for task execution
    - registering scraper factories
    - running and stopping scrapers safely
    """

    def __init__(self):
        """Initialize internal state without starting the loop."""
        self.__factory: ScraperFactory | None = None
        self.__scrapers: dict[str, IAsyncScraper] = {}
        self.__pool: AsyncPool = None

        self.__running_loop: asyncio.AbstractEventLoop | None = None
        self.__loop_thread: threading.Thread | None = None

    @property
    def is_started(self):
        """
        Check whether the async loop is currently running.

        Returns:
            True if the loop is running, False otherwise.
        """
        return (
            False if self.__running_loop is None else self.__running_loop.is_running()
        )

    @property
    def loop(self):
        return self.__running_loop

    def start(self):
        """
        Start the asyncio loop and the AsyncPool in a separate thread.

        Raises:
            RuntimeError: If the MultiRunner is already started.
        """

        if self.is_started:
            raise RuntimeError("Multirainer is already started.")

        ready: threading.Event = threading.Event()

        def run_loop():
            self.__running_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.__running_loop)

            async def init():
                await self.__pool.start()
                ready.set()

            self.__running_loop.create_task(init())
            self.__running_loop.run_forever()

        self.__pool = AsyncPool(common_config.pool_size)
        self.__loop_thread = threading.Thread(target=run_loop, daemon=False)
        self.__loop_thread.start()

        ready.wait()

    def stop(self):
        """
        Stop all scrapers, close the AsyncPool, and terminate the event loop.

        Raises:
            RuntimeError: If the MultiRunner was not started.
        """

        if not self.is_started:
            raise RuntimeError("Multirainer was not started.")

        self.stop_scrapers()
        while not all((i.is_stopped for i in self.__scrapers.values())):
            time.sleep(0.05)
        self.__close_async_loop()

        self.__factory = None
        self.__scrapers = {}
        self.__pool = None
        self.__running_loop = None
        self.__loop_thread = None

    def __close_async_loop(self):
        """
        Internal method to stop the AsyncPool and close the asyncio loop safely.
        """

        # close pool
        async def f(r: threading.Event):
            await self.__pool.stop()
            r.set()

        ready = threading.Event()
        self.__running_loop.create_task(f(ready))
        ready.wait()

        # close async loop
        self.__running_loop.call_soon_threadsafe(self.__running_loop.stop)
        while self.__running_loop.is_running():
            time.sleep(0.05)
        self.__running_loop.close()

    def register(self, scrapers: Iterable[type[IAsyncScraper]]):
        """
        Register scraper classes to be used by the MultiRunner.

        Args:
            scrapers: Iterable of IAsyncScraper subclasses.
        """
        self.__factory = ScraperFactory(scrapers)

    def run_scrapers(self, scrapers: Iterable[str] | None = None):
        """
        Launch scrapers asynchronously using the AsyncPool.

        Args:
            scrapers: Optional list of scraper names to run. If None, all configured scrapers are run.

        Raises:
            RuntimeError: If the MultiRunner is not started.
        """

        if not self.is_started:
            raise RuntimeError("Multirainer was not started.")

        if scrapers is None:
            scrapers = (k for k in scrappers_configs.keys())

        async def run_scrapers():
            for k in scrapers:
                scraper = self.__scrapers.get(k, None)

                if scraper and not scraper.is_stopped:
                    logger.info(f"The scraper {k} has already been launched.")
                    continue

                if scraper and scraper.is_stopped:
                    logger.warning(f"The scraper {k} restarted.")
                self.__scrapers[k] = self.__factory(scrappers_configs[k])
                await self.__pool.submit(self.__scrapers[k].async_start())

        self.__running_loop.create_task(run_scrapers())

    def stop_scrapers(self, scrapers: Iterable[str] | None = None):
        """
        Stop running scrapers asynchronously.

        Args:
            scrapers: Optional list of scraper names to stop. If None, stops all running scrapers.

        Raises:
            RuntimeError: If the MultiRunner is not started.
        """

        if not self.is_started:
            raise RuntimeError("Multirainer was not started.")

        if scrapers is None:
            scrapers = (k for k, v in self.__scrapers.items() if not v.is_stopped)

        async def stop_scrapers():
            await asyncio.gather(
                *[self.__scrapers[k].async_stop() for k in scrapers],
            )

        self.__running_loop.create_task(stop_scrapers())
