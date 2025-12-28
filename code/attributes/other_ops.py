"""
Other attribute operation benchmarks.

Measures:
- Read @property
- getattr(obj, 'attr')
- hasattr(obj, 'attr')
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.benchmark import (
    BenchmarkResult,
    collect_results,
    print_header,
    print_result,
    print_subheader,
    time_operation,
)

CATEGORY = 'attribute_other_ops'


# =============================================================================
# Test Classes
# =============================================================================


class ClassWithProperty:
    """Class with @property decorator."""

    def __init__(self, value):
        self._value = value
        self._cached = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def computed(self):
        """Property that does a simple computation."""
        return self._value * 2

    @property
    def cached_property_manual(self):
        """Manually cached property pattern."""
        if self._cached is None:
            self._cached = self._value * 2
        return self._cached


class SimpleClass:
    """Simple class for getattr/hasattr tests."""

    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3
        self.d = 4
        self.e = 5


class ClassWithSlots:
    """Slots class for getattr/hasattr comparison."""

    __slots__ = ('a', 'b', 'c', 'd', 'e')

    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3
        self.d = 4
        self.e = 5


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all other attribute operation benchmarks."""
    results = []

    print_header('Other Attribute Operations')

    # Create test instances
    prop_obj = ClassWithProperty(42)
    simple_obj = SimpleClass()
    slots_obj = ClassWithSlots()

    # -------------------------------------------------------------------------
    # @property
    # -------------------------------------------------------------------------
    print_subheader('@property Access')

    def read_property():
        return prop_obj.value

    time_ms = time_operation(read_property, iterations=10_000)
    results.append(BenchmarkResult('@property: read', time_ms, category=CATEGORY))
    print_result('@property: read', time_ms)

    def write_property():
        prop_obj.value = 100

    time_ms = time_operation(write_property, iterations=10_000)
    results.append(BenchmarkResult('@property: write (setter)', time_ms, category=CATEGORY))
    print_result('@property: write (setter)', time_ms)

    def read_computed_property():
        return prop_obj.computed

    time_ms = time_operation(read_computed_property, iterations=10_000)
    results.append(BenchmarkResult('@property: computed', time_ms, category=CATEGORY))
    print_result('@property: computed', time_ms)

    def read_cached_property():
        return prop_obj.cached_property_manual

    time_ms = time_operation(read_cached_property, iterations=10_000)
    results.append(BenchmarkResult('@property: cached (manual)', time_ms, category=CATEGORY))
    print_result('@property: cached (manual)', time_ms)

    # Compare to direct attribute access
    def read_direct():
        return prop_obj._value

    time_ms = time_operation(read_direct, iterations=10_000)
    results.append(BenchmarkResult('direct attr (comparison)', time_ms, category=CATEGORY))
    print_result('direct attr (comparison)', time_ms)

    # -------------------------------------------------------------------------
    # getattr()
    # -------------------------------------------------------------------------
    print_subheader('getattr()')

    def getattr_regular():
        return simple_obj.a

    time_ms = time_operation(getattr_regular, iterations=10_000)
    results.append(BenchmarkResult("getattr(obj, 'attr')", time_ms, category=CATEGORY))
    print_result("getattr(obj, 'attr')", time_ms)

    def getattr_slots():
        return slots_obj.a

    time_ms = time_operation(getattr_slots, iterations=10_000)
    results.append(BenchmarkResult("getattr(slots_obj, 'attr')", time_ms, category=CATEGORY))
    print_result("getattr(slots_obj, 'attr')", time_ms)

    def getattr_with_default():
        return getattr(simple_obj, 'missing', None)

    time_ms = time_operation(getattr_with_default, iterations=10_000)
    results.append(BenchmarkResult("getattr(obj, 'missing', default)", time_ms, category=CATEGORY))
    print_result("getattr(obj, 'missing', default)", time_ms)

    # Compare to direct access
    def direct_access():
        return simple_obj.a

    time_ms = time_operation(direct_access, iterations=10_000)
    results.append(BenchmarkResult('obj.attr (comparison)', time_ms, category=CATEGORY))
    print_result('obj.attr (comparison)', time_ms)

    # -------------------------------------------------------------------------
    # hasattr()
    # -------------------------------------------------------------------------
    print_subheader('hasattr()')

    def hasattr_existing():
        return hasattr(simple_obj, 'a')

    time_ms = time_operation(hasattr_existing, iterations=10_000)
    results.append(BenchmarkResult("hasattr(obj, 'existing')", time_ms, category=CATEGORY))
    print_result("hasattr(obj, 'existing')", time_ms)

    def hasattr_missing():
        return hasattr(simple_obj, 'missing')

    time_ms = time_operation(hasattr_missing, iterations=10_000)
    results.append(BenchmarkResult("hasattr(obj, 'missing')", time_ms, category=CATEGORY))
    print_result("hasattr(obj, 'missing')", time_ms)

    def hasattr_slots_existing():
        return hasattr(slots_obj, 'a')

    time_ms = time_operation(hasattr_slots_existing, iterations=10_000)
    results.append(BenchmarkResult("hasattr(slots_obj, 'existing')", time_ms, category=CATEGORY))
    print_result("hasattr(slots_obj, 'existing')", time_ms)

    def hasattr_slots_missing():
        return hasattr(slots_obj, 'missing')

    time_ms = time_operation(hasattr_slots_missing, iterations=10_000)
    results.append(BenchmarkResult("hasattr(slots_obj, 'missing')", time_ms, category=CATEGORY))
    print_result("hasattr(slots_obj, 'missing')", time_ms)

    # -------------------------------------------------------------------------
    # setattr()
    # -------------------------------------------------------------------------
    print_subheader('setattr()')

    def setattr_regular():
        setattr(simple_obj, 'a', 100)

    time_ms = time_operation(setattr_regular, iterations=10_000)
    results.append(BenchmarkResult("setattr(obj, 'attr', val)", time_ms, category=CATEGORY))
    print_result("setattr(obj, 'attr', val)", time_ms)

    def setattr_slots():
        setattr(slots_obj, 'a', 100)

    time_ms = time_operation(setattr_slots, iterations=10_000)
    results.append(BenchmarkResult("setattr(slots_obj, 'attr', val)", time_ms, category=CATEGORY))
    print_result("setattr(slots_obj, 'attr', val)", time_ms)

    # Compare to direct assignment
    def direct_assign():
        simple_obj.a = 100

    time_ms = time_operation(direct_assign, iterations=10_000)
    results.append(BenchmarkResult('obj.attr = val (comparison)', time_ms, category=CATEGORY))
    print_result('obj.attr = val (comparison)', time_ms)

    return results


def main():
    """Run benchmarks and output results."""
    results = run_benchmarks()
    output = collect_results(CATEGORY, results)  # type: ignore

    print()
    print(f'Total benchmarks: {len(results)}')

    return output


if __name__ == '__main__':
    main()
