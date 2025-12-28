# Basic operations benchmarks

from .arithmetic import run_benchmarks as run_arithmetic_benchmarks
from .list_ops import run_benchmarks as run_list_ops_benchmarks
from .string_ops import run_benchmarks as run_string_ops_benchmarks

__all__ = [
    'run_arithmetic_benchmarks',
    'run_list_ops_benchmarks',
    'run_string_ops_benchmarks',
]
