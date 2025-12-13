from .camoufox import CamoufoxBrowserManager
from .interface import IBrowserManager
from .playwright import PlaywrightBrowserManager

camoufox_manager = CamoufoxBrowserManager()
playwright_manager = PlaywrightBrowserManager()


__all__ = [
    "IBrowserManager",
    "CamoufoxBrowserManager",
    "PlaywrightBrowserManager",
    "camoufox_manager",
    "playwright_manager"
]