"""
Type checking overhead benchmarks.

Measures:
- isinstance() checks
- type() == type comparisons
- issubclass() checks
- hasattr() checks
- callable() checks
"""

import sys
from abc import ABC, abstractmethod
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

CATEGORY = "functions_type_checking"


# =============================================================================
# Test Classes
# =============================================================================


class BaseClass:
    """Base class for inheritance tests."""
    pass


class DerivedClass(BaseClass):
    """Derived class for inheritance tests."""
    pass


class DeepDerived(DerivedClass):
    """Deeply derived class (3 levels)."""
    pass


class AbstractBase(ABC):
    """Abstract base class."""

    @abstractmethod
    def method(self):
        pass


class ConcreteClass(AbstractBase):
    """Concrete implementation."""

    def method(self):
        pass


class ClassWithSlots:
    """Class with __slots__."""
    __slots__ = ["x", "y", "z"]

    def __init__(self):
        self.x = 1
        self.y = 2
        self.z = 3


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all type checking benchmarks."""
    results = []

    print_header("Type Checking Benchmarks")

    # Test objects
    obj = DerivedClass()
    deep_obj = DeepDerived()
    concrete_obj = ConcreteClass()
    slots_obj = ClassWithSlots()
    test_str = "hello"
    test_int = 42
    test_list = [1, 2, 3]
    test_dict = {"a": 1}

    # -------------------------------------------------------------------------
    # isinstance() Checks
    # -------------------------------------------------------------------------
    print_subheader("isinstance() Checks")

    def isinstance_exact():
        return isinstance(obj, DerivedClass)

    time_ms = time_operation(isinstance_exact, iterations=100000)
    results.append(BenchmarkResult("isinstance() exact match", time_ms, category=CATEGORY))
    print_result("isinstance() exact match", time_ms)

    def isinstance_parent():
        return isinstance(obj, BaseClass)

    time_ms = time_operation(isinstance_parent, iterations=100000)
    results.append(BenchmarkResult("isinstance() parent class", time_ms, category=CATEGORY))
    print_result("isinstance() parent class", time_ms)

    def isinstance_deep():
        return isinstance(deep_obj, BaseClass)

    time_ms = time_operation(isinstance_deep, iterations=100000)
    results.append(BenchmarkResult("isinstance() 3-level inheritance", time_ms, category=CATEGORY))
    print_result("isinstance() 3-level inheritance", time_ms)

    def isinstance_abc():
        return isinstance(concrete_obj, AbstractBase)

    time_ms = time_operation(isinstance_abc, iterations=100000)
    results.append(BenchmarkResult("isinstance() ABC check", time_ms, category=CATEGORY))
    print_result("isinstance() ABC check", time_ms)

    def isinstance_builtin():
        return isinstance(test_str, str)

    time_ms = time_operation(isinstance_builtin, iterations=100000)
    results.append(BenchmarkResult("isinstance(x, str)", time_ms, category=CATEGORY))
    print_result("isinstance(x, str)", time_ms)

    def isinstance_tuple():
        return isinstance(test_int, (int, float, str))

    time_ms = time_operation(isinstance_tuple, iterations=100000)
    results.append(BenchmarkResult("isinstance() tuple of types", time_ms, category=CATEGORY))
    print_result("isinstance() tuple of types", time_ms)

    def isinstance_false():
        return isinstance(test_str, int)

    time_ms = time_operation(isinstance_false, iterations=100000)
    results.append(BenchmarkResult("isinstance() returns False", time_ms, category=CATEGORY))
    print_result("isinstance() returns False", time_ms)

    # -------------------------------------------------------------------------
    # type() Comparisons
    # -------------------------------------------------------------------------
    print_subheader("type() Comparisons")

    def type_equals():
        return type(obj) == DerivedClass

    time_ms = time_operation(type_equals, iterations=100000)
    results.append(BenchmarkResult("type(x) == Class", time_ms, category=CATEGORY))
    print_result("type(x) == Class", time_ms)

    def type_is():
        return type(obj) is DerivedClass

    time_ms = time_operation(type_is, iterations=100000)
    results.append(BenchmarkResult("type(x) is Class", time_ms, category=CATEGORY))
    print_result("type(x) is Class", time_ms)

    def type_builtin():
        return type(test_str) is str

    time_ms = time_operation(type_builtin, iterations=100000)
    results.append(BenchmarkResult("type(x) is str", time_ms, category=CATEGORY))
    print_result("type(x) is str", time_ms)

    def type_in_tuple():
        return type(test_int) in (int, float, str)

    time_ms = time_operation(type_in_tuple, iterations=100000)
    results.append(BenchmarkResult("type(x) in (int, float, str)", time_ms, category=CATEGORY))
    print_result("type(x) in (int, float, str)", time_ms)

    # -------------------------------------------------------------------------
    # issubclass() Checks
    # -------------------------------------------------------------------------
    print_subheader("issubclass() Checks")

    def issubclass_direct():
        return issubclass(DerivedClass, BaseClass)

    time_ms = time_operation(issubclass_direct, iterations=100000)
    results.append(BenchmarkResult("issubclass() direct parent", time_ms, category=CATEGORY))
    print_result("issubclass() direct parent", time_ms)

    def issubclass_deep():
        return issubclass(DeepDerived, BaseClass)

    time_ms = time_operation(issubclass_deep, iterations=100000)
    results.append(BenchmarkResult("issubclass() 3-level", time_ms, category=CATEGORY))
    print_result("issubclass() 3-level", time_ms)

    def issubclass_abc():
        return issubclass(ConcreteClass, AbstractBase)

    time_ms = time_operation(issubclass_abc, iterations=100000)
    results.append(BenchmarkResult("issubclass() ABC", time_ms, category=CATEGORY))
    print_result("issubclass() ABC", time_ms)

    # -------------------------------------------------------------------------
    # Other Type Checks
    # -------------------------------------------------------------------------
    print_subheader("Other Type Checks")

    def callable_check_func():
        return callable(run_benchmarks)

    time_ms = time_operation(callable_check_func, iterations=100000)
    results.append(BenchmarkResult("callable() on function", time_ms, category=CATEGORY))
    print_result("callable() on function", time_ms)

    def callable_check_obj():
        return callable(test_str)

    time_ms = time_operation(callable_check_obj, iterations=100000)
    results.append(BenchmarkResult("callable() on non-callable", time_ms, category=CATEGORY))
    print_result("callable() on non-callable", time_ms)

    def hasattr_exists():
        return hasattr(obj, "__class__")

    time_ms = time_operation(hasattr_exists, iterations=100000)
    results.append(BenchmarkResult("hasattr() exists", time_ms, category=CATEGORY))
    print_result("hasattr() exists", time_ms)

    def hasattr_missing():
        return hasattr(obj, "nonexistent_attr")

    time_ms = time_operation(hasattr_missing, iterations=100000)
    results.append(BenchmarkResult("hasattr() missing", time_ms, category=CATEGORY))
    print_result("hasattr() missing", time_ms)

    def hasattr_slots():
        return hasattr(slots_obj, "x")

    time_ms = time_operation(hasattr_slots, iterations=100000)
    results.append(BenchmarkResult("hasattr() on __slots__ class", time_ms, category=CATEGORY))
    print_result("hasattr() on __slots__ class", time_ms)

    # -------------------------------------------------------------------------
    # Type Introspection
    # -------------------------------------------------------------------------
    print_subheader("Type Introspection")

    def get_class():
        return obj.__class__

    time_ms = time_operation(get_class, iterations=100000)
    results.append(BenchmarkResult("obj.__class__", time_ms, category=CATEGORY))
    print_result("obj.__class__", time_ms)

    def get_class_name():
        return obj.__class__.__name__

    time_ms = time_operation(get_class_name, iterations=100000)
    results.append(BenchmarkResult("obj.__class__.__name__", time_ms, category=CATEGORY))
    print_result("obj.__class__.__name__", time_ms)

    def get_mro():
        return obj.__class__.__mro__

    time_ms = time_operation(get_mro, iterations=100000)
    results.append(BenchmarkResult("obj.__class__.__mro__", time_ms, category=CATEGORY))
    print_result("obj.__class__.__mro__", time_ms)

    def get_bases():
        return DerivedClass.__bases__

    time_ms = time_operation(get_bases, iterations=100000)
    results.append(BenchmarkResult("Class.__bases__", time_ms, category=CATEGORY))
    print_result("Class.__bases__", time_ms)

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
