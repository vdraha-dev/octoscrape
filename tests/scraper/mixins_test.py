import pytest
from octoscrape.config import common_config

############################
# MixinContextCreator Test #
############################


@pytest.mark.asyncio
async def test_create_context(browser_manager, context_creator_scraper):
    async with browser_manager.create_browser():
        browser = browser_manager.browser
        context1 = await context_creator_scraper._new_context(browser)
        context2 = await context_creator_scraper._new_context(browser)

        assert context1 is not None
        assert context2 is not None
        assert context1 is not context2


@pytest.mark.asyncio
async def test_config_read(browser_manager, context_creator_scraper):
    async with browser_manager.create_browser():
        browser = browser_manager.browser
        context = await context_creator_scraper._new_context(
            browser
        )
        page = await context.new_page()
        size = page.viewport_size
        assert size["width"] == common_config.max_window_width
        assert size["height"] == common_config.max_window_height
