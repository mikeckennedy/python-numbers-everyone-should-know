"""
Function call overhead benchmarks.

Measures:
- Empty function call
- Function with 5 arguments
- Method call on object
- Lambda call
- Built-in function (len())
- *args and **kwargs overhead
- Closure call
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

CATEGORY = 'functions_calls'


# =============================================================================
# Test Functions and Classes
# =============================================================================


def empty_function():
    """Function that does nothing."""
    pass


def function_with_args(a, b, c, d, e):
    """Function with 5 positional arguments."""
    return a


def function_with_defaults(a, b=2, c=3, d=4, e=5):
    """Function with default arguments."""
    return a


def function_with_args_kwargs(*args, **kwargs):
    """Function with *args and **kwargs."""
    return args[0] if args else None


def function_returns_value():
    """Function that returns a value."""
    return 42


class SimpleClass:
    """Simple class for method call benchmarks."""

    def method(self):
        pass

    def method_with_args(self, a, b, c, d, e):
        return a

    @staticmethod
    def static_method():
        pass

    @classmethod
    def class_method(cls):
        pass

    @property
    def prop(self):
        return 42


# Closure factory
def make_closure(x):
    def inner():
        return x

    return inner


# Lambda
lambda_func = lambda: None  # noqa: E731
lambda_with_args = lambda a, b, c, d, e: a  # noqa: E731


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all function call benchmarks."""
    results = []

    print_header('Function Call Benchmarks')

    # -------------------------------------------------------------------------
    # Basic Function Calls
    # -------------------------------------------------------------------------
    print_subheader('Basic Function Calls')

    def call_empty():
        empty_function()

    time_ms = time_operation(call_empty, iterations=100_000)
    results.append(BenchmarkResult('empty function call', time_ms, category=CATEGORY))
    print_result('empty function call', time_ms)

    def call_with_return():
        return function_returns_value()

    time_ms = time_operation(call_with_return, iterations=100_000)
    results.append(BenchmarkResult('function with return', time_ms, category=CATEGORY))
    print_result('function with return', time_ms)

    def call_with_5_args():
        function_with_args(1, 2, 3, 4, 5)

    time_ms = time_operation(call_with_5_args, iterations=100_000)
    results.append(BenchmarkResult('function with 5 args', time_ms, category=CATEGORY))
    print_result('function with 5 args', time_ms)

    def call_with_defaults():
        function_with_defaults(1)

    time_ms = time_operation(call_with_defaults, iterations=100_000)
    results.append(BenchmarkResult('function with defaults (1 provided)', time_ms, category=CATEGORY))
    print_result('function with defaults (1 provided)', time_ms)

    def call_with_kwargs():
        function_with_defaults(a=1, b=2, c=3, d=4, e=5)

    time_ms = time_operation(call_with_kwargs, iterations=100_000)
    results.append(BenchmarkResult('function with keyword args', time_ms, category=CATEGORY))
    print_result('function with keyword args', time_ms)

    def call_args_kwargs():
        function_with_args_kwargs(1, 2, 3, x=4, y=5)

    time_ms = time_operation(call_args_kwargs, iterations=100_000)
    results.append(BenchmarkResult('function with *args/**kwargs', time_ms, category=CATEGORY))
    print_result('function with *args/**kwargs', time_ms)

    # -------------------------------------------------------------------------
    # Method Calls
    # -------------------------------------------------------------------------
    print_subheader('Method Calls')

    obj = SimpleClass()

    def call_method():
        obj.method()

    time_ms = time_operation(call_method, iterations=100_000)
    results.append(BenchmarkResult('instance method call', time_ms, category=CATEGORY))
    print_result('instance method call', time_ms)

    def call_method_with_args():
        obj.method_with_args(1, 2, 3, 4, 5)

    time_ms = time_operation(call_method_with_args, iterations=100_000)
    results.append(BenchmarkResult('method with 5 args', time_ms, category=CATEGORY))
    print_result('method with 5 args', time_ms)

    def call_static():
        SimpleClass.static_method()

    time_ms = time_operation(call_static, iterations=100_000)
    results.append(BenchmarkResult('static method call', time_ms, category=CATEGORY))
    print_result('static method call', time_ms)

    def call_classmethod():
        SimpleClass.class_method()

    time_ms = time_operation(call_classmethod, iterations=100_000)
    results.append(BenchmarkResult('class method call', time_ms, category=CATEGORY))
    print_result('class method call', time_ms)

    def call_property():
        _ = obj.prop

    time_ms = time_operation(call_property, iterations=100_000)
    results.append(BenchmarkResult('property access', time_ms, category=CATEGORY))
    print_result('property access', time_ms)

    # -------------------------------------------------------------------------
    # Lambda and Closure
    # -------------------------------------------------------------------------
    print_subheader('Lambda and Closure')

    def call_lambda():
        lambda_func()

    time_ms = time_operation(call_lambda, iterations=100_000)
    results.append(BenchmarkResult('lambda call (no args)', time_ms, category=CATEGORY))
    print_result('lambda call (no args)', time_ms)

    def call_lambda_args():
        lambda_with_args(1, 2, 3, 4, 5)

    time_ms = time_operation(call_lambda_args, iterations=100_000)
    results.append(BenchmarkResult('lambda call (5 args)', time_ms, category=CATEGORY))
    print_result('lambda call (5 args)', time_ms)

    closure = make_closure(42)

    def call_closure():
        closure()

    time_ms = time_operation(call_closure, iterations=100_000)
    results.append(BenchmarkResult('closure call', time_ms, category=CATEGORY))
    print_result('closure call', time_ms)

    # -------------------------------------------------------------------------
    # Built-in Functions
    # -------------------------------------------------------------------------
    print_subheader('Built-in Functions')

    test_list = [1, 2, 3, 4, 5]

    def call_len():
        len(test_list)

    time_ms = time_operation(call_len, iterations=100_000)
    results.append(BenchmarkResult('len() on list', time_ms, category=CATEGORY))
    print_result('len() on list', time_ms)

    def call_abs():
        abs(-42)

    time_ms = time_operation(call_abs, iterations=100_000)
    results.append(BenchmarkResult('abs()', time_ms, category=CATEGORY))
    print_result('abs()', time_ms)

    def call_min():
        min(1, 2, 3, 4, 5)

    time_ms = time_operation(call_min, iterations=100_000)
    results.append(BenchmarkResult('min() with 5 args', time_ms, category=CATEGORY))
    print_result('min() with 5 args', time_ms)

    def call_max_list():
        max(test_list)

    time_ms = time_operation(call_max_list, iterations=100_000)
    results.append(BenchmarkResult('max() on list', time_ms, category=CATEGORY))
    print_result('max() on list', time_ms)

    def call_sorted():
        sorted(test_list)

    time_ms = time_operation(call_sorted, iterations=50_000)
    results.append(BenchmarkResult('sorted() on 5-item list', time_ms, category=CATEGORY))
    print_result('sorted() on 5-item list', time_ms)

    # -------------------------------------------------------------------------
    # Function Creation Overhead
    # -------------------------------------------------------------------------
    print_subheader('Function Creation Overhead')

    def create_lambda():
        return lambda x: x + 1

    time_ms = time_operation(create_lambda, iterations=100_000)
    results.append(BenchmarkResult('create lambda', time_ms, category=CATEGORY))
    print_result('create lambda', time_ms)

    def create_closure():
        x = 42

        def inner():
            return x

        return inner

    time_ms = time_operation(create_closure, iterations=100_000)
    results.append(BenchmarkResult('create closure', time_ms, category=CATEGORY))
    print_result('create closure', time_ms)

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
