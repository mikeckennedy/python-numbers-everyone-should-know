"""
JSON deserialization benchmarks.

Measures:
- json.loads() - simple and complex
- orjson.loads() - simple and complex
- ujson.loads() - simple and complex
- msgspec.json.decode() - simple and complex
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

CATEGORY = "json_deserialization"

# Pre-serialize the test objects
SIMPLE_JSON = json.dumps(SIMPLE_OBJ)
COMPLEX_JSON = json.dumps(COMPLEX_OBJ)

# Also create bytes versions for orjson/msgspec
SIMPLE_JSON_BYTES = SIMPLE_JSON.encode("utf-8")
COMPLEX_JSON_BYTES = COMPLEX_JSON.encode("utf-8")


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all JSON deserialization benchmarks."""
    results = []

    print_header("JSON Deserialization Benchmarks")

    # Import optional libraries
    orjson = try_import("orjson")
    ujson = try_import("ujson")
    msgspec = try_import("msgspec")

    # -------------------------------------------------------------------------
    # stdlib json
    # -------------------------------------------------------------------------
    print_subheader("stdlib json.loads()")

    def json_loads_simple():
        return json.loads(SIMPLE_JSON)

    time_ms = time_operation(json_loads_simple, iterations=5000)
    results.append(BenchmarkResult("json.loads() - simple", time_ms, category=CATEGORY))
    print_result("json.loads() - simple", time_ms)

    def json_loads_complex():
        return json.loads(COMPLEX_JSON)

    time_ms = time_operation(json_loads_complex, iterations=5000)
    results.append(BenchmarkResult("json.loads() - complex", time_ms, category=CATEGORY))
    print_result("json.loads() - complex", time_ms)

    # -------------------------------------------------------------------------
    # orjson
    # -------------------------------------------------------------------------
    print_subheader("orjson.loads()")

    if orjson:
        def orjson_loads_simple():
            return orjson.loads(SIMPLE_JSON_BYTES)

        time_ms = time_operation(orjson_loads_simple, iterations=5000, warmup=500)
        results.append(BenchmarkResult("orjson.loads() - simple", time_ms, category=CATEGORY))
        print_result("orjson.loads() - simple", time_ms)

        def orjson_loads_complex():
            return orjson.loads(COMPLEX_JSON_BYTES)

        time_ms = time_operation(orjson_loads_complex, iterations=5000, warmup=500)
        results.append(BenchmarkResult("orjson.loads() - complex", time_ms, category=CATEGORY))
        print_result("orjson.loads() - complex", time_ms)

        # orjson also accepts str
        def orjson_loads_str():
            return orjson.loads(COMPLEX_JSON)

        time_ms = time_operation(orjson_loads_str, iterations=5000, warmup=500)
        results.append(BenchmarkResult("orjson.loads() - complex (str)", time_ms, category=CATEGORY))
        print_result("orjson.loads() - complex (str)", time_ms)
    else:
        print_skip_message("orjson")

    # -------------------------------------------------------------------------
    # ujson
    # -------------------------------------------------------------------------
    print_subheader("ujson.loads()")

    if ujson:
        def ujson_loads_simple():
            return ujson.loads(SIMPLE_JSON)

        time_ms = time_operation(ujson_loads_simple, iterations=5000)
        results.append(BenchmarkResult("ujson.loads() - simple", time_ms, category=CATEGORY))
        print_result("ujson.loads() - simple", time_ms)

        def ujson_loads_complex():
            return ujson.loads(COMPLEX_JSON)

        time_ms = time_operation(ujson_loads_complex, iterations=5000)
        results.append(BenchmarkResult("ujson.loads() - complex", time_ms, category=CATEGORY))
        print_result("ujson.loads() - complex", time_ms)
    else:
        print_skip_message("ujson")

    # -------------------------------------------------------------------------
    # msgspec
    # -------------------------------------------------------------------------
    print_subheader("msgspec.json.decode()")

    if msgspec:
        def msgspec_decode_simple():
            return msgspec.json.decode(SIMPLE_JSON_BYTES)

        time_ms = time_operation(msgspec_decode_simple, iterations=5000)
        results.append(BenchmarkResult("msgspec.json.decode() - simple", time_ms, category=CATEGORY))
        print_result("msgspec.json.decode() - simple", time_ms)

        def msgspec_decode_complex():
            return msgspec.json.decode(COMPLEX_JSON_BYTES)

        time_ms = time_operation(msgspec_decode_complex, iterations=5000)
        results.append(BenchmarkResult("msgspec.json.decode() - complex", time_ms, category=CATEGORY))
        print_result("msgspec.json.decode() - complex", time_ms)

        # msgspec also accepts str
        def msgspec_decode_str():
            return msgspec.json.decode(COMPLEX_JSON)

        time_ms = time_operation(msgspec_decode_str, iterations=5000)
        results.append(BenchmarkResult("msgspec.json.decode() - complex (str)", time_ms, category=CATEGORY))
        print_result("msgspec.json.decode() - complex (str)", time_ms)
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
