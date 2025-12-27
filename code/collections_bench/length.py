"""
Collection length benchmarks.

Measures:
- len() on list (1000 items)
- len() on dict (1000 items)
- len() on set (1000 items)
"""

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

CATEGORY = 'collections_length'


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all collection length benchmarks."""
    results = []

    print_header('Collection Length Benchmarks')

    # Setup test data
    test_list_1000 = list(range(1000))
    test_dict_1000 = {f'key_{i}': i for i in range(1000)}
    test_set_1000 = set(range(1000))

    # Also test with different sizes for comparison
    test_list_10 = list(range(10))
    test_list_100 = list(range(100))
    test_list_10000 = list(range(10000))

    # -------------------------------------------------------------------------
    # len() is O(1) - stored as attribute on collection
    # -------------------------------------------------------------------------
    print_subheader('len() on List')

    def len_list_10():
        return len(test_list_10)

    time_ms = time_operation(len_list_10, iterations=10000)
    results.append(BenchmarkResult('len(list) - 10 items', time_ms, category=CATEGORY))
    print_result('len(list) - 10 items', time_ms)

    def len_list_100():
        return len(test_list_100)

    time_ms = time_operation(len_list_100, iterations=10000)
    results.append(BenchmarkResult('len(list) - 100 items', time_ms, category=CATEGORY))
    print_result('len(list) - 100 items', time_ms)

    def len_list_1000():
        return len(test_list_1000)

    time_ms = time_operation(len_list_1000, iterations=10000)
    results.append(BenchmarkResult('len(list) - 1000 items', time_ms, category=CATEGORY))
    print_result('len(list) - 1000 items', time_ms)

    def len_list_10000():
        return len(test_list_10000)

    time_ms = time_operation(len_list_10000, iterations=10000)
    results.append(BenchmarkResult('len(list) - 10000 items', time_ms, category=CATEGORY))
    print_result('len(list) - 10000 items', time_ms)

    # -------------------------------------------------------------------------
    # len() on Dict
    # -------------------------------------------------------------------------
    print_subheader('len() on Dict')

    def len_dict_1000():
        return len(test_dict_1000)

    time_ms = time_operation(len_dict_1000, iterations=10000)
    results.append(BenchmarkResult('len(dict) - 1000 items', time_ms, category=CATEGORY))
    print_result('len(dict) - 1000 items', time_ms)

    # -------------------------------------------------------------------------
    # len() on Set
    # -------------------------------------------------------------------------
    print_subheader('len() on Set')

    def len_set_1000():
        return len(test_set_1000)

    time_ms = time_operation(len_set_1000, iterations=10000)
    results.append(BenchmarkResult('len(set) - 1000 items', time_ms, category=CATEGORY))
    print_result('len(set) - 1000 items', time_ms)

    # -------------------------------------------------------------------------
    # len() on String
    # -------------------------------------------------------------------------
    print_subheader('len() on String')

    test_str_1000 = 'a' * 1000

    def len_str_1000():
        return len(test_str_1000)

    time_ms = time_operation(len_str_1000, iterations=10000)
    results.append(BenchmarkResult('len(str) - 1000 chars', time_ms, category=CATEGORY))
    print_result('len(str) - 1000 chars', time_ms)

    # -------------------------------------------------------------------------
    # len() on Tuple
    # -------------------------------------------------------------------------
    print_subheader('len() on Tuple')

    test_tuple_1000 = tuple(range(1000))

    def len_tuple_1000():
        return len(test_tuple_1000)

    time_ms = time_operation(len_tuple_1000, iterations=10000)
    results.append(BenchmarkResult('len(tuple) - 1000 items', time_ms, category=CATEGORY))
    print_result('len(tuple) - 1000 items', time_ms)

    return results


def main():
    """Run benchmarks and output results."""
    results = run_benchmarks()
    output = collect_results(CATEGORY, results)

    print()
    print(f'Total benchmarks: {len(results)}')

    return output


if __name__ == '__main__':
    main()
