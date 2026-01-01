"""
Benchmark: Collection Memory Sizes

Measures the memory footprint of lists, dicts, and sets.
"""

import json
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.benchmark import (
    MemoryResult,
    measure_deep_size,
    print_header,
    print_memory_result,
    print_subheader,
)


def run_benchmarks() -> dict:
    """Run collection memory benchmarks."""
    print_header('Collection Memory Sizes')

    results: list[MemoryResult] = []

    # Lists
    print_subheader('Lists')

    empty_list = []
    size = measure_deep_size(empty_list)
    print_memory_result('Empty list []', size)
    results.append(MemoryResult(name='empty_list', value=size, unit='bytes', category='memory'))

    list_10 = list(range(10))
    size = measure_deep_size(list_10)
    print_memory_result('List with 10 ints (including elements)', size)
    results.append(MemoryResult(name='list_10_container', value=size, unit='bytes', category='memory'))

    list_100 = list(range(100))
    size = measure_deep_size(list_100)
    print_memory_result('List with 100 ints (including elements)', size)
    results.append(MemoryResult(name='list_100_container', value=size, unit='bytes', category='memory'))

    list_1000 = list(range(1_000))
    size = measure_deep_size(list_1000)
    print_memory_result('List with 1000 ints (including elements)', size)
    results.append(MemoryResult(name='list_1000_container', value=size, unit='bytes', category='memory'))

    list_1000_floats = list(float(i) for i in range(1_000))
    size = measure_deep_size(list_1000_floats)
    print_memory_result('List with 1000 floats (including elements)', size)
    results.append(MemoryResult(name='list_1000_floats_container', value=size, unit='bytes', category='memory'))

    # Dicts
    print_subheader('Dicts')

    empty_dict = {}
    size = measure_deep_size(empty_dict)
    print_memory_result('Empty dict {}', size)
    results.append(MemoryResult(name='empty_dict', value=size, unit='bytes', category='memory'))

    dict_10 = {i: i for i in range(10)}
    size = measure_deep_size(dict_10)
    print_memory_result('Dict with 10 items (including elements)', size)
    results.append(MemoryResult(name='dict_10_container', value=size, unit='bytes', category='memory'))

    dict_100 = {i: i for i in range(100)}
    size = measure_deep_size(dict_100)
    print_memory_result('Dict with 100 items (including elements)', size)
    results.append(MemoryResult(name='dict_100_container', value=size, unit='bytes', category='memory'))

    dict_1000 = {i: i for i in range(1_000)}
    size = measure_deep_size(dict_1000)
    print_memory_result('Dict with 1000 items (including elements)', size)
    results.append(MemoryResult(name='dict_1000_container', value=size, unit='bytes', category='memory'))

    # Sets
    print_subheader('Sets')

    empty_set = set()
    size = measure_deep_size(empty_set)
    print_memory_result('Empty set()', size)
    results.append(MemoryResult(name='empty_set', value=size, unit='bytes', category='memory'))

    set_10 = set(range(10))
    size = measure_deep_size(set_10)
    print_memory_result('Set with 10 items (including elements)', size)
    results.append(MemoryResult(name='set_10_container', value=size, unit='bytes', category='memory'))

    set_100 = set(range(100))
    size = measure_deep_size(set_100)
    print_memory_result('Set with 100 items (including elements)', size)
    results.append(MemoryResult(name='set_100_container', value=size, unit='bytes', category='memory'))

    set_1000 = set(range(1_000))
    size = measure_deep_size(set_1000)
    print_memory_result('Set with 1000 items (including elements)', size)
    results.append(MemoryResult(name='set_1000_container', value=size, unit='bytes', category='memory'))

    return {
        'category': 'memory',
        'section': 'collections',
        'results': [r.to_dict() for r in results],
    }


if __name__ == '__main__':
    results = run_benchmarks()
    print()
    print(json.dumps(results, indent=2))
