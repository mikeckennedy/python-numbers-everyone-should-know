# Python Numbers Everyone Should Know

Benchmark suite measuring common Python operation costs - inspired by "Latency Numbers Every Programmer Should Know."

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
└── run_all.py              # Main runner (Phase 12)
```

## Running Benchmarks

```bash
# Run individual benchmark
python code/collections_bench/access.py

# Run all benchmarks (when complete)
python code/run_all.py
```

## Development

- **Python:** 3.14.2
- **Dependencies:** See `requirements.piptools`
- **Plan:** See `coding-plan.md` for implementation status

### Key Utilities (code/utils/benchmark.py)

- `time_operation(func, iterations, warmup, repeat)` - Returns median ms
- `measure_size(obj)` - Shallow size in bytes
- `print_header()`, `print_result()` - Colored terminal output
- `BenchmarkResult`, `MemoryResult` - Result dataclasses
- `SIMPLE_OBJ`, `COMPLEX_OBJ` - Standard test objects

### Adding New Benchmarks

1. Create file in appropriate category folder
2. Import utilities from `utils.benchmark`
3. Define `run_benchmarks() -> list[BenchmarkResult]`
4. Add `main()` for standalone execution
5. Update folder's `__init__.py`
6. Mark complete in `coding-plan.md`
