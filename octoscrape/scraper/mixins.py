import asyncio
from playwright.async_api import Browser
from ..config import common_config


class MixinContextCreator:
    async def _new_context(self, browser:Browser):
        """
            Create async bowser context.
        """
        context = await browser.new_context(
                viewport={
                    "width": common_config.MaxWindowWidth,
                    "height": common_config.MaxWindowHeight,
                },
                proxy= self._config.Proxy if self._config.IsProxyAvailable else None
            )
        return context



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
