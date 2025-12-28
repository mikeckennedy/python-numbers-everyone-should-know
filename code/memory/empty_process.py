"""
Benchmark: Empty Python Process Memory

Measures the baseline memory usage of a fresh Python process by spawning
a subprocess that only measures its own memory - avoiding the overhead
of the benchmark suite imports.
"""

import statistics
import subprocess
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.benchmark import (
    MemoryResult,
    print_header,
    print_result,
)

# Number of subprocess runs to get stable measurement
ITERATIONS = 5


def measure_empty_process_memory_mb() -> float:
    """
    Measure memory of a fresh Python process by spawning a subprocess.

    Returns median memory in MB across multiple runs.
    """
    # Minimal Python code to measure just the process's own memory
    code = """
import resource
import sys

usage = resource.getrusage(resource.RUSAGE_SELF)
# ru_maxrss is in bytes on macOS, kilobytes on Linux
if sys.platform == 'darwin':
    memory_mb = usage.ru_maxrss / (1024 * 1024)
else:
    memory_mb = usage.ru_maxrss / 1024

print(memory_mb)
"""

    measurements = []

    for _ in range(ITERATIONS):
        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            memory_mb = float(result.stdout.strip())
            measurements.append(memory_mb)

    if measurements:
        return statistics.median(measurements)

    raise RuntimeError('Failed to measure subprocess memory')


def run_benchmarks() -> dict:
    """Run empty process memory benchmark."""
    print_header('Empty Python Process Memory')
    print('  (Measured in fresh subprocess)')

    memory_mb = measure_empty_process_memory_mb()

    print_result('Python process memory', memory_mb, unit='MB')

    result = MemoryResult(
        name='empty_process',
        value=memory_mb,
        unit='MB',
        category='memory',
    )

    return {
        'category': 'memory',
        'section': 'empty_process',
        'results': [result.to_dict()],
    }


if __name__ == '__main__':
    import json

    results = run_benchmarks()
    print()
    print(json.dumps(results, indent=2))
