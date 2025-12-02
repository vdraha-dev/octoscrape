import yaml
from .config import (
    CommonConfig, 
    ScraperConfig, 
    MultiScraperConfig
)


with open("config.yaml", "r", encoding="utf-8") as f:
    raw_config = yaml.safe_load(f)

common_config = CommonConfig(raw_config["common"])

scrappers_configs: dict[str, ScraperConfig |  MultiScraperConfig] = {
    key : MultiScraperConfig(value, key) if value.get("is_multiscraper", False) 
    else ScraperConfig(value, key)
    for key, value in raw_config["process"].items()
}