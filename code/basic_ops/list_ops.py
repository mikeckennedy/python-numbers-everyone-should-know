"""
Benchmark: List Operations

Measures the time for basic list operations including append, comprehensions, and loops.
"""

import json
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.benchmark import (
    BenchmarkResult,
    print_header,
    print_result,
    time_operation,
)


def run_benchmarks() -> dict:
    """Run list operation benchmarks."""
    print_header('List Operations')

    results: list[BenchmarkResult] = []

    lst = []
        
    # List append (single item)
    def append_test():
        lst.clear()
        lst.append(1)

    time_ms = time_operation(append_test, iterations=100000)
    print_result('list.append() single item', time_ms)
    results.append(BenchmarkResult(name='list_append', value=time_ms, category='basic_ops'))

    # List comprehension (10 items)
    def list_comp_10():
        return [i for i in range(10)]

    time_ms = time_operation(list_comp_10, iterations=10000)
    print_result('List comprehension (10 items)', time_ms)
    results.append(BenchmarkResult(name='list_comp_10', value=time_ms, category='basic_ops'))

    # For-loop (10 items)
    def for_loop_10():
        lst = []
        for i in range(10):
            lst.append(i)
        return lst

    time_ms = time_operation(for_loop_10, iterations=10000)
    print_result('For-loop (10 items)', time_ms)
    results.append(BenchmarkResult(name='for_loop_10', value=time_ms, category='basic_ops'))

    # List comprehension (100 items)
    def list_comp_100():
        return [i for i in range(100)]

    time_ms = time_operation(list_comp_100, iterations=10000)
    print_result('List comprehension (100 items)', time_ms)
    results.append(BenchmarkResult(name='list_comp_100', value=time_ms, category='basic_ops'))

    # For-loop (100 items)
    def for_loop_100():
        lst = []
        for i in range(100):
            lst.append(i)
        return lst

    time_ms = time_operation(for_loop_100, iterations=10000)
    print_result('For-loop (100 items)', time_ms)
    results.append(BenchmarkResult(name='for_loop_100', value=time_ms, category='basic_ops'))

    # List comprehension (1000 items)
    def list_comp_1000():
        return [i for i in range(1000)]

    time_ms = time_operation(list_comp_1000, iterations=1000)
    print_result('List comprehension (1000 items)', time_ms)
    results.append(BenchmarkResult(name='list_comp_1000', value=time_ms, category='basic_ops'))

    # For-loop (1000 items)
    def for_loop_1000():
        lst = []
        for i in range(1000):
            lst.append(i)
        return lst

    time_ms = time_operation(for_loop_1000, iterations=1000)
    print_result('For-loop (1000 items)', time_ms)
    results.append(BenchmarkResult(name='for_loop_1000', value=time_ms, category='basic_ops'))

    # List extend
    def list_extend():
        lst1 = [1, 2, 3]
        lst2 = [4, 5, 6]
        lst1.extend(lst2)

    time_ms = time_operation(list_extend, iterations=100000)
    print_result('list.extend() 3 items', time_ms)
    results.append(BenchmarkResult(name='list_extend', value=time_ms, category='basic_ops'))

    # List copy
    original = list(range(100))

    def list_copy():
        return original.copy()

    time_ms = time_operation(list_copy, iterations=10000)
    print_result('list.copy() 100 items', time_ms)
    results.append(BenchmarkResult(name='list_copy_100', value=time_ms, category='basic_ops'))

    return {
        'category': 'basic_ops',
        'section': 'list_ops',
        'results': [r.to_dict() for r in results],
    }


if __name__ == '__main__':
    results = run_benchmarks()
    print()
    print(json.dumps(results, indent=2))
