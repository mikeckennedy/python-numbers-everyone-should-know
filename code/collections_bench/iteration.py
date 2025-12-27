"""
Collection iteration benchmarks.

Measures:
- Iterate 1000-item list
- Iterate 1000-item dict (keys)
- Iterate range(1000)
- sum() of 1000 integers
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

CATEGORY = "collections_iteration"


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all collection iteration benchmarks."""
    results = []

    print_header("Collection Iteration Benchmarks")

    # Setup test data
    test_list = list(range(1000))
    test_dict = {f"key_{i}": i for i in range(1000)}
    test_set = set(range(1000))
    test_tuple = tuple(range(1000))

    # -------------------------------------------------------------------------
    # List Iteration
    # -------------------------------------------------------------------------
    print_subheader("List Iteration (1000 items)")

    def iterate_list():
        total = 0
        for item in test_list:
            total += item
        return total

    time_ms = time_operation(iterate_list, iterations=1000)
    results.append(BenchmarkResult("for item in list", time_ms, category=CATEGORY))
    print_result("for item in list", time_ms)

    # With enumerate
    def iterate_list_enumerate():
        total = 0
        for i, item in enumerate(test_list):
            total += item
        return total

    time_ms = time_operation(iterate_list_enumerate, iterations=1000)
    results.append(BenchmarkResult("for i, item in enumerate(list)", time_ms, category=CATEGORY))
    print_result("for i, item in enumerate(list)", time_ms)

    # -------------------------------------------------------------------------
    # Dict Iteration
    # -------------------------------------------------------------------------
    print_subheader("Dict Iteration (1000 items)")

    def iterate_dict_keys():
        total = 0
        for key in test_dict:
            total += 1
        return total

    time_ms = time_operation(iterate_dict_keys, iterations=1000)
    results.append(BenchmarkResult("for key in dict", time_ms, category=CATEGORY))
    print_result("for key in dict", time_ms)

    def iterate_dict_values():
        total = 0
        for value in test_dict.values():
            total += value
        return total

    time_ms = time_operation(iterate_dict_values, iterations=1000)
    results.append(BenchmarkResult("for value in dict.values()", time_ms, category=CATEGORY))
    print_result("for value in dict.values()", time_ms)

    def iterate_dict_items():
        total = 0
        for key, value in test_dict.items():
            total += value
        return total

    time_ms = time_operation(iterate_dict_items, iterations=1000)
    results.append(BenchmarkResult("for k, v in dict.items()", time_ms, category=CATEGORY))
    print_result("for k, v in dict.items()", time_ms)

    # -------------------------------------------------------------------------
    # Set Iteration
    # -------------------------------------------------------------------------
    print_subheader("Set Iteration (1000 items)")

    def iterate_set():
        total = 0
        for item in test_set:
            total += item
        return total

    time_ms = time_operation(iterate_set, iterations=1000)
    results.append(BenchmarkResult("for item in set", time_ms, category=CATEGORY))
    print_result("for item in set", time_ms)

    # -------------------------------------------------------------------------
    # Tuple Iteration
    # -------------------------------------------------------------------------
    print_subheader("Tuple Iteration (1000 items)")

    def iterate_tuple():
        total = 0
        for item in test_tuple:
            total += item
        return total

    time_ms = time_operation(iterate_tuple, iterations=1000)
    results.append(BenchmarkResult("for item in tuple", time_ms, category=CATEGORY))
    print_result("for item in tuple", time_ms)

    # -------------------------------------------------------------------------
    # Range Iteration
    # -------------------------------------------------------------------------
    print_subheader("Range Iteration")

    def iterate_range():
        total = 0
        for i in range(1000):
            total += i
        return total

    time_ms = time_operation(iterate_range, iterations=1000)
    results.append(BenchmarkResult("for i in range(1000)", time_ms, category=CATEGORY))
    print_result("for i in range(1000)", time_ms)

    # -------------------------------------------------------------------------
    # sum() Built-in
    # -------------------------------------------------------------------------
    print_subheader("sum() Built-in (1000 items)")

    def sum_list():
        return sum(test_list)

    time_ms = time_operation(sum_list, iterations=1000)
    results.append(BenchmarkResult("sum(list)", time_ms, category=CATEGORY))
    print_result("sum(list)", time_ms)

    def sum_range():
        return sum(range(1000))

    time_ms = time_operation(sum_range, iterations=1000)
    results.append(BenchmarkResult("sum(range(1000))", time_ms, category=CATEGORY))
    print_result("sum(range(1000))", time_ms)

    def sum_generator():
        return sum(i for i in range(1000))

    time_ms = time_operation(sum_generator, iterations=1000)
    results.append(BenchmarkResult("sum(generator)", time_ms, category=CATEGORY))
    print_result("sum(generator)", time_ms)

    # -------------------------------------------------------------------------
    # Other Aggregations
    # -------------------------------------------------------------------------
    print_subheader("Other Aggregations (1000 items)")

    def min_list():
        return min(test_list)

    time_ms = time_operation(min_list, iterations=1000)
    results.append(BenchmarkResult("min(list)", time_ms, category=CATEGORY))
    print_result("min(list)", time_ms)

    def max_list():
        return max(test_list)

    time_ms = time_operation(max_list, iterations=1000)
    results.append(BenchmarkResult("max(list)", time_ms, category=CATEGORY))
    print_result("max(list)", time_ms)

    def any_list():
        return any(test_list)

    time_ms = time_operation(any_list, iterations=1000)
    results.append(BenchmarkResult("any(list)", time_ms, category=CATEGORY))
    print_result("any(list)", time_ms)

    def all_list():
        # Use a list where all are truthy
        return all(test_list[1:])  # Skip 0 which is falsy

    time_ms = time_operation(all_list, iterations=1000)
    results.append(BenchmarkResult("all(list)", time_ms, category=CATEGORY))
    print_result("all(list)", time_ms)

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
