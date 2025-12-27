"""
Attribute access benchmarks.

Measures:
- Read from regular class
- Write to regular class
- Read from __slots__ class
- Write to __slots__ class
"""

import sys
from dataclasses import dataclass
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

CATEGORY = "attribute_access"


# =============================================================================
# Test Classes
# =============================================================================


class RegularClass:
    """Standard Python class with __dict__."""

    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e


class SlotsClass:
    """Class using __slots__ for memory efficiency."""

    __slots__ = ("a", "b", "c", "d", "e")

    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e


@dataclass
class DataClass:
    """Standard dataclass."""

    a: int
    b: int
    c: int
    d: int
    e: int


@dataclass(slots=True)
class SlotsDataClass:
    """Dataclass with slots=True."""

    a: int
    b: int
    c: int
    d: int
    e: int


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all attribute access benchmarks."""
    results = []

    print_header("Attribute Access Benchmarks")

    # Create test instances
    regular_obj = RegularClass(1, 2, 3, 4, 5)
    slots_obj = SlotsClass(1, 2, 3, 4, 5)
    dataclass_obj = DataClass(1, 2, 3, 4, 5)
    slots_dataclass_obj = SlotsDataClass(1, 2, 3, 4, 5)

    # -------------------------------------------------------------------------
    # Regular Class
    # -------------------------------------------------------------------------
    print_subheader("Regular Class (with __dict__)")

    def read_regular():
        return regular_obj.a

    time_ms = time_operation(read_regular, iterations=10000)
    results.append(BenchmarkResult("regular class: read attr", time_ms, category=CATEGORY))
    print_result("regular class: read attr", time_ms)

    def write_regular():
        regular_obj.a = 10

    time_ms = time_operation(write_regular, iterations=10000)
    results.append(BenchmarkResult("regular class: write attr", time_ms, category=CATEGORY))
    print_result("regular class: write attr", time_ms)

    # Read multiple attributes
    def read_regular_all():
        return (regular_obj.a, regular_obj.b, regular_obj.c, regular_obj.d, regular_obj.e)

    time_ms = time_operation(read_regular_all, iterations=10000)
    results.append(BenchmarkResult("regular class: read 5 attrs", time_ms, category=CATEGORY))
    print_result("regular class: read 5 attrs", time_ms)

    # -------------------------------------------------------------------------
    # Slots Class
    # -------------------------------------------------------------------------
    print_subheader("Slots Class (__slots__)")

    def read_slots():
        return slots_obj.a

    time_ms = time_operation(read_slots, iterations=10000)
    results.append(BenchmarkResult("slots class: read attr", time_ms, category=CATEGORY))
    print_result("slots class: read attr", time_ms)

    def write_slots():
        slots_obj.a = 10

    time_ms = time_operation(write_slots, iterations=10000)
    results.append(BenchmarkResult("slots class: write attr", time_ms, category=CATEGORY))
    print_result("slots class: write attr", time_ms)

    def read_slots_all():
        return (slots_obj.a, slots_obj.b, slots_obj.c, slots_obj.d, slots_obj.e)

    time_ms = time_operation(read_slots_all, iterations=10000)
    results.append(BenchmarkResult("slots class: read 5 attrs", time_ms, category=CATEGORY))
    print_result("slots class: read 5 attrs", time_ms)

    # -------------------------------------------------------------------------
    # Dataclass
    # -------------------------------------------------------------------------
    print_subheader("Dataclass")

    def read_dataclass():
        return dataclass_obj.a

    time_ms = time_operation(read_dataclass, iterations=10000)
    results.append(BenchmarkResult("dataclass: read attr", time_ms, category=CATEGORY))
    print_result("dataclass: read attr", time_ms)

    def write_dataclass():
        dataclass_obj.a = 10

    time_ms = time_operation(write_dataclass, iterations=10000)
    results.append(BenchmarkResult("dataclass: write attr", time_ms, category=CATEGORY))
    print_result("dataclass: write attr", time_ms)

    # -------------------------------------------------------------------------
    # Slots Dataclass
    # -------------------------------------------------------------------------
    print_subheader("Dataclass (slots=True)")

    def read_slots_dataclass():
        return slots_dataclass_obj.a

    time_ms = time_operation(read_slots_dataclass, iterations=10000)
    results.append(BenchmarkResult("slots dataclass: read attr", time_ms, category=CATEGORY))
    print_result("slots dataclass: read attr", time_ms)

    def write_slots_dataclass():
        slots_dataclass_obj.a = 10

    time_ms = time_operation(write_slots_dataclass, iterations=10000)
    results.append(BenchmarkResult("slots dataclass: write attr", time_ms, category=CATEGORY))
    print_result("slots dataclass: write attr", time_ms)

    # -------------------------------------------------------------------------
    # Dict Access (for comparison)
    # -------------------------------------------------------------------------
    print_subheader("Dict Access (comparison)")

    test_dict = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}

    def read_dict():
        return test_dict["a"]

    time_ms = time_operation(read_dict, iterations=10000)
    results.append(BenchmarkResult("dict: read key", time_ms, category=CATEGORY))
    print_result("dict: read key", time_ms)

    def write_dict():
        test_dict["a"] = 10

    time_ms = time_operation(write_dict, iterations=10000)
    results.append(BenchmarkResult("dict: write key", time_ms, category=CATEGORY))
    print_result("dict: write key", time_ms)

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
