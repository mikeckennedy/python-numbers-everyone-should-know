# Web framework benchmarks
#
# This module contains minimal web apps for benchmarking.
# All frameworks run on Granian for consistent, fair comparison.
# Requires external tools (wrk or hey) to measure request throughput.
#
# Usage:
#   1. Start a server: python run_server.py flask
#   2. Benchmark: wrk -t4 -c100 -d10s http://127.0.0.1:8000/
#   3. Or run all: python benchmark_servers.py
#
# Frameworks (all on Granian):
#   - Flask     (WSGI)
#   - Django    (WSGI)
#   - FastAPI   (ASGI)
#   - Starlette (ASGI)
#   - Litestar  (ASGI)
