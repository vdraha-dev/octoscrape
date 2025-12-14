import cmd
from .scraper import MultiRunner
import logging

logger = logging.getLogger(__name__)


class Shell(cmd.Cmd):
    prompt = "> "

    def __init__(self):
        super().__init__()
        self.runner : MultiRunner | None = None

    def do_start(self, arg):
        """
        Starts a scraper or a group of scrapers.

        Args:
            if no arguments are passed, all scrapers will start.

                Example: 
                    > start 

            if a list of keys is transferred, only the transferred scrapers will start

                Example:
                    > start Scraper1 Scraper2

        """

        self._create_scraper_if_no_exist()
        self.runner.start(self._process_arg_for_multirunner(arg))
        

    def do_stop(self, arg):
        """
        Stops a scraper or a group of scrapers.

        Args:
            if no arguments are passed, all scrapers will stopped.

                Example: 
                    > stop 

            if a list of keys is transferred, only the transferred scrapers will stopped

                Example:
                    > stop Scraper1 Scraper2

        """
    
        self.runner.stop(self._process_arg_for_multirunner(arg))

    def do_exit(self, arg):
        """Closes the shell and all scrapers"""
        self._stop_all()

        return True

    def _stop_all(self):
        if self.runner and self.runner.is_started:
            self.runner.stop()

    
    def _create_scraper_if_no_exist(self):
        if not self.runner:
            self.runner = MultiRunner()

        if not self.runner.is_started:
            self.runner.start()

    def _process_arg_for_multirunner(self, arg:str) -> list[str] | None:
        """
        Processes input arguments so that they can be passed to multirunner
        """
        if arg:
            return arg.split()
        return None

