# Collection access and iteration benchmarks

from .access import run_benchmarks as run_access_benchmarks
from .iteration import run_benchmarks as run_iteration_benchmarks
from .length import run_benchmarks as run_length_benchmarks

__all__ = [
    "run_access_benchmarks",
    "run_length_benchmarks",
    "run_iteration_benchmarks",
]

