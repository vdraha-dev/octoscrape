import asyncio
import pytest
from octoscrape.concurrency import AsyncPool


@pytest.mark.asyncio
async def test_basic_execution():
    pool = AsyncPool(concurrency=2)
    await pool.start()

    results = []

    async def task(value):
        await asyncio.sleep(0.01)
        results.append(value)

    await pool.submit(task(1))
    await pool.submit(task(2))
    await pool.submit(task(3))

    await pool.drain()
    await pool.stop()

    assert sorted(results) == [1, 2, 3]


@pytest.mark.asyncio
async def test_concurrency_limit():
    pool = AsyncPool(concurrency=2)
    await pool.start()

    active_count = []
    current_active = 0
    lock = asyncio.Lock()

    async def task():
        nonlocal current_active
        async with lock:
            current_active += 1
            active_count.append(current_active)

        await asyncio.sleep(0.05)

        async with lock:
            current_active -= 1

    for _ in range(5):
        await pool.submit(task())

    await pool.drain()
    await pool.stop()

    assert max(active_count) <= 2


@pytest.mark.asyncio
async def test_stop_prevents_new_submissions():
    pool = AsyncPool(concurrency=2)
    await pool.start()
    await pool.stop()

    coro = asyncio.sleep(0.01)
    with pytest.raises(RuntimeError, match="Pool stopped"):
        await pool.submit(coro)
    coro.close()


@pytest.mark.asyncio
async def test_stop_cancels_active_tasks():
    pool = AsyncPool(concurrency=2)
    await pool.start()

    completed = []

    async def long_task(value):
        try:
            await asyncio.sleep(1)
            completed.append(value)
        except asyncio.CancelledError:
            completed.append(f"cancelled_{value}")
            raise

    await pool.submit(long_task(1))
    await pool.submit(long_task(2))

    await asyncio.sleep(0.01)
    await pool.stop()

    assert "cancelled_1" in completed or "cancelled_2" in completed


@pytest.mark.asyncio
async def test_drain_waits_for_completion():
    pool = AsyncPool(concurrency=2)
    await pool.start()

    completed = []

    async def task(value):
        await asyncio.sleep(0.02)
        completed.append(value)

    for i in range(5):
        await pool.submit(task(i))

    await pool.drain()

    assert len(completed) == 5
    await pool.stop()


@pytest.mark.asyncio
async def test_cancel_all_cancels_active():
    pool = AsyncPool(concurrency=2)
    await pool.start()

    cancelled = []
    completed = []

    async def task(value):
        try:
            await asyncio.sleep(0.5)
            completed.append(value)
        except asyncio.CancelledError:
            cancelled.append(value)
            raise

    await pool.submit(task(1))
    await pool.submit(task(2))

    await asyncio.sleep(0.01)
    await pool.cancel_all()
    await asyncio.sleep(0.02)

    assert len(cancelled) > 0
    assert len(completed) == 0

    await pool.stop()


@pytest.mark.asyncio
async def test_cancel_all_clears_queue():
    pool = AsyncPool(concurrency=1)
    await pool.start()

    executed = []

    async def task(value):
        await asyncio.sleep(0.05)
        executed.append(value)

    for i in range(10):
        await pool.submit(task(i))

    await asyncio.sleep(0.1)
    await pool.cancel_all()
    await asyncio.sleep(0.1)

    assert len(executed) <= 1

    await pool.stop()


@pytest.mark.asyncio
async def test_exception_handling():
    pool = AsyncPool(concurrency=2)
    await pool.start()

    results = []

    async def failing_task():
        await asyncio.sleep(0.01)
        raise ValueError("Test error")

    async def normal_task(value):
        await asyncio.sleep(0.01)
        results.append(value)

    await pool.submit(failing_task())
    await pool.submit(normal_task(1))
    await pool.submit(normal_task(2))

    await pool.drain()
    await pool.stop()

    assert sorted(results) == [1, 2]


@pytest.mark.asyncio
async def test_empty_pool_drain():
    pool = AsyncPool(concurrency=2)
    await pool.start()

    # .drain without tasks should not hang
    await asyncio.wait_for(pool.drain(), timeout=1.0)

    await pool.stop()


@pytest.mark.asyncio
async def test_multiple_drains():
    pool = AsyncPool(concurrency=2)
    await pool.start()

    results = []

    async def task(value):
        await asyncio.sleep(0.01)
        results.append(value)

    await pool.submit(task(1))
    await pool.drain()

    await pool.submit(task(2))
    await pool.drain()

    assert sorted(results) == [1, 2]

    await pool.stop()


@pytest.mark.asyncio
async def test_high_load():
    pool = AsyncPool(concurrency=10)
    await pool.start()

    counter = []

    async def task(value):
        await asyncio.sleep(0.001)
        counter.append(value)

    for i in range(100):
        await pool.submit(task(i))

    await pool.drain()
    await pool.stop()

    assert len(counter) == 100
    assert sorted(counter) == list(range(100))


@pytest.mark.asyncio
async def test_zero_concurrency():
    """Checking behavior with concurrency=0 (boundary case)."""
    pool = AsyncPool(concurrency=0)
    await pool.start()

    # With zero parallelism, tasks should not be executed.
    executed = []

    async def task():
        executed.append(1)

    await pool.submit(task())
    await asyncio.sleep(0.1)

    # The task should not be completed.
    assert len(executed) == 0

    await pool.stop()


@pytest.mark.asyncio
async def test_lifecycle():
    def get_state(p: AsyncPool):
        return (p._queue.qsize(), len(p._workers), len(p._active_tasks), p.is_stopped)

    pool = AsyncPool(concurrency=2)

    # state before start
    assert (0, 0, 0, True) == get_state(pool)

    await pool.start()
    results = []

    # state after start
    assert (0, 2, 0, False) == get_state(pool)

    async def task(value):
        await asyncio.sleep(0.02)
        results.append(value)

    await pool.submit(task(1))
    await pool.submit(task(2))
    await pool.submit(task(3))

    # state after adding tasks
    assert (3, 2, 0, False) == get_state(pool)

    await asyncio.sleep(0.01)

    # state after start of tasks execution
    assert (1, 2, 2, False) == get_state(pool)

    await pool.drain()

    # state after completing all tasks
    assert (0, 2, 0, False) == get_state(pool)

    await pool.stop()

    # state after stop
    assert (0, 0, 0, True) == get_state(pool)

    assert sorted(results) == [1, 2, 3]


@pytest.mark.asyncio
async def test_context_exception_handling():
    async with AsyncPool(concurrency=2) as pool:
        results = []

        async def failing_task():
            await asyncio.sleep(0.01)
            raise ValueError("Test error")

        async def normal_task(value):
            await asyncio.sleep(0.01)
            results.append(value)

        await pool.submit(failing_task())
        await pool.submit(normal_task(1))
        await pool.submit(normal_task(2))

    assert sorted(results) == [1, 2]


@pytest.mark.asyncio
async def test_context_lifecycle():
    def get_state(p: AsyncPool):
        return (p._queue.qsize(), len(p._workers), len(p._active_tasks), p.is_stopped)

    async with AsyncPool(concurrency=2) as pool:
        results = []

        # state after start
        assert (0, 2, 0, False) == get_state(pool)

        async def task(value):
            await asyncio.sleep(0.02)
            results.append(value)

        await pool.submit(task(1))
        await pool.submit(task(2))
        await pool.submit(task(3))

        # state after adding tasks
        assert (3, 2, 0, False) == get_state(pool)

        await asyncio.sleep(0.01)

        # state after start of tasks execution
        assert (1, 2, 2, False) == get_state(pool)

    # state after stop
    assert (0, 0, 0, True) == get_state(pool)
    assert sorted(results) == [1, 2, 3]
