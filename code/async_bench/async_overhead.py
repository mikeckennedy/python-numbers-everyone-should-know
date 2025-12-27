"""
Async overhead benchmarks.

Measures:
- await already-completed coroutine
- Create coroutine object (no await)
- asyncio.sleep(0)
- asyncio.gather() on completed coroutines
- Task creation and scheduling
- async context managers
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.benchmark import (
    BenchmarkResult,
    collect_results,
    print_header,
    print_result,
    print_subheader,
    time_operation,
)

CATEGORY = "async_overhead"


# =============================================================================
# Test Coroutines and Classes
# =============================================================================


async def empty_coro():
    """Empty coroutine."""
    pass


async def return_value_coro():
    """Coroutine that returns a value."""
    return 42


async def already_complete():
    """Coroutine that's immediately ready."""
    return "done"


async def with_sleep_zero():
    """Coroutine with sleep(0)."""
    await asyncio.sleep(0)
    return "done"


async def nested_await():
    """Coroutine that awaits another coroutine."""
    result = await return_value_coro()
    return result


async def multiple_awaits():
    """Coroutine with multiple awaits."""
    a = await return_value_coro()
    b = await return_value_coro()
    c = await return_value_coro()
    return a + b + c


class AsyncContextManager:
    """Simple async context manager."""

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


class AsyncIterator:
    """Simple async iterator."""

    def __init__(self, n):
        self.n = n
        self.i = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.i >= self.n:
            raise StopAsyncIteration
        self.i += 1
        return self.i


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all async overhead benchmarks."""
    results = []

    print_header("Async Overhead Benchmarks")

    # Get or create event loop
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # -------------------------------------------------------------------------
    # Coroutine Creation
    # -------------------------------------------------------------------------
    print_subheader("Coroutine Creation")

    def create_coro():
        coro = empty_coro()
        coro.close()  # Must close to avoid warning

    time_ms = time_operation(create_coro, iterations=100000)
    results.append(BenchmarkResult("create coroutine object", time_ms, category=CATEGORY))
    print_result("create coroutine object", time_ms)

    def create_coro_with_return():
        coro = return_value_coro()
        coro.close()

    time_ms = time_operation(create_coro_with_return, iterations=100000)
    results.append(BenchmarkResult("create coroutine (with return)", time_ms, category=CATEGORY))
    print_result("create coroutine (with return)", time_ms)

    # -------------------------------------------------------------------------
    # Running Coroutines
    # -------------------------------------------------------------------------
    print_subheader("Running Coroutines")

    def run_empty():
        loop.run_until_complete(empty_coro())

    time_ms = time_operation(run_empty, iterations=10000)
    results.append(BenchmarkResult("run_until_complete(empty)", time_ms, category=CATEGORY))
    print_result("run_until_complete(empty)", time_ms)

    def run_with_return():
        loop.run_until_complete(return_value_coro())

    time_ms = time_operation(run_with_return, iterations=10000)
    results.append(BenchmarkResult("run_until_complete(return value)", time_ms, category=CATEGORY))
    print_result("run_until_complete(return value)", time_ms)

    def run_nested():
        loop.run_until_complete(nested_await())

    time_ms = time_operation(run_nested, iterations=10000)
    results.append(BenchmarkResult("run nested await", time_ms, category=CATEGORY))
    print_result("run nested await", time_ms)

    def run_multiple():
        loop.run_until_complete(multiple_awaits())

    time_ms = time_operation(run_multiple, iterations=10000)
    results.append(BenchmarkResult("run 3 sequential awaits", time_ms, category=CATEGORY))
    print_result("run 3 sequential awaits", time_ms)

    # -------------------------------------------------------------------------
    # asyncio.sleep()
    # -------------------------------------------------------------------------
    print_subheader("asyncio.sleep()")

    def run_sleep_zero():
        loop.run_until_complete(asyncio.sleep(0))

    time_ms = time_operation(run_sleep_zero, iterations=10000)
    results.append(BenchmarkResult("asyncio.sleep(0)", time_ms, category=CATEGORY))
    print_result("asyncio.sleep(0)", time_ms)

    def run_coro_with_sleep():
        loop.run_until_complete(with_sleep_zero())

    time_ms = time_operation(run_coro_with_sleep, iterations=10000)
    results.append(BenchmarkResult("coroutine with sleep(0)", time_ms, category=CATEGORY))
    print_result("coroutine with sleep(0)", time_ms)

    # -------------------------------------------------------------------------
    # asyncio.gather()
    # -------------------------------------------------------------------------
    print_subheader("asyncio.gather()")

    def run_gather_5():
        loop.run_until_complete(asyncio.gather(
            return_value_coro(),
            return_value_coro(),
            return_value_coro(),
            return_value_coro(),
            return_value_coro(),
        ))

    time_ms = time_operation(run_gather_5, iterations=5000)
    results.append(BenchmarkResult("gather() 5 coroutines", time_ms, category=CATEGORY))
    print_result("gather() 5 coroutines", time_ms)

    def run_gather_10():
        loop.run_until_complete(asyncio.gather(
            *[return_value_coro() for _ in range(10)]
        ))

    time_ms = time_operation(run_gather_10, iterations=5000)
    results.append(BenchmarkResult("gather() 10 coroutines", time_ms, category=CATEGORY))
    print_result("gather() 10 coroutines", time_ms)

    def run_gather_100():
        loop.run_until_complete(asyncio.gather(
            *[return_value_coro() for _ in range(100)]
        ))

    time_ms = time_operation(run_gather_100, iterations=1000)
    results.append(BenchmarkResult("gather() 100 coroutines", time_ms, category=CATEGORY))
    print_result("gather() 100 coroutines", time_ms)

    # -------------------------------------------------------------------------
    # Task Creation
    # -------------------------------------------------------------------------
    print_subheader("Task Creation")

    async def create_and_await_task():
        task = asyncio.create_task(return_value_coro())
        return await task

    def run_create_task():
        loop.run_until_complete(create_and_await_task())

    time_ms = time_operation(run_create_task, iterations=5000)
    results.append(BenchmarkResult("create_task() + await", time_ms, category=CATEGORY))
    print_result("create_task() + await", time_ms)

    async def create_multiple_tasks():
        tasks = [asyncio.create_task(return_value_coro()) for _ in range(10)]
        return await asyncio.gather(*tasks)

    def run_multiple_tasks():
        loop.run_until_complete(create_multiple_tasks())

    time_ms = time_operation(run_multiple_tasks, iterations=2000)
    results.append(BenchmarkResult("create 10 tasks + gather", time_ms, category=CATEGORY))
    print_result("create 10 tasks + gather", time_ms)

    # -------------------------------------------------------------------------
    # Async Context Managers
    # -------------------------------------------------------------------------
    print_subheader("Async Context Managers")

    async def use_async_ctx():
        async with AsyncContextManager():
            pass

    def run_async_ctx():
        loop.run_until_complete(use_async_ctx())

    time_ms = time_operation(run_async_ctx, iterations=10000)
    results.append(BenchmarkResult("async with (context manager)", time_ms, category=CATEGORY))
    print_result("async with (context manager)", time_ms)

    # -------------------------------------------------------------------------
    # Async Iteration
    # -------------------------------------------------------------------------
    print_subheader("Async Iteration")

    async def iterate_5():
        result = []
        async for i in AsyncIterator(5):
            result.append(i)
        return result

    def run_iterate_5():
        loop.run_until_complete(iterate_5())

    time_ms = time_operation(run_iterate_5, iterations=5000)
    results.append(BenchmarkResult("async for (5 items)", time_ms, category=CATEGORY))
    print_result("async for (5 items)", time_ms)

    async def iterate_100():
        result = []
        async for i in AsyncIterator(100):
            result.append(i)
        return result

    def run_iterate_100():
        loop.run_until_complete(iterate_100())

    time_ms = time_operation(run_iterate_100, iterations=1000)
    results.append(BenchmarkResult("async for (100 items)", time_ms, category=CATEGORY))
    print_result("async for (100 items)", time_ms)

    # -------------------------------------------------------------------------
    # Comparison: Sync vs Async
    # -------------------------------------------------------------------------
    print_subheader("Sync vs Async Comparison")

    def sync_function():
        return 42

    def call_sync():
        return sync_function()

    time_ms = time_operation(call_sync, iterations=100000)
    results.append(BenchmarkResult("sync function call", time_ms, category=CATEGORY))
    print_result("sync function call", time_ms)

    def call_async_equivalent():
        return loop.run_until_complete(return_value_coro())

    time_ms = time_operation(call_async_equivalent, iterations=10000)
    results.append(BenchmarkResult("async equivalent (run_until_complete)", time_ms, category=CATEGORY))
    print_result("async equivalent (run_until_complete)", time_ms)

    return results


def main():
    """Run benchmarks and output results."""
    results = run_benchmarks()
    output = collect_results(CATEGORY, results)

    print()
    print(f"Total benchmarks: {len(results)}")

    return output


if __name__ == "__main__":
    main()
