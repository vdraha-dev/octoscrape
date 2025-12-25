from octoscrape.shell import Shell
from dummies.scrapers import DummiesScraper


if __name__ == "__main__":
    Shell([DummiesScraper]).cmdloop()