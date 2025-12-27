# Function call benchmarks

from .exceptions import run_benchmarks as run_exceptions_benchmarks
from .function_calls import run_benchmarks as run_function_calls_benchmarks
from .type_checking import run_benchmarks as run_type_checking_benchmarks

__all__ = [
    "run_function_calls_benchmarks",
    "run_exceptions_benchmarks",
    "run_type_checking_benchmarks",
]
