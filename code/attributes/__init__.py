# Attribute access benchmarks

from .attribute_access import run_benchmarks as run_attribute_access_benchmarks
from .other_ops import run_benchmarks as run_other_ops_benchmarks

__all__ = [
    'run_attribute_access_benchmarks',
    'run_other_ops_benchmarks',
]
