from __future__ import annotations

from contextlib import asynccontextmanager

from playwright.async_api import Browser, async_playwright

from ..config import common_config
from .interface import IBrowserManager


class PlaywrightBrowserManager(IBrowserManager):
    """
    Singleton manager for Playwright browser lifecycle management.

    This class is responsible for:
    - ensuring only one browser instance exists at a time
    - managing browser creation and cleanup via async context manager
    - providing safe access to the active browser instance
    """

    __instance: PlaywrightBrowserManager | None = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__browser = None
        return cls.__instance

    @asynccontextmanager
    async def create_browser(self):
        if self.initialized:
            raise RuntimeError("The browser already exists")

        async with async_playwright() as p:
            self.__browser = await p.firefox.launch(
                headless=common_config.headless,
                args=[
                    f"--width={common_config.max_window_width}",
                    f"--height={common_config.max_window_height}",
                ],
            )
            try:
                yield
            finally:
                self.__browser = None

    @property
    def browser(self) -> Browser:
        if not self.initialized:
            raise RuntimeError("Playwriht browser has not been created yet.")
        return self.__browser

    @property
    def initialized(self) -> bool:
        return self.__browser is not None
