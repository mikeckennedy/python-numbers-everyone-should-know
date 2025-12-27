# JSON and serialization benchmarks

from .deserialization import run_benchmarks as run_deserialization_benchmarks
from .pydantic_bench import run_benchmarks as run_pydantic_benchmarks
from .serialization import run_benchmarks as run_serialization_benchmarks

__all__ = [
    'run_serialization_benchmarks',
    'run_deserialization_benchmarks',
    'run_pydantic_benchmarks',
]
