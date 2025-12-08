import pytest


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
async def test_config_read(browser_manager, context_creator_scraper, common_config):
    async with browser_manager.create_browser(common_config):
        browser = browser_manager.browser
        context = await context_creator_scraper._new_context(browser, config=common_config)
        page = await context.new_page()
        size = page.viewport_size
        assert size["width"] == common_config.MaxWindowWidth
        assert size["height"] == common_config.MaxWindowHeight



##################
# MixinSync Test #
##################

def test_start(sync_scraper, mocker):
    async_mock = mocker.AsyncMock()
    mocker.patch.object(sync_scraper, "async_start", async_mock)
    sync_scraper.start()
    async_mock.assert_awaited_once()


def test_stop(sync_scraper, mocker):
    async_mock = mocker.AsyncMock()
    mocker.patch.object(sync_scraper, "async_stop", async_mock)
    sync_scraper.stop()
    async_mock.assert_awaited_once()
