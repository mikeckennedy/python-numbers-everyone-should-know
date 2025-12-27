"""
Pickle vs JSON serialization benchmarks.

Measures:
- pickle.dumps() (complex obj)
- pickle.loads() (complex obj)
- json.dumps() (complex obj)
- json.loads() (complex obj)
"""

import json
import pickle
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.benchmark import (
    COMPLEX_OBJ,
    BenchmarkResult,
    collect_results,
    print_header,
    print_result,
    print_subheader,
    time_operation,
    try_import,
)

CATEGORY = "file_io_serialization"

# Pre-serialize for loading benchmarks
PICKLE_DATA = pickle.dumps(COMPLEX_OBJ)
JSON_DATA = json.dumps(COMPLEX_OBJ)
JSON_BYTES = JSON_DATA.encode("utf-8")


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all pickle vs JSON benchmarks."""
    results = []

    print_header("Pickle vs JSON Serialization")

    # Import optional libraries
    orjson = try_import("orjson")
    msgspec = try_import("msgspec")

    # -------------------------------------------------------------------------
    # Pickle
    # -------------------------------------------------------------------------
    print_subheader("pickle (stdlib)")

    def pickle_dumps():
        return pickle.dumps(COMPLEX_OBJ)

    time_ms = time_operation(pickle_dumps, iterations=5000)
    results.append(BenchmarkResult("pickle.dumps()", time_ms, category=CATEGORY))
    print_result("pickle.dumps()", time_ms)

    def pickle_loads():
        return pickle.loads(PICKLE_DATA)

    time_ms = time_operation(pickle_loads, iterations=5000)
    results.append(BenchmarkResult("pickle.loads()", time_ms, category=CATEGORY))
    print_result("pickle.loads()", time_ms)

    # Different protocols
    def pickle_dumps_p4():
        return pickle.dumps(COMPLEX_OBJ, protocol=4)

    time_ms = time_operation(pickle_dumps_p4, iterations=5000)
    results.append(BenchmarkResult("pickle.dumps() protocol=4", time_ms, category=CATEGORY))
    print_result("pickle.dumps() protocol=4", time_ms)

    def pickle_dumps_p5():
        return pickle.dumps(COMPLEX_OBJ, protocol=5)

    time_ms = time_operation(pickle_dumps_p5, iterations=5000)
    results.append(BenchmarkResult("pickle.dumps() protocol=5", time_ms, category=CATEGORY))
    print_result("pickle.dumps() protocol=5", time_ms)

    # -------------------------------------------------------------------------
    # JSON (stdlib)
    # -------------------------------------------------------------------------
    print_subheader("json (stdlib)")

    def json_dumps():
        return json.dumps(COMPLEX_OBJ)

    time_ms = time_operation(json_dumps, iterations=5000)
    results.append(BenchmarkResult("json.dumps()", time_ms, category=CATEGORY))
    print_result("json.dumps()", time_ms)

    def json_loads():
        return json.loads(JSON_DATA)

    time_ms = time_operation(json_loads, iterations=5000)
    results.append(BenchmarkResult("json.loads()", time_ms, category=CATEGORY))
    print_result("json.loads()", time_ms)

    # -------------------------------------------------------------------------
    # orjson (for comparison)
    # -------------------------------------------------------------------------
    print_subheader("orjson (comparison)")

    if orjson:
        orjson_data = orjson.dumps(COMPLEX_OBJ)

        def orjson_dumps():
            return orjson.dumps(COMPLEX_OBJ)

        time_ms = time_operation(orjson_dumps, iterations=5000)
        results.append(BenchmarkResult("orjson.dumps()", time_ms, category=CATEGORY))
        print_result("orjson.dumps()", time_ms)

        def orjson_loads():
            return orjson.loads(orjson_data)

        time_ms = time_operation(orjson_loads, iterations=5000)
        results.append(BenchmarkResult("orjson.loads()", time_ms, category=CATEGORY))
        print_result("orjson.loads()", time_ms)
    else:
        print("  orjson not installed, skipping")

    # -------------------------------------------------------------------------
    # msgspec (for comparison)
    # -------------------------------------------------------------------------
    print_subheader("msgspec (comparison)")

    if msgspec:
        msgspec_json_data = msgspec.json.encode(COMPLEX_OBJ)
        msgspec_msgpack_data = msgspec.msgpack.encode(COMPLEX_OBJ)

        def msgspec_json_encode():
            return msgspec.json.encode(COMPLEX_OBJ)

        time_ms = time_operation(msgspec_json_encode, iterations=5000)
        results.append(BenchmarkResult("msgspec.json.encode()", time_ms, category=CATEGORY))
        print_result("msgspec.json.encode()", time_ms)

        def msgspec_json_decode():
            return msgspec.json.decode(msgspec_json_data)

        time_ms = time_operation(msgspec_json_decode, iterations=5000)
        results.append(BenchmarkResult("msgspec.json.decode()", time_ms, category=CATEGORY))
        print_result("msgspec.json.decode()", time_ms)

        # msgpack (binary format like pickle)
        def msgspec_msgpack_encode():
            return msgspec.msgpack.encode(COMPLEX_OBJ)

        time_ms = time_operation(msgspec_msgpack_encode, iterations=5000)
        results.append(BenchmarkResult("msgspec.msgpack.encode()", time_ms, category=CATEGORY))
        print_result("msgspec.msgpack.encode()", time_ms)

        def msgspec_msgpack_decode():
            return msgspec.msgpack.decode(msgspec_msgpack_data)

        time_ms = time_operation(msgspec_msgpack_decode, iterations=5000)
        results.append(BenchmarkResult("msgspec.msgpack.decode()", time_ms, category=CATEGORY))
        print_result("msgspec.msgpack.decode()", time_ms)
    else:
        print("  msgspec not installed, skipping")

    # -------------------------------------------------------------------------
    # Size comparison
    # -------------------------------------------------------------------------
    print_subheader("Serialized Sizes")

    print(f"  pickle (default):  {len(PICKLE_DATA):>6} bytes")
    print(f"  pickle (proto=5):  {len(pickle.dumps(COMPLEX_OBJ, protocol=5)):>6} bytes")
    print(f"  json:              {len(JSON_DATA):>6} bytes")
    if orjson:
        print(f"  orjson:            {len(orjson.dumps(COMPLEX_OBJ)):>6} bytes")
    if msgspec:
        print(f"  msgspec json:      {len(msgspec.json.encode(COMPLEX_OBJ)):>6} bytes")
        print(f"  msgspec msgpack:   {len(msgspec.msgpack.encode(COMPLEX_OBJ)):>6} bytes")

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
