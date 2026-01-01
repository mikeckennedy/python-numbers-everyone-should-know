# Python vs C# Performance Comparison

Results from running identical basic operations benchmarks in Python 3.14 and .NET 10.0.

## Summary

Overall, **C# is 2-14x faster** than Python for most operations, with the notable exception of f-string formatting where Python edges ahead slightly.

## Key Findings

### Arithmetic Operations (C# wins: 2-14x faster)
- **Integer operations**: C# is 2.5-11.6x faster
- **Float operations**: C# is 9.7-14.2x faster
- Float division shows the largest gap (14.2x speedup in C#)

### String Operations (Mixed results)
- **Simple concatenation**: C# is 2.6-2.9x faster
- **f-string vs interpolation**: Python is slightly faster (1.1x)
- **Format methods**: C# String.Format() is 2.0x faster than Python's .format()
- **Join/Split**: C# is 1.6-2.6x faster

### List Operations (C# wins: 1.4-10.7x faster)
- **Single append**: C# is 2.0x faster
- **Small lists (10 items)**: C# is 1.6-1.7x faster
- **Medium lists (100 items)**: C# is 2.6-5.0x faster
- **Large lists (1000 items)**: C# is 2.3-10.7x faster
  - List comprehensions show the biggest gap (10.7x)
- **List copy**: C# is 5.4x faster

## Detailed Results

```
Operation                               Python (ms)         C# (ms)      Speedup
--------------------------------------------------------------------------------

Arithmetic Operations
--------------------------------------------------------------------------------
Int Add                                    0.000020        0.000008        2.54x
Int Multiply                               0.000021        0.000002        9.77x
Int Divide                                 0.000024        0.000002       11.59x
Float Add                                  0.000020        0.000002        9.68x
Float Multiply                             0.000023        0.000002       10.87x
Float Divide                               0.000022        0.000002       14.19x

String Operations
--------------------------------------------------------------------------------
Concat Small                               0.000040        0.000014        2.89x
Concat Medium                              0.000043        0.000016        2.64x
F String                                   0.000065        0.000072   1.10x (Py)
Format Method                              0.000101        0.000050        2.03x
Percent Formatting                         0.000084        0.000046        1.83x
Join Small                                 0.000046        0.000018        2.58x
Split                                      0.000079        0.000049        1.62x

List Operations
--------------------------------------------------------------------------------
List Append                                0.000029        0.000014        1.98x
List Comp 10                               0.000095        0.000056        1.68x
For Loop 10                                0.000120        0.000077        1.55x
List Comp 100                              0.000631        0.000126        4.99x
For Loop 100                               0.000952        0.000367        2.59x
List Comp 1000                             0.009521        0.000892       10.68x
For Loop 1000                              0.011918        0.005185        2.30x
List Extend                                0.000066        0.000049        1.35x
List Copy 100                              0.000128        0.000024        5.41x
```

## Test Environment

- **Python**: 3.14.2
- **C#**: .NET 10.0.101
- **Platform**: macOS (Darwin 25.2.0)
- **Compiler**: Release mode with optimizations

## Methodology

Both benchmarks use identical approaches:
- Warmup iterations before measurement
- Garbage collection before timing
- Multiple repeated runs with median calculation
- Same iteration counts for each operation
- Results in milliseconds per operation

## Interpretation

These results show that:

1. **C# excels at numeric computation** - The JIT compiler produces highly optimized machine code for arithmetic operations

2. **String formatting is competitive** - Python's f-strings are remarkably well-optimized, actually beating C#'s string interpolation slightly

3. **List operations scale better in C#** - The performance gap widens with larger collections, suggesting better memory layout and cache utilization

4. **Python's overhead is consistent** - Most operations show a fairly predictable 2-5x difference, with some outliers

5. **Both are very fast** - Even the "slower" operations are sub-millisecond, showing both runtimes are highly optimized for these basic operations

## Running the Benchmarks

```bash
# Run comparison
cd code/basic_ops/vs_dotnet
python compare.py

# Run just C#
dotnet run --configuration Release

# Run just Python
python ../arithmetic.py
python ../string_ops.py
python ../list_ops.py
```
