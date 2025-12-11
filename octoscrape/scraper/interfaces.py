from abc import ABC, abstractmethod
from ..config import ScraperConfig


class IAsyncScraper(ABC):
    def __init__(self, config: ScraperConfig):
        self._config: ScraperConfig = config
        self._is_stopped: bool = True

    @property
    def Name(self):
        return self._config.Name
    
    @property
    def HumanName(self):
        return self._config.HumanName
    
    @property
    def FullName(self):
        key = self._config.Key
        if len(key) > 0:
            key += "."

        human_name = self._config.HumanName
        if len(human_name) > 0:
            human_name = f" | {human_name}"

        return f"{key}{self._config.Name}{human_name}"

    @property
    def is_stopped(self) -> bool:
        return self._is_stopped
    

    @abstractmethod
    async def async_start(self):...


    @abstractmethod
    async def async_stop(self):...
