from multiprocessing import Process, Semaphore
from multiprocessing.managers import BaseManager
from multiprocessing.synchronize import Event

from .IScraper import IScraper


class MultiRunner:
    def __init__(self, manager: BaseManager, pool_size):
        self.__manager = manager
        self.__processes = list[Process]
        self.__sem = Semaphore(pool_size)
        self.__stop_event:Event = Event()
    

    def run_process(self, parser:str, *args, **kwargs):
        worker:IScraper = self.__manager.Worker(parser, *args, **kwargs)

        def wrapped_start():
            with self.__sem:
                worker.set_stop_event(self.__stop_event)
                worker.start()

        p = Process(target=wrapped_start)
        p.start()
        self.__processes.append(p)


    def run_processes(self, arg_list):
        for a in arg_list:
            self.run_process(a)


    def stop(self):
        self.__stop_event.set()


    def join(self):
        for p in self.__processes:
            p.join()