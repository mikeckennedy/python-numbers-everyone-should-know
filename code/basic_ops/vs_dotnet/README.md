# Python vs C# Basic Operations Benchmark

This directory contains a C# implementation of the Python basic operations benchmarks for performance comparison.

## Requirements

- .NET 10.0 SDK
- Python 3.14+ (for comparison)

## Running the C# Benchmark

```bash
cd code/basic_ops/vs_dotnet
dotnet run --configuration Release
```

## Running the Python Benchmarks

```bash
# From the project root
python code/basic_ops/arithmetic.py
python code/basic_ops/string_ops.py
python code/basic_ops/list_ops.py
```

## Running the Comparison

```bash
python compare.py
```

This will run both Python and C# benchmarks and display a side-by-side comparison table.

## What's Being Measured

### Arithmetic Operations
- Integer addition, multiplication, division
- Float addition, multiplication, division

### String Operations
- Small and medium string concatenation
- String interpolation (f-strings in Python, $ in C#)
- Format methods (`.format()` vs `String.Format()`)
- String join and split operations

### List Operations
- Single item append/add
- List comprehensions (Python) vs LINQ (C#)
- For-loops with append/add
- List extend/AddRange
- List copying

## Notes

- All benchmarks use the same iteration counts as the Python versions
- C# benchmarks include warmup runs and garbage collection between tests
- Results are in microseconds (µs) per operation
- C# is compiled in Release mode for optimal performance
