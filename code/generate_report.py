"""Generate the-report.md from results.json using template placeholders.

This script reads results.json, formats benchmark values with appropriate units,
and fills in all {{CATEGORY.BENCHMARK_NAME}} placeholders in the-report.md file.

Usage:
    python code/generate_report.py
    python code/generate_report.py --results custom_results.json
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


def load_results(json_path: str | Path) -> dict:
    """Load benchmark results from JSON file."""
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f'Results file not found: {json_path}')

    with open(path) as f:
        return json.load(f)


def normalize_name(name: str) -> str:
    """Normalize benchmark name to placeholder format.

    Converts: "json.dumps() - simple" → "JSON_DUMPS_SIMPLE"
              "orjson.dumps() - complex" → "ORJSON_DUMPS_COMPLEX"
              "dict[key] (existing)" → "DICT_KEY_EXISTING"
              "try/except (no exception)" → "TRY_EXCEPT_NO_EXCEPTION"
              "regular class: read attr" → "REGULAR_CLASS_READ_ATTR"
    """
    # Replace common separators and special chars with underscores
    name = name.replace('()', '')
    name = name.replace(' - ', '_')
    name = name.replace('  ', ' ')
    name = re.sub(r'[()[\]{}]', ' ', name)
    name = re.sub(r'[/+%:@.]', '_', name)  # Replace special chars with underscores (including periods)
    name = re.sub(r"[,'\"]+", '', name)  # Remove commas and quotes
    name = name.replace(' ', '_')
    name = re.sub(r'_+', '_', name)  # Collapse multiple underscores
    name = name.strip('_')

    return name.upper()


def format_ops_per_sec(ms_value: float) -> str:
    """Format operations per second from millisecond value.

    Args:
        ms_value: Time in milliseconds

    Returns:
        Formatted ops/sec string like "53.5M ops/sec" or "1.6k ops/sec"
    """
    # Calculate ops/sec: 1 second = 1000 ms, so ops/sec = 1000 / ms
    ops_per_sec = 1000 / ms_value

    if ops_per_sec < 1_000:
        return f'{ops_per_sec:.1f} ops/sec'
    elif ops_per_sec < 1_000_000:
        k_ops = ops_per_sec / 1_000
        return f'{k_ops:.1f}k ops/sec'
    elif ops_per_sec < 1_000_000_000:
        m_ops = ops_per_sec / 1_000_000
        return f'{m_ops:.1f}M ops/sec'
    else:
        g_ops = ops_per_sec / 1_000_000_000
        return f'{g_ops:.1f}G ops/sec'


def format_value(value: float, unit: str) -> str:
    """Format value with appropriate unit conversion.

    Time values (ms):
        < 0.001 ms → nanoseconds (ns) + ops/sec
        < 1 ms → microseconds (μs) + ops/sec
        >= 1 ms → milliseconds (ms) + ops/sec

    Memory values:
        bytes → bytes/KB/MB based on magnitude
        MB → MB
    """
    if unit == 'ms':
        # Calculate ops/sec for all time values
        ops_suffix = f' ({format_ops_per_sec(value)})'

        if value < 0.001:
            # Convert to nanoseconds
            ns_value = value * 1_000_000
            if ns_value < 100:
                return f'{ns_value:.1f} ns{ops_suffix}'
            else:
                return f'{ns_value:,.0f} ns{ops_suffix}'
        elif value < 1:
            # Convert to microseconds
            us_value = value * 1_000
            if us_value < 10:
                return f'{us_value:.2f} μs{ops_suffix}'
            elif us_value < 100:
                return f'{us_value:.1f} μs{ops_suffix}'
            else:
                return f'{us_value:,.0f} μs{ops_suffix}'
        else:
            # Keep as milliseconds
            if value < 10:
                return f'{value:.3f} ms{ops_suffix}'
            elif value < 100:
                return f'{value:.2f} ms{ops_suffix}'
            else:
                return f'{value:,.1f} ms{ops_suffix}'

    elif unit == 'bytes':
        if value < 1024:
            return f'{int(value):,} bytes'
        elif value < 1024 * 1024:
            kb_value = value / 1024
            if kb_value < 10:
                return f'{kb_value:.2f} KB'
            else:
                return f'{kb_value:,.1f} KB'
        else:
            mb_value = value / (1024 * 1024)
            return f'{mb_value:,.2f} MB'

    elif unit == 'MB':
        return f'{value:,.2f} MB'

    elif unit == 'req/sec':
        # Convert req/sec to time per request + req/sec in parentheses
        # Time per request = 1 / req_per_sec (in seconds), then convert to appropriate unit
        time_per_req_sec = 1.0 / value
        time_per_req_ms = time_per_req_sec * 1000

        # Format req/sec portion
        if value < 1_000:
            req_suffix = f'{value:.1f} req/sec'
        elif value < 1_000_000:
            k_req = value / 1_000
            req_suffix = f'{k_req:.1f}k req/sec'
        else:
            m_req = value / 1_000_000
            req_suffix = f'{m_req:.2f}M req/sec'

        # Format time portion (similar to ms handling)
        if time_per_req_ms < 0.001:
            ns_value = time_per_req_ms * 1_000_000
            return f'{ns_value:.1f} ns ({req_suffix})'
        elif time_per_req_ms < 1:
            us_value = time_per_req_ms * 1_000
            if us_value < 10:
                return f'{us_value:.2f} μs ({req_suffix})'
            elif us_value < 100:
                return f'{us_value:.1f} μs ({req_suffix})'
            else:
                return f'{us_value:,.0f} μs ({req_suffix})'
        else:
            if time_per_req_ms < 10:
                return f'{time_per_req_ms:.3f} ms ({req_suffix})'
            elif time_per_req_ms < 100:
                return f'{time_per_req_ms:.2f} ms ({req_suffix})'
            else:
                return f'{time_per_req_ms:,.1f} ms ({req_suffix})'

    # Fallback for unknown units
    return f'{value} {unit}'


def create_placeholder_map(results: dict) -> dict[str, str]:
    """Create mapping of placeholder names to formatted values.

    Returns a dict like:
        {
            'METADATA.PYTHON_VERSION': '3.14.2',
            'MEMORY.EMPTY_PROCESS': '25.77 MB',
            'BASIC_OPS.INT_ADD': '20.6 ns',
            ...
        }
    """
    placeholder_map = {}

    # Add metadata placeholders
    metadata = results.get('metadata', {})
    placeholder_map['METADATA.PYTHON_VERSION'] = metadata.get('python_version', 'Unknown')
    placeholder_map['METADATA.PYTHON_IMPLEMENTATION'] = metadata.get('python_implementation', 'Unknown')
    placeholder_map['METADATA.PLATFORM'] = metadata.get('platform', 'Unknown')
    placeholder_map['METADATA.PROCESSOR'] = metadata.get('processor', 'Unknown')

    # Format timestamp
    timestamp = metadata.get('timestamp', '')
    if timestamp:
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            placeholder_map['METADATA.TIMESTAMP'] = dt.strftime('%Y-%m-%d')
        except (ValueError, AttributeError):
            placeholder_map['METADATA.TIMESTAMP'] = timestamp
    else:
        placeholder_map['METADATA.TIMESTAMP'] = 'Unknown'

    # Add system info placeholders
    ram_gb = metadata.get('ram_gb', 0)
    if ram_gb:
        placeholder_map['SYSTEM.RAM'] = f'{ram_gb:.1f} GB'
    else:
        placeholder_map['SYSTEM.RAM'] = 'Unknown'

    cpu_cores_physical = metadata.get('cpu_cores_physical', 0)
    cpu_cores_logical = metadata.get('cpu_cores_logical', 0)
    if cpu_cores_physical and cpu_cores_logical:
        placeholder_map['SYSTEM.CPU_CORES'] = f'{cpu_cores_physical} cores ({cpu_cores_logical} logical)'
    elif cpu_cores_logical:
        placeholder_map['SYSTEM.CPU_CORES'] = f'{cpu_cores_logical} cores'
    else:
        placeholder_map['SYSTEM.CPU_CORES'] = 'Unknown'

    # Add benchmark results
    categories = results.get('categories', {})
    for category_key, category_data in categories.items():
        category_upper = category_key.upper()

        for result in category_data.get('results', []):
            name = result['name']
            value = result['value']
            unit = result['unit']

            # Create normalized placeholder name
            normalized_name = normalize_name(name)
            placeholder_name = f'{category_upper}.{normalized_name}'

            # Format the value
            formatted_value = format_value(value, unit)
            placeholder_map[placeholder_name] = formatted_value

    return placeholder_map


def fill_template(template_content: str, placeholder_map: dict[str, str]) -> str:
    """Replace all {{PLACEHOLDER}} patterns with actual values.

    Uses case-insensitive matching to be forgiving of placeholder format.
    """

    def replacer(match):
        placeholder = match.group(1).strip().upper()
        return placeholder_map.get(placeholder, match.group(0))  # Keep original if not found

    # Match {{...}} patterns
    pattern = r'\{\{([^}]+)\}\}'
    filled = re.sub(pattern, replacer, template_content)

    return filled


def generate_report_from_template(results_path: str | Path, template_path: str | Path, output_path: str | Path) -> None:
    """Generate report by filling template with benchmark results.

    Args:
        results_path: Path to results.json file
        template_path: Path to template file (e.g., the-report-template.md)
        output_path: Path to output file (e.g., the-report.md)
    """
    print(f'Loading results from {results_path}...')
    results = load_results(results_path)

    print(f'Reading template from {template_path}...')
    template_path = Path(template_path)
    if not template_path.exists():
        raise FileNotFoundError(f'Template file not found: {template_path}')

    template_content = template_path.read_text(encoding='utf-8')

    print('Creating placeholder map...')
    placeholder_map = create_placeholder_map(results)
    print(f'  Found {len(placeholder_map)} placeholders')

    print('Filling template...')
    filled_content = fill_template(template_content, placeholder_map)

    print(f'Writing filled report to {output_path}...')
    output_path = Path(output_path)
    output_path.write_text(filled_content, encoding='utf-8')

    print('✓ Report generated successfully!')
    print(f'  Template: {template_path}')
    print(f'  Output: {output_path}')


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Generate the-report.md from the-report-template.md and results.json')
    parser.add_argument('--results', default='results.json', help='Path to results JSON file (default: results.json)')
    parser.add_argument(
        '--template', default='the-report-template.md', help='Path to template file (default: the-report-template.md)'
    )
    parser.add_argument('--output', default='the-report.md', help='Path to output report file (default: the-report.md)')

    args = parser.parse_args()

    try:
        generate_report_from_template(args.results, args.template, args.output)
    except Exception as e:
        print(f'Error: {e}')
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
