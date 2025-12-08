from __future__ import annotations
from playwright.async_api import async_playwright, Browser
from .interface import IBrowserManager
from ..config import CommonConfig, common_config
from contextlib import asynccontextmanager


class PlaywrightBrowserManager(IBrowserManager):
    '''Singleton manager for browser management'''
    __instance: PlaywrightBrowserManager | None = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__browser = None
            cls.__instance.__initialized = False
        return cls.__instance


    @asynccontextmanager
    async def create_browser(self, config: CommonConfig | None = None):
        if self.__initialized:
            raise RuntimeError("The browser already exists")

        config = config if config else common_config
        async with async_playwright() as p:
            self.__browser = await p.firefox.launch(
            headless=common_config.Headless,
                args=[
                    f"--width={config.MaxWindowWidth}",
                    f"--height={config.MaxWindowHeight}",
                ],
            )
            self.__initialized = True
            try:
                yield
            finally:
                self.__browser = None
                self.__initialized = False


    @property
    def browser(self) -> Browser:
        if not self.__initialized:
            raise RuntimeError("Playwriht browser has not been created yet.")
        return self.__browser
    

    @property
    def initialized(self) -> bool:
        return self.__initialized