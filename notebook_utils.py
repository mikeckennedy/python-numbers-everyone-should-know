"""
Visualization and data processing utilities for Python Numbers marimo notebook.
This module contains all the data loading, processing, and chart creation logic
to keep the notebook clean and report-focused.
"""

import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# ============================================================================
# Data Loading
# ============================================================================


def load_benchmark_results():
    """Load benchmark results from results.json"""
    results_path = Path('results.json')
    with open(results_path) as f:
        data = json.load(f)
    return data['metadata'], data['categories']


# ============================================================================
# Formatting Utilities
# ============================================================================


def format_time(ms_value):
    """Convert milliseconds to appropriate unit with ops/sec"""
    if ms_value < 0.001:
        ns_value = ms_value * 1_000_000
        ops_sec = 1_000_000_000 / ns_value if ns_value > 0 else 0
        return f'{ns_value:.1f} ns', f'{ops_sec / 1_000_000:.1f}M ops/sec'
    elif ms_value < 1:
        us_value = ms_value * 1_000
        ops_sec = 1_000_000 / us_value if us_value > 0 else 0
        return f'{us_value:.2f} μs', f'{ops_sec / 1_000:.1f}k ops/sec'
    else:
        ops_sec = 1_000 / ms_value if ms_value > 0 else 0
        return f'{ms_value:.2f} ms', f'{ops_sec:.1f} ops/sec'


def format_memory(bytes_value):
    """Convert bytes to appropriate unit"""
    if bytes_value < 1024:
        return f'{bytes_value} bytes'
    elif bytes_value < 1024**2:
        return f'{bytes_value / 1024:.2f} KB'
    else:
        return f'{bytes_value / (1024**2):.2f} MB'


# ============================================================================
# Chart Creation - Memory
# ============================================================================


def create_string_memory_chart(memory_results):
    """Create string memory usage chart (excluding 1000 char)"""
    string_data = [r for r in memory_results if 'string' in r['name'] and '1000_char' not in r['name']]
    string_df = pd.DataFrame(string_data)
    string_df['_size'] = string_df['name'].str.extract(r'(\d+)').fillna('0').astype(int)
    string_df = string_df.sort_values('_size')

    fig = px.bar(
        string_df,
        x='name',
        y='value',
        title='String Memory Usage by Size (up to 100 chars)',
        labels={'name': 'String Type', 'value': 'Bytes'},
        text='value',
    )
    fig.update_traces(texttemplate='%{text} bytes', textposition='outside', marker_color='#1565C0', textfont_size=14)
    fig.update_layout(
        showlegend=False,
        height=500,
        yaxis=dict(range=[0, string_df['value'].max() * 1.2]),
        margin=dict(t=50, b=100),
        xaxis_tickangle=-45,
    )
    return fig


def create_individual_numbers_chart(memory_results):
    """Create individual integer and float memory chart"""
    data = [
        r
        for r in memory_results
        if ('int' in r['name'] or 'float' in r['name']) and 'list' not in r['name'] and 'container' not in r['name']
    ]
    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x='name',
        y='value',
        title='Individual Integer and Float Memory Usage',
        labels={'name': 'Type', 'value': 'Bytes'},
        text='value',
    )
    fig.update_traces(texttemplate='%{text} bytes', textposition='outside', marker_color='#2E7D32', textfont_size=14)
    fig.update_layout(
        showlegend=False,
        height=500,
        yaxis=dict(range=[0, df['value'].max() * 1.2]),
        margin=dict(t=50, b=100),
        xaxis_tickangle=-45,
    )
    return fig


def create_number_lists_chart(memory_results):
    """Create list memory chart (1000 items: ints vs floats)"""
    data = [
        r
        for r in memory_results
        if '_1000_' in r['name'] and 'container' in r['name'] and 'list' in r['name'] and 'class' not in r['name']
    ]
    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x='name',
        y='value',
        title='List Memory Usage (1,000 items: ints vs floats)',
        labels={'name': 'List Type', 'value': 'Bytes'},
        text='value',
    )
    fig.update_traces(
        texttemplate='%{text:,.0f} bytes', textposition='outside', marker_color='#00838F', textfont_size=14
    )
    fig.update_layout(
        showlegend=False,
        height=500,
        yaxis=dict(range=[0, df['value'].max() * 1.2]),
        margin=dict(t=50, b=120),
        xaxis_tickangle=-45,
    )
    return fig


def create_empty_collections_chart(memory_results):
    """Create empty collection overhead chart"""
    data = [r for r in memory_results if r['name'] in ['empty_list', 'empty_dict', 'empty_set']]
    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        y='name',
        x='value',
        title='Empty Collection Memory Overhead',
        labels={'name': 'Collection Type', 'value': 'Bytes'},
        orientation='h',
        text='value',
    )
    fig.update_traces(texttemplate='%{text} bytes', textposition='outside', marker_color='#E65100', textfont_size=14)
    fig.update_layout(showlegend=False, height=400, xaxis=dict(range=[0, df['value'].max() * 1.2]), margin=dict(l=150))
    return fig


def create_collection_growth_chart(memory_results):
    """Create collection memory growth chart (excluding floats)"""
    growth_data = [
        r
        for r in memory_results
        if any(size in r['name'] for size in ['_10_', '_100_', '_1000_'])
        and 'container' in r['name']
        and 'floats' not in r['name']
    ]

    records = []
    for r in growth_data:
        name = r['name']
        if 'list' in name:
            coll_type = 'List (ints)'
        elif 'dict' in name:
            coll_type = 'Dict'
        elif 'set' in name:
            coll_type = 'Set'
        else:
            continue

        if '_10_' in name:
            size = 10
        elif '_100_' in name:
            size = 100
        elif '_1000_' in name:
            size = 1000
        else:
            continue

        records.append({'Collection': coll_type, 'Size': size, 'Bytes': r['value']})

    df = pd.DataFrame(records)

    fig = px.line(
        df,
        x='Size',
        y='Bytes',
        color='Collection',
        markers=True,
        title='Collection Memory Growth: List (ints), Dict, and Set',
        labels={'Size': 'Number of Items', 'Bytes': 'Memory (bytes)'},
        log_y=True,
    )
    fig.update_layout(height=500)
    return fig


def create_class_memory_chart(memory_results):
    """Create class instance memory chart"""
    data = [r for r in memory_results if 'class' in r['name'] and '5attr' in r['name'] or 'namedtuple' in r['name']]
    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x='name',
        y='value',
        title='Class Instance Memory (5 attributes)',
        labels={'name': 'Class Type', 'value': 'Bytes'},
        text='value',
    )
    fig.update_traces(texttemplate='%{text} bytes', textposition='outside', marker_color='#6A1B9A', textfont_size=14)
    fig.update_layout(
        showlegend=False,
        height=500,
        yaxis=dict(range=[0, df['value'].max() * 1.2]),
        margin=dict(t=50, b=120),
        xaxis_tickangle=-45,
    )
    return fig


def create_aggregate_class_memory_chart(memory_results):
    """Create aggregate class memory chart (1000 instances) and calculate savings"""
    data = [r for r in memory_results if 'list_1000' in r['name'] and 'class' in r['name']]
    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x='name',
        y='value',
        title='Memory for 1,000 Class Instances',
        labels={'name': 'Class Type', 'value': 'Bytes'},
        text='value',
    )
    fig.update_traces(
        texttemplate='%{text:,.0f} bytes<br>(%{customdata[0]})',
        textposition='outside',
        customdata=[[f'{v / 1024:.1f} KB'] for v in df['value']],
        marker_color='#C62828',
        textfont_size=14,
    )
    fig.update_layout(
        showlegend=False,
        height=500,
        yaxis=dict(range=[0, df['value'].max() * 1.2]),
        margin=dict(t=50, b=120),
        xaxis_tickangle=-45,
    )

    # Calculate savings
    regular_mem = next(r['value'] for r in data if 'regular' in r['name'])
    slots_mem = next(r['value'] for r in data if 'slots' in r['name'])
    savings_pct = ((regular_mem - slots_mem) / regular_mem) * 100
    savings_kb = (regular_mem - slots_mem) / 1024

    return fig, savings_pct, savings_kb


# ============================================================================
# Chart Creation - Basic Operations
# ============================================================================


def create_arithmetic_chart(basic_results):
    """Create arithmetic operations speed chart"""
    data = [r for r in basic_results if any(op in r['name'] for op in ['int_add', 'float_add', 'int_multiply'])]

    records = []
    for r in data:
        time_str, ops_str = format_time(r['value'])
        records.append(
            {
                'Operation': r['name'].replace('_', ' ').title(),
                'Time': r['value'],
                'Display': f'{time_str} ({ops_str})',
            }
        )

    df = pd.DataFrame(records)

    fig = px.bar(
        df,
        x='Operation',
        y='Time',
        title='Arithmetic Operation Speed',
        labels={'Time': 'Time (ms)'},
        text='Display',
    )
    fig.update_traces(textposition='outside', marker_color='#1976D2', textfont_size=14)
    fig.update_layout(
        showlegend=False, height=500, yaxis=dict(range=[0, df['Time'].max() * 1.2]), margin=dict(t=50, b=100)
    )
    return fig


def create_string_operations_chart(basic_results):
    """Create string operations comparison chart"""
    data = [
        r
        for r in basic_results
        if any(op in r['name'] for op in ['concat_small', 'f_string', 'format_method', 'percent_formatting'])
    ]

    name_map = {
        'concat_small': 'Concatenation (+)',
        'f_string': 'f-string',
        'format_method': '.format()',
        'percent_formatting': '% formatting',
    }

    records = []
    for r in data:
        time_str, ops_str = format_time(r['value'])
        records.append(
            {
                'Operation': name_map.get(r['name'], r['name']),
                'Time': r['value'],
                'Display': f'{time_str}',
            }
        )

    df = pd.DataFrame(records).sort_values('Time')

    # Create performance-based colors
    fastest = df['Time'].min()
    df['Relative'] = df['Time'] / fastest

    colors = []
    for rel in df['Relative']:
        if rel < 1.5:
            colors.append('#2E7D32')  # Green - fast
        elif rel < 2:
            colors.append('#F9A825')  # Yellow - medium
        elif rel < 2.5:
            colors.append('#EF6C00')  # Orange - slower
        else:
            colors.append('#C62828')  # Red - slow

    fig = px.bar(
        df,
        y='Operation',
        x='Time',
        title='String Formatting Speed Comparison',
        labels={'Time': 'Time (ms)'},
        orientation='h',
        text='Display',
    )
    fig.update_traces(textposition='outside', marker_color=colors, textfont_size=14)
    fig.update_layout(height=500, xaxis=dict(range=[0, df['Time'].max() * 1.2]), margin=dict(l=150, t=50))
    return fig


def create_list_comp_vs_loop_chart(basic_results):
    """Create list comprehension vs for loop comparison"""
    data = [r for r in basic_results if '1000' in r['name'] and ('comp' in r['name'] or 'loop' in r['name'])]

    comp_time = next(r['value'] for r in data if 'comp' in r['name'])
    loop_time = next(r['value'] for r in data if 'loop' in r['name'])

    fig = go.Figure()

    for idx, (method, time_val) in enumerate([('List Comprehension', comp_time), ('For Loop', loop_time)]):
        time_str, ops_str = format_time(time_val)
        fig.add_trace(
            go.Bar(
                x=[method],
                y=[time_val],
                name=method,
                text=f'{time_str}<br>({ops_str})',
                textposition='outside',
                marker_color=['#3b82f6', '#ef4444'][idx],
                textfont_size=14,
            )
        )

    fig.update_layout(
        title='List Comprehension vs For Loop (1,000 items)',
        yaxis_title='Time (ms)',
        showlegend=False,
        height=500,
        yaxis=dict(range=[0, max(comp_time, loop_time) * 1.2]),
        margin=dict(t=50, b=100),
    )
    return fig


# ============================================================================
# Helper Functions
# ============================================================================


def get_category_options():
    """Get category options for navigation dropdown"""
    return {
        'Memory Costs': 'memory',
        'Basic Operations': 'basic_ops',
        'Collections': 'collections',
        'Attributes': 'attributes',
        'JSON & Serialization': 'json',
        'Web Frameworks': 'web',
        'File I/O': 'file_io',
        'Database': 'database',
        'Functions': 'functions',
        'Async': 'async',
        'Imports': 'imports',
    }


def get_benchmark_counts(categories):
    """Get benchmark counts per category"""
    return {name: cat['benchmark_count'] for name, cat in categories.items()}
