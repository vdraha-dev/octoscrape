import asyncio
from examples.q2s import Q2S
from octoscrape.config import scrappers_configs

sc = Q2S(scrappers_configs["Q2S"])


if __name__ == "__main__":
    asyncio.run(sc.async_start())