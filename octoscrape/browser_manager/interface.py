from abc import ABC, abstractmethod
from playwright.async_api import Browser
from contextlib import asynccontextmanager


class IBrowserManager(ABC):
    '''Interface for singeltone browser'''

    @property
    @abstractmethod
    def browser(self) -> Browser:
        '''
        Returns the browser if there is one, 
        otherwise throws an error
        '''

    
    @property
    @abstractmethod
    def initialized(self) -> bool:
        '''
        Returns true if the browser is created 
        otherwise return false
        '''


    @abstractmethod
    @asynccontextmanager
    async def create_browser(self):
        '''Creates a single browser for the manager'''