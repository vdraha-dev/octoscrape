import pytest


@pytest.mark.asyncio
async def test_creation_of_two_browsers(browser_manager):
    with pytest.raises(
        RuntimeError,
        match="The browser already exists"
    ):
        async with browser_manager.create_browser():
            async with browser_manager.create_browser():...


@pytest.mark.asyncio
async def test_unique_browser(browser_manager):
    async with browser_manager.create_browser():
        br1 = browser_manager.get_browser()
        br2 = browser_manager.get_browser()
        assert br1 is br2


@pytest.mark.asyncio
async def test_uninitialized_browser(browser_manager):
    with pytest.raises(
        RuntimeError,
        match="browser has not been created yet"
    ):
        browser_manager.get_browser()


@pytest.mark.asyncio
async def test_context_homogeneity(browser_manager):
    def get_state(mngr):
        cls_n = browser_manager.__class__.__name__
        instance = getattr(browser_manager, f"_{cls_n}__instance")
        browser = getattr(instance, f"_{cls_n}__browser")
        initialized = getattr(instance, f"_{cls_n}__initialized")
        return browser, initialized

    assert (None, False) == get_state(browser_manager)

    async with browser_manager.create_browser():
        assert browser_manager.get_browser() is not None
        assert (browser_manager.get_browser(), True) == get_state(browser_manager)
    
    assert (None, False) == get_state(browser_manager)    
