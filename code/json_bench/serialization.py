"""
JSON serialization benchmarks.

Measures:
- json.dumps() - simple and complex
- orjson.dumps() - simple and complex
- ujson.dumps() - simple and complex
- msgspec.json.encode() - simple and complex
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.benchmark import (
    COMPLEX_OBJ,
    SIMPLE_OBJ,
    BenchmarkResult,
    collect_results,
    print_header,
    print_result,
    print_skip_message,
    print_subheader,
    time_operation,
    try_import,
)

CATEGORY = "json_serialization"


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all JSON serialization benchmarks."""
    results = []

    print_header("JSON Serialization Benchmarks")

    # Import optional libraries
    orjson = try_import("orjson")
    ujson = try_import("ujson")
    msgspec = try_import("msgspec")

    # -------------------------------------------------------------------------
    # stdlib json
    # -------------------------------------------------------------------------
    print_subheader("stdlib json.dumps()")

    def json_dumps_simple():
        return json.dumps(SIMPLE_OBJ)

    time_ms = time_operation(json_dumps_simple, iterations=5000)
    results.append(BenchmarkResult("json.dumps() - simple", time_ms, category=CATEGORY))
    print_result("json.dumps() - simple", time_ms)

    def json_dumps_complex():
        return json.dumps(COMPLEX_OBJ)

    time_ms = time_operation(json_dumps_complex, iterations=5000)
    results.append(BenchmarkResult("json.dumps() - complex", time_ms, category=CATEGORY))
    print_result("json.dumps() - complex", time_ms)

    # With ensure_ascii=False (faster for unicode)
    def json_dumps_complex_no_ascii():
        return json.dumps(COMPLEX_OBJ, ensure_ascii=False)

    time_ms = time_operation(json_dumps_complex_no_ascii, iterations=5000)
    results.append(BenchmarkResult("json.dumps() - complex (no ascii)", time_ms, category=CATEGORY))
    print_result("json.dumps() - complex (no ascii)", time_ms)

    # -------------------------------------------------------------------------
    # orjson
    # -------------------------------------------------------------------------
    print_subheader("orjson.dumps()")

    if orjson:
        def orjson_dumps_simple():
            return orjson.dumps(SIMPLE_OBJ)

        time_ms = time_operation(orjson_dumps_simple, iterations=5000)
        results.append(BenchmarkResult("orjson.dumps() - simple", time_ms, category=CATEGORY))
        print_result("orjson.dumps() - simple", time_ms)

        def orjson_dumps_complex():
            return orjson.dumps(COMPLEX_OBJ)

        time_ms = time_operation(orjson_dumps_complex, iterations=5000)
        results.append(BenchmarkResult("orjson.dumps() - complex", time_ms, category=CATEGORY))
        print_result("orjson.dumps() - complex", time_ms)
    else:
        print_skip_message("orjson")

    # -------------------------------------------------------------------------
    # ujson
    # -------------------------------------------------------------------------
    print_subheader("ujson.dumps()")

    if ujson:
        def ujson_dumps_simple():
            return ujson.dumps(SIMPLE_OBJ)

        time_ms = time_operation(ujson_dumps_simple, iterations=5000)
        results.append(BenchmarkResult("ujson.dumps() - simple", time_ms, category=CATEGORY))
        print_result("ujson.dumps() - simple", time_ms)

        def ujson_dumps_complex():
            return ujson.dumps(COMPLEX_OBJ)

        time_ms = time_operation(ujson_dumps_complex, iterations=5000)
        results.append(BenchmarkResult("ujson.dumps() - complex", time_ms, category=CATEGORY))
        print_result("ujson.dumps() - complex", time_ms)
    else:
        print_skip_message("ujson")

    # -------------------------------------------------------------------------
    # msgspec
    # -------------------------------------------------------------------------
    print_subheader("msgspec.json.encode()")

    if msgspec:
        def msgspec_encode_simple():
            return msgspec.json.encode(SIMPLE_OBJ)

        time_ms = time_operation(msgspec_encode_simple, iterations=5000)
        results.append(BenchmarkResult("msgspec.json.encode() - simple", time_ms, category=CATEGORY))
        print_result("msgspec.json.encode() - simple", time_ms)

        def msgspec_encode_complex():
            return msgspec.json.encode(COMPLEX_OBJ)

        time_ms = time_operation(msgspec_encode_complex, iterations=5000)
        results.append(BenchmarkResult("msgspec.json.encode() - complex", time_ms, category=CATEGORY))
        print_result("msgspec.json.encode() - complex", time_ms)
    else:
        print_skip_message("msgspec")

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
