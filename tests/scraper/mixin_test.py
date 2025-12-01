import pytest

####################
# Playwright Tests #
####################

@pytest.mark.asyncio
async def test_minxin_playwright_browser_viewport(mixin_playwright):
    async with mixin_playwright.get_async_playwright_browser() as browser:
        page = await browser.new_page()
        size = page.viewport_size
        assert size["width"] == 1280
        assert size["height"] == 720


@pytest.mark.asyncio
async def test_minxin_playwright_context_viewport(mixin_playwright, common_config_dict):
    async with mixin_playwright.get_async_playwright_browser() as browser:
        context = await mixin_playwright.new_context(browser)
        page = await context.new_page()
        size = page.viewport_size
        assert size["width"] == common_config_dict["max_width"]
        assert size["height"] == common_config_dict["max_height"]
        

##################
# Camoufox Tests #
##################

@pytest.mark.asyncio
async def test_minxin_camoufox_browser_viewport(mixin_camoufox):
    async with mixin_camoufox.get_async_camoufox_browser() as browser:
        page = await browser.new_page()
        size = page.viewport_size
        assert size["width"] == 1280
        assert size["height"] == 720


@pytest.mark.asyncio
async def test_minxin_camoufox_context_viewport(mixin_camoufox, common_config_dict):
    async with mixin_camoufox.get_async_camoufox_browser() as browser:
        context = await mixin_camoufox.new_context(browser)
        page = await context.new_page()
        size = page.viewport_size
        assert size["width"] == common_config_dict["max_width"]
        assert size["height"] == common_config_dict["max_height"]