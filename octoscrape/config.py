from pathlib import Path
import json


class CommonConfig:
    '''
        General configuration for all streams 
    '''

    def __init__(self, config: dict):
        self.__config = config

    @property
    def PathToCsvDir(self) -> Path:
        '''
            Path to the folder where the results will be stored
        '''
        return Path(self.__config.get("path_to_csv", "."))

    @property
    def MaxWindowWidth(self) -> int:
        '''
            Browser window width
        '''
        return self.__config.get("max_width", 1920)

    @property
    def MaxWindowHeight(self) -> int:
        '''
            Browser window height
        '''
        return self.__config.get("max_height", 1080)
    
    @property
    def PoolSize(self) -> int:
        '''
            Number of processes that can be run simultaneously
        '''
        return self.__config.get("pool_size", 1)



class ScraperConfig:
    '''
        Config for a specific scraper
    '''

    def __init__(self, config: dict, key:str = ""):
        self.__config = config
        self.__key = key

    @property
    def Key(self) -> str:
        '''
            Returns the scraper sconfig key if available
        '''
        return self.__key
    
    @property
    def Scraper(self) -> str:
        '''
            Needed as a key for the scraper factory
        '''
        try:
            return self.__config.get("label", self.Name)
        except KeyError:
            raise AttributeError("Attribute 'Scraper' is not available: optional key " \
            "'label' is missing and required key 'name' is not present in the configuration.")

    @property
    def HumanName(self) -> str:
        '''
            Name intended for a person
        '''
        return self.__config.get("human_name", "")

    
    @property
    def Name(self) -> str:
        '''
            Name for work processes, such as creating the resulting file    
        '''
        try:
            return self.__config["name"]
        except KeyError:
            raise AttributeError("Attribute 'Name' is not available: " \
            "key 'name' is missing in the configuration.")
    
    @property
    def Url(self) -> str:
        '''
            Starting page
        '''
        try:
            return self.__config["url"]
        except KeyError:
            raise AttributeError("Attribute 'Url' is not available: " \
            "key 'url' is missing in the configuration.")
    
    @property
    def Headless(self) -> bool:
        '''
            Launching the browser in headless mode
        '''
        return  self.__config.get("headless", False)
    
    @property
    def IsProxyAvailable(self) -> bool:
        '''
            Indicates whether proxy settings are available
        '''
        def is_json_dict(s: str | dict) -> bool:
            if isinstance(s, dict):
                return True
            try:
                obj = json.loads(s)
                return isinstance(obj, dict)
            except (json.JSONDecodeError, TypeError):
                return False

        proxy = self.__config.get("proxy", None)
        if proxy is None or not is_json_dict(proxy):
            return False
        
        return True
    
    @property
    def Proxy(self) -> dict[str, str]:
        '''
            If proxy is available, return proxy configuration
            
            Otherwise return None
        '''
        if self.IsProxyAvailable:
            proxy = self.__config.get("proxy", {})
            if isinstance(proxy, dict):
                return proxy
            return json.loads(proxy)
        return None 
    
    @property
    def PoolSize(self) -> int:
        '''  
            Sets the number of coroutines that can be executed simultaneously

            Only if the browser is asynchronous 
        '''
        return self.__config.get("pool_size", 1)
    

    def __eq__(self, other):
        if self.__config is other.__config:
            return True

        props = (name for name, attr in self.__class__.__dict__.items() 
                 if isinstance(attr, property) and not name == "Key")
        return all(getattr(self, name) == getattr(other, name) for name in props)


class MultiScraperConfig:
    def __init__(self, config: dict, key:str = ""):
        self.__key = key
        self.__config = config
        self.__inner_dict: dict[str, ScraperConfig] = {}

        for key_, value in self.__config.get("scrapers", {}).items():
            self.__inner_dict[key_] = ScraperConfig(value, key_)

    @property
    def Key(self) -> str:
        '''
            Returns the scraper sconfig key if available
        '''
        return self.__key
    
    @property
    def Name(self) -> str:
        '''
            Name for work processes  
        '''
        try:
            return self.__config["name"]
        except KeyError:
            raise AttributeError("Attribute 'Name' is not available: " \
            "key 'name' is missing in the configuration.")
    
    @property
    def HumanName(self) -> str:
        '''
            Name intended for a person
        '''
        return self.__config.get("human_name", "") 
    
    @property
    def Scraper(self) -> str:
        '''
            Needed as a key for the scraper factory
        '''
        try:
            return self.__config.get("label", self.Name)
        except KeyError:
            raise AttributeError("Attribute 'Scraper' is not available: optional key " \
            "'label' is missing and required key 'name' is not present in the configuration.")
        
    
    @property
    def PoolSize(self) -> int:
        '''  
            Sets the number of scrapers that can be executed simultaneously

            Only if the browser is asynchronous 
        '''
        return self.__config.get("pool_size", 1)


    def __getitem__(self, key:str) -> ScraperConfig:
        return self.__inner_dict[key]


    def __setitem__(self, key:str, value: dict | ScraperConfig):
        if isinstance(value, dict):
            if len(value) > 1:
                self.__inner_dict[key] = ScraperConfig(value)
            else:
                for key_, value_ in value.items():
                    self.__inner_dict[key] = ScraperConfig(value_, key_)
        elif isinstance(value, ScraperConfig):
            self.__inner_dict[key] = value
        else:
            raise TypeError(f"Invalid type: {type(value)}")


    def __delitem__(self, key:str):
        del self.__inner_dict[key]

    
    def __contains__(self, key:str) -> bool:
        return key in self.__inner_dict
    

    def __eq__(self, other):
        if self.__config is other.__config:
            return True

        props = (name for name, attr in self.__class__.__dict__.items() 
                 if isinstance(attr, property) and not name == "Key")
        return all(getattr(self, name) == getattr(other, name) for name in props)
    

    def __len__(self):
        return len(self.__inner_dict)