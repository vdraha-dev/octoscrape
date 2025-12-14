import json

_attribute_error = (
    "Attribute '{attribute}' is not available: "
    "key '{attribute_key}' is missing in the configuration."
)


class ScraperConfig:
    """Config for a specific scraper."""

    def __init__(self, config: dict, key: str = ""):
        self.__config = config
        self.__key = key

    @property
    def key(self) -> str:
        """Returns the scraper sconfig key if available."""
        return self.__key

    @property
    def scraper(self) -> str:
        """Uses as key for the scraper factory.

        Raises:
            AttributeError: if the 'scraper' key is missing from the config.

        """
        try:
            return self.__config["scraper"]
        except KeyError:
            raise AttributeError(
                _attribute_error.format(attribute="scraper", attribute_key="scraper")
            )

    @property
    def human_name(self) -> str:
        """Name intended for a person"""
        return self.__config.get("human_name", "")

    @property
    def name(self) -> str:
        """Name for work processes, such as creating the resulting file.

        Raises:
            AttributeError: if the 'name' key is missing from the config .

        """
        try:
            return self.__config["name"]
        except KeyError:
            raise AttributeError(
                _attribute_error.format(attribute="name", attribute_key="name")
            )

    @property
    def url(self) -> str:
        """Starting page.

        Raises:
            AttributeError: if the 'url' key is missing from the config .

        """
        try:
            return self.__config["url"]
        except KeyError:
            raise AttributeError(
                _attribute_error.format(attribute="url", attribute_key="url")
            )

    @property
    def is_proxy_available(self) -> bool:
        """Indicates whether proxy settings are available."""

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
    def proxy(self) -> dict[str, str]:
        """If proxy is available, return proxy configuration.
        Otherwise return None.
        """
        if self.is_proxy_available:
            proxy = self.__config.get("proxy", {})
            if isinstance(proxy, dict):
                return proxy
            return json.loads(proxy)
        return None

    @property
    def pool_size(self) -> int:
        """Sets the number of coroutines that can be executed simultaneously.

        Only if the browser is asynchronous.
        """
        return self.__config.get("pool_size", 1)

    def __eq__(self, other):
        if self.__config is other.__config:
            return True

        props = (
            name
            for name, attr in self.__class__.__dict__.items()
            if isinstance(attr, property) and not name == "key"
        )
        return all(getattr(self, name) == getattr(other, name) for name in props)
