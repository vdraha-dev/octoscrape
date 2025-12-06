import asyncio
from playwright.async_api import Browser, BrowserContext
from ..config import common_config, CommonConfig


class MixinContextCreator:
    async def _new_context(self, browser:Browser, *, config: CommonConfig | None = None) -> BrowserContext:
        """
            Create async bowser context.
        """
        if config is None:
            config = common_config
        return await browser.new_context(
                viewport={
                    "width": config.MaxWindowWidth,
                    "height": config.MaxWindowHeight,
                },
                proxy= self._config.Proxy if self._config.IsProxyAvailable else None
            )


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
