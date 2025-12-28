"""
Collection access benchmarks.

Measures:
- Dict lookup by key
- Set membership (in)
- List index access
- List membership (in, 1000 items)
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

CATEGORY = 'collections_access'


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all collection access benchmarks."""
    results = []

    print_header('Collection Access Benchmarks')

    # Setup test data
    test_dict = {f'key_{i}': i for i in range(1_000)}
    test_set = {f'item_{i}' for i in range(1_000)}
    test_list = list(range(1_000))

    # Keys/items that exist (middle of collection)
    existing_key = 'key_500'
    existing_item = 'item_500'
    existing_index = 500

    # Keys/items that don't exist
    missing_key = 'key_9999'
    missing_item = 'item_9999'

    # -------------------------------------------------------------------------
    # Dict Lookup
    # -------------------------------------------------------------------------
    print_subheader('Dict Lookup (1000 items)')

    # Existing key
    def dict_lookup_existing():
        return test_dict[existing_key]

    time_ms = time_operation(dict_lookup_existing, iterations=10_000)
    results.append(BenchmarkResult('dict[key] (existing)', time_ms, category=CATEGORY))
    print_result('dict[key] (existing)', time_ms)

    # Using .get() with existing key
    def dict_get_existing():
        return test_dict.get(existing_key)

    time_ms = time_operation(dict_get_existing, iterations=10_000)
    results.append(BenchmarkResult('dict.get(key) (existing)', time_ms, category=CATEGORY))
    print_result('dict.get(key) (existing)', time_ms)

    # Using .get() with missing key
    def dict_get_missing():
        return test_dict.get(missing_key)

    time_ms = time_operation(dict_get_missing, iterations=10_000)
    results.append(BenchmarkResult('dict.get(key) (missing)', time_ms, category=CATEGORY))
    print_result('dict.get(key) (missing)', time_ms)

    # Membership check (in)
    def dict_in_existing():
        return existing_key in test_dict

    time_ms = time_operation(dict_in_existing, iterations=10_000)
    results.append(BenchmarkResult('key in dict (existing)', time_ms, category=CATEGORY))
    print_result('key in dict (existing)', time_ms)

    def dict_in_missing():
        return missing_key in test_dict

    time_ms = time_operation(dict_in_missing, iterations=10_000)
    results.append(BenchmarkResult('key in dict (missing)', time_ms, category=CATEGORY))
    print_result('key in dict (missing)', time_ms)

    # -------------------------------------------------------------------------
    # Set Membership
    # -------------------------------------------------------------------------
    print_subheader('Set Membership (1000 items)')

    def set_in_existing():
        return existing_item in test_set

    time_ms = time_operation(set_in_existing, iterations=10_000)
    results.append(BenchmarkResult('item in set (existing)', time_ms, category=CATEGORY))
    print_result('item in set (existing)', time_ms)

    def set_in_missing():
        return missing_item in test_set

    time_ms = time_operation(set_in_missing, iterations=10_000)
    results.append(BenchmarkResult('item in set (missing)', time_ms, category=CATEGORY))
    print_result('item in set (missing)', time_ms)

    # -------------------------------------------------------------------------
    # List Access
    # -------------------------------------------------------------------------
    print_subheader('List Index Access (1000 items)')

    # Index access
    def list_index_access():
        return test_list[existing_index]

    time_ms = time_operation(list_index_access, iterations=10_000)
    results.append(BenchmarkResult('list[index]', time_ms, category=CATEGORY))
    print_result('list[index]', time_ms)

    # Negative index access
    def list_negative_index():
        return test_list[-1]

    time_ms = time_operation(list_negative_index, iterations=10_000)
    results.append(BenchmarkResult('list[-1]', time_ms, category=CATEGORY))
    print_result('list[-1]', time_ms)

    # -------------------------------------------------------------------------
    # List Membership (O(n) operation)
    # -------------------------------------------------------------------------
    print_subheader('List Membership - O(n) (1000 items)')

    # Value at beginning
    def list_in_first():
        return 0 in test_list

    time_ms = time_operation(list_in_first, iterations=1_000)
    results.append(BenchmarkResult('item in list (first)', time_ms, category=CATEGORY))
    print_result('item in list (first)', time_ms)

    # Value in middle
    def list_in_middle():
        return 500 in test_list

    time_ms = time_operation(list_in_middle, iterations=1_000)
    results.append(BenchmarkResult('item in list (middle)', time_ms, category=CATEGORY))
    print_result('item in list (middle)', time_ms)

    # Value at end
    def list_in_last():
        return 999 in test_list

    time_ms = time_operation(list_in_last, iterations=1_000)
    results.append(BenchmarkResult('item in list (last)', time_ms, category=CATEGORY))
    print_result('item in list (last)', time_ms)

    # Missing value (full scan)
    def list_in_missing():
        return 9999 in test_list

    time_ms = time_operation(list_in_missing, iterations=1_000)
    results.append(BenchmarkResult('item in list (missing)', time_ms, category=CATEGORY))
    print_result('item in list (missing)', time_ms)

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
