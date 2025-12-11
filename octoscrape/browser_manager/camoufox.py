from __future__ import annotations
from camoufox.async_api import AsyncCamoufox, Browser
from browserforge.fingerprints import Screen
from .interface import IBrowserManager
from ..config import common_config
from contextlib import asynccontextmanager


class CamoufoxBrowserManager(IBrowserManager):
    """Singleton manager for browser management"""
    __instance: CamoufoxBrowserManager | None = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__browser = None
            cls.__instance.__initialized = False
        return cls.__instance
    

    @asynccontextmanager
    async def create_browser(self):
        if self.__initialized:
            raise RuntimeError("The browser already exists")
        
        async with AsyncCamoufox(
            headless=common_config.Headless,
            os=["windows", "linux", "macos"],
            screen=Screen(
                max_width=common_config.MaxWindowWidth,
                max_height=common_config.MaxWindowHeight
            )
        ) as browser:
            self.__browser = browser
            self.__initialized = True
            try:
                yield
            finally:
                self.__browser = None
                self.__initialized = False
    

    @property
    def browser(self) -> Browser:
        if not self.__initialized:
            raise RuntimeError("Camoufox browser has not been created yet.")
        return self.__browser


    @property
    def initialized(self) -> bool:
        return self.__initialized