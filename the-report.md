# Python Numbers Programmer Should Know

*Inspired by "Latency Numbers Every Programmer Should Know" — but for Python.*

A practical reference for understanding the cost of common Python operations. All benchmarks run on macOS-26.2-arm64-arm-64bit-Mach-O with Python 3.14.2.

---

## Quick Reference Table

| Category | Operation | Time | Memory |
|----------|-----------|------|--------|
| **Memory** | Empty Python process | — | 25.77 MB |
| | Empty string | — | 41 bytes |
| | 100-char string | — | 141 bytes |
| | Small int (0-256) | — | 28 bytes |
| | Large int | — | 28 bytes |
| | Float | — | 24 bytes |
| | Empty list | — | 56 bytes |
| | List with 1000 ints | — | 7.87 KB |
| | Empty dict | — | 64 bytes |
| | Dict with 1000 items | — | 36.1 KB |
| | Empty set | — | 216 bytes |
| | Regular class instance (5 attrs) | — | 48 bytes |
| | `__slots__` class instance (5 attrs) | — | 72 bytes |
| | dataclass instance | — | 48 bytes |
| | namedtuple instance | — | 88 bytes |
| **Basic Ops** | Add two integers | 20.6 ns | — |
| | Add two floats | 19.1 ns | — |
| | String concatenation (small) | 40.0 ns | — |
| | f-string formatting | 70.8 ns | — |
| | `.format()` | 106 ns | — |
| | `%` formatting | 87.1 ns | — |
| | List append | 28.1 ns | — |
| | List comprehension (1000 items) | 9.55 μs | — |
| | Equivalent for-loop | 12.0 μs | — |
| **Collections** | Dict lookup by key | 20.5 ns | — |
| | Set membership check | 19.1 ns | — |
| | List index access | 18.7 ns | — |
| | List membership check (1000 items) | 4.19 μs | — |
| | `len()` on list | 18.5 ns | — |
| | Iterate 1000-item list | 8.03 μs | — |
| | Iterate 1000-item dict | 9.03 μs | — |
| | `range(1000)` iteration | 9.69 μs | — |
| | `sum()` of 1000 ints | 1.85 μs | — |
| **Attributes** | Read from regular class | 14.3 ns | — |
| | Write to regular class | 16.5 ns | — |
| | Read from `__slots__` class | 15.2 ns | — |
| | Write to `__slots__` class | 15.5 ns | — |
| | Read from `@property` | 21.5 ns | — |
| | `getattr()` | 23.7 ns | — |
| | `hasattr()` | 22.9 ns | — |
| **JSON** | `json.dumps()` (simple) | 692 ns | — |
| | `json.loads()` (simple) | 568 ns | — |
| | `json.dumps()` (complex) | 2.62 μs | — |
| | `json.loads()` (complex) | 2.19 μs | — |
| | `orjson.dumps()` (complex) | 325 ns | — |
| | `orjson.loads()` (complex) | 868 ns | — |
| | `ujson.dumps()` (complex) | 1.61 μs | — |
| | `msgspec` encode (complex) | 442 ns | — |
| | Pydantic `model_dump_json()` | 1.57 μs | — |
| | Pydantic `model_validate_json()` | 2.70 μs | — |
| **Web Frameworks** | Flask (return JSON) | {{WEB.FLASK_RETURN_JSON}} | — |
| | Django (return JSON) | {{WEB.DJANGO_RETURN_JSON}} | — |
| | FastAPI async (return JSON) | {{WEB.FASTAPI_ASYNC_RETURN_JSON}} | — |
| | FastAPI sync (return JSON) | {{WEB.FASTAPI_SYNC_RETURN_JSON}} | — |
| | Starlette (return JSON) | {{WEB.STARLETTE_RETURN_JSON}} | — |
| **File I/O** | Open and close file | 8.99 μs | — |
| | Read 1KB file | 9.83 μs | — |
| | Write 1KB file | 29.9 μs | — |
| | Write 1MB file | 264 μs | — |
| | `pickle.dumps()` | 1.11 μs | — |
| | `pickle.loads()` | 1.39 μs | — |
| **Database** | SQLite insert (JSON blob) | 153 μs | — |
| | SQLite select by PK | 3.60 μs | — |
| | SQLite update one field | 5.09 μs | — |
| | diskcache set | 24.0 μs | — |
| | diskcache get | 4.36 μs | — |
| | MongoDB insert_one | 110 μs | — |
| | MongoDB find_one by _id | 118 μs | — |
| | MongoDB find_one by nested field | 123 μs | — |
| **Functions** | Empty function call | 20.7 ns | — |
| | Function with 5 args | 26.0 ns | — |
| | Method call | 23.1 ns | — |
| | Lambda call | 20.9 ns | — |
| | try/except (no exception) | 23.0 ns | — |
| | try/except (exception raised) | 154 ns | — |
| | `isinstance()` check | 18.3 ns | — |
| **Async** | `await` completed coroutine | 27.3 μs | — |
| | Create coroutine object | 44.5 ns | — |
| | `asyncio.sleep(0)` | 40.8 μs | — |

---

## Memory Costs

Understanding how much memory different Python objects consume.

### Empty Python Process

**Result:** 25.77 MB

---

### Strings

| String | Size |
|--------|------|
| Empty string `""` | 41 bytes |
| 1-char string `"a"` | 42 bytes |
| 100-char string | 141 bytes |

---

### Numbers

| Type | Size |
|------|------|
| Small int (0-256, cached) | 28 bytes |
| Large int (1000) | 28 bytes |
| Very large int (10**100) | 72 bytes |
| Float | 24 bytes |

---

### Collections

| Collection | Empty | 1000 items |
|------------|-------|------------|
| List | 56 bytes | 7.87 KB |
| Dict | 64 bytes | 36.1 KB |
| Set | 216 bytes | 32.2 KB |

---

### Classes and Instances

| Type | Empty | 5 attributes |
|------|-------|--------------|
| Regular class | 48 bytes | 48 bytes |
| `__slots__` class | 32 bytes | 72 bytes |
| dataclass | — | 48 bytes |
| `@dataclass(slots=True)` | — | 72 bytes |
| namedtuple | — | 88 bytes |

---

## Basic Operations

The cost of fundamental Python operations.

### Arithmetic

| Operation | Time |
|-----------|------|
| Add two integers | 20.6 ns |
| Add two floats | 19.1 ns |
| Multiply two integers | 20.3 ns |

---

### String Operations

| Operation | Time |
|-----------|------|
| Concatenation (`+`) | 40.0 ns |
| f-string | 70.8 ns |
| `.format()` | 106 ns |
| `%` formatting | 87.1 ns |

---

### List Operations

| Operation | Time |
|-----------|------|
| `list.append()` | 28.1 ns |
| List comprehension (1000 items) | 9.55 μs |
| Equivalent for-loop (1000 items) | 12.0 μs |

---

## Collection Access and Iteration

How fast can you get data out of Python's built-in collections?

### Access by Key/Index

| Operation | Time |
|-----------|------|
| Dict lookup by key | 20.5 ns |
| Set membership (`in`) | 19.1 ns |
| List index access | 18.7 ns |
| List membership (`in`, 1000 items) | 4.19 μs |

---

### Length

| Collection | `len()` time |
|------------|--------------|
| List (1000 items) | 18.5 ns |
| Dict (1000 items) | 18.9 ns |
| Set (1000 items) | 18.6 ns |

---

### Iteration

| Operation | Time |
|-----------|------|
| Iterate 1000-item list | 8.03 μs |
| Iterate 1000-item dict (keys) | 9.03 μs |
| Iterate `range(1000)` | 9.69 μs |
| `sum()` of 1000 integers | 1.85 μs |

---

## Class and Object Attributes

The cost of reading and writing attributes, and how `__slots__` changes things.

### Attribute Access

| Operation | Regular Class | `__slots__` Class |
|-----------|---------------|-------------------|
| Read attribute | 14.3 ns | 15.2 ns |
| Write attribute | 16.5 ns | 15.5 ns |

---

### Other Attribute Operations

| Operation | Time |
|-----------|------|
| Read `@property` | 21.5 ns |
| `getattr(obj, 'attr')` | 23.7 ns |
| `hasattr(obj, 'attr')` | 22.9 ns |

---

## JSON and Serialization

Comparing standard library JSON with optimized alternatives.

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

### Serialization (dumps)

| Library | Simple Object | Complex Object |
|---------|---------------|----------------|
| `json` (stdlib) | 692 ns | 2.62 μs |
| `orjson` | 61.6 ns | 325 ns |
| `ujson` | 250 ns | 1.61 μs |
| `msgspec` | 67.6 ns | 442 ns |

---

### Deserialization (loads)

| Library | Simple Object | Complex Object |
|---------|---------------|----------------|
| `json` (stdlib) | 568 ns | 2.19 μs |
| `orjson` | 126 ns | 868 ns |
| `ujson` | 261 ns | 1.46 μs |
| `msgspec` | 100 ns | 845 ns |

---

### Pydantic

| Operation | Time |
|-----------|------|
| `model_dump_json()` | 1.57 μs |
| `model_validate_json()` | 2.70 μs |
| `model_dump()` (to dict) | 1.80 μs |
| `model_validate()` (from dict) | 2.13 μs |

---

## Web Frameworks

Returning a simple JSON response. Benchmarked with `wrk` or `hey` against localhost.

### Test Setup

Each framework returns the same JSON payload from a minimal endpoint.

### Results

| Framework | Requests/sec | Latency (p50) | Latency (p99) |
|-----------|--------------|---------------|---------------|
| Flask | {{WEB.FLASK_REQUESTS_PER_SEC}} | {{WEB.FLASK_LATENCY_P50}} | {{WEB.FLASK_LATENCY_P99}} |
| Django | {{WEB.DJANGO_REQUESTS_PER_SEC}} | {{WEB.DJANGO_LATENCY_P50}} | {{WEB.DJANGO_LATENCY_P99}} |
| FastAPI (async) | {{WEB.FASTAPI_ASYNC_REQUESTS_PER_SEC}} | {{WEB.FASTAPI_ASYNC_LATENCY_P50}} | {{WEB.FASTAPI_ASYNC_LATENCY_P99}} |
| FastAPI (sync) | {{WEB.FASTAPI_SYNC_REQUESTS_PER_SEC}} | {{WEB.FASTAPI_SYNC_LATENCY_P50}} | {{WEB.FASTAPI_SYNC_LATENCY_P99}} |
| Starlette | {{WEB.STARLETTE_REQUESTS_PER_SEC}} | {{WEB.STARLETTE_LATENCY_P50}} | {{WEB.STARLETTE_LATENCY_P99}} |
| Falcon | {{WEB.FALCON_REQUESTS_PER_SEC}} | {{WEB.FALCON_LATENCY_P50}} | {{WEB.FALCON_LATENCY_P99}} |

---

## File I/O

Reading and writing files of various sizes.

### Basic Operations

| Operation | Time |
|-----------|------|
| Open and close (no read) | 8.99 μs |
| Read 1KB file | 9.83 μs |
| Read 1MB file | 31.7 μs |
| Write 1KB file | 29.9 μs |
| Write 1MB file | 264 μs |

---

### Pickle vs JSON to Disk

| Operation | Time |
|-----------|------|
| `pickle.dumps()` (complex obj) | 1.11 μs |
| `pickle.loads()` (complex obj) | 1.39 μs |
| `json.dumps()` (complex obj) | 2.59 μs |
| `json.loads()` (complex obj) | 2.30 μs |

---

## Database and Persistence

Comparing SQLite, diskcache, and MongoDB using the same complex object.

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

### SQLite (JSON blob approach)

| Operation | Time |
|-----------|------|
| Insert one object | 153 μs |
| Select by primary key | 3.60 μs |
| Update one field | 5.09 μs |
| Delete | 158 μs |
| Select with `json_extract()` | 4.36 μs |

---

### diskcache

| Operation | Time |
|-----------|------|
| `cache.set(key, obj)` | 24.0 μs |
| `cache.get(key)` | 4.36 μs |
| `cache.delete(key)` | 52.2 μs |
| Check key exists | 1.92 μs |

---

### MongoDB

| Operation | Time |
|-----------|------|
| `insert_one()` | 110 μs |
| `find_one()` by `_id` | 118 μs |
| `find_one()` by nested field | 123 μs |
| `update_one()` | 109 μs |
| `delete_one()` | 26.2 ns |

---

### Comparison Table

| Operation | SQLite | diskcache | MongoDB |
|-----------|--------|-----------|---------|
| Write one object | 153 μs | 24.0 μs | 110 μs |
| Read by key/id | 3.60 μs | 4.36 μs | 118 μs |
| Read by nested field | 4.36 μs | N/A | 123 μs |
| Update one field | 5.09 μs | 24.0 μs | 109 μs |
| Delete | 158 μs | 52.2 μs | 26.2 ns |

---

## Function and Call Overhead

The hidden cost of function calls, exceptions, and async.

### Function Calls

| Operation | Time |
|-----------|------|
| Empty function call | 20.7 ns |
| Function with 5 arguments | 26.0 ns |
| Method call on object | 23.1 ns |
| Lambda call | 20.9 ns |
| Built-in function (`len()`) | 17.5 ns |

---

### Exceptions

| Operation | Time |
|-----------|------|
| `try/except` (no exception raised) | 23.0 ns |
| `try/except` (exception raised) | 154 ns |

---

### Type Checking

| Operation | Time |
|-----------|------|
| `isinstance()` | 18.3 ns |
| `type() == type` | 21.2 ns |

---

## Async Overhead

The cost of async machinery.

| Operation | Time |
|-----------|------|
| `await` already-completed coroutine | 27.3 μs |
| Create coroutine object (no await) | 44.5 ns |
| `asyncio.sleep(0)` | 40.8 μs |
| `asyncio.gather()` on 10 completed | 51.1 μs |

---

## Methodology

### Benchmarking Approach

- All benchmarks run multiple times with warmup
- Timing uses `timeit` or `perf_counter_ns` as appropriate
- Memory measured with `sys.getsizeof()` and `tracemalloc`
- Results are median of N runs

### Environment

- **OS:** macOS-26.2-arm64-arm-64bit-Mach-O
- **Python:** 3.14.2 (CPython)
- **CPU:** arm
- **RAM:** {{SYSTEM.RAM}}

### Code Repository

All benchmark code available at: https://github.com/mkennedy/python-numbers-everyone-should-know

---

## Key Takeaways

1. **Memory overhead**: Python objects have significant memory overhead - even an empty list is 56 bytes
2. **Dict/set speed**: Dictionary and set lookups are extremely fast (O(1) average case) compared to list membership checks (O(n))
3. **JSON performance**: Alternative JSON libraries like `orjson` and `msgspec` are 3-8x faster than stdlib `json`
4. **Async overhead**: Creating and awaiting coroutines has measurable overhead - only use async when you need concurrency
5. **`__slots__` tradeoff**: While `__slots__` saves memory, the difference for attribute access speed is minimal

---

## Acknowledgments

Inspired by [Latency Numbers Every Programmer Should Know](https://gist.github.com/jboner/2841832) and similar resources.

---

*Last updated: 2025-12-27*
