from abc import abstractmethod
from playwright.async_api import Browser
from contextlib import asynccontextmanager


class IBrowserManager:
    '''Interface for singeltone browser'''

    @abstractmethod
    def get_browser(self) -> Browser:
        '''
        Returns the browser if there is one, 
        otherwise throws an error
        '''


    @abstractmethod
    @asynccontextmanager
    async def create_browser(self):
        '''Creates a single browser for the manager'''