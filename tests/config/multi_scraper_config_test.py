import pytest
from octoscrape.config import ScraperConfig

def test_default_name(default_multi_scraper_config):
    with pytest.raises(AttributeError):
        default_multi_scraper_config.Name


def test_default_human_name(default_multi_scraper_config):
    assert default_multi_scraper_config.HumanName == ""


def test_default_scraper(default_multi_scraper_config):
    with pytest.raises(AttributeError):
        default_multi_scraper_config.Scraper


def test_default_pool_size(default_multi_scraper_config):
    assert default_multi_scraper_config.PoolSize == 1


def test_default_len(default_multi_scraper_config):
    assert len(default_multi_scraper_config) == 2


def test_name(multi_scraper_config, multi_scraper_dict):
    assert multi_scraper_config.Name == multi_scraper_dict["name"]


def test_human_name(multi_scraper_config, multi_scraper_dict):
    assert multi_scraper_config.HumanName == multi_scraper_dict["human_name"]


def test_scraper(multi_scraper_config, multi_scraper_dict):
    assert multi_scraper_config.Scraper == multi_scraper_dict["label"]


def test_pool_size(multi_scraper_config, multi_scraper_dict):
    assert multi_scraper_config.PoolSize == multi_scraper_dict["pool_size"]


def test_len(multi_scraper_config):
    assert len(multi_scraper_config) == 3


def test_get_item(multi_scraper_config):
    dict_ = {
        "human_name":   "Like a human 2",
        "name":         "name2",
        "url":          "url2"
    }

    assert multi_scraper_config["scr2"] == ScraperConfig(dict_)


def test_missing_item(multi_scraper_config):
    with pytest.raises(KeyError):
        multi_scraper_config["scr4"]


def test_set_item_scraper_config(fresh_multi_scraper_config, additional_scraper):
    fresh_multi_scraper_config["src4"] = ScraperConfig(additional_scraper)

    assert len(fresh_multi_scraper_config) == 4
    assert fresh_multi_scraper_config["src4"] == ScraperConfig(additional_scraper)


def test_set_item_dict(fresh_multi_scraper_config, additional_scraper):
    fresh_multi_scraper_config["src4"] = additional_scraper

    assert len(fresh_multi_scraper_config) == 4
    assert fresh_multi_scraper_config["src4"].Key == ""
    assert fresh_multi_scraper_config["src4"] == ScraperConfig(additional_scraper)


def test_set_item_dict_with_key(fresh_multi_scraper_config, additional_scraper):
    key = "keyqw"
    dict_ = {key: additional_scraper}
    fresh_multi_scraper_config["src4"] = dict_

    assert len(fresh_multi_scraper_config) == 4
    assert fresh_multi_scraper_config["src4"].Key == key
    assert fresh_multi_scraper_config["src4"] == ScraperConfig(additional_scraper)
