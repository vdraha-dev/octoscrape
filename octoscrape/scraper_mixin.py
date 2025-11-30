from camoufox import AsyncCamoufox
from browserforge.fingerprints import Screen
from playwright.async_api import async_playwright 
from contextlib import asynccontextmanager
import asyncio


class MixinAsyncCamoufox:
    @asynccontextmanager
    async def get_async_camoufox_browser(self):
        """
            Custom async context for running AsyncCamoufox
            with all settings (headless, screen, proxy).
        """
        async with AsyncCamoufox(
            headless=self._config.Headless,
            os=["windows"],
            screen=Screen(
                max_width=self._common_config.MaxWindowWidth,
                max_height=self._common_config.MaxWindowHeight
            ),
            geoip=self._config.IsProxyAvailable,
            proxy=( 
                self._config.Proxy 
                if self._config.IsProxyAvailable else None
            )
        ) as browser:
            yield browser



class MixinAsyncPlaywright:
    @asynccontextmanager
    async def get_async_playwright_browser(self):
        """
            Custom async context for running Playwright
            with all settings (headless, screen, proxy).
        """
        async with async_playwright() as p:
            browser = await p.firefox.launch(
                headless=self._config.Headless,
                args=[
                    f"--width={self._common_config.MaxWindowWidth}",
                    f"--height={self._common_config.MaxWindowHeight}",
                ],
                proxy=( 
                    self._config.Proxy 
                    if self._config.IsProxyAvailable else None
                )
            )
            yield browser



class MixinSync:
    def start(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            return asyncio.run_coroutine_threadsafe(self.async_start(), loop).result()
        else:
            asyncio.run(self.async_start())


    def stop(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            return asyncio.run_coroutine_threadsafe(self.async_stop(), loop).result()
        else:
            asyncio.run(self.async_stop())