# Database benchmarks

from .diskcache_bench import run_benchmarks as run_diskcache_benchmarks
from .mongodb_bench import run_benchmarks as run_mongodb_benchmarks
from .sqlite_bench import run_benchmarks as run_sqlite_benchmarks

__all__ = [
    'run_sqlite_benchmarks',
    'run_diskcache_benchmarks',
    'run_mongodb_benchmarks',
]
