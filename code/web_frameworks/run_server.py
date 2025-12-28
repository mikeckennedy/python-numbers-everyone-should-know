#!/usr/bin/env python3
"""
Helper script to start web framework servers for benchmarking.

All servers run on Granian for consistent comparison.

Usage:
    python run_server.py flask [--port 8000] [--workers 4]
    python run_server.py django [--port 8000] [--workers 4]
    python run_server.py fastapi [--port 8000] [--workers 4]
    python run_server.py starlette [--port 8000] [--workers 4]
    python run_server.py litestar [--port 8000] [--workers 4]
"""

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ServerConfig:
    name: str
    module: str
    interface: str  # "wsgi" or "asgi"


SERVERS = {
    'flask': ServerConfig(name='flask', module='flask_app:app', interface='wsgi'),
    'django': ServerConfig(name='django', module='django_app:application', interface='wsgi'),
    'fastapi': ServerConfig(name='fastapi', module='fastapi_app:app', interface='asgi'),
    'starlette': ServerConfig(name='starlette', module='starlette_app:app', interface='asgi'),
    'litestar': ServerConfig(name='litestar', module='litestar_app:app', interface='asgi'),
}


def run_server(framework: str, port: int = 8000, workers: int = 4):
    """Start a server for the specified framework using Granian."""
    if framework not in SERVERS:
        print(f'Unknown framework: {framework}')
        print(f'Available: {", ".join(SERVERS.keys())}')
        sys.exit(1)

    config = SERVERS[framework]

    # Change to the web_frameworks directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    cmd = [
        'granian',
        '--interface',
        config.interface,
        '--host',
        '127.0.0.1',
        '--port',
        str(port),
        '--workers',
        str(workers),
        '--no-ws',
        # '--loop',
        # 'uvloop',
        config.module,
    ]

    print(f'Starting {framework} on Granian ({config.interface.upper()})')
    print(f'Workers: {workers}')
    print(f'URL: http://127.0.0.1:{port}/')
    print(f'Command: {" ".join(cmd)}')
    print()

    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print(f'\n{framework} server stopped.')
    except FileNotFoundError:
        print('Error: granian not found.')
        print('Install with: pip install granian')
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Run web framework servers on Granian for benchmarking')
    parser.add_argument(
        'framework',
        choices=list(SERVERS.keys()),
        help='Framework to run',
    )
    parser.add_argument(
        '--port',
        '-p',
        type=int,
        default=8000,
        help='Port to run on (default: 8000)',
    )
    parser.add_argument(
        '--workers',
        '-w',
        type=int,
        default=4,
        help='Number of worker processes (default: 4)',
    )

    args = parser.parse_args()
    run_server(args.framework, args.port, args.workers)


if __name__ == '__main__':
    main()
