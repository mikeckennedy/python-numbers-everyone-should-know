"""
DiskCache benchmarks.

Measures:
- cache.set(key, obj)
- cache.get(key)
- cache.delete(key)
- Check key exists
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.benchmark import (
    USER_DATA,
    BenchmarkResult,
    collect_results,
    print_header,
    print_result,
    print_skip_message,
    print_subheader,
    time_operation,
    try_import,
)

CATEGORY = 'database_diskcache'


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all DiskCache benchmarks."""
    results = []

    print_header('DiskCache Benchmarks')

    # Import diskcache
    diskcache = try_import('diskcache')
    if not diskcache:
        print_skip_message('diskcache', 'not installed (pip install diskcache)')
        return results

    # Create temporary cache directory
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = diskcache.Cache(tmpdir)

        # -------------------------------------------------------------------------
        # Set Operations
        # -------------------------------------------------------------------------
        print_subheader('Set Operations')

        # Use a fixed key for consistent benchmarking
        def cache_set():
            cache.set('bench:user', USER_DATA)

        time_ms = time_operation(cache_set, iterations=1_000)
        results.append(BenchmarkResult('cache.set() (complex obj)', time_ms, category=CATEGORY))
        print_result('cache.set() (complex obj)', time_ms)

        # Set simple value
        def cache_set_simple():
            cache.set('bench:simple', 'hello world')

        time_ms = time_operation(cache_set_simple, iterations=1_000)
        results.append(BenchmarkResult('cache.set() (string)', time_ms, category=CATEGORY))
        print_result('cache.set() (string)', time_ms)

        # Set with expire
        def cache_set_expire():
            cache.set('bench:expire', USER_DATA, expire=3600)

        time_ms = time_operation(cache_set_expire, iterations=1_000)
        results.append(BenchmarkResult('cache.set() with expire', time_ms, category=CATEGORY))
        print_result('cache.set() with expire', time_ms)

        # -------------------------------------------------------------------------
        # Get Operations
        # -------------------------------------------------------------------------
        print_subheader('Get Operations')

        # Setup: ensure we have a key to get
        cache.set('test_key', USER_DATA)
        cache.set('test_simple', 'hello')

        def cache_get():
            return cache.get('test_key')

        time_ms = time_operation(cache_get, iterations=5_000)
        results.append(BenchmarkResult('cache.get() (complex obj)', time_ms, category=CATEGORY))
        print_result('cache.get() (complex obj)', time_ms)

        def cache_get_simple():
            return cache.get('test_simple')

        time_ms = time_operation(cache_get_simple, iterations=5_000)
        results.append(BenchmarkResult('cache.get() (string)', time_ms, category=CATEGORY))
        print_result('cache.get() (string)', time_ms)

        # Get with default
        def cache_get_default():
            return cache.get('nonexistent', default=None)

        time_ms = time_operation(cache_get_default, iterations=5_000)
        results.append(BenchmarkResult('cache.get() miss (with default)', time_ms, category=CATEGORY))
        print_result('cache.get() miss (with default)', time_ms)

        # -------------------------------------------------------------------------
        # Check Operations
        # -------------------------------------------------------------------------
        print_subheader('Check Operations')

        def cache_contains_hit():
            return 'test_key' in cache

        time_ms = time_operation(cache_contains_hit, iterations=5_000)
        results.append(BenchmarkResult('key in cache (hit)', time_ms, category=CATEGORY))
        print_result('key in cache (hit)', time_ms)

        def cache_contains_miss():
            return 'nonexistent_key' in cache

        time_ms = time_operation(cache_contains_miss, iterations=5_000)
        results.append(BenchmarkResult('key in cache (miss)', time_ms, category=CATEGORY))
        print_result('key in cache (miss)', time_ms)

        # -------------------------------------------------------------------------
        # Delete Operations
        # -------------------------------------------------------------------------
        print_subheader('Delete Operations')

        # Pre-populate a key to delete (recreated each time)
        cache.set('bench:delete', 'value')

        def cache_delete():
            # Delete and immediately recreate for next iteration
            cache.delete('bench:delete')
            cache.set('bench:delete', 'value')

        time_ms = time_operation(cache_delete, iterations=1_000)
        results.append(BenchmarkResult('cache.delete()', time_ms, category=CATEGORY))
        print_result('cache.delete()', time_ms)

        # Pop (get and delete)
        cache.set('bench:pop', USER_DATA)

        def cache_pop():
            # Pop and immediately recreate for next iteration
            result = cache.pop('bench:pop')
            cache.set('bench:pop', USER_DATA)
            return result

        time_ms = time_operation(cache_pop, iterations=1_000)
        results.append(BenchmarkResult('cache.pop() (get+delete)', time_ms, category=CATEGORY))
        print_result('cache.pop() (get+delete)', time_ms)

        # -------------------------------------------------------------------------
        # Batch Operations
        # -------------------------------------------------------------------------
        print_subheader('Batch Operations')

        # Prepare batch data
        batch_data = {f'batch:{i}': USER_DATA for i in range(10)}

        def cache_set_many():
            for k, v in batch_data.items():
                cache.set(k, v)

        time_ms = time_operation(cache_set_many, iterations=200)
        results.append(BenchmarkResult('set 10 items (loop)', time_ms, category=CATEGORY))
        print_result('set 10 items (loop)', time_ms)

        # Read many
        batch_keys = list(batch_data.keys())

        def cache_get_many():
            return [cache.get(k) for k in batch_keys]

        time_ms = time_operation(cache_get_many, iterations=500)
        results.append(BenchmarkResult('get 10 items (loop)', time_ms, category=CATEGORY))
        print_result('get 10 items (loop)', time_ms)

        # -------------------------------------------------------------------------
        # Statistics
        # -------------------------------------------------------------------------
        print_subheader('Cache Statistics')
        print(f'  Total keys in cache: {len(cache)}')
        print(f'  Cache directory size: {cache.volume() / 1024:.1f} KB')

        # Cleanup
        cache.close()

    return results


def main():
    """Run benchmarks and output results."""
    results = run_benchmarks()
    output = collect_results(CATEGORY, results)  # type: ignore

    print()
    print(f'Total benchmarks: {len(results)}')

    return output


if __name__ == '__main__':
    main()
