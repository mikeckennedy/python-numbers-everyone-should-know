# Python Numbers Everyone Should Know - Coding Plan

*Benchmark suite to measure common Python operation costs*

---

## Overview

- **Python Version:** 3.14.2
- **Platform:** macOS
- **Time Units:** All measurements in milliseconds (ms)
- **Output:** Colored terminal output (colorama) + JSON results

---

## Phase 1: Setup & Infrastructure

### 1.1 Dependencies (`requirements.piptools`)

```
# JSON libraries
orjson
ujson
msgspec

# Data validation
pydantic

# Database/persistence
diskcache
pymongo

# Web frameworks
flask
django
fastapi
starlette
litestar
uvicorn
gunicorn

# Utilities
colorama

# Benchmarking tools (external)
# wrk or hey - install via homebrew
```

### 1.2 Shared Utilities (`code/utils/benchmark.py`)

- Timing functions using `timeit` and `perf_counter_ns`
- Memory measurement with `sys.getsizeof()` and `tracemalloc`
- Colored output helpers (colorama)
- JSON result output formatting
- Graceful library import with skip functionality
- Standard test objects (simple_obj, complex_obj, user_data)

### 1.3 Folder Structure

```
code/
├── utils/
│   ├── __init__.py
│   └── benchmark.py
├── memory/
│   ├── __init__.py
│   ├── empty_process.py
│   ├── strings.py
│   ├── numbers.py
│   ├── collections.py
│   └── classes.py
├── basic_ops/
│   ├── __init__.py
│   ├── arithmetic.py
│   ├── string_ops.py
│   └── list_ops.py
├── collections_bench/
│   ├── __init__.py
│   ├── access.py
│   ├── length.py
│   └── iteration.py
├── attributes/
│   ├── __init__.py
│   ├── attribute_access.py
│   └── other_ops.py
├── json_bench/
│   ├── __init__.py
│   ├── serialization.py
│   ├── deserialization.py
│   └── pydantic_bench.py
├── web_frameworks/
│   ├── __init__.py
│   ├── flask_app.py
│   ├── django_app.py
│   ├── fastapi_app.py
│   ├── starlette_app.py
│   ├── litestar_app.py
│   ├── run_server.py
│   └── benchmark_servers.sh
├── file_io/
│   ├── __init__.py
│   ├── basic_ops.py
│   └── pickle_vs_json.py
├── database/
│   ├── __init__.py
│   ├── sqlite_bench.py
│   ├── diskcache_bench.py
│   └── mongodb_bench.py
├── functions/
│   ├── __init__.py
│   ├── function_calls.py
│   ├── exceptions.py
│   └── type_checking.py
├── async_bench/
│   ├── __init__.py
│   └── async_overhead.py
└── run_all.py
```

---

## Phase 2: Memory Benchmarks (`code/memory/`)

### 2.1 `empty_process.py`
- Measure memory of empty Python process
- Use `tracemalloc` and/or `resource` module

### 2.2 `strings.py`
- Empty string `""`
- 1-char string `"a"`
- 100-char string

### 2.3 `numbers.py`
- Small int (0-256, cached)
- Large int (1000)
- Very large int (10**100)
- Float

### 2.4 `collections.py`
- List: empty and 1000 items
- Dict: empty and 1000 items
- Set: empty and 1000 items

### 2.5 `classes.py`
- Regular class: empty and 5 attributes
- `__slots__` class: empty and 5 attributes
- dataclass: 5 attributes
- `@dataclass(slots=True)`: 5 attributes
- namedtuple: 5 attributes

---

## Phase 3: Basic Operations (`code/basic_ops/`)

### 3.1 `arithmetic.py`
- Add two integers
- Add two floats
- Multiply two integers

### 3.2 `string_ops.py`
- Concatenation (`+`)
- f-string formatting
- `.format()` method
- `%` formatting

### 3.3 `list_ops.py`
- `list.append()`
- List comprehension (1000 items)
- Equivalent for-loop (1000 items)

---

## Phase 4: Collection Access (`code/collections_bench/`)

### 4.1 `access.py`
- Dict lookup by key
- Set membership (`in`)
- List index access
- List membership (`in`, 1000 items)

### 4.2 `length.py`
- `len()` on list (1000 items)
- `len()` on dict (1000 items)
- `len()` on set (1000 items)

### 4.3 `iteration.py`
- Iterate 1000-item list
- Iterate 1000-item dict (keys)
- Iterate `range(1000)`
- `sum()` of 1000 integers

---

## Phase 5: Attributes (`code/attributes/`)

### 5.1 `attribute_access.py`
- Read from regular class
- Write to regular class
- Read from `__slots__` class
- Write to `__slots__` class

### 5.2 `other_ops.py`
- Read `@property`
- `getattr(obj, 'attr')`
- `hasattr(obj, 'attr')`

---

## Phase 6: JSON & Serialization (`code/json_bench/`)

### Test Objects

```python
# Simple object
simple_obj = {"id": 123, "name": "Alice", "active": True}

# Complex object
complex_obj = {
    "id": 12345,
    "username": "alice_dev",
    "email": "alice@example.com",
    "profile": {
        "bio": "Software engineer who loves Python",
        "location": "Portland, OR",
        "website": "https://alice.dev",
        "joined": "2020-03-15T08:30:00Z"
    },
    "posts": [
        {"id": 1, "title": "First Post", "tags": ["python", "tutorial"], "views": 1520},
        {"id": 2, "title": "Second Post", "tags": ["rust", "wasm"], "views": 843},
        {"id": 3, "title": "Third Post", "tags": ["python", "async"], "views": 2341},
    ],
    "settings": {
        "theme": "dark",
        "notifications": True,
        "email_frequency": "weekly"
    }
}
```

### 6.1 `serialization.py`
- `json.dumps()` - simple and complex
- `orjson.dumps()` - simple and complex
- `ujson.dumps()` - simple and complex
- `msgspec.json.encode()` - simple and complex

### 6.2 `deserialization.py`
- `json.loads()` - simple and complex
- `orjson.loads()` - simple and complex
- `ujson.loads()` - simple and complex
- `msgspec.json.decode()` - simple and complex

### 6.3 `pydantic_bench.py`
- `model_dump_json()`
- `model_validate_json()`
- `model_dump()` (to dict)
- `model_validate()` (from dict)

---

## Phase 7: Web Frameworks (`code/web_frameworks/`)

### 7.1 Framework Apps
Each returns the same JSON payload from a minimal endpoint:

- `flask_app.py` - Flask with gunicorn
- `django_app.py` - Django with gunicorn
- `fastapi_app.py` - FastAPI async + sync endpoints with uvicorn
- `starlette_app.py` - Starlette with uvicorn
- `litestar_app.py` - Falcon with gunicorn

### 7.2 `run_server.py`
Helper script to start each server on configurable port.

### 7.3 `benchmark_servers.sh`
Shell script that:
1. Starts each server
2. Runs `wrk` or `hey` benchmark
3. Collects results
4. Stops server
5. Outputs JSON results

---

## Phase 8: File I/O (`code/file_io/`)

### 8.1 `basic_ops.py`
- Open and close (no read)
- Read 1KB file
- Read 1MB file
- Write 1KB file
- Write 1MB file

### 8.2 `pickle_vs_json.py`
- `pickle.dumps()` (complex obj)
- `pickle.loads()` (complex obj)
- `json.dumps()` (complex obj)
- `json.loads()` (complex obj)

---

## Phase 9: Database (`code/database/`)

### Test Object

```python
user_data = {
    "id": 12345,
    "username": "alice_dev",
    "email": "alice@example.com",
    "profile": {
        "bio": "Software engineer who loves Python",
        "location": "Portland, OR",
        "website": "https://alice.dev",
        "joined": "2020-03-15T08:30:00Z"
    },
    "posts": [
        {"id": 1, "title": "First Post", "tags": ["python", "tutorial"], "views": 1520},
        {"id": 2, "title": "Second Post", "tags": ["rust", "wasm"], "views": 843},
        {"id": 3, "title": "Third Post", "tags": ["python", "async"], "views": 2341},
    ],
    "settings": {
        "theme": "dark",
        "notifications": True,
        "email_frequency": "weekly"
    }
}
```

### 9.1 `sqlite_bench.py`
- Insert one object (JSON blob)
- Select by primary key
- Update one field
- Delete
- Select with `json_extract()`

### 9.2 `diskcache_bench.py`
- `cache.set(key, obj)`
- `cache.get(key)`
- `cache.delete(key)`
- Check key exists

### 9.3 `mongodb_bench.py`
- `insert_one()`
- `find_one()` by `_id`
- `find_one()` by nested field
- `update_one()`
- `delete_one()`
- **Graceful skip** if MongoDB not running

---

## Phase 10: Functions (`code/functions/`)

### 10.1 `function_calls.py`
- Empty function call
- Function with 5 arguments
- Method call on object
- Lambda call
- Built-in function (`len()`)

### 10.2 `exceptions.py`
- `try/except` (no exception raised)
- `try/except` (exception raised)

### 10.3 `type_checking.py`
- `isinstance()`
- `type() == type`

---

## Phase 11: Async (`code/async_bench/`)

### 11.1 `async_overhead.py`
- `await` already-completed coroutine
- Create coroutine object (no await)
- `asyncio.sleep(0)`
- `asyncio.gather()` on 10 completed coroutines

---

## Phase 12: Runner (`code/run_all.py`)

Main script that:
1. Discovers and imports all benchmark modules
2. Runs each benchmark category
3. Collects results into unified JSON structure
4. Displays colored summary table to terminal
5. Saves results to `results.json`
6. Optionally generates markdown for report update

### Output Format

```json
{
  "metadata": {
    "python_version": "3.14.2",
    "platform": "macOS ...",
    "timestamp": "2024-..."
  },
  "results": {
    "memory": {
      "empty_process": {"value": 0.0, "unit": "MB"},
      "strings": {...}
    },
    "basic_ops": {...},
    ...
  }
}
```

---

## Execution Order

1. **Phase 1:** Setup infrastructure (dependencies, utils, folders)
2. **Phases 2-11:** Create benchmark files in order
3. **Phase 12:** Create runner and test full suite

---

## File Count Summary

| Category | Files |
|----------|-------|
| Utils | 2 |
| Memory | 5 |
| Basic Ops | 3 |
| Collections | 3 |
| Attributes | 2 |
| JSON | 3 |
| Web Frameworks | 7 |
| File I/O | 2 |
| Database | 3 |
| Functions | 3 |
| Async | 1 |
| Runner | 1 |
| **Total** | **~35 files** |

---

## Notes

- Each benchmark file is self-contained and can run independently
- All files output colored results using colorama
- All files return structured data for JSON aggregation
- Graceful handling when optional dependencies unavailable
- Warmup iterations before timing for accurate results

