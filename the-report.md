# Python Numbers Programmer Should Know

*Inspired by "Latency Numbers Every Programmer Should Know" — but for Python.*

A practical reference for understanding the cost of common Python operations. All benchmarks run on macOS-26.2-arm64-arm-64bit-Mach-O with Python 3.14.2.

---

## Quick Reference Table

| Category | Operation | Time | Memory |
|----------|-----------|------|--------|
| **Memory** | Empty Python process | — | 26.02 MB |
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
| | List of 1000 regular class instances | — | 165.2 KB |
| | List of 1000 `__slots__` class instances | — | 79.1 KB |
| | dataclass instance | — | 48 bytes |
| | namedtuple instance | — | 88 bytes |
| **Basic Ops** | Add two integers | 18.7 ns | — |
| | Add two floats | 18.5 ns | — |
| | String concatenation (small) | 42.3 ns | — |
| | f-string formatting | 68.7 ns | — |
| | `.format()` | 102 ns | — |
| | `%` formatting | 81.7 ns | — |
| | List append | 29.1 ns | — |
| | List comprehension (1000 items) | 9.39 μs | — |
| | Equivalent for-loop | 11.9 μs | — |
| **Collections** | Dict lookup by key | 21.5 ns | — |
| | Set membership check | 20.8 ns | — |
| | List index access | 17.7 ns | — |
| | List membership check (1000 items) | 3.95 μs | — |
| | `len()` on list | 17.9 ns | — |
| | Iterate 1000-item list | 7.77 μs | — |
| | Iterate 1000-item dict | 8.70 μs | — |
| | `range(1000)` iteration | 9.66 μs | — |
| | `sum()` of 1000 ints | 1.83 μs | — |
| **Attributes** | Read from regular class | 15.0 ns | — |
| | Write to regular class | 15.6 ns | — |
| | Read from `__slots__` class | 14.0 ns | — |
| | Write to `__slots__` class | 15.3 ns | — |
| | Read from `@property` | 22.9 ns | — |
| | `getattr()` | 23.2 ns | — |
| | `hasattr()` | 22.1 ns | — |
| **JSON** | `json.dumps()` (simple) | 667 ns | — |
| | `json.loads()` (simple) | 561 ns | — |
| | `json.dumps()` (complex) | 2.65 μs | — |
| | `json.loads()` (complex) | 2.16 μs | — |
| | `orjson.dumps()` (complex) | 310 ns | — |
| | `orjson.loads()` (complex) | 854 ns | — |
| | `ujson.dumps()` (complex) | 1.52 μs | — |
| | `msgspec` encode (complex) | 416 ns | — |
| | Pydantic `model_dump_json()` | 1.62 μs | — |
| | Pydantic `model_validate_json()` | 2.83 μs | — |
| **Web Frameworks** | Flask (return JSON) | {{WEB.FLASK_RETURN_JSON}} | — |
| | Django (return JSON) | {{WEB.DJANGO_RETURN_JSON}} | — |
| | FastAPI async (return JSON) | {{WEB.FASTAPI_ASYNC_RETURN_JSON}} | — |
| | FastAPI sync (return JSON) | {{WEB.FASTAPI_SYNC_RETURN_JSON}} | — |
| | Starlette (return JSON) | {{WEB.STARLETTE_RETURN_JSON}} | — |
| **File I/O** | Open and close file | 9.03 μs | — |
| | Read 1KB file | 12.6 μs | — |
| | Write 1KB file | 31.8 μs | — |
| | Write 1MB file | 499 μs | — |
| | `pickle.dumps()` | 1.29 μs | — |
| | `pickle.loads()` | 1.45 μs | — |
| **Database** | SQLite insert (JSON blob) | 172 μs | — |
| | SQLite select by PK | 3.75 μs | — |
| | SQLite update one field | 5.33 μs | — |
| | diskcache set | 27.4 μs | — |
| | diskcache get | 4.68 μs | — |
| | MongoDB insert_one | 115 μs | — |
| | MongoDB find_one by _id | 121 μs | — |
| | MongoDB find_one by nested field | 124 μs | — |
| **Functions** | Empty function call | 19.6 ns | — |
| | Function with 5 args | 25.7 ns | — |
| | Method call | 23.1 ns | — |
| | Lambda call | 18.5 ns | — |
| | try/except (no exception) | 22.2 ns | — |
| | try/except (exception raised) | 154 ns | — |
| | `isinstance()` check | 18.8 ns | — |
| **Async** | `await` completed coroutine | 54.9 μs | — |
| | Create coroutine object | 45.3 ns | — |
| | `asyncio.sleep(0)` | 62.4 μs | — |

---

## Memory Costs

Understanding how much memory different Python objects consume.

### Empty Python Process

**Result:** 26.02 MB

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

**Aggregate Memory Usage (1000 instances):**

| Type | Total Memory |
|------|--------------|
| List of 1000 regular class instances | 165.2 KB |
| List of 1000 `__slots__` class instances | 79.1 KB |

---

## Basic Operations

The cost of fundamental Python operations.

### Arithmetic

| Operation | Time |
|-----------|------|
| Add two integers | 18.7 ns |
| Add two floats | 18.5 ns |
| Multiply two integers | 18.5 ns |

---

### String Operations

| Operation | Time |
|-----------|------|
| Concatenation (`+`) | 42.3 ns |
| f-string | 68.7 ns |
| `.format()` | 102 ns |
| `%` formatting | 81.7 ns |

---

### List Operations

| Operation | Time |
|-----------|------|
| `list.append()` | 29.1 ns |
| List comprehension (1000 items) | 9.39 μs |
| Equivalent for-loop (1000 items) | 11.9 μs |

---

## Collection Access and Iteration

How fast can you get data out of Python's built-in collections?

### Access by Key/Index

| Operation | Time |
|-----------|------|
| Dict lookup by key | 21.5 ns |
| Set membership (`in`) | 20.8 ns |
| List index access | 17.7 ns |
| List membership (`in`, 1000 items) | 3.95 μs |

---

### Length

| Collection | `len()` time |
|------------|--------------|
| List (1000 items) | 17.9 ns |
| Dict (1000 items) | 17.5 ns |
| Set (1000 items) | 17.3 ns |

---

### Iteration

| Operation | Time |
|-----------|------|
| Iterate 1000-item list | 7.77 μs |
| Iterate 1000-item dict (keys) | 8.70 μs |
| Iterate `range(1000)` | 9.66 μs |
| `sum()` of 1000 integers | 1.83 μs |

---

## Class and Object Attributes

The cost of reading and writing attributes, and how `__slots__` changes things.

### Attribute Access

| Operation | Regular Class | `__slots__` Class |
|-----------|---------------|-------------------|
| Read attribute | 15.0 ns | 14.0 ns |
| Write attribute | 15.6 ns | 15.3 ns |

---

### Other Attribute Operations

| Operation | Time |
|-----------|------|
| Read `@property` | 22.9 ns |
| `getattr(obj, 'attr')` | 23.2 ns |
| `hasattr(obj, 'attr')` | 22.1 ns |

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
| `json` (stdlib) | 667 ns | 2.65 μs |
| `orjson` | 60.4 ns | 310 ns |
| `ujson` | 229 ns | 1.52 μs |
| `msgspec` | 71.1 ns | 416 ns |

---

### Deserialization (loads)

| Library | Simple Object | Complex Object |
|---------|---------------|----------------|
| `json` (stdlib) | 561 ns | 2.16 μs |
| `orjson` | 107 ns | 854 ns |
| `ujson` | 277 ns | 1.46 μs |
| `msgspec` | 93.2 ns | 862 ns |

---

### Pydantic

| Operation | Time |
|-----------|------|
| `model_dump_json()` | 1.62 μs |
| `model_validate_json()` | 2.83 μs |
| `model_dump()` (to dict) | 1.77 μs |
| `model_validate()` (from dict) | 2.25 μs |

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
| Open and close (no read) | 9.03 μs |
| Read 1KB file | 12.6 μs |
| Read 1MB file | 38.3 μs |
| Write 1KB file | 31.8 μs |
| Write 1MB file | 499 μs |

---

### Pickle vs JSON to Disk

| Operation | Time |
|-----------|------|
| `pickle.dumps()` (complex obj) | 1.29 μs |
| `pickle.loads()` (complex obj) | 1.45 μs |
| `json.dumps()` (complex obj) | 2.89 μs |
| `json.loads()` (complex obj) | 2.35 μs |

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
| Insert one object | 172 μs |
| Select by primary key | 3.75 μs |
| Update one field | 5.33 μs |
| Delete | 168 μs |
| Select with `json_extract()` | 4.11 μs |

---

### diskcache

| Operation | Time |
|-----------|------|
| `cache.set(key, obj)` | 27.4 μs |
| `cache.get(key)` | 4.68 μs |
| `cache.delete(key)` | 54.0 μs |
| Check key exists | 2.03 μs |

---

### MongoDB

| Operation | Time |
|-----------|------|
| `insert_one()` | 115 μs |
| `find_one()` by `_id` | 121 μs |
| `find_one()` by nested field | 124 μs |
| `update_one()` | 129 μs |
| `delete_one()` | 32.0 ns |

---

### Comparison Table

| Operation | SQLite | diskcache | MongoDB |
|-----------|--------|-----------|---------|
| Write one object | 172 μs | 27.4 μs | 115 μs |
| Read by key/id | 3.75 μs | 4.68 μs | 121 μs |
| Read by nested field | 4.11 μs | N/A | 124 μs |
| Update one field | 5.33 μs | 27.4 μs | 129 μs |
| Delete | 168 μs | 54.0 μs | 32.0 ns |

---

## Function and Call Overhead

The hidden cost of function calls, exceptions, and async.

### Function Calls

| Operation | Time |
|-----------|------|
| Empty function call | 19.6 ns |
| Function with 5 arguments | 25.7 ns |
| Method call on object | 23.1 ns |
| Lambda call | 18.5 ns |
| Built-in function (`len()`) | 17.9 ns |

---

### Exceptions

| Operation | Time |
|-----------|------|
| `try/except` (no exception raised) | 22.2 ns |
| `try/except` (exception raised) | 154 ns |

---

### Type Checking

| Operation | Time |
|-----------|------|
| `isinstance()` | 18.8 ns |
| `type() == type` | 20.8 ns |

---

## Async Overhead

The cost of async machinery.

| Operation | Time |
|-----------|------|
| `await` already-completed coroutine | 54.9 μs |
| Create coroutine object (no await) | 45.3 ns |
| `asyncio.sleep(0)` | 62.4 μs |
| `asyncio.gather()` on 10 completed | 70.2 μs |

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
