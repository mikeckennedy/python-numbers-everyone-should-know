"""
Benchmark: Class Instance Memory Sizes

Measures the memory footprint of different class types and instances.
"""

import json
import sys
from collections import namedtuple
from dataclasses import dataclass
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


# Regular class
class RegularClass:
    def __init__(self, a=None, b=None, c=None, d=None, e=None):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e


# Regular class with no attributes
class RegularClassEmpty:
    pass


# Slots class
class SlotsClass:
    __slots__ = ['a', 'b', 'c', 'd', 'e']

    def __init__(self, a=None, b=None, c=None, d=None, e=None):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e


# Slots class with no attributes
class SlotsClassEmpty:
    __slots__ = []


# Regular dataclass
@dataclass
class RegularDataclass:
    a: int = 0
    b: int = 0
    c: int = 0
    d: int = 0
    e: int = 0


# Slots dataclass
@dataclass(slots=True)
class SlotsDataclass:
    a: int = 0
    b: int = 0
    c: int = 0
    d: int = 0
    e: int = 0


# Named tuple
PersonTuple = namedtuple('PersonTuple', ['a', 'b', 'c', 'd', 'e'])


def run_benchmarks() -> dict:
    """Run class memory benchmarks."""
    print_header('Class Instance Memory Sizes')

    results: list[MemoryResult] = []

    # Regular class
    print_subheader('Regular Class')

    empty_regular = RegularClassEmpty()
    size = measure_deep_size(empty_regular)
    print_memory_result('Regular class (empty)', size)
    results.append(MemoryResult(name='regular_class_empty', value=size, unit='bytes', category='memory'))

    # Need to also measure __dict__
    dict_size = measure_deep_size(empty_regular.__dict__)
    print_memory_result('  └─ __dict__ overhead', dict_size)

    # We are using dynamically created numbers outside of [-5, 255] to avoid 
    # Python's caching and reuse of these ints.

    regular_5attr = RegularClass(int('1000'), int('1001'), int('1002'), int('1003'), int('1004'))
    size = measure_deep_size(regular_5attr)
    print_memory_result('Regular class (5 attrs)', size)
    results.append(MemoryResult(name='regular_class_5attr', value=size, unit='bytes', category='memory'))

    dict_size = measure_deep_size(regular_5attr.__dict__)
    print_memory_result('  └─ __dict__ overhead', dict_size)

    # Slots class
    print_subheader('__slots__ Class')

    empty_slots = SlotsClassEmpty()
    size = measure_deep_size(empty_slots)
    print_memory_result('Slots class (empty)', size)
    results.append(MemoryResult(name='slots_class_empty', value=size, unit='bytes', category='memory'))

    slots_5attr = SlotsClass(int('1000'), int('1001'), int('1002'), int('1003'), int('1004'))
    size = measure_deep_size(slots_5attr)
    print_memory_result('Slots class (5 attrs)', size)
    results.append(MemoryResult(name='slots_class_5attr', value=size, unit='bytes', category='memory'))

    # Dataclass
    print_subheader('Dataclass')

    dataclass_5attr = RegularDataclass(int('1000'), int('1001'), int('1002'), int('1003'), int('1004'))
    size = measure_deep_size(dataclass_5attr)
    print_memory_result('Dataclass (5 attrs)', size)
    results.append(MemoryResult(name='dataclass_5attr', value=size, unit='bytes', category='memory'))

    dict_size = measure_deep_size(dataclass_5attr.__dict__)
    print_memory_result('  └─ __dict__ overhead', dict_size)

    # Slots dataclass
    print_subheader('Slots Dataclass')

    slots_dataclass_5attr = SlotsDataclass(int('1000'), int('1001'), int('1002'), int('1003'), int('1004'))
    size = measure_deep_size(slots_dataclass_5attr)
    print_memory_result('Slots dataclass (5 attrs)', size)
    results.append(MemoryResult(name='slots_dataclass_5attr', value=size, unit='bytes', category='memory'))

    # Named tuple
    print_subheader('Named Tuple')

    named_tuple_5attr = PersonTuple(int('1000'), int('1001'), int('1002'), int('1003'), int('1004'))
    size = measure_deep_size(named_tuple_5attr)
    print_memory_result('Named tuple (5 attrs)', size)
    results.append(MemoryResult(name='namedtuple_5attr', value=size, unit='bytes', category='memory'))

    # Lists of 1000 instances
    print_subheader('Lists of 1000 Instances')

    regular_list = [
        RegularClass(
            int('1000') + 5 * i, int('1001') + 5 * i, int('1002') + 5 * i, int('1003') + 5 * i, int('1004') + 5 * i
        )
        for i in range(1_000)
    ]
    size = measure_deep_size(regular_list)
    print_memory_result('List of 1000 regular class instances', size)
    results.append(MemoryResult(name='list_1000_regular_class', value=size, unit='bytes', category='memory'))

    slots_list = [
        SlotsClass(
            int('1000') + 5 * i, int('1001') + 5 * i, int('1002') + 5 * i, int('1003') + 5 * i, int('1004') + 5 * i
        )
        for i in range(1_000)
    ]
    size = measure_deep_size(slots_list)
    print_memory_result('List of 1000 __slots__ class instances', size)
    results.append(MemoryResult(name='list_1000_slots_class', value=size, unit='bytes', category='memory'))

    return {
        'category': 'memory',
        'section': 'classes',
        'results': [r.to_dict() for r in results],
    }


if __name__ == '__main__':
    results = run_benchmarks()
    print()
    print(json.dumps(results, indent=2))
