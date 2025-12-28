"""
Basic file I/O benchmarks.

Measures:
- Open and close (no read)
- Read 1KB file
- Read 1MB file
- Write 1KB file
- Write 1MB file
"""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.benchmark import (
    BenchmarkResult,
    collect_results,
    print_header,
    print_result,
    print_subheader,
    time_operation,
)

CATEGORY = 'file_io_basic'

# Test data
DATA_1KB = b'x' * 1024
DATA_1MB = b'x' * (1024 * 1024)


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all basic file I/O benchmarks."""
    results = []

    print_header('File I/O Benchmarks')

    # Create temp directory for test files
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create test files for reading
        file_1kb = tmppath / 'test_1kb.bin'
        file_1mb = tmppath / 'test_1mb.bin'
        file_1kb.write_bytes(DATA_1KB)
        file_1mb.write_bytes(DATA_1MB)

        # Files for writing (will be overwritten each iteration)
        write_file_1kb = tmppath / 'write_1kb.bin'
        write_file_1mb = tmppath / 'write_1mb.bin'

        # ---------------------------------------------------------------------
        # Open/Close Operations
        # ---------------------------------------------------------------------
        print_subheader('Open/Close Operations')

        def open_close_read():
            f = open(file_1kb, 'rb')
            f.close()

        time_ms = time_operation(open_close_read, iterations=5_000)
        results.append(BenchmarkResult('open() + close() (read mode)', time_ms, category=CATEGORY))
        print_result('open() + close() (read mode)', time_ms)

        def open_close_write():
            f = open(write_file_1kb, 'wb')
            f.close()

        time_ms = time_operation(open_close_write, iterations=5_000)
        results.append(BenchmarkResult('open() + close() (write mode)', time_ms, category=CATEGORY))
        print_result('open() + close() (write mode)', time_ms)

        def open_close_context():
            with open(file_1kb, 'rb'):
                pass

        time_ms = time_operation(open_close_context, iterations=5_000)
        results.append(BenchmarkResult('with open() (context manager)', time_ms, category=CATEGORY))
        print_result('with open() (context manager)', time_ms)

        # ---------------------------------------------------------------------
        # Read Operations
        # ---------------------------------------------------------------------
        print_subheader('Read Operations')

        def read_1kb():
            with open(file_1kb, 'rb') as f:
                return f.read()

        time_ms = time_operation(read_1kb, iterations=5_000)
        results.append(BenchmarkResult('read 1KB file', time_ms, category=CATEGORY))
        print_result('read 1KB file', time_ms)

        def read_1mb():
            with open(file_1mb, 'rb') as f:
                return f.read()

        time_ms = time_operation(read_1mb, iterations=1_000)
        results.append(BenchmarkResult('read 1MB file', time_ms, category=CATEGORY))
        print_result('read 1MB file', time_ms)

        # Text mode reading
        text_file = tmppath / 'test_text.txt'
        text_file.write_text('Hello, World!\n' * 100)

        def read_text():
            with open(text_file, 'r') as f:
                return f.read()

        time_ms = time_operation(read_text, iterations=5_000)
        results.append(BenchmarkResult('read text file (1.4KB)', time_ms, category=CATEGORY))
        print_result('read text file (1.4KB)', time_ms)

        # Read lines
        def read_lines():
            with open(text_file, 'r') as f:
                return f.readlines()

        time_ms = time_operation(read_lines, iterations=5_000)
        results.append(BenchmarkResult('readlines() (100 lines)', time_ms, category=CATEGORY))
        print_result('readlines() (100 lines)', time_ms)

        # ---------------------------------------------------------------------
        # Write Operations
        # ---------------------------------------------------------------------
        print_subheader('Write Operations')

        def write_1kb():
            with open(write_file_1kb, 'wb') as f:
                f.write(DATA_1KB)

        time_ms = time_operation(write_1kb, iterations=5_000)
        results.append(BenchmarkResult('write 1KB file', time_ms, category=CATEGORY))
        print_result('write 1KB file', time_ms)

        def write_1mb():
            with open(write_file_1mb, 'wb') as f:
                f.write(DATA_1MB)

        time_ms = time_operation(write_1mb, iterations=500)
        results.append(BenchmarkResult('write 1MB file', time_ms, category=CATEGORY))
        print_result('write 1MB file', time_ms)

        # Write with flush
        def write_1kb_flush():
            with open(write_file_1kb, 'wb') as f:
                f.write(DATA_1KB)
                f.flush()

        time_ms = time_operation(write_1kb_flush, iterations=5_000)
        results.append(BenchmarkResult('write 1KB + flush()', time_ms, category=CATEGORY))
        print_result('write 1KB + flush()', time_ms)

        # Write with fsync (ensures data hits disk)
        def write_1kb_fsync():
            with open(write_file_1kb, 'wb') as f:
                f.write(DATA_1KB)
                f.flush()
                os.fsync(f.fileno())

        time_ms = time_operation(write_1kb_fsync, iterations=1_000)
        results.append(BenchmarkResult('write 1KB + fsync()', time_ms, category=CATEGORY))
        print_result('write 1KB + fsync()', time_ms)

        # ---------------------------------------------------------------------
        # pathlib Operations
        # ---------------------------------------------------------------------
        print_subheader('pathlib Operations')

        def pathlib_read_bytes():
            return file_1kb.read_bytes()

        time_ms = time_operation(pathlib_read_bytes, iterations=5_000)
        results.append(BenchmarkResult('Path.read_bytes() 1KB', time_ms, category=CATEGORY))
        print_result('Path.read_bytes() 1KB', time_ms)

        def pathlib_write_bytes():
            write_file_1kb.write_bytes(DATA_1KB)

        time_ms = time_operation(pathlib_write_bytes, iterations=5_000)
        results.append(BenchmarkResult('Path.write_bytes() 1KB', time_ms, category=CATEGORY))
        print_result('Path.write_bytes() 1KB', time_ms)

        def pathlib_read_text():
            return text_file.read_text()

        time_ms = time_operation(pathlib_read_text, iterations=5_000)
        results.append(BenchmarkResult('Path.read_text()', time_ms, category=CATEGORY))
        print_result('Path.read_text()', time_ms)

        # ---------------------------------------------------------------------
        # File existence checks
        # ---------------------------------------------------------------------
        print_subheader('File Existence Checks')

        def exists_check():
            return file_1kb.exists()

        time_ms = time_operation(exists_check, iterations=1_0000)
        results.append(BenchmarkResult('Path.exists()', time_ms, category=CATEGORY))
        print_result('Path.exists()', time_ms)

        def is_file_check():
            return file_1kb.is_file()

        time_ms = time_operation(is_file_check, iterations=1_0000)
        results.append(BenchmarkResult('Path.is_file()', time_ms, category=CATEGORY))
        print_result('Path.is_file()', time_ms)

        def os_path_exists():
            return os.path.exists(str(file_1kb))

        time_ms = time_operation(os_path_exists, iterations=1_0000)
        results.append(BenchmarkResult('os.path.exists()', time_ms, category=CATEGORY))
        print_result('os.path.exists()', time_ms)

    return results


def main():
    """Run benchmarks and output results."""
    results = run_benchmarks()
    output = collect_results(CATEGORY, results)

    print()
    print(f'Total benchmarks: {len(results)}')

    return output


if __name__ == '__main__':
    main()
