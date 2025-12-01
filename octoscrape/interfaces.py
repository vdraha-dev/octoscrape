from abc import ABC, abstractmethod
from multiprocessing.synchronize import Event
from .config import CommonConfig, ScraperConfig, MultiScraperConfig
from .mixins import MixinSync

class IAsyncScraper(ABC):
    def __init__(self, config: ScraperConfig | MultiScraperConfig, common_config: CommonConfig):
        self._config = config
        self._common_config = common_config
        self.__stop_event: Event | None = None


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
    

    def set_stop_event(self, event: Event):
        self.__stop_event = event
    

    @abstractmethod
    async def async_start(self):...


    @abstractmethod
    async def async_stop(self):...


class IScraper(IAsyncScraper, MixinSync):...