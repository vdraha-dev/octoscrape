from playwright.async_api import Browser, BrowserContext
from ..config import common_config


class MixinContextCreator:
    async def _new_context(self, browser:Browser) -> BrowserContext:
        """
            Create async bowser context.
        """
        return await browser.new_context(
                viewport={
                    "width": common_config.MaxWindowWidth,
                    "height": common_config.MaxWindowHeight,
                },
                proxy= self._config.Proxy if self._config.IsProxyAvailable else None
            )
