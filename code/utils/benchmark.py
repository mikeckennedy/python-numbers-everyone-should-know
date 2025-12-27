"""
Shared benchmark utilities for Python Numbers Everyone Should Know.

Provides timing, memory measurement, colored output, and result formatting.
"""

import gc
import statistics
import sys
import timeit
from dataclasses import dataclass
from time import perf_counter_ns
from typing import Any, Callable, Optional

from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)


# =============================================================================
# Standard Test Objects
# =============================================================================

SIMPLE_OBJ = {"id": 123, "name": "Alice", "active": True}

COMPLEX_OBJ = {
    "id": 12345,
    "username": "alice_dev",
    "email": "alice@example.com",
    "profile": {
        "bio": "Software engineer who loves Python",
        "location": "Portland, OR",
        "website": "https://alice.dev",
        "joined": "2020-03-15T08:30:00Z",
    },
    "posts": [
        {"id": 1, "title": "First Post", "tags": ["python", "tutorial"], "views": 1520},
        {"id": 2, "title": "Second Post", "tags": ["rust", "wasm"], "views": 843},
        {"id": 3, "title": "Third Post", "tags": ["python", "async"], "views": 2341},
    ],
    "settings": {"theme": "dark", "notifications": True, "email_frequency": "weekly"},
}

# Alias for database benchmarks
USER_DATA = COMPLEX_OBJ


# =============================================================================
# Result Data Structures
# =============================================================================


@dataclass
class BenchmarkResult:
    """Single benchmark measurement result."""

    name: str
    value: float  # Always in milliseconds
    unit: str = "ms"
    category: str = ""
    details: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        result = {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
        }
        if self.category:
            result["category"] = self.category
        if self.details:
            result["details"] = self.details
        return result


@dataclass
class MemoryResult:
    """Memory measurement result."""

    name: str
    value: float  # In bytes or MB depending on context
    unit: str  # "bytes" or "MB"
    category: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "category": self.category,
        }


# =============================================================================
# Timing Utilities
# =============================================================================


def time_operation(
    func: Callable[[], Any],
    iterations: int = 1000,
    warmup: int = 100,
    repeat: int = 5,
) -> float:
    """
    Time an operation and return median time in milliseconds.

    Args:
        func: Zero-argument callable to time
        iterations: Number of iterations per timing run
        warmup: Number of warmup iterations before timing
        repeat: Number of timing runs to take median of

    Returns:
        Median time per operation in milliseconds
    """
    # Warmup - capture results to prevent optimizer elimination
    result = None
    for _ in range(warmup):
        result = func()

    # Collect garbage before timing
    gc.collect()

    # Disable GC during timing to prevent interference
    gc.disable()
    try:
        # Time multiple runs
        times = []
        for _ in range(repeat):
            start = perf_counter_ns()
            for _ in range(iterations):
                result = func()
            end = perf_counter_ns()
            # Calculate per-operation time in milliseconds
            time_per_op_ms = (end - start) / iterations / 1_000_000
            times.append(time_per_op_ms)

        return statistics.median(times)
    finally:
        # Re-enable GC
        gc.enable()


def time_operation_ns(
    func: Callable[[], Any],
    iterations: int = 1000,
    warmup: int = 100,
    repeat: int = 5,
) -> float:
    """
    Time an operation and return median time in nanoseconds.
    Useful for very fast operations, then convert to ms for display.

    Returns:
        Median time per operation in nanoseconds
    """
    # Warmup - capture results to prevent optimizer elimination
    result = None
    for _ in range(warmup):
        result = func()

    gc.collect()

    # Disable GC during timing to prevent interference
    gc.disable()
    try:
        times = []
        for _ in range(repeat):
            start = perf_counter_ns()
            for _ in range(iterations):
                result = func()
            end = perf_counter_ns()
            time_per_op_ns = (end - start) / iterations
            times.append(time_per_op_ns)

        return statistics.median(times)
    finally:
        # Re-enable GC
        gc.enable()


def ns_to_ms(ns: float) -> float:
    """Convert nanoseconds to milliseconds."""
    return ns / 1_000_000


def time_with_timeit(
    stmt: str,
    setup: str = "pass",
    globals_dict: Optional[dict] = None,
    number: int = 1000,
    repeat: int = 5,
) -> float:
    """
    Time a statement using timeit and return median time in milliseconds.

    Args:
        stmt: Statement to time
        setup: Setup code
        globals_dict: Global variables for the statement
        number: Number of executions per timing
        repeat: Number of timing runs

    Returns:
        Median time per operation in milliseconds
    """
    timer = timeit.Timer(stmt, setup, globals=globals_dict)

    # Warmup
    timer.timeit(number=100)

    gc.collect()

    # Time
    times = timer.repeat(repeat=repeat, number=number)
    # Convert to per-operation milliseconds
    times_per_op_ms = [t / number * 1000 for t in times]

    return statistics.median(times_per_op_ms)


# =============================================================================
# Memory Utilities
# =============================================================================


def measure_size(obj: Any) -> int:
    """
    Measure the size of an object in bytes using sys.getsizeof.

    Note: This only measures the immediate object, not referenced objects.
    """
    return sys.getsizeof(obj)


def measure_deep_size(obj: Any) -> int:
    """
    Measure the total memory of an object including all referenced objects.

    Uses recursive traversal with seen tracking to avoid double-counting.
    """
    seen = set()

    def _get_size(o: Any) -> int:
        # Avoid counting the same object twice
        obj_id = id(o)
        if obj_id in seen:
            return 0
        seen.add(obj_id)

        size = sys.getsizeof(o)

        # Recursively get size of contents
        if isinstance(o, dict):
            size += sum(_get_size(k) + _get_size(v) for k, v in o.items())
        elif isinstance(o, (list, tuple, set, frozenset)):
            size += sum(_get_size(item) for item in o)
        elif hasattr(o, "__dict__"):
            size += _get_size(o.__dict__)
        elif hasattr(o, "__slots__"):
            size += sum(
                _get_size(getattr(o, slot))
                for slot in o.__slots__
                if hasattr(o, slot)
            )

        return size

    return _get_size(obj)


def measure_process_memory_mb() -> float:
    """
    Measure current process memory usage in MB.
    """
    import resource

    # Returns memory in bytes on macOS
    usage = resource.getrusage(resource.RUSAGE_SELF)
    # ru_maxrss is in bytes on macOS, kilobytes on Linux
    if sys.platform == "darwin":
        return usage.ru_maxrss / (1024 * 1024)
    else:
        return usage.ru_maxrss / 1024


# =============================================================================
# Output Formatting
# =============================================================================


def format_ms(ms: float, width: int = 12) -> str:
    """Format milliseconds value for display."""
    if ms < 0.000001:
        return f"{ms:.9f}".rjust(width)
    elif ms < 0.001:
        return f"{ms:.6f}".rjust(width)
    elif ms < 1:
        return f"{ms:.4f}".rjust(width)
    else:
        return f"{ms:.2f}".rjust(width)


def format_bytes(b: int) -> str:
    """Format bytes for display."""
    if b < 1024:
        return f"{b} bytes"
    elif b < 1024 * 1024:
        return f"{b / 1024:.2f} KB"
    else:
        return f"{b / (1024 * 1024):.2f} MB"


def print_header(title: str) -> None:
    """Print a colored section header."""
    print()
    print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 60}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{title.center(60)}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 60}")
    print()


def print_subheader(title: str) -> None:
    """Print a colored subsection header."""
    print()
    print(f"{Fore.YELLOW}{Style.BRIGHT}{title}")
    print(f"{Fore.YELLOW}{'-' * len(title)}")


def print_result(
    name: str, value: float, unit: str = "ms", name_width: int = 40
) -> None:
    """Print a single benchmark result with color."""
    formatted_name = name.ljust(name_width)
    if unit == "ms":
        formatted_value = format_ms(value)
    elif unit == "bytes":
        formatted_value = format_bytes(int(value))
    else:
        formatted_value = f"{value:.2f} {unit}"

    print(f"{Fore.WHITE}{formatted_name} {Fore.GREEN}{formatted_value}")


def print_memory_result(name: str, size_bytes: int, name_width: int = 40) -> None:
    """Print a memory measurement result."""
    formatted_name = name.ljust(name_width)
    formatted_value = format_bytes(size_bytes)
    print(f"{Fore.WHITE}{formatted_name} {Fore.MAGENTA}{formatted_value}")


def print_comparison_table(
    headers: list[str],
    rows: list[list[str]],
    col_widths: Optional[list[int]] = None,
) -> None:
    """Print a formatted comparison table."""
    if col_widths is None:
        col_widths = [
            max(len(str(row[i])) for row in [headers] + rows) + 2
            for i in range(len(headers))
        ]

    # Header
    header_line = ""
    for i, h in enumerate(headers):
        header_line += f"{Fore.CYAN}{Style.BRIGHT}{str(h).ljust(col_widths[i])}"
    print(header_line)

    # Separator
    sep_line = ""
    for w in col_widths:
        sep_line += f"{Fore.CYAN}{'-' * w}"
    print(sep_line)

    # Rows
    for row in rows:
        row_line = ""
        for i, cell in enumerate(row):
            if i == 0:
                row_line += f"{Fore.WHITE}{str(cell).ljust(col_widths[i])}"
            else:
                row_line += f"{Fore.GREEN}{str(cell).ljust(col_widths[i])}"
        print(row_line)


def print_skip_message(library: str, reason: str = "not installed") -> None:
    """Print a skip message for unavailable libraries."""
    print(f"{Fore.YELLOW}⚠ Skipping {library}: {reason}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"{Fore.RED}✗ Error: {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"{Fore.GREEN}✓ {message}")


# =============================================================================
# Library Import Helpers
# =============================================================================


def try_import(module_name: str) -> Optional[Any]:
    """
    Try to import a module, returning None if not available.

    Usage:
        orjson = try_import("orjson")
        if orjson:
            # use orjson
    """
    try:
        import importlib

        return importlib.import_module(module_name)
    except ImportError:
        return None


def require_import(module_name: str) -> Any:
    """
    Import a module or raise with helpful error message.
    """
    module = try_import(module_name)
    if module is None:
        raise ImportError(
            f"Required module '{module_name}' is not installed. "
            f"Run: uv pip install {module_name}"
        )
    return module


# =============================================================================
# Benchmark Runner Helpers
# =============================================================================


def run_benchmarks(
    benchmarks: list[tuple[str, Callable[[], Any]]],
    category: str = "",
    iterations: int = 1000,
) -> list[BenchmarkResult]:
    """
    Run a list of benchmarks and return results.

    Args:
        benchmarks: List of (name, function) tuples
        category: Category name for results
        iterations: Number of iterations per benchmark

    Returns:
        List of BenchmarkResult objects
    """
    results = []
    for name, func in benchmarks:
        try:
            time_ms = time_operation(func, iterations=iterations)
            result = BenchmarkResult(name=name, value=time_ms, category=category)
            results.append(result)
            print_result(name, time_ms)
        except Exception as e:
            print_error(f"{name}: {e}")
    return results


def collect_results(
    category: str,
    results: list[BenchmarkResult | MemoryResult],
) -> dict[str, Any]:
    """
    Collect results into a dictionary structure for JSON output.
    """
    return {
        "category": category,
        "results": [r.to_dict() for r in results],
    }
