#!/usr/bin/env python3
"""
Python Numbers Everyone Should Know - Main Runner

Runs all benchmarks and collects results into a unified JSON structure.

Usage:
    python run_all.py                  # Run all benchmarks
    python run_all.py --quick          # Run subset for quick test
    python run_all.py --category memory # Run specific category
    python run_all.py --output results.json  # Custom output file
"""

import argparse
import datetime
import json
import platform
import random
import sys
import warnings
from pathlib import Path
from typing import Any

import psutil
from colorama import Fore, Style, init

# Suppress Pydantic V1 compatibility warning on Python 3.14+
warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')


# Initialize colorama
init(autoreset=True)

# Add code directory to path
CODE_DIR = Path(__file__).parent
sys.path.insert(0, str(CODE_DIR))


# =============================================================================
# Benchmark Registry
# =============================================================================

BENCHMARK_CATEGORIES = {
    'memory': {
        'name': 'Memory Sizes',
        'modules': [
            ('memory.empty_process', 'run_benchmarks'),
            ('memory.strings', 'run_benchmarks'),
            ('memory.numbers_mem', 'run_benchmarks'),
            ('memory.collections_mem', 'run_benchmarks'),
            ('memory.classes', 'run_benchmarks'),
        ],
    },
    'basic_ops': {
        'name': 'Basic Operations',
        'modules': [
            ('basic_ops.arithmetic', 'run_benchmarks'),
            ('basic_ops.string_ops', 'run_benchmarks'),
            ('basic_ops.list_ops', 'run_benchmarks'),
        ],
    },
    'collections': {
        'name': 'Collection Operations',
        'modules': [
            ('collections_bench.access', 'run_benchmarks'),
            ('collections_bench.length', 'run_benchmarks'),
            ('collections_bench.iteration', 'run_benchmarks'),
        ],
    },
    'attributes': {
        'name': 'Attribute Access',
        'modules': [
            ('attributes.attribute_access', 'run_benchmarks'),
            ('attributes.other_ops', 'run_benchmarks'),
        ],
    },
    'json': {
        'name': 'JSON Serialization',
        'modules': [
            ('json_bench.serialization', 'run_benchmarks'),
            ('json_bench.deserialization', 'run_benchmarks'),
            ('json_bench.pydantic_bench', 'run_benchmarks'),
        ],
    },
    'web': {
        'name': 'Web Frameworks',
        'modules': [
            ('web_frameworks.benchmarks', 'run_benchmarks'),
        ],
    },
    'file_io': {
        'name': 'File I/O',
        'modules': [
            ('file_io.basic_ops', 'run_benchmarks'),
            ('file_io.pickle_vs_json', 'run_benchmarks'),
        ],
    },
    'database': {
        'name': 'Database Operations',
        'modules': [
            ('database.sqlite_bench', 'run_benchmarks'),
            ('database.diskcache_bench', 'run_benchmarks'),
            ('database.mongodb_bench', 'run_benchmarks'),
        ],
    },
    'functions': {
        'name': 'Function Calls',
        'modules': [
            ('functions.function_calls', 'run_benchmarks'),
            ('functions.exceptions', 'run_benchmarks'),
            ('functions.type_checking', 'run_benchmarks'),
        ],
    },
    'async': {
        'name': 'Async Overhead',
        'modules': [
            ('async_bench.async_overhead', 'run_benchmarks'),
        ],
    },
    'imports': {
        'name': 'Import Times',
        'modules': [
            ('imports.import_times', 'run_benchmarks'),
        ],
    },
}

# Quick mode runs a subset
QUICK_CATEGORIES = ['basic_ops', 'collections', 'functions']


# =============================================================================
# Runner Functions
# =============================================================================


def get_metadata() -> dict[str, Any]:
    """Collect system metadata."""
    # Get system RAM in GB
    ram_gb = psutil.virtual_memory().total / (1024**3)

    # Get CPU core counts
    cpu_cores_physical = psutil.cpu_count(logical=False) or 0
    cpu_cores_logical = psutil.cpu_count(logical=True) or 0

    return {
        'python_version': platform.python_version(),
        'python_implementation': platform.python_implementation(),
        'platform': platform.platform(),
        'processor': platform.processor(),
        'ram_gb': round(ram_gb, 1),
        'cpu_cores_physical': cpu_cores_physical,
        'cpu_cores_logical': cpu_cores_logical,
        'timestamp': datetime.datetime.now().isoformat(),
    }


def import_and_run(module_name: str, func_name: str) -> list[dict[str, Any]]:
    """Import a module and run its benchmark function.

    Returns a list of result dictionaries (handles both BenchmarkResult objects
    and pre-serialized dict formats from different modules).
    """
    try:
        import importlib

        module = importlib.import_module(module_name)
        func = getattr(module, func_name)
        raw_results = func()

        # Handle different return formats
        if isinstance(raw_results, dict):
            # Some modules return {"results": [...]} dict format
            if 'results' in raw_results:
                return raw_results['results']
            return [raw_results]
        elif isinstance(raw_results, list):
            # Most modules return list of BenchmarkResult/MemoryResult
            results = []
            for r in raw_results:
                if hasattr(r, 'to_dict'):
                    results.append(r.to_dict())
                elif isinstance(r, dict):
                    results.append(r)
            return results
        return []
    except ImportError as e:
        print(f'{Fore.RED}✗ Failed to import {module_name}: {e}')
        return []
    except Exception as e:
        print(f'{Fore.RED}✗ Error running {module_name}.{func_name}: {e}')
        return []


def run_category(category_key: str, category_info: dict) -> dict[str, Any]:
    """Run all benchmarks in a category."""
    print()
    print(f'{Fore.CYAN}{Style.BRIGHT}{"=" * 60}')
    print(f'{Fore.CYAN}{Style.BRIGHT}  Category: {category_info["name"]}')
    print(f'{Fore.CYAN}{Style.BRIGHT}{"=" * 60}')

    all_results = []

    # Randomize module execution order to reduce ordering bias
    modules = list(category_info['modules'])
    random.shuffle(modules)

    for module_name, func_name in modules:
        results = import_and_run(module_name, func_name)
        all_results.extend(results)

    return {
        'name': category_info['name'],
        'benchmark_count': len(all_results),
        'results': all_results,
    }


def print_summary(all_results: dict[str, Any]) -> None:
    """Print a summary table of all results."""
    print()
    print(f'{Fore.CYAN}{Style.BRIGHT}{"=" * 60}')
    print(f'{Fore.CYAN}{Style.BRIGHT}{"SUMMARY".center(60)}')
    print(f'{Fore.CYAN}{Style.BRIGHT}{"=" * 60}')
    print()

    total_benchmarks = 0

    # Header
    print(f'{Fore.WHITE}{Style.BRIGHT}{"Category":<30} {"Benchmarks":>15}')
    print(f'{Fore.CYAN}{"-" * 45}')

    for category_key, category_data in all_results['categories'].items():
        count = category_data['benchmark_count']
        total_benchmarks += count
        print(f'{Fore.WHITE}{category_data["name"]:<30} {Fore.GREEN}{count:>15}')

    print(f'{Fore.CYAN}{"-" * 45}')
    print(f'{Fore.WHITE}{Style.BRIGHT}{"TOTAL":<30} {Fore.GREEN}{Style.BRIGHT}{total_benchmarks:>15}')
    print()


def print_highlights(all_results: dict[str, Any]) -> None:
    """Print performance highlights."""
    print(f'{Fore.YELLOW}{Style.BRIGHT}Performance Highlights')
    print(f'{Fore.YELLOW}{"-" * 25}')

    highlights = []

    # Collect some interesting results
    for category_key, category_data in all_results['categories'].items():
        for result in category_data['results']:
            name = result['name']
            value = result['value']
            unit = result['unit']

            # Pick interesting benchmarks
            if any(
                kw in name.lower()
                for kw in ['empty function', 'dict lookup', 'list append', 'json.dumps', 'isinstance', 'try/except']
            ):
                highlights.append((name, value, unit))

    # Print top highlights
    for name, value, unit in highlights[:10]:
        if unit == 'ms':
            if value < 0.001:
                display = f'{value * 1_000_000:.0f} ns'
            elif value < 1:
                display = f'{value * 1000:.1f} µs'
            else:
                display = f'{value:.2f} ms'
        else:
            display = f'{value} {unit}'
        print(f'  {Fore.WHITE}{name:<40} {Fore.GREEN}{display}')

    print()


def save_results(results: dict[str, Any], output_path: Path) -> None:
    """Save results to JSON file."""
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'{Fore.GREEN}✓ Results saved to {output_path}')


def main():
    parser = argparse.ArgumentParser(description='Run Python Numbers Everyone Should Know benchmarks')
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Run quick subset of benchmarks',
    )
    parser.add_argument(
        '--category',
        '-c',
        choices=list(BENCHMARK_CATEGORIES.keys()),
        help='Run specific category only',
    )
    parser.add_argument(
        '--output',
        '-o',
        type=Path,
        default=CODE_DIR.parent / 'results.json',
        help='Output JSON file (default: results.json)',
    )
    parser.add_argument(
        '--no-save',
        action='store_true',
        help="Don't save results to file",
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List available categories and exit',
    )

    args = parser.parse_args()

    # List categories
    if args.list:
        print(f'{Fore.CYAN}{Style.BRIGHT}Available benchmark categories:')
        print()
        for key, info in BENCHMARK_CATEGORIES.items():
            module_count = len(info['modules'])
            print(f'  {Fore.WHITE}{key:<15} {Fore.GREEN}{info["name"]:<25} ({module_count} modules)')
        return

    # Determine which categories to run
    if args.category:
        categories_to_run = {args.category: BENCHMARK_CATEGORIES[args.category]}
    elif args.quick:
        categories_to_run = {k: v for k, v in BENCHMARK_CATEGORIES.items() if k in QUICK_CATEGORIES}
        print(f'{Fore.YELLOW}Running in quick mode (subset of benchmarks)')
    else:
        categories_to_run = BENCHMARK_CATEGORIES

    # Print header
    print()
    print(f'{Fore.CYAN}{Style.BRIGHT}╔{"═" * 58}╗')
    print(f'{Fore.CYAN}{Style.BRIGHT}║{"Python Numbers Everyone Should Know".center(58)}║')
    print(f'{Fore.CYAN}{Style.BRIGHT}║{"Benchmark Suite".center(58)}║')
    print(f'{Fore.CYAN}{Style.BRIGHT}╚{"═" * 58}╝')

    # Collect metadata
    metadata = get_metadata()
    print()
    print(f'{Fore.WHITE}Python: {Fore.GREEN}{metadata["python_version"]} ({metadata["python_implementation"]})')
    print(f'{Fore.WHITE}Platform: {Fore.GREEN}{metadata["platform"]}')
    print(f'{Fore.WHITE}Started: {Fore.GREEN}{metadata["timestamp"]}')

    # Run benchmarks
    all_results = {
        'metadata': metadata,
        'categories': {},
    }

    for category_key, category_info in categories_to_run.items():
        category_results = run_category(category_key, category_info)
        all_results['categories'][category_key] = category_results

    # Print summary
    print_summary(all_results)
    print_highlights(all_results)

    # Save results
    if not args.no_save:
        save_results(all_results, args.output)

    print(f'{Fore.GREEN}{Style.BRIGHT}✓ Benchmark suite complete!')


if __name__ == '__main__':
    main()
