"""
Benchmark: String Operations

Measures the time for various string operations including concatenation and formatting.
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
    """Run string operation benchmarks."""
    print_header("String Operations")

    results = []

    # String concatenation (small strings)
    s1, s2 = "hello", "world"
    time_ns = time_operation_ns(lambda: s1 + " " + s2, iterations=100000)
    time_ms = ns_to_ms(time_ns)
    print_result("Concatenation (+) small strings", time_ms)
    results.append(
        BenchmarkResult(name="concat_small", value=time_ms, category="basic_ops")
    )

    # String concatenation (medium strings)
    s1_med = "hello" * 10
    s2_med = "world" * 10
    time_ns = time_operation_ns(lambda: s1_med + " " + s2_med, iterations=10000)
    time_ms = ns_to_ms(time_ns)
    print_result("Concatenation (+) medium strings", time_ms)
    results.append(
        BenchmarkResult(name="concat_medium", value=time_ms, category="basic_ops")
    )

    # f-string formatting
    name, age = "Alice", 30
    time_ns = time_operation_ns(
        lambda: f"Hello {name}, you are {age} years old", iterations=100000
    )
    time_ms = ns_to_ms(time_ns)
    print_result("f-string formatting", time_ms)
    results.append(
        BenchmarkResult(name="f_string", value=time_ms, category="basic_ops")
    )

    # .format() method
    time_ns = time_operation_ns(
        lambda: "Hello {}, you are {} years old".format(name, age),
        iterations=100000,
    )
    time_ms = ns_to_ms(time_ns)
    print_result(".format() method", time_ms)
    results.append(
        BenchmarkResult(name="format_method", value=time_ms, category="basic_ops")
    )

    # % formatting
    time_ns = time_operation_ns(
        lambda: "Hello %s, you are %d years old" % (name, age), iterations=100000
    )
    time_ms = ns_to_ms(time_ns)
    print_result("% formatting", time_ms)
    results.append(
        BenchmarkResult(name="percent_formatting", value=time_ms, category="basic_ops")
    )

    # String join (small list)
    words = ["hello", "world", "python", "test"]
    time_ns = time_operation_ns(lambda: " ".join(words), iterations=100000)
    time_ms = ns_to_ms(time_ns)
    print_result("Join small list", time_ms)
    results.append(
        BenchmarkResult(name="join_small", value=time_ms, category="basic_ops")
    )

    # String split
    sentence = "hello world python test"
    time_ns = time_operation_ns(lambda: sentence.split(), iterations=100000)
    time_ms = ns_to_ms(time_ns)
    print_result("Split string", time_ms)
    results.append(BenchmarkResult(name="split", value=time_ms, category="basic_ops"))

    return {
        "category": "basic_ops",
        "section": "string_ops",
        "results": [r.to_dict() for r in results],
    }


if __name__ == "__main__":
    results = run_benchmarks()
    print()
    print(json.dumps(results, indent=2))
