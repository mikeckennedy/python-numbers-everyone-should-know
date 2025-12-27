# File I/O benchmarks

from .basic_ops import run_benchmarks as run_basic_ops_benchmarks
from .pickle_vs_json import run_benchmarks as run_pickle_vs_json_benchmarks

__all__ = [
    'run_basic_ops_benchmarks',
    'run_pickle_vs_json_benchmarks',
]
