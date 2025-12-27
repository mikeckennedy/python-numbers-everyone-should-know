"""
Benchmark: Empty Python Process Memory

Measures the baseline memory usage of a Python process.
"""

import json
import resource
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.benchmark import (
    MemoryResult,
    print_header,
    print_result,
)


def measure_process_memory_mb() -> float:
    """
    Measure current process memory usage in MB using resource module.
    """
    usage = resource.getrusage(resource.RUSAGE_SELF)
    # ru_maxrss is in bytes on macOS, kilobytes on Linux
    if sys.platform == "darwin":
        return usage.ru_maxrss / (1024 * 1024)
    else:
        return usage.ru_maxrss / 1024


def run_benchmarks() -> dict:
    """Run empty process memory benchmark."""
    print_header("Empty Python Process Memory")

    memory_mb = measure_process_memory_mb()

    print_result("Python process memory", memory_mb, unit="MB")

    result = MemoryResult(
        name="empty_process",
        value=memory_mb,
        unit="MB",
        category="memory",
    )

    return {
        "category": "memory",
        "section": "empty_process",
        "results": [result.to_dict()],
    }


if __name__ == "__main__":
    results = run_benchmarks()
    print()
    print(json.dumps(results, indent=2))
