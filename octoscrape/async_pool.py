import asyncio


class AsyncPool:
    def __init__(self, concurrency: int):
        self._sem = asyncio.Semaphore(concurrency)
        self._queue = asyncio.Queue()

        self._workers: list[asyncio.Task] = []
        self._active_tasks: set[asyncio.Task] = set()

        self._stopped = False


    async def start(self):
        """Launch workers (based on concurrency)."""
        for _ in range(self._sem._value):  # concurrency == initial semaphore value
            worker = asyncio.create_task(self._worker())
            self._workers.append(worker)


    async def stop(self):
        """Stop gracefully: no new tasks, cancel active ones."""
        self._stopped = True

        # cancel active tasks
        for task in self._active_tasks:
            task.cancel()

        # cancel worker tasks
        for w in self._workers:
            w.cancel()

        # wait workers termination
        await asyncio.gather(*self._workers, return_exceptions=True)


    async def submit(self, coro):
        """Submit a coroutine to execution. If stopped — ignore or raise."""
        if self._stopped:
            raise RuntimeError("Pool stopped: cannot submit new jobs.")

        await self._queue.put(coro)


    async def _worker(self):
        """Worker continuously pulls jobs from the queue."""
        try:
            while True:
                coro = await self._queue.get()

                async with self._sem:
                    task = asyncio.create_task(coro)
                    self._active_tasks.add(task)

                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
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
                self._queue.get_nowait()
                self._queue.task_done()
            except asyncio.QueueEmpty:
                break

        await asyncio.sleep(0)  # let cancellations propagate
