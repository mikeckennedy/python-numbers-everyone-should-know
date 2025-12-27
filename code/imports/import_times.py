"""
Import time benchmarks.

Measures the time to import various modules by running each import
in a fresh subprocess to avoid caching effects.

Tests:
- Built-in modules (json, os, sys)
- Standard library (pathlib, dataclasses, typing)
- Local module (small .py file)
- Small external package (diskcache)
- Rust-based external package (pydantic)
- Large external package (django)
"""

import statistics
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.benchmark import (
    BenchmarkResult,
    collect_results,
    print_header,
    print_result,
    print_skip_message,
    print_subheader,
)

CATEGORY = "import_times"

# Number of subprocess runs for each import
ITERATIONS = 10
WARMUP = 2


def time_import_subprocess(module_name: str, from_import: str = None) -> float | None:
    """
    Time an import by running it in a fresh subprocess.

    Returns median time in milliseconds, or None if import fails.
    """
    if from_import:
        import_stmt = f"from {module_name} import {from_import}"
    else:
        import_stmt = f"import {module_name}"

    # Python code to time the import
    code = f'''
import time
start = time.perf_counter_ns()
{import_stmt}
end = time.perf_counter_ns()
print((end - start) / 1_000_000)  # Convert to ms
'''

    times = []

    # Warmup runs (not counted)
    for _ in range(WARMUP):
        try:
            subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=30,
            )
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            pass

    # Timed runs
    for _ in range(ITERATIONS):
        try:
            result = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0 and result.stdout.strip():
                time_ms = float(result.stdout.strip())
                times.append(time_ms)
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, ValueError):
            continue

    if len(times) >= 3:
        return statistics.median(times)
    return None


def check_module_available(module_name: str) -> bool:
    """Check if a module can be imported."""
    code = f"import {module_name}"
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        timeout=30,
    )
    return result.returncode == 0


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all import time benchmarks."""
    results = []

    print_header("Import Time Benchmarks")
    print("  (Each import timed in fresh subprocess)")

    # -------------------------------------------------------------------------
    # Built-in Modules (compiled into Python)
    # -------------------------------------------------------------------------
    print_subheader("Built-in Modules")

    builtins = [
        ("sys", "sys (built-in)"),
        ("os", "os"),
        ("json", "json"),
        ("math", "math"),
        ("time", "time"),
    ]

    for module, label in builtins:
        time_ms = time_import_subprocess(module)
        if time_ms is not None:
            results.append(BenchmarkResult(f"import {label}", time_ms, category=CATEGORY))
            print_result(f"import {label}", time_ms)

    # -------------------------------------------------------------------------
    # Standard Library (pure Python)
    # -------------------------------------------------------------------------
    print_subheader("Standard Library")

    stdlib = [
        ("pathlib", "pathlib"),
        ("dataclasses", "dataclasses"),
        ("typing", "typing"),
        ("collections", "collections"),
        ("datetime", "datetime"),
        ("re", "re"),
        ("logging", "logging"),
        ("urllib.parse", "urllib.parse"),
        ("asyncio", "asyncio"),
        ("sqlite3", "sqlite3"),
    ]

    for module, label in stdlib:
        time_ms = time_import_subprocess(module)
        if time_ms is not None:
            results.append(BenchmarkResult(f"import {label}", time_ms, category=CATEGORY))
            print_result(f"import {label}", time_ms)

    # -------------------------------------------------------------------------
    # Local Module
    # -------------------------------------------------------------------------
    print_subheader("Local Module")

    # Create a test that imports our local module
    local_module_path = Path(__file__).parent / "local_module.py"
    if local_module_path.exists():
        # We need to run from the imports directory for relative import to work
        code = f'''
import sys
sys.path.insert(0, "{local_module_path.parent}")
import time
start = time.perf_counter_ns()
import local_module
end = time.perf_counter_ns()
print((end - start) / 1_000_000)
'''
        times = []
        for _ in range(WARMUP):
            subprocess.run([sys.executable, "-c", code], capture_output=True, timeout=30)
        for _ in range(ITERATIONS):
            result = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0 and result.stdout.strip():
                times.append(float(result.stdout.strip()))

        if times:
            time_ms = statistics.median(times)
            results.append(BenchmarkResult("import local_module (small .py)", time_ms, category=CATEGORY))
            print_result("import local_module (small .py)", time_ms)

    # -------------------------------------------------------------------------
    # External Packages - Small
    # -------------------------------------------------------------------------
    print_subheader("External Packages (Small)")

    small_packages = [
        ("colorama", "colorama"),
        ("diskcache", "diskcache"),
    ]

    for module, label in small_packages:
        if check_module_available(module):
            time_ms = time_import_subprocess(module)
            if time_ms is not None:
                results.append(BenchmarkResult(f"import {label}", time_ms, category=CATEGORY))
                print_result(f"import {label}", time_ms)
        else:
            print_skip_message(label, "not installed")

    # -------------------------------------------------------------------------
    # External Packages - Rust-based
    # -------------------------------------------------------------------------
    print_subheader("External Packages (Rust-based)")

    rust_packages = [
        ("pydantic", "pydantic"),
        ("orjson", "orjson"),
        ("msgspec", "msgspec"),
    ]

    for module, label in rust_packages:
        if check_module_available(module):
            time_ms = time_import_subprocess(module)
            if time_ms is not None:
                results.append(BenchmarkResult(f"import {label}", time_ms, category=CATEGORY))
                print_result(f"import {label}", time_ms)
        else:
            print_skip_message(label, "not installed")

    # -------------------------------------------------------------------------
    # External Packages - Large
    # -------------------------------------------------------------------------
    print_subheader("External Packages (Large)")

    large_packages = [
        ("django", "django"),
        ("flask", "flask"),
        ("fastapi", "fastapi"),
        ("starlette", "starlette"),
        ("litestar", "litestar"),
    ]

    for module, label in large_packages:
        if check_module_available(module):
            time_ms = time_import_subprocess(module)
            if time_ms is not None:
                results.append(BenchmarkResult(f"import {label}", time_ms, category=CATEGORY))
                print_result(f"import {label}", time_ms)
        else:
            print_skip_message(label, "not installed")

    # -------------------------------------------------------------------------
    # Comparison: from X import Y
    # -------------------------------------------------------------------------
    print_subheader("From Import Comparison")

    # Compare 'import X' vs 'from X import Y'
    if check_module_available("pydantic"):
        time_ms = time_import_subprocess("pydantic", "BaseModel")
        if time_ms is not None:
            results.append(BenchmarkResult("from pydantic import BaseModel", time_ms, category=CATEGORY))
            print_result("from pydantic import BaseModel", time_ms)

    if check_module_available("django"):
        # Just importing django.conf is faster than full django
        time_ms = time_import_subprocess("django.conf", "settings")
        if time_ms is not None:
            results.append(BenchmarkResult("from django.conf import settings", time_ms, category=CATEGORY))
            print_result("from django.conf import settings", time_ms)

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
