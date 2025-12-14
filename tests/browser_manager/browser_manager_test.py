import pytest


@pytest.mark.asyncio
async def test_creation_of_two_browsers(browser_manager):
    with pytest.raises(RuntimeError, match="The browser already exists"):
        async with browser_manager.create_browser():
            async with browser_manager.create_browser():
                ...


@pytest.mark.asyncio
async def test_unique_browser(browser_manager):
    async with browser_manager.create_browser():
        br1 = browser_manager.browser
        br2 = browser_manager.browser
        assert br1 is not None
        assert br2 is not None
        assert br1 is br2


@pytest.mark.asyncio
async def test_uninitialized_browser(browser_manager):
    with pytest.raises(RuntimeError, match="browser has not been created yet"):
        browser_manager.browser


@pytest.mark.asyncio
async def test_browser_manager_context_lifecycle(browser_manager):
    def get_browser(mngr):
        cls_n = browser_manager.__class__.__name__
        instance = getattr(browser_manager, f"_{cls_n}__instance")
        browser = getattr(instance, f"_{cls_n}__browser")
        return browser

    assert (None, False) == (get_browser(browser_manager), browser_manager.initialized)

    async with browser_manager.create_browser():
        assert (browser_manager.browser, True) == (
            get_browser(browser_manager),
            browser_manager.initialized,
        )

    assert (None, False) == (get_browser(browser_manager), browser_manager.initialized)
