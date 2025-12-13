import yaml

from .common_config_acessor import CommonConfig
from .scraper_config_acessor import ScraperConfig

with open("config.yaml", "r", encoding="utf-8") as f:
    raw_config = yaml.safe_load(f)

common_config = CommonConfig(raw_config["common"])
scrappers_configs: dict[str, ScraperConfig] = {
    key: ScraperConfig(value, key) for key, value in raw_config["scrapers"].items()
}

__all__ = ["CommonConfig", "ScraperConfig", "common_config", "scrappers_configs"]
