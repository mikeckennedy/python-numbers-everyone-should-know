#!/usr/bin/env python3
"""
Compare async benchmarks with and without uvloop.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

# Create two versions of async_overhead.py
async_file = Path("code/async_bench/async_overhead.py")
content = async_file.read_text()

# Version without uvloop
content_no_uvloop = content.replace(
    """    # Try to use uvloop if available
    try:
        import uvloop

        uvloop.install()
        print_header('Async Overhead Benchmarks (with uvloop)')
    except ImportError:
        print_header('Async Overhead Benchmarks')""",
    """    # uvloop disabled for comparison
    print_header('Async Overhead Benchmarks (standard asyncio)')"""
)

# Version with uvloop
content_with_uvloop = content

print("=" * 80)
print("RUNNING WITHOUT UVLOOP (standard asyncio)")
print("=" * 80)
print()

with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
    f.write(content_no_uvloop)
    temp_file = f.name

try:
    subprocess.run([sys.executable, temp_file], check=True)
finally:
    Path(temp_file).unlink()

print()
print()
print("=" * 80)
print("RUNNING WITH UVLOOP")
print("=" * 80)
print()

subprocess.run([sys.executable, "code/async_bench/async_overhead.py"], check=True)
