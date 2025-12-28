# Memory benchmarks

from .classes import run_benchmarks as run_classes_benchmarks
from .collections_mem import run_benchmarks as run_collections_mem_benchmarks
from .empty_process import run_benchmarks as run_empty_process_benchmarks
from .numbers_mem import run_benchmarks as run_numbers_mem_benchmarks
from .strings import run_benchmarks as run_strings_benchmarks

__all__ = [
    'run_classes_benchmarks',
    'run_collections_mem_benchmarks',
    'run_empty_process_benchmarks',
    'run_numbers_mem_benchmarks',
    'run_strings_benchmarks',
]
