# Marimo Notebook Visualization Plan

*Converting the Python Numbers Report into an Interactive Infographic*

---

## Overview

Transform `the-report.md` into an interactive marimo notebook powered by `results.json` with comprehensive visualizations, comparison charts, and insights that help developers understand Python performance characteristics.

**Goals:**
- Interactive, data-driven visualizations
- Easy to update when re-running benchmarks
- Professional infographic quality
- Educational and insightful
- Responsive and explorable

---

## Phase 1: Setup & Dependencies

### 1.1 Required Libraries

Add to `requirements.piptools`:
```
marimo          # Reactive notebook framework
plotly          # Interactive charts
pandas          # Data manipulation
altair          # Declarative visualizations (alternative to plotly)
matplotlib      # Static charts (if needed)
seaborn         # Statistical visualizations (if needed)
```

### 1.2 Notebook Structure

The notebook will be organized into cells with clear sections:
1. **Header & Metadata** - Title, system info, last updated
2. **Quick Reference Dashboard** - Top-level metrics
3. **Memory Costs** - Visualizations for all memory benchmarks
4. **Basic Operations** - Speed comparisons for fundamental operations
5. **Collections** - Access patterns, iteration, and performance
6. **Attributes** - Class attribute access comparisons
7. **JSON & Serialization** - Library comparison charts
8. **Web Frameworks** - Framework performance comparison
9. **File I/O** - Read/write performance
10. **Database** - SQLite vs diskcache vs MongoDB
11. **Functions** - Call overhead, exceptions, type checking
12. **Async** - Async overhead visualization
13. **Imports** - Import time comparison
14. **Key Takeaways** - Summary insights

---

## Phase 2: Data Loading & Preparation

### 2.1 Load Results Cell

```python
import marimo as mo
import json
import pandas as pd
from pathlib import Path

# Load benchmark results
def load_results():
    results_path = Path("results.json")
    with open(results_path) as f:
        return json.load(f)

data = load_results()
metadata = data["metadata"]
categories = data["categories"]
```

### 2.2 Data Processing Functions

Create helper functions for each category:
- Convert milliseconds to appropriate units (ns, μs, ms)
- Format memory units (bytes, KB, MB)
- Calculate ops/sec from timing data
- Create pandas DataFrames for each category
- Prepare comparison data structures

```python
def format_time(ms_value):
    """Convert milliseconds to appropriate unit"""
    if ms_value < 0.001:
        return f"{ms_value * 1_000_000:.1f} ns"
    elif ms_value < 1:
        return f"{ms_value * 1_000:.2f} μs"
    else:
        return f"{ms_value:.2f} ms"

def format_memory(bytes_value):
    """Convert bytes to appropriate unit"""
    if bytes_value < 1024:
        return f"{bytes_value} bytes"
    elif bytes_value < 1024**2:
        return f"{bytes_value/1024:.2f} KB"
    else:
        return f"{bytes_value/(1024**2):.2f} MB"

def ops_per_sec(ms_value):
    """Calculate operations per second"""
    return 1000 / ms_value if ms_value > 0 else 0
```

---

## Phase 3: Header & Metadata Section

### 3.1 Title Cell

```python
mo.md(f"""
# Python Numbers Every Programmer Should Know
## Interactive Performance Benchmark Dashboard

*Inspired by "Latency Numbers Every Programmer Should Know" -- but for Python.*

**Last Updated:** {metadata['timestamp']}
""")
```

### 3.2 System Information Card

```python
system_info = mo.md(f"""
### System Information

| Property | Value |
|----------|-------|
| Python Version | {metadata['python_version']} ({metadata['python_implementation']}) |
| Platform | {metadata['platform']} |
| Processor | {metadata['processor']} |
| CPU Cores | {metadata['cpu_cores_physical']} physical / {metadata['cpu_cores_logical']} logical |
| RAM | {metadata['ram_gb']} GB |
""")
```

---

## Phase 4: Quick Reference Dashboard

### 4.1 Top Metrics Card

Create a visual dashboard showing:
- Fastest operation (with time)
- Slowest operation (with time)
- Most memory-efficient structure
- Least memory-efficient structure
- Best JSON library
- Fastest web framework

### 4.2 Interactive Filter

```python
category_selector = mo.ui.dropdown(
    options=list(categories.keys()),
    label="Select Category",
    value="basic_ops"
)
```

---

## Phase 5: Memory Costs Visualizations

### 5.1 Empty Python Process

Large callout card showing the baseline memory cost.

### 5.2 String Memory Chart

- Bar chart showing memory growth for strings (empty, 1-char, 10-char, 100-char, 1000-char)
- Trend line visualization

### 5.3 Number Memory Comparison

- Bar chart comparing int vs float
- Show small int, large int, very large int progression

### 5.4 Collection Memory Comparison

**Chart 1: Empty Collections**
- Horizontal bar chart: empty list, dict, set

**Chart 2: Growth by Size**
- Line chart showing memory growth (10, 100, 1000 items)
- Separate lines for list, dict, set

### 5.5 Class Instance Memory

**Chart 1: Single Instance Comparison**
- Bar chart: regular class, slots class, dataclass, namedtuple

**Chart 2: Aggregate Memory (1000 instances)**
- Bar chart comparing total memory for 1000 instances
- Show the slots advantage

### 5.6 Interactive Memory Explorer

Allow users to:
- Select collection type
- Input number of items
- See estimated memory usage

```python
collection_type = mo.ui.dropdown(["list", "dict", "set"])
item_count = mo.ui.slider(0, 10000, value=1000, label="Item count")
# Calculate and display estimated memory
```

---

## Phase 6: Basic Operations Visualizations

### 6.1 Arithmetic Operations

- Bar chart comparing int add, float add, multiply
- Show ops/sec for context

### 6.2 String Operations Comparison

- Horizontal bar chart: concat, f-string, .format(), % formatting
- Color-code by speed (green = fast, yellow = medium, red = slow)
- Show relative performance (1x, 2x, 3x slower)

### 6.3 List Operations

**Chart 1: Single Operation Speed**
- Bar chart: list.append() performance

**Chart 2: List Comprehension vs For Loop**
- Grouped bar chart showing different sizes (10, 100, 1000)
- Clear winner visualization

---

## Phase 7: Collections Visualizations

### 7.1 Access Speed Comparison

- Bar chart: dict lookup, set membership, list index, list membership
- Log scale if needed due to O(n) operations
- Annotate with Big-O complexity

### 7.2 len() Performance

- Show that len() is O(1) across all collection types
- Near-identical performance regardless of size

### 7.3 Iteration Speed

- Bar chart comparing iteration over different collection types (1000 items)
- Include list, dict, set, tuple, range()

### 7.4 Interactive Collection Performance Explorer

```python
operation = mo.ui.dropdown(["lookup", "membership", "iteration"])
collection = mo.ui.dropdown(["list", "dict", "set"])
# Show performance for selected combination
```

---

## Phase 8: Attribute Access Visualizations

### 8.1 Regular vs Slots Comparison

- Side-by-side bar chart: read and write operations
- Show the (minimal) speed difference

### 8.2 Property vs Direct Access

- Bar chart: direct attr, @property, getattr(), hasattr()
- Show overhead of each approach

---

## Phase 9: JSON & Serialization

### 9.1 Serialization Library Comparison

**Chart 1: Simple Object**
- Horizontal bar chart: json, orjson, ujson, msgspec
- Show speedup factor vs stdlib json

**Chart 2: Complex Object**
- Same comparison for complex object
- Highlight that advantage increases with complexity

### 9.2 Deserialization Comparison

- Similar charts for loads/decode operations

### 9.3 Pydantic Performance

- Separate section showing Pydantic's performance
- Compare model_dump_json() vs json.dumps()

### 9.4 Interactive JSON Library Selector

```python
json_lib = mo.ui.dropdown(["json", "orjson", "ujson", "msgspec"])
object_size = mo.ui.radio(["simple", "complex"])
# Show performance for selected library + object
```

---

## Phase 10: Web Frameworks

### 10.1 Requests/Sec Comparison

- Horizontal bar chart showing req/sec for each framework
- Sort by performance (fastest at top)
- Add color gradient

### 10.2 Latency Comparison

- P50 and P99 latency side-by-side grouped bars
- Lower is better visualization

### 10.3 Framework Trade-offs Chart

- Scatter plot: Performance vs Features
- X-axis: requests/sec
- Y-axis: "Feature richness" score (manual/subjective)
- Size of bubble: Import time overhead

---

## Phase 11: File I/O

### 11.1 Basic Operations

- Bar chart: open/close, read 1KB, read 1MB, write 1KB, write 1MB
- Show relationship between size and time

### 11.2 Pickle vs JSON

- Grouped bar chart comparing serialization methods
- Highlight pickle's speed advantage

---

## Phase 12: Database Comparison

### 12.1 Write Performance

- Grouped bar chart: SQLite, diskcache, MongoDB
- Operation: write one object

### 12.2 Read Performance

- Similar chart for read operations
- Show SQLite's speed advantage

### 12.3 Operation Matrix Heatmap

- Rows: Operation type (insert, select, update, delete)
- Columns: Database (SQLite, diskcache, MongoDB)
- Color: Performance (darker = faster)

---

## Phase 13: Functions & Call Overhead

### 13.1 Function Call Types

- Bar chart: empty function, 5 args, method, lambda, builtin
- Show minimal overhead differences

### 13.2 Exception Cost

- Dramatic comparison: try/except (no exception) vs (exception raised)
- Show the 6x+ cost of raising exceptions

### 13.3 Type Checking Speed

- Bar chart: isinstance(), type() ==, type() is
- Show they're all very fast

---

## Phase 14: Async Overhead

### 14.1 Async vs Sync Cost

- Side-by-side comparison showing ~2000x overhead
- Clear visualization of when async is worth it

### 14.2 Async Operations Breakdown

- Bar chart: create coroutine, await, sleep(0), gather()
- Show relative costs

---

## Phase 15: Import Times

### 15.1 Standard Library Imports

- Horizontal bar chart showing import times
- Group by: builtin, stdlib-small, stdlib-large

### 15.2 Third-Party Package Imports

- Separate chart for external packages
- Highlight expensive imports (fastapi, litestar)

### 15.3 Import Time Impact Visualization

- Show cumulative effect: "Your app startup time"
- Let users select packages they use, show total import overhead

---

## Phase 16: Key Takeaways Section

### 16.1 Top Insights

Create visual callout boxes for each key takeaway:

```python
mo.callout(
    "Dict/Set Lookups vs List Membership",
    kind="info"
)
# Add comparison showing O(1) vs O(n)
```

### 16.2 Performance Rules of Thumb

Visual guide with icons:
- 🏃 Dict/set for membership checks
- 🐌 Avoid exceptions in hot loops
- 📦 Use __slots__ for many instances
- ⚡ Consider orjson/msgspec for JSON
- 🔄 Async only for I/O-bound work

### 16.3 Interactive "What If" Calculator

```python
operation = mo.ui.dropdown(["dict lookup", "list membership", ...])
count = mo.ui.slider(1, 1_000_000, value=10000)
# Show: "This operation will take approximately X ms"
```

---

## Phase 17: Update & Maintenance Strategy

### 17.1 Auto-reload Results

The notebook should:
1. Check if `results.json` exists
2. Load data on notebook startup
3. Optionally: watch for file changes and auto-reload

### 17.2 Version Comparison Feature

Future enhancement: allow loading multiple `results.json` files to compare:
- Different Python versions
- Different hardware
- Different OS platforms

### 17.3 Export Functionality

Add cells that can:
- Export specific charts as PNG/SVG
- Generate shareable HTML snippets
- Create social media preview cards

---

## Phase 18: Styling & Polish

### 18.1 Color Scheme

Define consistent color palette:
- Primary: Blues for neutral data
- Performance grades: Green (fast) → Yellow (medium) → Red (slow)
- Categories: Distinct color per benchmark category

### 18.2 Typography

- Clear headers with marimo's markdown
- Monospace for code/numbers
- Consistent sizing hierarchy

### 18.3 Layout

- Use marimo's layout features for side-by-side comparisons
- Card-based design for metrics
- Proper spacing and white space

---

## Implementation Order

1. **Phase 1-2:** Setup and data loading (foundation)
2. **Phase 3:** Header and metadata (quick win)
3. **Phase 4:** Dashboard (high-level overview)
4. **Phase 5:** Memory visualizations (good starting point)
5. **Phase 6-7:** Basic ops and collections (most interesting)
6. **Phase 9:** JSON comparison (clear winner visualization)
7. **Phase 10:** Web frameworks (another highlight)
8. **Phase 8, 11-15:** Remaining categories
9. **Phase 16:** Key takeaways (synthesis)
10. **Phase 17-18:** Polish and maintenance features

---

## Technical Notes

### Chart Library Choice

**Recommendation: Plotly**
- ✅ Interactive (zoom, pan, hover tooltips)
- ✅ Professional appearance
- ✅ Works well in marimo
- ✅ Responsive
- ✅ Export capabilities

**Alternative: Altair**
- ✅ Declarative syntax
- ✅ Great for exploratory visualization
- ✅ Vega-Lite based
- ❌ Less interactive than Plotly

### Data Processing

Use pandas DataFrames throughout:
```python
def create_memory_df(memory_results):
    """Convert memory results to DataFrame"""
    records = []
    for result in memory_results:
        records.append({
            'name': result['name'],
            'value': result['value'],
            'unit': result['unit'],
            'category': result.get('category', 'memory')
        })
    return pd.DataFrame(records)
```

### Marimo Best Practices

- Keep cells focused (one visualization per cell)
- Use reactive variables for interactivity
- Cache expensive computations with `@mo.cache`
- Use `mo.ui` components for user interaction
- Organize with `mo.md()` section headers

---

## File Structure

```
marimo-notebook.py          # Main notebook
plans/
  ├── 001-coding-plan.md
  └── 002-marimo-visualization-plan.md  # This file
results.json                 # Data source
code/
  └── generate_report.py     # May need to extract helper functions
```

---

## Success Criteria

The completed notebook should:
1. ✅ Load data from `results.json` automatically
2. ✅ Display all benchmark categories with appropriate visualizations
3. ✅ Include interactive elements for exploration
4. ✅ Be visually appealing and professional
5. ✅ Provide educational insights
6. ✅ Be easily updatable (just re-run benchmarks)
7. ✅ Export-ready for sharing
8. ✅ Fast to load and render

---

## Future Enhancements

- **Comparison Mode:** Load multiple result files to compare
- **Filtering:** Filter by time ranges, operation types, etc.
- **Search:** Search for specific operations
- **Annotations:** Add contextual notes to specific benchmarks
- **Sharing:** Generate shareable links or embedded views
- **Real-time:** Live benchmarking mode (run benchmarks from notebook)

---

*Let's build an interactive, beautiful, and educational performance reference!*

