"""
Visualization and data processing utilities for Python Numbers marimo notebook.
This module contains all the data loading, processing, and chart creation logic
to keep the notebook clean and report-focused.
"""

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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


# ============================================================================
# Chart Creation - Collections
# ============================================================================


def create_collection_access_chart(coll_results):
    """Create collection access speed comparison"""
    data = [
        r
        for r in coll_results
        if r.get('category') == 'collections_access'
        and r['name'] in ['dict[key] (existing)', 'item in set (existing)', 'list[index]', 'item in list (last)']
    ]

    records = []
    for r in data:
        time_str, ops_str = format_time(r['value'])
        records.append({'Operation': r['name'], 'Time': r['value'], 'Display': f'{time_str} ({ops_str})'})

    df = pd.DataFrame(records).sort_values('Time')

    fig = px.bar(
        df,
        y='Operation',
        x='Time',
        title='Collection Access Speed (note: list membership is O(n) for 1000 items)',
        labels={'Time': 'Time (ms)'},
        orientation='h',
        text='Display',
        log_x=True,
    )
    fig.update_traces(textposition='outside', marker_color='#1976D2', textfont_size=14)
    fig.update_layout(height=500, margin=dict(l=200, t=50))
    return fig


def create_collection_iteration_chart(coll_results):
    """Create collection iteration speed comparison"""
    data = [
        r
        for r in coll_results
        if r.get('category') == 'collections_iteration'
        and any(
            pattern in r['name']
            for pattern in ['for item in list', 'for key in dict', 'for item in set', 'for i in range']
        )
        and 'enumerate' not in r['name']
    ]

    records = []
    for r in data:
        time_str, ops_str = format_time(r['value'])
        records.append({'Operation': r['name'], 'Time': r['value'], 'Display': f'{time_str} ({ops_str})'})

    df = pd.DataFrame(records).sort_values('Time')

    fig = px.bar(
        df,
        y='Operation',
        x='Time',
        title='Iteration Speed Comparison (1,000 items)',
        labels={'Time': 'Time (ms)'},
        orientation='h',
        text='Display',
    )
    fig.update_traces(textposition='outside', marker_color='#00838F', textfont_size=14)
    fig.update_layout(height=500, margin=dict(l=200, t=50))
    return fig


# ============================================================================
# Chart Creation - JSON & Serialization
# ============================================================================


def create_json_serialization_chart(json_results):
    """Create JSON serialization comparison (complex object)"""
    data = [
        r
        for r in json_results
        if ('dumps' in r['name'] or 'encode' in r['name']) and 'complex' in r['name'] and 'no ascii' not in r['name']
    ]

    records = []
    for r in data:
        time_str, ops_str = format_time(r['value'])
        library = r['name'].split('.')[0].split('(')[0]
        records.append({'Library': library, 'Time': r['value'], 'Display': f'{time_str} ({ops_str})'})

    df = pd.DataFrame(records).sort_values('Time')
    json_time = df[df['Library'] == 'json']['Time'].iloc[0]
    df['Speedup'] = json_time / df['Time']

    fig = px.bar(
        df,
        y='Library',
        x='Time',
        title='JSON Serialization Speed (Complex Object)',
        labels={'Time': 'Time (ms)'},
        orientation='h',
        text='Display',
    )
    fig.update_traces(textposition='outside', marker_color='#4CAF50', textfont_size=14)
    fig.update_layout(height=500, margin=dict(l=150, t=50))
    return fig, df


def create_json_deserialization_chart(json_results):
    """Create JSON deserialization comparison (complex object)"""
    data = [
        r
        for r in json_results
        if ('loads' in r['name'] or 'decode' in r['name']) and 'complex' in r['name'] and 'str' not in r['name']
    ]

    records = []
    for r in data:
        time_str, ops_str = format_time(r['value'])
        library = r['name'].split('.')[0].split('(')[0]
        records.append({'Library': library, 'Time': r['value'], 'Display': f'{time_str} ({ops_str})'})

    df = pd.DataFrame(records).sort_values('Time')
    json_time = df[df['Library'] == 'json']['Time'].iloc[0]
    df['Speedup'] = json_time / df['Time']

    fig = px.bar(
        df,
        y='Library',
        x='Time',
        title='JSON Deserialization Speed (Complex Object)',
        labels={'Time': 'Time (ms)'},
        orientation='h',
        text='Display',
    )
    fig.update_traces(textposition='outside', marker_color='#FF9800', textfont_size=14)
    fig.update_layout(height=500, margin=dict(l=150, t=50))
    return fig, df


# ============================================================================
# Chart Creation - Database
# ============================================================================


def create_database_comparison_chart(db_results):
    """Create database write/read performance comparison"""
    sqlite_insert = next((r for r in db_results if 'INSERT (JSON blob)' in r['name']), None)
    sqlite_select = next((r for r in db_results if 'SELECT by primary key' in r['name']), None)
    diskcache_set = next((r for r in db_results if 'cache.set() (complex obj)' in r['name']), None)
    diskcache_get = next((r for r in db_results if 'cache.get() (complex obj)' in r['name']), None)

    if not all([sqlite_insert, sqlite_select, diskcache_set, diskcache_get]):
        return None

    records = []
    for name, val in [
        ('SQLite Write', sqlite_insert['value']),
        ('SQLite Read', sqlite_select['value']),
        ('diskcache Write', diskcache_set['value']),
        ('diskcache Read', diskcache_get['value']),
    ]:
        time_str, ops_str = format_time(val)
        records.append({'Operation': name, 'Time': val, 'Display': f'{time_str} ({ops_str})'})

    df = pd.DataFrame(records)

    fig = px.bar(
        df,
        x='Operation',
        y='Time',
        title='Database Performance: SQLite vs diskcache',
        labels={'Time': 'Time (ms)'},
        text='Display',
        log_y=True,
    )
    fig.update_traces(textposition='outside', marker_color='#9C27B0', textfont_size=14)
    fig.update_layout(height=500, margin=dict(t=50, b=100))
    return fig


# ============================================================================
# Chart Creation - File I/O
# ============================================================================


def create_file_io_chart(file_results):
    """Create file I/O operations chart"""
    data = [
        r
        for r in file_results
        if r.get('category') == 'file_io_basic'
        and any(op in r['name'] for op in ['open() + close()', 'read 1KB', 'read 1MB', 'write 1KB', 'write 1MB'])
    ]

    records = []
    for r in data:
        time_str, ops_str = format_time(r['value'])
        records.append({'Operation': r['name'], 'Time': r['value'], 'Display': f'{time_str}'})

    df = pd.DataFrame(records)

    fig = px.bar(
        df,
        x='Operation',
        y='Time',
        title='File I/O Performance',
        labels={'Time': 'Time (ms)'},
        text='Display',
        log_y=True,
    )
    fig.update_traces(textposition='outside', marker_color='#795548', textfont_size=14)
    fig.update_layout(height=500, margin=dict(t=50, b=120), xaxis_tickangle=-45)
    return fig


def create_pickle_vs_json_chart(file_results):
    """Create pickle vs JSON comparison"""
    pickle_dumps = next((r for r in file_results if r['name'] == 'pickle.dumps()'), None)
    pickle_loads = next((r for r in file_results if r['name'] == 'pickle.loads()'), None)
    json_dumps = next((r for r in file_results if r['name'] == 'json.dumps()'), None)
    json_loads = next((r for r in file_results if r['name'] == 'json.loads()'), None)

    if not all([pickle_dumps, pickle_loads, json_dumps, json_loads]):
        return None

    fig = go.Figure()

    operations = ['Serialize (dumps)', 'Deserialize (loads)']
    pickle_times = [pickle_dumps['value'], pickle_loads['value']]
    json_times = [json_dumps['value'], json_loads['value']]

    fig.add_trace(
        go.Bar(
            name='Pickle',
            x=operations,
            y=pickle_times,
            text=[format_time(t)[0] for t in pickle_times],
            textposition='outside',
            marker_color='#8b5cf6',
            textfont_size=14,
        )
    )

    fig.add_trace(
        go.Bar(
            name='JSON',
            x=operations,
            y=json_times,
            text=[format_time(t)[0] for t in json_times],
            textposition='outside',
            marker_color='#f59e0b',
            textfont_size=14,
        )
    )

    fig.update_layout(
        title='Pickle vs JSON Serialization (Complex Object)',
        yaxis_title='Time (ms)',
        barmode='group',
        height=500,
        margin=dict(t=50, b=100),
    )
    return fig


# ============================================================================
# Chart Creation - Functions & Async
# ============================================================================


def create_function_calls_chart(func_results):
    """Create function call overhead chart"""
    data = [
        r
        for r in func_results
        if r.get('category') == 'functions_calls'
        and any(
            name in r['name']
            for name in ['empty function', 'function with 5 args', 'instance method', 'lambda call (no', 'len() on']
        )
    ]

    records = []
    for r in data:
        time_str, ops_str = format_time(r['value'])
        records.append({'Operation': r['name'], 'Time': r['value'], 'Display': f'{time_str}'})

    df = pd.DataFrame(records).sort_values('Time')

    fig = px.bar(
        df,
        y='Operation',
        x='Time',
        title='Function Call Overhead Comparison',
        labels={'Time': 'Time (ms)'},
        orientation='h',
        text='Display',
    )
    fig.update_traces(textposition='outside', marker_color='#607D8B', textfont_size=14)
    fig.update_layout(height=500, margin=dict(l=200, t=50))
    return fig


def create_exception_cost_chart(func_results):
    """Create exception cost comparison"""
    no_exception = next((r for r in func_results if 'try/except (no exception raised)' in r['name']), None)
    with_exception = next((r for r in func_results if 'raise + catch ValueError' == r['name']), None)

    if not all([no_exception, with_exception]):
        return None, None

    fig = go.Figure()

    exception_types = ['No Exception', 'Exception Raised']
    exception_times = [no_exception['value'], with_exception['value']]

    fig.add_trace(
        go.Bar(
            x=exception_types,
            y=exception_times,
            text=[format_time(t)[0] for t in exception_times],
            textposition='outside',
            marker_color=['#10b981', '#ef4444'],
            textfont_size=14,
        )
    )

    exception_overhead = with_exception['value'] / no_exception['value']

    fig.update_layout(
        title=f'Exception Cost: {exception_overhead:.0f}x Overhead When Raised',
        yaxis_title='Time (ms)',
        showlegend=False,
        height=500,
        margin=dict(t=50, b=100),
    )

    return fig, exception_overhead


def create_async_overhead_chart(async_results):
    """Create async vs sync comparison"""
    sync_func = next((r for r in async_results if 'sync function call' in r['name']), None)
    async_func = next((r for r in async_results if 'async equivalent' in r['name']), None)

    if not all([sync_func, async_func]):
        return None, None

    fig = go.Figure()

    func_types = ['Sync Function', 'Async Function']
    func_times = [sync_func['value'], async_func['value']]

    fig.add_trace(
        go.Bar(
            x=func_types,
            y=func_times,
            text=[format_time(t)[0] for t in func_times],
            textposition='outside',
            marker_color=['#3b82f6', '#f59e0b'],
            textfont_size=14,
        )
    )

    async_overhead = async_func['value'] / sync_func['value']

    fig.update_layout(
        title=f'Async Overhead: {async_overhead:.0f}x Slower for Simple Operations',
        yaxis_title='Time (ms)',
        showlegend=False,
        height=500,
        yaxis_type='log',
        margin=dict(t=50, b=100),
    )

    return fig, async_overhead


# ============================================================================
# Chart Creation - Imports
# ============================================================================


def create_import_times_chart(import_results):
    """Create import times comparison (top slowest)"""
    df = pd.DataFrame(import_results).sort_values('value', ascending=False).head(12)

    fig = px.bar(
        df,
        y='name',
        x='value',
        title='Import Times (Top 12 Slowest)',
        labels={'name': 'Module', 'value': 'Time (ms)'},
        orientation='h',
        text='value',
    )
    fig.update_traces(texttemplate='%{text:.1f} ms', textposition='outside', marker_color='#E91E63', textfont_size=14)
    fig.update_layout(height=600, margin=dict(l=200, t=50))
    return fig
