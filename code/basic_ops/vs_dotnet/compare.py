#!/usr/bin/env python3
"""
Run Python and C# benchmarks and compare results side by side.
"""

import json
import subprocess
import sys
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from basic_ops.arithmetic import run_benchmarks as run_arithmetic
from basic_ops.string_ops import run_benchmarks as run_string_ops
from basic_ops.list_ops import run_benchmarks as run_list_ops


def run_python_benchmarks():
    """Run Python benchmarks and collect results."""
    print("Running Python benchmarks...")
    print()

    results = {}

    # Run arithmetic benchmarks
    arithmetic_data = run_arithmetic()
    for result in arithmetic_data['results']:
        results[result['name']] = result['value']

    print()

    # Run string benchmarks
    string_data = run_string_ops()
    for result in string_data['results']:
        results[result['name']] = result['value']

    print()

    # Run list benchmarks
    list_data = run_list_ops()
    for result in list_data['results']:
        results[result['name']] = result['value']

    return results


def run_csharp_benchmarks():
    """Run C# benchmarks and collect results."""
    print("\n" + "="*80 + "\n")
    print("Running C# benchmarks...")
    print()

    # Build and run C# project
    csharp_dir = Path(__file__).parent

    try:
        # Run in release mode for fair comparison
        result = subprocess.run(
            ['dotnet', 'run', '--configuration', 'Release'],
            cwd=csharp_dir,
            capture_output=True,
            text=True,
            check=True
        )

        # Parse JSON output from the C# program
        output_lines = result.stdout.split('\n')
        json_start = -1
        for i, line in enumerate(output_lines):
            if line.strip() == 'JSON Output:':
                json_start = i + 1
                break

        if json_start == -1:
            print("Error: Could not find JSON output in C# benchmark")
            return {}

        json_text = '\n'.join(output_lines[json_start:])
        data = json.loads(json_text)

        # Convert to dict
        results = {}
        for result in data['results']:
            results[result['name']] = result['value']

        return results

    except subprocess.CalledProcessError as e:
        print(f"Error running C# benchmarks: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return {}
    except FileNotFoundError:
        print("Error: dotnet command not found. Please install .NET 10.0 SDK")
        return {}


def print_comparison(python_results, csharp_results):
    """Print side-by-side comparison table."""
    print("\n" + "="*80 + "\n")
    print("COMPARISON: Python vs C#")
    print("="*80)
    print()

    # Define benchmark groups for organized output
    groups = {
        'Arithmetic Operations': [
            'int_add',
            'int_multiply',
            'int_divide',
            'float_add',
            'float_multiply',
            'float_divide'
        ],
        'String Operations': [
            'concat_small',
            'concat_medium',
            'f_string',
            'format_method',
            'percent_formatting',
            'join_small',
            'split'
        ],
        'List Operations': [
            'list_append',
            'list_comp_10',
            'for_loop_10',
            'list_comp_100',
            'for_loop_100',
            'list_comp_1000',
            'for_loop_1000',
            'list_extend',
            'list_copy_100'
        ]
    }

    # Print header
    print(f"{'Operation':<35} {'Python (ms)':>15} {'C# (ms)':>15} {'Speedup':>12}")
    print("-" * 80)

    for group_name, benchmark_names in groups.items():
        print(f"\n{group_name}")
        print("-" * 80)

        for name in benchmark_names:
            if name in python_results and name in csharp_results:
                py_val = python_results[name]
                cs_val = csharp_results[name]

                # Calculate speedup (positive = C# faster, negative = Python faster)
                if cs_val > 0:
                    speedup = py_val / cs_val
                    speedup_str = f"{speedup:.2f}x"
                    if speedup < 1:
                        speedup_str = f"{1/speedup:.2f}x (Py)"
                else:
                    speedup_str = "N/A"

                # Format name nicely
                display_name = name.replace('_', ' ').title()

                print(f"{display_name:<35} {py_val:>15.6f} {cs_val:>15.6f} {speedup_str:>12}")

    print("\n" + "="*80)
    print("Note: Speedup shows how many times faster C# is compared to Python.")
    print("      (Py) indicates Python is faster for that operation.")
    print("="*80 + "\n")


def main():
    """Main comparison runner."""
    # Run benchmarks
    python_results = run_python_benchmarks()
    csharp_results = run_csharp_benchmarks()

    if not csharp_results:
        print("\nWarning: C# benchmarks failed to run. Showing Python results only.")
        return

    # Print comparison
    print_comparison(python_results, csharp_results)


if __name__ == '__main__':
    main()
