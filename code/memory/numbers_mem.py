"""
Benchmark: Number Memory Sizes

Measures the memory footprint of integers and floats.
"""

import json
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.benchmark import (
    MemoryResult,
    measure_size,
    print_header,
    print_memory_result,
    print_subheader,
)


def run_benchmarks() -> dict:
    """Run number memory benchmarks."""
    print_header('Number Memory Sizes')

    results: list[MemoryResult] = []

    # Integers
    print_subheader('Integers')

    # Small int (0-256 range, cached by Python)
    small_int = 42
    size = measure_size(small_int)
    print_memory_result('Small int (42, cached range)', size)
    results.append(MemoryResult(name='small_int', value=size, unit='bytes', category='memory'))

    # Boundary int (just outside cache)
    boundary_int = 257
    size = measure_size(boundary_int)
    print_memory_result('Boundary int (257)', size)
    results.append(MemoryResult(name='boundary_int', value=size, unit='bytes', category='memory'))

    # Large int
    large_int = 1_000
    size = measure_size(large_int)
    print_memory_result('Large int (1,000)', size)
    results.append(MemoryResult(name='large_int', value=size, unit='bytes', category='memory'))

    # Very large int
    very_large_int = 10**20
    size = measure_size(very_large_int)
    print_memory_result('Very large int (10^20)', size)
    results.append(MemoryResult(name='very_large_int_20', value=size, unit='bytes', category='memory'))

    # Huge int
    huge_int = 10**100
    size = measure_size(huge_int)
    print_memory_result('Huge int (10^100)', size)
    results.append(MemoryResult(name='huge_int_100', value=size, unit='bytes', category='memory'))

    # Floats
    print_subheader('Floats')

    # Float
    f = 3.14159
    size = measure_size(f)
    print_memory_result('Float (3.14159)', size)
    results.append(MemoryResult(name='float', value=size, unit='bytes', category='memory'))

    # Large float
    large_float = 1.0e308
    size = measure_size(large_float)
    print_memory_result('Large float (1e308)', size)
    results.append(MemoryResult(name='large_float', value=size, unit='bytes', category='memory'))

    return {
        'category': 'memory',
        'section': 'numbers',
        'results': [r.to_dict() for r in results],
    }


if __name__ == '__main__':
    results = run_benchmarks()
    print()
    print(json.dumps(results, indent=2))
