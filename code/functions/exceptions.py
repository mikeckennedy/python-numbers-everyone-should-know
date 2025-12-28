"""
Exception handling overhead benchmarks.

Measures:
- try/except (no exception raised)
- try/except (exception raised and caught)
- try/except/finally overhead
- raise and catch different exception types
- Exception creation overhead
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

CATEGORY = 'functions_exceptions'


# =============================================================================
# Test Functions
# =============================================================================


def no_exception():
    """Function that doesn't raise."""
    return 42


def raises_value_error():
    """Function that raises ValueError."""
    raise ValueError('test error')


def raises_custom_error():
    """Function that raises custom exception."""
    raise CustomError('test error')


class CustomError(Exception):
    """Custom exception for benchmarking."""

    pass


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all exception handling benchmarks."""
    results = []

    print_header('Exception Handling Benchmarks')

    # -------------------------------------------------------------------------
    # Try/Except Overhead (No Exception)
    # -------------------------------------------------------------------------
    print_subheader('Try/Except Overhead (No Exception)')

    def no_try_except():
        x = no_exception()
        return x

    time_ms = time_operation(no_try_except, iterations=100_000)
    results.append(BenchmarkResult('function call (no try/except)', time_ms, category=CATEGORY))
    print_result('function call (no try/except)', time_ms)

    def with_try_except():
        try:
            x = no_exception()
            return x
        except Exception:
            pass

    time_ms = time_operation(with_try_except, iterations=100_000)
    results.append(BenchmarkResult('try/except (no exception raised)', time_ms, category=CATEGORY))
    print_result('try/except (no exception raised)', time_ms)

    def with_try_except_specific():
        try:
            x = no_exception()
            return x
        except ValueError:
            pass

    time_ms = time_operation(with_try_except_specific, iterations=100_000)
    results.append(BenchmarkResult('try/except ValueError (not raised)', time_ms, category=CATEGORY))
    print_result('try/except ValueError (not raised)', time_ms)

    def with_try_except_finally():
        try:
            x = no_exception()
            return x
        except Exception:
            pass
        finally:
            pass

    time_ms = time_operation(with_try_except_finally, iterations=100_000)
    results.append(BenchmarkResult('try/except/finally (no exception)', time_ms, category=CATEGORY))
    print_result('try/except/finally (no exception)', time_ms)

    def with_multiple_except():
        try:
            x = no_exception()
            return x
        except ValueError:
            pass
        except TypeError:
            pass
        except KeyError:
            pass

    time_ms = time_operation(with_multiple_except, iterations=100_000)
    results.append(BenchmarkResult('try with 3 except clauses (not raised)', time_ms, category=CATEGORY))
    print_result('try with 3 except clauses (not raised)', time_ms)

    # -------------------------------------------------------------------------
    # Try/Except (Exception Raised)
    # -------------------------------------------------------------------------
    print_subheader('Try/Except (Exception Raised)')

    def catch_value_error():
        try:
            raises_value_error()
        except ValueError:
            pass

    time_ms = time_operation(catch_value_error, iterations=50_000)
    results.append(BenchmarkResult('raise + catch ValueError', time_ms, category=CATEGORY))
    print_result('raise + catch ValueError', time_ms)

    def catch_with_exception():
        try:
            raises_value_error()
        except Exception:
            pass

    time_ms = time_operation(catch_with_exception, iterations=50_000)
    results.append(BenchmarkResult('raise ValueError, catch Exception', time_ms, category=CATEGORY))
    print_result('raise ValueError, catch Exception', time_ms)

    def catch_custom_error():
        try:
            raises_custom_error()
        except CustomError:
            pass

    time_ms = time_operation(catch_custom_error, iterations=50_000)
    results.append(BenchmarkResult('raise + catch custom exception', time_ms, category=CATEGORY))
    print_result('raise + catch custom exception', time_ms)

    def catch_with_binding():
        try:
            raises_value_error()
        except ValueError as e:
            _ = e

    time_ms = time_operation(catch_with_binding, iterations=50_000)
    results.append(BenchmarkResult("raise + catch with 'as e'", time_ms, category=CATEGORY))
    print_result("raise + catch with 'as e'", time_ms)

    def catch_with_finally():
        try:
            raises_value_error()
        except ValueError:
            pass
        finally:
            pass

    time_ms = time_operation(catch_with_finally, iterations=50_000)
    results.append(BenchmarkResult('raise + catch + finally', time_ms, category=CATEGORY))
    print_result('raise + catch + finally', time_ms)

    # -------------------------------------------------------------------------
    # Exception Creation
    # -------------------------------------------------------------------------
    print_subheader('Exception Creation')

    def create_value_error():
        return ValueError('test error')

    time_ms = time_operation(create_value_error, iterations=100_000)
    results.append(BenchmarkResult('create ValueError', time_ms, category=CATEGORY))
    print_result('create ValueError', time_ms)

    def create_custom_error():
        return CustomError('test error')

    time_ms = time_operation(create_custom_error, iterations=100_000)
    results.append(BenchmarkResult('create custom exception', time_ms, category=CATEGORY))
    print_result('create custom exception', time_ms)

    def create_exception_with_traceback():
        try:
            raise ValueError('test')
        except ValueError as e:
            return e

    time_ms = time_operation(create_exception_with_traceback, iterations=50_000)
    results.append(BenchmarkResult('exception with traceback', time_ms, category=CATEGORY))
    print_result('exception with traceback', time_ms)

    # -------------------------------------------------------------------------
    # Re-raise Patterns
    # -------------------------------------------------------------------------
    print_subheader('Re-raise Patterns')

    def catch_and_reraise():
        try:
            try:
                raises_value_error()
            except ValueError:
                raise
        except ValueError:
            pass

    time_ms = time_operation(catch_and_reraise, iterations=50_000)
    results.append(BenchmarkResult('catch and re-raise (bare raise)', time_ms, category=CATEGORY))
    print_result('catch and re-raise (bare raise)', time_ms)

    def catch_wrap_reraise():
        try:
            try:
                raises_value_error()
            except ValueError as e:
                raise RuntimeError('wrapped') from e
        except RuntimeError:
            pass

    time_ms = time_operation(catch_wrap_reraise, iterations=50_000)
    results.append(BenchmarkResult('catch, wrap, re-raise (from e)', time_ms, category=CATEGORY))
    print_result('catch, wrap, re-raise (from e)', time_ms)

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
