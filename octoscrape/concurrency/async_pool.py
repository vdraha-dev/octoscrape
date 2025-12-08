from __future__ import annotations
import asyncio
import logging as logger
from typing import Coroutine


class AsyncPool:
    def __init__(self, concurrency: int):
        self.__concurency = concurrency
        self._sem = asyncio.Semaphore(self.__concurency)
        self._queue: asyncio.Queue[Coroutine] = asyncio.Queue()

        self._workers: list[asyncio.Task] = []
        self._active_tasks: set[asyncio.Task] = set()

        self._stopped = True

    @property
    def is_stopped(self):
        return self._stopped


    async def __aenter__(self) -> AsyncPool:
        await self.start()
        return self


    async def __aexit__(self, exc_type, exc, tb):
        await self.drain()
        await self.stop()
        return False


    async def start(self):
        """Launch workers (based on concurrency)."""
        self._stopped = False
        for _ in range(self.__concurency):  # concurrency == initial semaphore value
            worker = asyncio.create_task(self._worker())
            self._workers.append(worker)


    async def stop(self):
        """Stop gracefully: no new tasks, cancel active ones."""
        self._stopped = True

        await self.cancel_all()

        # cancel worker tasks
        for w in self._workers:
            w.cancel()

        # wait workers termination
        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()


    async def submit(self, coro:Coroutine):
        """Submit a coroutine to execution. If stopped — ignore or raise."""
        if self._stopped:
            raise RuntimeError("Pool stopped: cannot submit new jobs.")
        await self._queue.put(coro)


    async def _worker(self):
        """Worker continuously pulls jobs from the queue."""
        try:
            while not self._stopped:
                try:
                    coro = await asyncio.wait_for(
                        self._queue.get(), 
                        timeout=0.1
                    )
                except asyncio.TimeoutError:
                    continue

                async with self._sem:
                    task = asyncio.create_task(coro)
                    self._active_tasks.add(task)

                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
                    except Exception:
                        print("Worker task raised an exception")
                        logger.error("Worker task raised an exception", exc_info=True)
                    finally:
                        self._active_tasks.discard(task)
                        self._queue.task_done()

        except asyncio.CancelledError:
            pass


    async def drain(self):
        """Wait until all queued tasks finish."""
        await self._queue.join()


    async def cancel_all(self):
        """Cancel all actively running tasks AND clear queue."""
        # cancel active
        for task in list(self._active_tasks):
            task.cancel()

        # remove queued jobs
        while not self._queue.empty():
            try:
                coro = self._queue.get_nowait()
                self._queue.task_done()
                coro.close()
            except asyncio.QueueEmpty:
                break
            except (RuntimeError, GeneratorExit) as e:
                logger.warning(f"Expected exception when closing coroutine: {e}")

        await asyncio.sleep(0)  # let cancellations propagate
