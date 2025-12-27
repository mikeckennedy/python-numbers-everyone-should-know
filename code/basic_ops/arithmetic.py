"""
Benchmark: Arithmetic Operations

Measures the time for basic arithmetic operations on integers and floats.
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
    time_operation_ns,
    ns_to_ms,
)


def run_benchmarks() -> dict:
    """Run arithmetic operation benchmarks."""
    print_header("Arithmetic Operations")

    results = []

    # Integer addition
    a_int, b_int = 123, 456
    time_ns = time_operation_ns(lambda: a_int + b_int, iterations=100000)
    time_ms = ns_to_ms(time_ns)
    print_result("Add two integers", time_ms)
    results.append(BenchmarkResult(name="int_add", value=time_ms, category="basic_ops"))

    # Integer multiplication
    time_ns = time_operation_ns(lambda: a_int * b_int, iterations=100000)
    time_ms = ns_to_ms(time_ns)
    print_result("Multiply two integers", time_ms)
    results.append(
        BenchmarkResult(name="int_multiply", value=time_ms, category="basic_ops")
    )

    # Integer division
    time_ns = time_operation_ns(lambda: a_int / b_int, iterations=100000)
    time_ms = ns_to_ms(time_ns)
    print_result("Divide two integers", time_ms)
    results.append(
        BenchmarkResult(name="int_divide", value=time_ms, category="basic_ops")
    )

    # Float addition
    a_float, b_float = 123.456, 789.012
    time_ns = time_operation_ns(lambda: a_float + b_float, iterations=100000)
    time_ms = ns_to_ms(time_ns)
    print_result("Add two floats", time_ms)
    results.append(
        BenchmarkResult(name="float_add", value=time_ms, category="basic_ops")
    )

    # Float multiplication
    time_ns = time_operation_ns(lambda: a_float * b_float, iterations=100000)
    time_ms = ns_to_ms(time_ns)
    print_result("Multiply two floats", time_ms)
    results.append(
        BenchmarkResult(name="float_multiply", value=time_ms, category="basic_ops")
    )

    # Float division
    time_ns = time_operation_ns(lambda: a_float / b_float, iterations=100000)
    time_ms = ns_to_ms(time_ns)
    print_result("Divide two floats", time_ms)
    results.append(
        BenchmarkResult(name="float_divide", value=time_ms, category="basic_ops")
    )

    return {
        "category": "basic_ops",
        "section": "arithmetic",
        "results": [r.to_dict() for r in results],
    }


if __name__ == "__main__":
    results = run_benchmarks()
    print()
    print(json.dumps(results, indent=2))
