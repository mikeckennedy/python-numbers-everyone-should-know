# Python Numbers Everyone Should Know

Benchmark suite measuring common Python operation costs - inspired by "Latency Numbers Every Programmer Should Know."

This project provides comprehensive performance benchmarks for Python 3.14, measuring everything from basic arithmetic operations to web framework request handling, helping developers understand the real-world performance characteristics of Python code.

## Full article, table, and write up

See the full write up associated with this project at: 

[Python Numbers Every Programmer Should Know @ mkennedy.codes](https://mkennedy.codes/posts/python-numbers-every-programmer-should-know/)

## Features

- **Comprehensive Coverage**: Memory sizes, basic operations, collections, attributes, JSON serialization, web frameworks, file I/O, databases, functions, async overhead, and import times
- **Accurate Measurements**: GC-controlled timing, dead code elimination prevention, proper warmup iterations
- **Multiple Output Formats**: Colored terminal output + JSON results for analysis
- **Flexible Execution**: Run all benchmarks, specific categories, or individual tests

## Installation

### Prerequisites

- Python 3.14.2 (or compatible version)
- pip or uv for package management

### Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Using uv (faster)
uv pip install -r requirements.txt
```

### Optional: MongoDB (for database benchmarks)

The MongoDB benchmarks will gracefully skip if MongoDB is not running:

```bash
# macOS
brew install mongodb-community
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

### Optional: Web Benchmark Tools

For web framework benchmarks, install `wrk` or `hey`:

```bash
# macOS
brew install wrk

# Or use hey
brew install hey
```

## Running Benchmarks

### Run All Benchmarks

```bash
# From project root
python3 code/run_all.py

# Or change to code directory
cd code
python3 run_all.py
```

This will:
- Run all benchmark categories in randomized order
- Display colored results in terminal
- Save results to `results.json`
- Show summary statistics at the end

### Run Specific Category

```bash
# Run only memory benchmarks
python3 code/run_all.py --category memory

# Run only JSON benchmarks
python3 code/run_all.py --category json_bench

# Run only web framework benchmarks
python3 code/run_all.py --category web
```

Available categories:
- `memory` - Memory sizes for strings, numbers, collections, classes
- `basic_ops` - Arithmetic, string operations, list operations
- `collections_bench` - Collection access, iteration, length operations
- `attributes` - Attribute access patterns and performance
- `json_bench` - JSON serialization/deserialization (stdlib, orjson, ujson, msgspec, pydantic)
- `web` - Request handling (Flask, Django, FastAPI, Starlette, Litestar)
- `file_io` - File read/write operations, pickle vs JSON
- `database` - SQLite, diskcache, MongoDB operations
- `functions` - Function call overhead, exceptions, type checking
- `async_bench` - Async/await overhead
- `imports` - Import time measurements

### Quick Test Run

```bash
# Run a subset of benchmarks for quick verification
python3 code/run_all.py --quick
```

### Custom Output File

```bash
# Save results to custom location
python3 code/run_all.py --output my-results.json
```

### Run Individual Benchmark

Each benchmark file can be run independently:

```bash
# Memory benchmarks
python3 code/memory/strings.py
python3 code/memory/numbers_mem.py
python3 code/memory/collections_mem.py
python3 code/memory/classes.py

# Basic operations
python3 code/basic_ops/arithmetic.py
python3 code/basic_ops/string_ops.py
python3 code/basic_ops/list_ops.py

# Collection benchmarks
python3 code/collections_bench/access.py
python3 code/collections_bench/iteration.py
python3 code/collections_bench/length.py

# Attribute access
python3 code/attributes/attribute_access.py
python3 code/attributes/other_ops.py

# JSON benchmarks
python3 code/json_bench/serialization.py
python3 code/json_bench/deserialization.py
python3 code/json_bench/pydantic_bench.py

# File I/O
python3 code/file_io/basic_ops.py
python3 code/file_io/pickle_vs_json.py

# Database
python3 code/database/sqlite_bench.py
python3 code/database/diskcache_bench.py
python3 code/database/mongodb_bench.py

# Functions
python3 code/functions/function_calls.py
python3 code/functions/exceptions.py
python3 code/functions/type_checking.py

# Async
python3 code/async_bench/async_overhead.py

# Imports
python3 code/imports/import_times.py
```

## Generating the Report

After running benchmarks, you have two options for viewing the results:

### Option 1: Interactive Notebook (Recommended)

View results in an interactive marimo notebook with visualizations:

```bash
# Run the marimo notebook
marimo edit marimo-notebook.py

# Or run it as an app
marimo run marimo-notebook.py
```

The notebook includes:
- **Interactive Charts**: Plotly visualizations for all benchmark categories
- **Comparisons**: Side-by-side performance comparisons
- **Insights**: Key takeaways and performance recommendations
- **Live Data**: Automatically loads from `results.json`
- **Easy Updates**: Just re-run benchmarks and refresh the notebook

### Option 2: Markdown Report

Generate a static markdown report from the results:

```bash
# Generate the-report.md from results.json
python3 code/generate_report.py

# Or specify custom paths
python3 code/generate_report.py --results my-results.json --template custom-template.md --output my-report.md
```

This will:
- Read benchmark results from `results.json`
- Fill in all placeholders in `the-report-template.md`
- Generate `the-report.md` with formatted values
- Apply automatic unit conversions (ms → ns/μs/ms, bytes → KB/MB)
- Add digit grouping (1,000 instead of 1000) for readability

The report generator uses a template-based system where placeholders like `{{MEMORY.EMPTY_PROCESS}}` are replaced with actual benchmark values. This ensures consistency and makes it easy to regenerate the report whenever benchmarks are updated.

## Understanding the Output

### Terminal Output

The benchmarks produce colored terminal output with:
- **Category Headers**: Bold section titles
- **Subheaders**: Operation groupings
- **Results**: Operation name + timing in milliseconds or memory in bytes/KB/MB
- **Summary**: JSON output location and statistics

### JSON Output

Results are saved to `results.json` with structure:

```json
{
  "metadata": {
    "python_version": "3.14.2",
    "platform": "macOS-...",
    "timestamp": "2024-..."
  },
  "results": {
    "memory": {
      "empty_process": {"value": 0.0, "unit": "MB"},
      "strings": {...}
    },
    "basic_ops": {...},
    ...
  }
}
```

## Project Structure

```
code/
├── utils/benchmark.py      # Shared timing, memory, and output utilities
├── memory/                 # Memory size benchmarks (Phase 2)
├── basic_ops/              # Arithmetic, strings, lists (Phase 3)
├── collections_bench/      # Access, length, iteration (Phase 4)
├── attributes/             # Attribute access patterns (Phase 5)
├── json_bench/             # JSON serialization (Phase 6)
├── web_frameworks/         # Framework request benchmarks (Phase 7)
├── file_io/                # File read/write benchmarks (Phase 8)
├── database/               # SQLite, diskcache, MongoDB (Phase 9)
├── functions/              # Function call overhead (Phase 10)
├── async_bench/            # Async overhead (Phase 11)
├── imports/                # Import time measurements (Phase 11b)
└── run_all.py              # Main runner (Phase 12)
```

## Development

See [coding-plan.md](coding-plan.md) for detailed implementation status and [CLAUDE.md](CLAUDE.md) for development guidelines.

### Key Utilities (code/utils/benchmark.py)

- `time_operation(func, iterations, warmup, repeat)` - Returns median ms
- `measure_size(obj)` - Shallow size in bytes
- `print_header()`, `print_result()` - Colored terminal output
- `BenchmarkResult`, `MemoryResult` - Result dataclasses
- `SIMPLE_OBJ`, `COMPLEX_OBJ` - Standard test objects

### Benchmark Accuracy

The suite includes several measures to ensure accurate benchmarks:
- **GC Control**: Garbage collection disabled during timing windows
- **Dead Code Prevention**: Results captured to prevent optimizer elimination
- **Proper Warmup**: Especially for complex operations (pydantic, orjson)
- **Randomized Order**: Benchmark execution order randomized to reduce bias
- **Consistent State**: Database benchmarks use fixed keys for reproducibility
- **Statistical Stability**: Multiple runs with median calculation

## License

MIT License - See LICENSE file for details
