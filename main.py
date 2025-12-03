from scrapers_examples.q2s import Q2S
from octoscrape.scraper_config import scrappers_configs
import asyncio

sc = Q2S(scrappers_configs["Q2S"])
    
    
if __name__ == "__main__":
    asyncio.run(sc.async_start())