from playwright.async_api import Browser, BrowserContext

from ..config import common_config


class MixinContextCreator:
    async def _new_context(self, browser: Browser) -> BrowserContext:
        """Create async bowser context."""

        return await browser.new_context(
            viewport={
                "width": common_config.max_window_width,
                "height": common_config.max_window_height,
            },
            proxy=self._config.proxy if self._config.is_proxy_available else None,
        )
