import pytest
from octoscrape.config import ScraperConfig


def test_comparsion_equal():
    dict1 = {
        "human_name":   "Like a human 1",
        "name":         "name1",
        "url":          "url1"
    }

    dict2 = {
        "human_name":   "Like a human 1",
        "name":         "name1",
        "url":          "url1"
    }

    assert ScraperConfig(dict1) == ScraperConfig(dict2)


def test_comparsion_not_equal():
    dict1 = {
        "human_name":   "Like a human 1",
        "name":         "name1",
        "url":          "url1"
    }

    dict2 = {
        "human_name":   "Like a human 1",
        "name":         "name2",
        "url":          "url1"
    }

    assert ScraperConfig(dict1) != ScraperConfig(dict2)


def test_default_human_name(default_scraper_config):
    assert default_scraper_config.HumanName == ""


def test_default_key(default_scraper_config):
    assert default_scraper_config.Key == ""


def test_default_name(default_scraper_config):
    with pytest.raises(AttributeError):
        default_scraper_config.Name


def test_default_url(default_scraper_config):
    with pytest.raises(AttributeError):
        default_scraper_config.Url


def test_default_label(default_scraper_config):
    with pytest.raises(AttributeError):
        default_scraper_config.Scraper


def test_default_pool_size(default_scraper_config):
    assert default_scraper_config.PoolSize == 1


def test_default_proxy_availible(default_scraper_config):
    assert default_scraper_config.IsProxyAvailable == False


def test_default_proxy(default_scraper_config):
    assert default_scraper_config.Proxy is None


def test_required_name(
        only_required_fields_scraper_config, 
        only_required_fields_scraper_dict):
        assert only_required_fields_scraper_config.Name == only_required_fields_scraper_dict["name"]


def test_required_url(
        only_required_fields_scraper_config, 
        only_required_fields_scraper_dict):
        assert only_required_fields_scraper_config.Url == only_required_fields_scraper_dict["url"]


def test_required_scraper(
        only_required_fields_scraper_config, 
        only_required_fields_scraper_dict):
        assert only_required_fields_scraper_config.Scraper == only_required_fields_scraper_dict["name"]


def test_human_name(scraper_config, scraper_dict):
    assert scraper_config.HumanName == scraper_dict["human_name"]


def test_human_key(scraper_config):
    assert scraper_config.Key == "ScraperKey"


def test_name(scraper_config, scraper_dict):
    assert scraper_config.Name == scraper_dict["name"]


def test_url(scraper_config, scraper_dict):
    assert scraper_config.Url == scraper_dict["url"]


def test_scraper(scraper_config, scraper_dict):
    assert scraper_config.Scraper == scraper_dict["label"]


def test_pool_size(scraper_config, scraper_dict):
    assert scraper_config.PoolSize == scraper_dict["pool_size"]


def test_is_proxy_availible(scraper_config):
    assert scraper_config.IsProxyAvailable == True


def test_proxy(scraper_config, scraper_dict):
    assert scraper_config.Proxy == scraper_dict["proxy"]


def test_is_proxy_availible_str(scraper_config_proxy_str):
    assert scraper_config_proxy_str.IsProxyAvailable == True


def test_proxy_str(scraper_config_proxy_str, scraper_dict):
    assert scraper_config_proxy_str.Proxy == scraper_dict["proxy"]