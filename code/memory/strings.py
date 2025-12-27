"""
Benchmark: String Memory Sizes

Measures the memory footprint of strings of various sizes.
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
)


def run_benchmarks() -> dict:
    """Run string memory benchmarks."""
    print_header('String Memory Sizes')

    results = []

    # Empty string
    empty_str = ''
    size = measure_size(empty_str)
    print_memory_result('Empty string ""', size)
    results.append(MemoryResult(name='empty_string', value=size, unit='bytes', category='memory'))

    # 1-character string
    one_char = 'a'
    size = measure_size(one_char)
    print_memory_result('1-char string "a"', size)
    results.append(MemoryResult(name='1_char_string', value=size, unit='bytes', category='memory'))

    # 10-character string
    ten_char = 'a' * 10
    size = measure_size(ten_char)
    print_memory_result('10-char string', size)
    results.append(MemoryResult(name='10_char_string', value=size, unit='bytes', category='memory'))

    # 100-character string
    hundred_char = 'a' * 100
    size = measure_size(hundred_char)
    print_memory_result('100-char string', size)
    results.append(MemoryResult(name='100_char_string', value=size, unit='bytes', category='memory'))

    # 1000-character string
    thousand_char = 'a' * 1000
    size = measure_size(thousand_char)
    print_memory_result('1000-char string', size)
    results.append(MemoryResult(name='1000_char_string', value=size, unit='bytes', category='memory'))

    return {
        'category': 'memory',
        'section': 'strings',
        'results': [r.to_dict() for r in results],
    }


if __name__ == '__main__':
    results = run_benchmarks()
    print()
    print(json.dumps(results, indent=2))
