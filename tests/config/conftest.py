import pytest
import copy
from octoscrape.config import (
    CommonConfig,
    ScraperConfig
)

###################################
# Fixtures for CommonConfig tests #
###################################

@pytest.fixture(scope="session")
def default_common_config() -> CommonConfig:
    return CommonConfig({})


@pytest.fixture(scope="session")
def common_config_dict() -> dict:
    return {
        "path_to_csv":  "some/path/to/csv",
        "max_width":    11111111,
        "max_height":   22222222,
        "pool_size":    33333333,
        "headless":     True
    }


@pytest.fixture(scope="session")
def common_config(common_config_dict) -> CommonConfig:
    return CommonConfig(common_config_dict)



####################################
# Fixtures for ScraperConfig tests #
####################################

@pytest.fixture(scope="session")
def default_scraper_config() -> ScraperConfig:
    return ScraperConfig({})


@pytest.fixture(scope="session")
def only_required_fields_scraper_dict():
    return {
        "human_name":   "required_human_like_name",
        "name":         "required_working_name",
        "url":          "required_start_page",
    }


@pytest.fixture(scope="session")
def only_required_fields_scraper_config(only_required_fields_scraper_dict) -> ScraperConfig:
    return ScraperConfig(only_required_fields_scraper_dict)


@pytest.fixture(scope="session")
def scraper_dict() -> dict:
    return {
        "human_name":   "human_like_name",
        "name":         "working_name",
        "url":          "start_page",
        "label":        "label",
        "pool_size":    1111111,
        "proxy": {
            "server":   "http://example.com:8080",
            "username": "user",
            "password": "pass"
        }
    }


@pytest.fixture(scope="session")
def scraper_config(scraper_dict) -> ScraperConfig:
    return ScraperConfig(scraper_dict, "ScraperKey")


@pytest.fixture(scope="session")
def scraper_config_proxy_str() -> ScraperConfig:
    return ScraperConfig({
        "proxy":'{"server": "http://example.com:8080", "username": "user", "password": "pass"}'
    })
