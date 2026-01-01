#!/usr/bin/env python3
"""Quick test to verify timing is working correctly."""

import sys
from pathlib import Path
from time import perf_counter_ns

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.benchmark import time_operation_ns, ns_to_ms

# Test simple addition
a, b = 123, 456

# Manual timing
start = perf_counter_ns()
iterations = 100_000
for _ in range(iterations):
    x = a + b
end = perf_counter_ns()

time_per_op_ns = (end - start) / iterations
print(f"Manual timing: {time_per_op_ns:.2f} ns per operation")
print(f"Manual timing: {time_per_op_ns / 1000:.2f} µs per operation")
print(f"Manual timing: {time_per_op_ns / 1_000_000:.6f} ms per operation")

# Using utility
time_ns = time_operation_ns(lambda: a + b, iterations=100_000)
time_ms = ns_to_ms(time_ns)
print(f"\nUtility timing: {time_ns:.2f} ns per operation")
print(f"Utility ns_to_ms: {time_ms:.6f} (should be ms)")
print(f"Utility converted to µs: {time_ns / 1000:.6f} µs")
