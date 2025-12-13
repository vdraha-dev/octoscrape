from __future__ import annotations

from contextlib import asynccontextmanager

from browserforge.fingerprints import Screen
from camoufox.async_api import AsyncCamoufox, Browser

from ..config import common_config
from .interface import IBrowserManager


class CamoufoxBrowserManager(IBrowserManager):
    """
    Singleton manager for Camoufox browser lifecycle management.

    This class is responsible for:
    - ensuring only one browser instance exists at a time
    - managing browser creation and cleanup via async context manager
    - providing safe access to the active browser instance
    """

    __instance: CamoufoxBrowserManager | None = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__browser = None
        return cls.__instance

    @asynccontextmanager
    async def create_browser(self):
        if self.initialized:
            raise RuntimeError("The browser already exists")

        async with AsyncCamoufox(
            headless=common_config.Headless,
            os=["windows", "linux", "macos"],
            screen=Screen(
                max_width=common_config.MaxWindowWidth,
                max_height=common_config.MaxWindowHeight,
            ),
        ) as browser:
            self.__browser = browser
            try:
                yield
            finally:
                self.__browser = None

    @property
    def browser(self) -> Browser:
        if not self.initialized:
            raise RuntimeError("Camoufox browser has not been created yet.")
        return self.__browser

    @property
    def initialized(self) -> bool:
        return self.__browser is not None
