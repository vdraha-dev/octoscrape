import pytest

from octoscrape.config import ScraperConfig


def test_comparsion_equal():
    dict1 = {
        "human_name": "Like a human 1",
        "name": "name1",
        "url": "url1",
        "scraper": "scr",
    }

    dict2 = {
        "human_name": "Like a human 1",
        "name": "name1",
        "url": "url1",
        "scraper": "scr",
    }

    assert ScraperConfig(dict1) == ScraperConfig(dict2)


def test_comparsion_not_equal():
    dict1 = {
        "human_name": "Like a human 1",
        "name": "name1",
        "url": "url1",
        "scraper": "scr",
    }

    dict2 = {
        "human_name": "Like a human 1",
        "name": "name2",
        "url": "url1",
        "scraper": "scr",
    }

    assert ScraperConfig(dict1) != ScraperConfig(dict2)


def test_default_human_name(default_scraper_config):
    assert default_scraper_config.human_name == ""


def test_default_key(default_scraper_config):
    assert default_scraper_config.key == ""


def test_default_name(default_scraper_config):
    with pytest.raises(AttributeError):
        default_scraper_config.name


def test_default_url(default_scraper_config):
    with pytest.raises(AttributeError):
        default_scraper_config.url


def test_default_label(default_scraper_config):
    with pytest.raises(AttributeError):
        default_scraper_config.scraper


def test_default_pool_size(default_scraper_config):
    assert default_scraper_config.pool_size == 1


def test_default_proxy_availible(default_scraper_config):
    assert default_scraper_config.is_proxy_available == False


def test_default_proxy(default_scraper_config):
    assert default_scraper_config.proxy is None


def test_required_name(
    only_required_fields_scraper_config, only_required_fields_scraper_dict
):
    assert (
        only_required_fields_scraper_config.name
        == only_required_fields_scraper_dict["name"]
    )


def test_required_url(
    only_required_fields_scraper_config, only_required_fields_scraper_dict
):
    assert (
        only_required_fields_scraper_config.url
        == only_required_fields_scraper_dict["url"]
    )


def test_human_name(scraper_config, scraper_config_dict):
    assert scraper_config.human_name == scraper_config_dict["human_name"]


def test_human_key(scraper_config):
    assert scraper_config.key == "ScraperKey"


def test_name(scraper_config, scraper_config_dict):
    assert scraper_config.name == scraper_config_dict["name"]


def test_url(scraper_config, scraper_config_dict):
    assert scraper_config.url == scraper_config_dict["url"]


def test_scraper(scraper_config, scraper_config_dict):
    assert scraper_config.scraper == scraper_config_dict["scraper"]


def test_pool_size(scraper_config, scraper_config_dict):
    assert scraper_config.pool_size == scraper_config_dict["pool_size"]


def test_is_proxy_availible(scraper_config):
    assert scraper_config.is_proxy_available == True


def test_proxy(scraper_config, scraper_config_dict):
    assert scraper_config.proxy == scraper_config_dict["proxy"]


def test_is_proxy_availible_str(scraper_config_proxy_str):
    assert scraper_config_proxy_str.is_proxy_available == True


def test_proxy_str(scraper_config_proxy_str, scraper_config_dict):
    assert scraper_config_proxy_str.proxy == scraper_config_dict["proxy"]
