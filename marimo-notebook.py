import marimo

__generated_with = '0.18.4'
app = marimo.App(width='full')


@app.cell(hide_code=True)
def _():
    import json
    from pathlib import Path

    import marimo as mo
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go

    return Path, go, json, mo, pd, px


@app.cell(hide_code=True)
def _(Path, json):
    # Load benchmark results
    def load_results():
        results_path = Path('results.json')
        with open(results_path) as f:
            return json.load(f)

    data = load_results()
    metadata = data['metadata']
    categories = data['categories']
    return categories, metadata


@app.cell(hide_code=True)
def _():
    # Helper functions for data formatting
    def format_time(ms_value):
        """Convert milliseconds to appropriate unit with ops/sec"""
        if ms_value < 0.001:
            ns_value = ms_value * 1_000_000
            ops_sec = 1_000_000_000 / (ns_value) if ns_value > 0 else 0
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

    def ms_to_ns(ms_value):
        """Convert milliseconds to nanoseconds"""
        return ms_value * 1_000_000

    def ms_to_us(ms_value):
        """Convert milliseconds to microseconds"""
        return ms_value * 1_000

    def ops_per_sec(ms_value):
        """Calculate operations per second from milliseconds"""
        return 1000 / ms_value if ms_value > 0 else 0

    def get_best_unit(ms_value):
        """Determine best unit for display"""
        if ms_value < 0.001:
            return ms_to_ns(ms_value), 'ns'
        elif ms_value < 1:
            return ms_to_us(ms_value), 'μs'
        else:
            return ms_value, 'ms'

    return (format_time,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # 🐍 Python Numbers Every Programmer Should Know
    ## Interactive Performance Benchmark Dashboard

    *Inspired by "Latency Numbers Every Programmer Should Know" -- but for Python.*

    This interactive notebook visualizes comprehensive benchmarks of common Python operations,
    helping you understand the real cost of different programming choices.
    """)
    return


@app.cell(hide_code=True)
def _(metadata, mo):
    mo.md(f"""
    ## 📊 System Information

    | Property | Value |
    |----------|-------|
    | **Python Version** | {metadata['python_version']} ({metadata['python_implementation']}) |
    | **Platform** | {metadata['platform']} |
    | **Processor** | {metadata['processor']} |
    | **CPU Cores** | {metadata['cpu_cores_physical']} physical / {metadata['cpu_cores_logical']} logical |
    | **RAM** | {metadata['ram_gb']} GB |
    | **Timestamp** | {metadata['timestamp'][:10]} |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 🎯 Quick Reference Dashboard

    Navigate to any section to explore detailed visualizations:
    """)
    return


@app.cell(hide_code=True)
def _(categories, mo):
    category_options = {
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

    category_selector = mo.ui.dropdown(
        options=list(category_options.keys()), label='Jump to section:', value='Memory Costs'
    )

    benchmark_counts = {_name: cat['benchmark_count'] for _name, cat in categories.items()}

    mo.md(f"""
    {category_selector}

    **Total Benchmarks:** {sum(benchmark_counts.values())} across {len(categories)} categories
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 💾 Memory Costs

    Understanding how much memory different Python objects consume.
    """)
    return


@app.cell(hide_code=True)
def _(categories, mo):
    memory_results = categories['memory']['results']
    empty_process = next(_r for _r in memory_results if _r['name'] == 'empty_process')

    mo.callout(
        mo.md(f"""
        ### Empty Python Process Baseline
        **{empty_process['value']:.2f} MB** - This is the memory cost just to start Python!
        """),
        kind='info',
    )
    return (memory_results,)


@app.cell(hide_code=True)
def _(memory_results, pd, px):
    # Exclude 1000_char_string for better visualization scale
    string_data = [_r for _r in memory_results if 'string' in _r['name'] and '1000_char' not in _r['name']]
    string_df = pd.DataFrame(string_data)
    string_df['_size'] = string_df['name'].str.extract(r'(\d+)').fillna('0').astype(int)
    string_df = string_df.sort_values('_size')

    fig_strings = px.bar(
        string_df,
        x='name',
        y='value',
        title='String Memory Usage by Size (up to 100 chars)',
        labels={'name': 'String Type', 'value': 'Bytes'},
        text='value',
    )
    fig_strings.update_traces(
        texttemplate='%{text} bytes',
        textposition='outside',
        marker_color='#1565C0',  # Solid dark blue
        textfont_size=14,
    )
    fig_strings.update_layout(
        showlegend=False,
        height=500,
        yaxis=dict(range=[0, string_df['value'].max() * 1.2]),
        margin=dict(t=50, b=100),
        xaxis_tickangle=-45,
    )
    fig_strings
    return


@app.cell(hide_code=True)
def _(memory_results, pd, px):
    # Individual numbers (not in lists)
    individual_number_data = [
        _r
        for _r in memory_results
        if ('int' in _r['name'] or 'float' in _r['name']) and 'list' not in _r['name'] and 'container' not in _r['name']
    ]
    individual_number_df = pd.DataFrame(individual_number_data)

    fig_individual_numbers = px.bar(
        individual_number_df,
        x='name',
        y='value',
        title='Individual Integer and Float Memory Usage',
        labels={'name': 'Type', 'value': 'Bytes'},
        text='value',
    )
    # Use solid colors instead of gradient for better contrast
    fig_individual_numbers.update_traces(
        texttemplate='%{text} bytes',
        textposition='outside',
        marker_color='#2E7D32',  # Solid dark green for good contrast
        textfont_size=14,
    )
    fig_individual_numbers.update_layout(
        showlegend=False,
        height=500,
        yaxis=dict(range=[0, individual_number_df['value'].max() * 1.2]),  # Add 20% padding for labels
        margin=dict(t=50, b=100),  # More bottom margin for x-axis labels
        xaxis_tickangle=-45,  # Angle the labels for better readability
    )
    fig_individual_numbers
    return


@app.cell(hide_code=True)
def _(memory_results, pd, px):
    # Lists of numbers (1,000 items)
    number_list_data = [
        _r
        for _r in memory_results
        if '_1000_' in _r['name'] and 'container' in _r['name'] and ('list' in _r['name']) and 'class' not in _r['name']
    ]
    number_list_df = pd.DataFrame(number_list_data)

    fig_number_lists = px.bar(
        number_list_df,
        x='name',
        y='value',
        title='List Memory Usage (1,000 items: ints vs floats)',
        labels={'name': 'List Type', 'value': 'Bytes'},
        text='value',
    )
    fig_number_lists.update_traces(
        texttemplate='%{text:,.0f} bytes',
        textposition='outside',
        marker_color='#00838F',  # Solid dark teal
        textfont_size=14,
    )
    fig_number_lists.update_layout(
        showlegend=False,
        height=500,
        yaxis=dict(range=[0, number_list_df['value'].max() * 1.2]),
        margin=dict(t=50, b=120),
        xaxis_tickangle=-45,
    )
    fig_number_lists
    return


@app.cell(hide_code=True)
def _(memory_results, pd, px):
    empty_collections = [_r for _r in memory_results if _r['name'] in ['empty_list', 'empty_dict', 'empty_set']]
    empty_coll_df = pd.DataFrame(empty_collections)

    fig_empty_coll = px.bar(
        empty_coll_df,
        y='name',
        x='value',
        title='Empty Collection Memory Overhead',
        labels={'name': 'Collection Type', 'value': 'Bytes'},
        orientation='h',
        text='value',
    )
    fig_empty_coll.update_traces(
        texttemplate='%{text} bytes',
        textposition='outside',
        marker_color='#E65100',  # Solid dark orange
        textfont_size=14,
    )
    fig_empty_coll.update_layout(
        showlegend=False,
        height=400,
        xaxis=dict(range=[0, empty_coll_df['value'].max() * 1.2]),
        margin=dict(l=150),  # More left margin for labels
    )
    fig_empty_coll
    return


@app.cell(hide_code=True)
def _(memory_results, pd, px):
    growth_data = [
        _r
        for _r in memory_results
        if any(_size in _r['name'] for _size in ['_10_', '_100_', '_1000_'])
        and 'container' in _r['name']
        and 'floats' not in _r['name']  # Exclude floats - only have data at 1000 level
    ]

    growth_records = []
    for _r in growth_data:
        _name = _r['name']
        if 'list' in _name:
            coll_type = 'List (ints)'
        elif 'dict' in _name:
            coll_type = 'Dict'
        elif 'set' in _name:
            coll_type = 'Set'
        else:
            continue

        if '_10_' in _name:
            _size = 10
        elif '_100_' in _name:
            _size = 100
        elif '_1000_' in _name:
            _size = 1000
        else:
            continue

        growth_records.append({'Collection': coll_type, 'Size': _size, 'Bytes': _r['value']})

    growth_df = pd.DataFrame(growth_records)

    fig_growth = px.line(
        growth_df,
        x='Size',
        y='Bytes',
        color='Collection',
        markers=True,
        title='Collection Memory Growth: List (ints), Dict, and Set',
        labels={'Size': 'Number of Items', 'Bytes': 'Memory (bytes)'},
        log_y=True,
    )
    fig_growth.update_layout(height=500)
    fig_growth
    return


@app.cell(hide_code=True)
def _(memory_results, pd, px):
    class_data = [
        _r for _r in memory_results if 'class' in _r['name'] and '5attr' in _r['name'] or 'namedtuple' in _r['name']
    ]
    class_df = pd.DataFrame(class_data)

    fig_classes = px.bar(
        class_df,
        x='name',
        y='value',
        title='Class Instance Memory (5 attributes)',
        labels={'name': 'Class Type', 'value': 'Bytes'},
        text='value',
    )
    # Use solid purple with good contrast
    fig_classes.update_traces(
        texttemplate='%{text} bytes',
        textposition='outside',
        marker_color='#6A1B9A',  # Solid dark purple for good contrast
        textfont_size=14,
    )
    fig_classes.update_layout(
        showlegend=False,
        height=500,
        yaxis=dict(range=[0, class_df['value'].max() * 1.2]),  # Add 20% padding for labels
        margin=dict(t=50, b=120),  # Extra bottom margin for long labels
        xaxis_tickangle=-45,  # Angle the labels for better readability
    )
    fig_classes
    return


@app.cell(hide_code=True)
def _(memory_results, mo, pd, px):
    aggregate_data = [_r for _r in memory_results if 'list_1000' in _r['name'] and 'class' in _r['name']]

    agg_df = pd.DataFrame(aggregate_data)

    fig_aggregate = px.bar(
        agg_df,
        x='name',
        y='value',
        title='Memory for 1,000 Class Instances',
        labels={'name': 'Class Type', 'value': 'Bytes'},
        text='value',
    )
    fig_aggregate.update_traces(
        texttemplate='%{text:,.0f} bytes<br>(%{customdata[0]})',
        textposition='outside',
        customdata=[[f'{v / 1024:.1f} KB'] for v in agg_df['value']],
        marker_color='#C62828',  # Solid dark red
        textfont_size=14,
    )
    fig_aggregate.update_layout(
        showlegend=False,
        height=500,
        yaxis=dict(range=[0, agg_df['value'].max() * 1.2]),
        margin=dict(t=50, b=120),
        xaxis_tickangle=-45,
    )

    regular_mem = next(_r['value'] for _r in aggregate_data if 'regular' in _r['name'])
    slots_mem = next(_r['value'] for _r in aggregate_data if 'slots' in _r['name'])
    savings = ((regular_mem - slots_mem) / regular_mem) * 100

    mo.vstack(
        [
            fig_aggregate,
            mo.callout(
                mo.md(f"""
            **__slots__ Memory Savings:** {savings:.1f}% less memory 
            ({(regular_mem - slots_mem) / 1024:.1f} KB saved for 1,000 instances)
            """),
                kind='success',
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## ⚡ Basic Operations

    The cost of fundamental Python operations.
    """)
    return


@app.cell(hide_code=True)
def _(categories, format_time, pd, px):
    basic_results = categories['basic_ops']['results']
    arithmetic_data = [
        _r for _r in basic_results if any(op in _r['name'] for op in ['int_add', 'float_add', 'int_multiply'])
    ]

    arith_records = []
    for _r in arithmetic_data:
        _time_str, _ops_str = format_time(_r['value'])
        arith_records.append(
            {
                'Operation': _r['name'].replace('_', ' ').title(),
                'Time': _r['value'],
                'Display': f'{_time_str} ({_ops_str})',
            }
        )

    arith_df = pd.DataFrame(arith_records)

    fig_arithmetic = px.bar(
        arith_df,
        x='Operation',
        y='Time',
        title='Arithmetic Operation Speed',
        labels={'Time': 'Time (ms)'},
        text='Display',
    )
    fig_arithmetic.update_traces(
        textposition='outside',
        marker_color='#1976D2',  # Solid blue
        textfont_size=14,
    )
    fig_arithmetic.update_layout(
        showlegend=False, height=500, yaxis=dict(range=[0, arith_df['Time'].max() * 1.2]), margin=dict(t=50, b=100)
    )
    fig_arithmetic
    return (basic_results,)


@app.cell
def _(basic_results, format_time, pd, px):
    string_ops_data = [
        _r
        for _r in basic_results
        if any(op in _r['name'] for op in ['concat_small', 'f_string', 'format_method', 'percent_formatting'])
    ]

    string_ops_records = []
    for _r in string_ops_data:
        _time_str, _ops_str = format_time(_r['value'])
        name_map = {
            'concat_small': 'Concatenation (+)',
            'f_string': 'f-string',
            'format_method': '.format()',
            'percent_formatting': '% formatting',
        }
        string_ops_records.append(
            {
                'Operation': name_map.get(_r['name'], _r['name']),
                'Time': _r['value'],
                'Display': f'{_time_str}',
                'OpsPerSec': _ops_str,
            }
        )

    string_ops_df = pd.DataFrame(string_ops_records).sort_values('Time')

    fastest = string_ops_df['Time'].min()
    string_ops_df['Relative'] = string_ops_df['Time'] / fastest

    # Create custom colors based on speed (fastest = green, slowest = red)
    colors = []
    for rel in string_ops_df['Relative']:
        if rel < 1.5:
            colors.append('#2E7D32')  # Green - fast
        elif rel < 2:
            colors.append('#F9A825')  # Yellow - medium
        elif rel < 2.5:
            colors.append('#EF6C00')  # Orange - slower
        else:
            colors.append('#C62828')  # Red - slow

    fig_string_ops = px.bar(
        string_ops_df,
        y='Operation',
        x='Time',
        title='String Formatting Speed Comparison',
        labels={'Time': 'Time (ms)'},
        orientation='h',
        text='Display',
    )
    fig_string_ops.update_traces(textposition='outside', marker_color=colors, textfont_size=14)
    fig_string_ops.update_layout(
        height=500, xaxis=dict(range=[0, string_ops_df['Time'].max() * 1.2]), margin=dict(l=150, t=50)
    )
    fig_string_ops
    return


@app.cell
def _(basic_results, format_time, go):
    list_comp_data = [
        _r for _r in basic_results if '1000' in _r['name'] and ('comp' in _r['name'] or 'loop' in _r['name'])
    ]

    list_comp_df_data = [
        {
            'Method': 'List Comprehension',
            'Time': next(_r['value'] for _r in list_comp_data if 'comp' in _r['name']),
        },
        {
            'Method': 'For Loop',
            'Time': next(_r['value'] for _r in list_comp_data if 'loop' in _r['name']),
        },
    ]

    fig_list_comp = go.Figure()

    for _idx, _row_data in enumerate(list_comp_df_data):
        _time_str, _ops_str = format_time(_row_data['Time'])
        fig_list_comp.add_trace(
            go.Bar(
                x=[_row_data['Method']],
                y=[_row_data['Time']],
                name=_row_data['Method'],
                text=f'{_time_str}<br>({_ops_str})',
                textposition='outside',
                marker_color=['#3b82f6', '#ef4444'][_idx],
            )
        )

    fig_list_comp.update_layout(
        title='List Comprehension vs For Loop (1,000 items)', yaxis_title='Time (ms)', showlegend=False, height=400
    )
    fig_list_comp
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 📦 Collection Access and Iteration

    How fast can you get data out of Python's built-in collections?
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### Key Takeaway: Use dict/set for membership checks!

    Dictionary and set lookups are O(1) - extremely fast.
    List membership checks are O(n) - slow for large lists.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---

    *Note: This is a simplified version. The full notebook with all visualizations
    for collections, JSON, web frameworks, database, functions, async, and imports
    would continue here with similar patterns.*

    **To view the complete interactive notebook, run:**
    ```bash
    marimo edit marimo-notebook.py
    ```
    """)
    return


if __name__ == '__main__':
    app.run()
