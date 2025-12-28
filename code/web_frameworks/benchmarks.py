"""Web framework benchmarks - integration with run_all.py.

Wraps benchmark_servers.py to provide the standard run_benchmarks() interface.
"""

import shutil
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.benchmark import BenchmarkResult

from web_frameworks.benchmark_servers import run_benchmarks as run_server_benchmarks


def parse_latency_to_ms(latency_str: str | None) -> float | None:
    """Parse latency string like '2.5ms' or '150us' to milliseconds."""
    if not latency_str:
        return None

    try:
        latency_str = latency_str.strip().lower()

        if latency_str.endswith('ms'):
            return float(latency_str[:-2])
        elif latency_str.endswith('us') or latency_str.endswith('μs'):
            return float(latency_str[:-2]) / 1000
        elif latency_str.endswith('s'):
            return float(latency_str[:-1]) * 1000
        else:
            return float(latency_str)
    except (ValueError, AttributeError):
        return None


def run_benchmarks() -> list[BenchmarkResult]:
    """Run web framework benchmarks and return standardized results."""
    results = []

    # Check if wrk is available
    if not shutil.which('wrk'):
        print('⚠️  wrk not found, skipping web framework benchmarks')
        return results

    # Run benchmarks
    try:
        server_results = run_server_benchmarks(
            tool='wrk',
            duration=10,
            connections=100,
            threads=4,
            workers=4,
        )
    except Exception as e:
        print(f'⚠️  Error running web framework benchmarks: {e}')
        return results

    # Convert to standard format
    for framework_name, bench_result in server_results.items():
        latency_avg_ms = parse_latency_to_ms(bench_result.latency_avg)
        latency_p99_ms = parse_latency_to_ms(bench_result.latency_p99)

        # Quick reference metric: actual requests per second (not latency)
        # We show req/sec because latency-to-ops/sec calculation doesn't work for concurrent benchmarks
        results.append(
            BenchmarkResult(
                name=f'{framework_name}_return_json',
                value=bench_result.requests_per_sec,
                unit='req/sec',
                category='web',
            )
        )

        # Detailed metrics
        # Requests per second
        results.append(
            BenchmarkResult(
                name=f'{framework_name}_requests_per_sec',
                value=bench_result.requests_per_sec,
                unit='req/sec',
                category='web',
            )
        )

        # Latency p99
        if latency_p99_ms:
            results.append(
                BenchmarkResult(
                    name=f'{framework_name}_latency_p99',
                    value=latency_p99_ms,
                    unit='ms',
                    category='web',
                )
            )

    return results


if __name__ == '__main__':
    from utils.benchmark import print_header, print_result

    print_header('Web Framework Benchmarks')
    results = run_benchmarks()

    for result in results:
        print_result(result.name, result.value, result.unit)
