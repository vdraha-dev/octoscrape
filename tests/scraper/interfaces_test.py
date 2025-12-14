import pytest


#############
# AsyncTest #
#############


def test_async_init(async_scraper, scraper_config):
    assert async_scraper._config == scraper_config
    assert async_scraper._config is scraper_config
    assert async_scraper._is_stopped is True


def test_async_full_name(async_scraper, scraper_config_dict):
    assert (
        async_scraper.full_name
        == f"ScraperKey.{scraper_config_dict['name']} | {scraper_config_dict['human_name']}"
    )


def test_async_full_name_without_key(
    create_fresh_scraper_config, create_fresh_async_scraper, fresh_scraper_config_dict
):
    scraper = create_fresh_async_scraper(
        create_fresh_scraper_config(fresh_scraper_config_dict)
    )
    assert (
        scraper.full_name
        == f"{fresh_scraper_config_dict['name']} | {fresh_scraper_config_dict['human_name']}"
    )


def test_async_full_name_without_human_name(
    create_fresh_scraper_config, create_fresh_async_scraper, fresh_scraper_config_dict
):
    del fresh_scraper_config_dict["human_name"]
    scraper = create_fresh_async_scraper(
        create_fresh_scraper_config(fresh_scraper_config_dict, "ScraperKey")
    )
    assert scraper.full_name == f"ScraperKey.{fresh_scraper_config_dict['name']}"


def test_async_full_name_without_key_and_human_name(
    create_fresh_scraper_config, create_fresh_async_scraper, fresh_scraper_config_dict
):
    del fresh_scraper_config_dict["human_name"]
    scraper = create_fresh_async_scraper(
        create_fresh_scraper_config(fresh_scraper_config_dict)
    )
    assert scraper.full_name == f"{fresh_scraper_config_dict['name']}"


@pytest.mark.asyncio
async def test_async_start(async_scraper):
    await async_scraper.async_start()


@pytest.mark.asyncio
async def test_async_stop(async_scraper):
    await async_scraper.async_stop()

