import pytest


#############
# AsyncTest #
#############

def test_async_init(async_scraper, scraper_config):
    assert async_scraper._config == scraper_config
    assert async_scraper._config is scraper_config
    assert async_scraper._stop_event is None


def test_async_full_name(async_scraper, scraper_config_dict):
    assert async_scraper.FullName == f"ScraperKey.{scraper_config_dict['name']} | {scraper_config_dict['human_name']}"


def test_async_full_name_without_key(
        create_fresh_scraper_config,
        create_fresh_async_scraper, 
        fresh_scraper_config_dict):
    scraper = create_fresh_async_scraper(create_fresh_scraper_config(fresh_scraper_config_dict))
    assert scraper.FullName == f"{fresh_scraper_config_dict['name']} | {fresh_scraper_config_dict['human_name']}"


def test_async_full_name_without_human_name(
        create_fresh_scraper_config,
        create_fresh_async_scraper, 
        fresh_scraper_config_dict):
    del fresh_scraper_config_dict["human_name"]
    scraper = create_fresh_async_scraper(create_fresh_scraper_config(fresh_scraper_config_dict, "ScraperKey"))
    assert scraper.FullName == f"ScraperKey.{fresh_scraper_config_dict['name']}"


def test_async_full_name_without_key_and_human_name(
        create_fresh_scraper_config,
        create_fresh_async_scraper, 
        fresh_scraper_config_dict):
    del fresh_scraper_config_dict["human_name"]
    scraper = create_fresh_async_scraper(create_fresh_scraper_config(fresh_scraper_config_dict))
    assert scraper.FullName == f"{fresh_scraper_config_dict['name']}"


@pytest.mark.asyncio
async def test_async_start(async_scraper):
    await async_scraper.async_start()


@pytest.mark.asyncio
async def test_async_stop(async_scraper):
    await async_scraper.async_stop()


def test_async_full_name_without_key_and_human_name(
        create_fresh_scraper_config,
        create_fresh_async_scraper, 
        fresh_scraper_config_dict):
    scraper = create_fresh_async_scraper(create_fresh_scraper_config(fresh_scraper_config_dict))

    assert scraper._stop_event is None
    event = object()
    scraper.set_stop_event(event)
    assert scraper._stop_event is event

    
############
# SyncTest #
############

def test_init(sync_scraper, scraper_config):
    assert sync_scraper._config == scraper_config
    assert sync_scraper._config is scraper_config
    assert sync_scraper._stop_event is None


def test_full_name(sync_scraper, scraper_config_dict):
    assert sync_scraper.FullName == f"ScraperKey.{scraper_config_dict['name']} | {scraper_config_dict['human_name']}"


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