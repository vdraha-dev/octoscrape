from pathlib import Path


class CommonConfig:
    """General configuration for all streams."""

    def __init__(self, config: dict):
        self.__config = config

    @property
    def path_to_csv_dir(self) -> Path:
        """Path to the folder where the results will be stored."""
        return Path(self.__config.get("path_to_csv", "."))

    @property
    def max_window_width(self) -> int:
        """Browser window width."""
        return self.__config.get("max_width", 1920)

    @property
    def max_window_height(self) -> int:
        """Browser window height."""
        return self.__config.get("max_height", 1080)

    @property
    def pool_size(self) -> int:
        """Number of processes that can be run simultaneously."""
        return self.__config.get("pool_size", 1)

    @property
    def headless(self) -> bool:
        """Launching the browser in headless mode."""
        return self.__config.get("headless", False)
