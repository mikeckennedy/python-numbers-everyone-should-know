#!/usr/bin/env python3
"""
Benchmark web framework servers using wrk or hey.

All frameworks run on Granian for consistent, fair comparison.
Granian supports both WSGI (Flask, Django) and ASGI (FastAPI, Starlette, Litestar).

Prerequisites:
    brew install wrk   # or: brew install hey

Usage:
    python benchmark_servers.py [--tool wrk|hey] [--duration 10] [--connections 100]

The script will:
    1. Start each server with Granian
    2. Wait for it to be ready
    3. Run the benchmark
    4. Stop the server
    5. Output results
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.benchmark import print_header, print_subheader

# Configuration
SCRIPT_DIR = Path(__file__).parent
DEFAULT_WORKERS = 4
DEFAULT_PORT = 8000


@dataclass
class ServerConfig:
    name: str
    module: str
    interface: str  # "wsgi" or "asgi"


SERVERS = [
    ServerConfig(name='flask', module='flask_app:app', interface='wsgi'),
    ServerConfig(name='django', module='django_app:application', interface='wsgi'),
    ServerConfig(name='fastapi', module='fastapi_app:app', interface='asgi'),
    ServerConfig(name='starlette', module='starlette_app:app', interface='asgi'),
    ServerConfig(name='litestar', module='litestar_app:app', interface='asgi'),
]


@dataclass
class BenchmarkResult:
    name: str
    requests_per_sec: float
    latency_avg: str
    latency_p99: str | None = None
    transfer_per_sec: str | None = None
    errors: int = 0


def get_granian_command(server: ServerConfig, port: int, workers: int) -> list[str]:
    """Build granian command for a server."""
    return [
        'granian',
        '--interface',
        server.interface,
        '--host',
        '127.0.0.1',
        '--port',
        str(port),
        '--workers',
        str(workers),
        '--no-ws',  # Disable websockets for simpler benchmarking
        '--loop',
        'uvloop',
        server.module,
    ]


def check_tool(tool: str) -> bool:
    """Check if benchmark tool is available."""
    return shutil.which(tool) is not None


def wait_for_server(port: int, timeout: float = 15.0) -> bool:
    """Wait for server to be ready."""
    import socket

    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except (ConnectionRefusedError, socket.timeout, OSError):
            time.sleep(0.2)
    return False


def run_wrk(port: int, duration: int, connections: int, threads: int) -> BenchmarkResult | None:
    """Run wrk benchmark and parse results."""
    url = f'http://127.0.0.1:{port}/'

    # Warmup
    subprocess.run(
        ['wrk', '-t1', '-c10', '-d2s', url],
        capture_output=True,
        text=True,
    )

    # Actual benchmark
    result = subprocess.run(
        ['wrk', f'-t{threads}', f'-c{connections}', f'-d{duration}s', '--latency', url],
        capture_output=True,
        text=True,
    )

    output = result.stdout
    print(output)

    # Parse results
    rps_match = re.search(r'Requests/sec:\s+([\d.]+)', output)
    latency_match = re.search(r'Latency\s+([\d.]+\w+)', output)
    p99_match = re.search(r'99%\s+([\d.]+\w+)', output)
    transfer_match = re.search(r'Transfer/sec:\s+([\d.]+\w+)', output)
    errors_match = re.search(r'Socket errors:.*?(\d+) total', output)

    if rps_match and latency_match:
        return BenchmarkResult(
            name='',
            requests_per_sec=float(rps_match.group(1)),
            latency_avg=latency_match.group(1),
            latency_p99=p99_match.group(1) if p99_match else None,
            transfer_per_sec=transfer_match.group(1) if transfer_match else None,
            errors=int(errors_match.group(1)) if errors_match else 0,
        )
    return None


def run_hey(port: int, duration: int, connections: int) -> BenchmarkResult | None:
    """Run hey benchmark and parse results."""
    url = f'http://127.0.0.1:{port}/'

    # Warmup
    subprocess.run(
        ['hey', '-n', '1000', '-c', '10', url],
        capture_output=True,
        text=True,
    )

    # Actual benchmark
    result = subprocess.run(
        ['hey', '-z', f'{duration}s', '-c', str(connections), url],
        capture_output=True,
        text=True,
    )

    output = result.stdout
    print(output)

    # Parse results
    rps_match = re.search(r'Requests/sec:\s+([\d.]+)', output)
    latency_match = re.search(r'Average:\s+([\d.]+)', output)
    p99_match = re.search(r'99% in ([\d.]+) secs', output)

    if rps_match and latency_match:
        latency_ms = float(latency_match.group(1)) * 1000
        return BenchmarkResult(
            name='',
            requests_per_sec=float(rps_match.group(1)),
            latency_avg=f'{latency_ms:.2f}ms',
            latency_p99=f'{float(p99_match.group(1)) * 1000:.2f}ms' if p99_match else None,
        )
    return None


def kill_server(proc: subprocess.Popen):
    """Kill server process and its children."""
    try:
        # Try graceful termination first
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            # Force kill
            proc.kill()
            proc.wait(timeout=2)
    except Exception:
        pass


def run_benchmarks(
    tool: str = 'wrk',
    duration: int = 10,
    connections: int = 100,
    threads: int = 4,
    workers: int = DEFAULT_WORKERS,
    port: int = DEFAULT_PORT,
    frameworks: list[str] | None = None,
) -> dict[str, BenchmarkResult]:
    """Run benchmarks for all servers."""
    results: dict[str, BenchmarkResult] = {}

    print_header('Web Framework Benchmark Suite')
    print('Server: Granian (all frameworks)')
    print(f'Workers: {workers}')
    print(f'Tool: {tool}')
    print(f'Duration: {duration}s')
    print(f'Connections: {connections}')
    print()

    # Filter servers if specific frameworks requested
    servers = SERVERS
    if frameworks:
        servers = [s for s in SERVERS if s.name in frameworks]

    for server in servers:
        print_subheader(f'{server.name} ({server.interface.upper()})')

        # Build command
        cmd = get_granian_command(server, port, workers)

        # Start server
        print(f'Starting {server.name} with Granian...')
        print(f'  Command: {" ".join(cmd)}')
        proc = subprocess.Popen(
            cmd,
            cwd=SCRIPT_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid,  # Create new process group for clean shutdown
        )

        try:
            # Wait for server
            if not wait_for_server(port):
                print(f'Error: {server.name} failed to start')
                kill_server(proc)
                continue

            print(f'{server.name} ready, running benchmark...')
            print()

            # Run benchmark
            if tool == 'wrk':
                result = run_wrk(port, duration, connections, threads)
            else:
                result = run_hey(port, duration, connections)

            if result:
                result.name = server.name
                results[server.name] = result

        finally:
            # Stop server
            print(f'\nStopping {server.name}...')
            kill_server(proc)
            # Also kill any orphaned granian workers
            subprocess.run(
                ['pkill', '-f', f'granian.*{server.module}'],
                capture_output=True,
            )
            time.sleep(1)

    return results


def print_summary(results: dict[str, BenchmarkResult]):
    """Print benchmark summary."""
    print_header('Summary')

    # Sort by requests/sec
    sorted_results = sorted(results.values(), key=lambda r: r.requests_per_sec, reverse=True)

    print(f'{"Framework":<12} {"Req/sec":>12} {"Latency":>12} {"p99":>12}')
    print('-' * 50)

    for r in sorted_results:
        p99 = r.latency_p99 or 'N/A'
        print(f'{r.name:<12} {r.requests_per_sec:>12.2f} {r.latency_avg:>12} {p99:>12}')


def output_json(results: dict[str, BenchmarkResult]) -> dict:
    """Output results as JSON."""
    return {
        name: {
            'requests_per_sec': r.requests_per_sec,
            'latency_avg': r.latency_avg,
            'latency_p99': r.latency_p99,
            'errors': r.errors,
        }
        for name, r in results.items()
    }


def main():
    parser = argparse.ArgumentParser(description='Benchmark web framework servers (all running on Granian)')
    parser.add_argument(
        '--tool',
        '-t',
        choices=['wrk', 'hey'],
        default='wrk',
        help='Benchmark tool to use (default: wrk)',
    )
    parser.add_argument(
        '--duration',
        '-d',
        type=int,
        default=10,
        help='Benchmark duration in seconds (default: 10)',
    )
    parser.add_argument(
        '--connections',
        '-c',
        type=int,
        default=100,
        help='Number of concurrent connections (default: 100)',
    )
    parser.add_argument(
        '--threads',
        type=int,
        default=4,
        help='Number of threads for wrk (default: 4)',
    )
    parser.add_argument(
        '--workers',
        '-w',
        type=int,
        default=DEFAULT_WORKERS,
        help=f'Number of Granian workers (default: {DEFAULT_WORKERS})',
    )
    parser.add_argument(
        '--port',
        '-p',
        type=int,
        default=DEFAULT_PORT,
        help=f'Port to run servers on (default: {DEFAULT_PORT})',
    )
    parser.add_argument(
        '--frameworks',
        '-f',
        nargs='+',
        choices=['flask', 'django', 'fastapi', 'starlette', 'litestar'],
        help='Specific frameworks to benchmark (default: all)',
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON',
    )

    args = parser.parse_args()

    # Check tool availability
    if not check_tool(args.tool):
        print(f'Error: {args.tool} not found.')
        print(f'Install with: brew install {args.tool}')
        sys.exit(1)

    if not check_tool('granian'):
        print('Error: granian not found.')
        print('Install with: pip install granian')
        sys.exit(1)

    # Run benchmarks
    results = run_benchmarks(
        tool=args.tool,
        duration=args.duration,
        connections=args.connections,
        threads=args.threads,
        workers=args.workers,
        port=args.port,
        frameworks=args.frameworks,
    )

    # Output
    if results:
        print_summary(results)

        if args.json:
            print('\nJSON Results:')
            print(json.dumps(output_json(results), indent=2))

    return results


if __name__ == '__main__':
    main()
