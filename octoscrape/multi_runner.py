from multiprocessing import Process, Event, Semaphore
from typing import Callable, Any


class MultiRunner:
    def __init__(self, factory: Callable[..., Any], pool_size: int):
        self.__factory = factory
        self.__sem = Semaphore(pool_size)
        self.__stop_event = Event()
        self.__processes: list[Process] = []


    def __process_entry(self, worker_obj):
        with self.__sem:
            worker_obj.set_stop_event(self.__stop_event)
            worker_obj.start()


    def run_process(self, label: str, *args, **kwargs):
        if self.__stop_event.is_set():
            raise RuntimeError("Cannot run new process: MultiRunner is already stopped.")
        worker = self.__factory(label, *args, **kwargs)

        p = Process(target=self.__process_entry, args=(worker,))
        p.start()
        self.__processes.append(p)


    def stop_all(self):
        self.__stop_event.set()
        for p in self.__processes:
            p.join()

    
    @property
    def is_stopped(self) -> bool:
        return self.__stop_event.is_set()