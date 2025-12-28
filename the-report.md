# Python Numbers Programmer Should Know

*Inspired by "Latency Numbers Every Programmer Should Know" -- but for Python.*

A practical reference for understanding the cost of common Python operations. All benchmarks run on macOS-26.2-arm64-arm-64bit-Mach-O with Python 3.14.2.

---

## Quick Reference Table

| Category | Operation | Time | Memory |
|----------|-----------|------|--------|
| **Memory** | Empty Python process | — | 25.73 MB |
| | Empty string | — | 41 bytes |
| | 100-char string | — | 141 bytes |
| | Small int (0-256) | — | 28 bytes |
| | Large int | — | 28 bytes |
| | Float | — | 24 bytes |
| | Empty list | — | 56 bytes |
| | List with 1,000 ints | — | 7.87 KB |
| | List with 1,000 floats | — | 8.65 KB |
| | Empty dict | — | 64 bytes |
| | Dict with 1,000 items | — | 36.1 KB |
| | Empty set | — | 216 bytes |
| | Set with 1,000 items | — | 32.2 KB |
| | Regular class instance (5 attrs) | — | 48 bytes |
| | `__slots__` class instance (5 attrs) | — | 72 bytes |
| | List of 1,000 regular class instances | — | 165.2 KB |
| | List of 1,000 `__slots__` class instances | — | 79.1 KB |
| | dataclass instance | — | 48 bytes |
| | namedtuple instance | — | 88 bytes |
| **Basic Ops** | Add two integers | 20.3 ns | — |
| | Add two floats | 19.5 ns | — |
| | String concatenation (small) | 39.6 ns | — |
| | f-string formatting | 67.8 ns | — |
| | `.format()` | 99.8 ns | — |
| | `%` formatting | 85.6 ns | — |
| | List append | 29.8 ns | — |
| | List comprehension (1,000 items) | 9.46 μs | — |
| | Equivalent for-loop (1,000 items) | 13.5 μs | — |
| **Collections** | Dict lookup by key | 25.3 ns | — |
| | Set membership check | 23.4 ns | — |
| | List index access | 20.2 ns | — |
| | List membership check (1,000 items) | 3.93 μs | — |
| | `len()` on list | 18.6 ns | — |
| | Iterate 1,000-item list | 8.44 μs | — |
| | Iterate 1,000-item dict | 9.02 μs | — |
| | `range(1000)` iteration | 9.73 μs | — |
| | `sum()` of 1,000 ints | 1.74 μs | — |
| **Attributes** | Read from regular class | 13.7 ns | — |
| | Write to regular class | 16.1 ns | — |
| | Read from `__slots__` class | 13.9 ns | — |
| | Write to `__slots__` class | 14.9 ns | — |
| | Read from `@property` | 19.6 ns | — |
| | `getattr()` | 23.6 ns | — |
| | `hasattr()` | 21.7 ns | — |
| **JSON** | `json.dumps()` (simple) | 706 ns | — |
| | `json.loads()` (simple) | 604 ns | — |
| | `json.dumps()` (complex) | 2.68 μs | — |
| | `json.loads()` (complex) | 2.36 μs | — |
| | `orjson.dumps()` (complex) | 330 ns | — |
| | `orjson.loads()` (complex) | 908 ns | — |
| | `ujson.dumps()` (complex) | 1.78 μs | — |
| | `msgspec` encode (complex) | 456 ns | — |
| | Pydantic `model_dump_json()` | 1.60 μs | — |
| | Pydantic `model_validate_json()` | 2.75 μs | — |
| **Web Frameworks** | Flask (return JSON) | {{WEB.FLASK_RETURN_JSON}} | — |
| | Django (return JSON) | {{WEB.DJANGO_RETURN_JSON}} | — |
| | FastAPI async (return JSON) | {{WEB.FASTAPI_ASYNC_RETURN_JSON}} | — |
| | FastAPI sync (return JSON) | {{WEB.FASTAPI_SYNC_RETURN_JSON}} | — |
| | Starlette (return JSON) | {{WEB.STARLETTE_RETURN_JSON}} | — |
| **File I/O** | Open and close file | 9.30 μs | — |
| | Read 1KB file | 10.8 μs | — |
| | Write 1KB file | 28.3 μs | — |
| | Write 1MB file | 473 μs | — |
| | `pickle.dumps()` | 1.11 μs | — |
| | `pickle.loads()` | 1.41 μs | — |
| **Database** | SQLite insert (JSON blob) | 182 μs | — |
| | SQLite select by PK | 3.57 μs | — |
| | SQLite update one field | 5.30 μs | — |
| | diskcache set | 23.9 μs | — |
| | diskcache get | 4.18 μs | — |
| | MongoDB insert_one | 115 μs | — |
| | MongoDB find_one by _id | 122 μs | — |
| | MongoDB find_one by nested field | 168 μs | — |
| **Functions** | Empty function call | 19.5 ns | — |
| | Function with 5 args | 23.8 ns | — |
| | Method call | 22.2 ns | — |
| | Lambda call | 18.6 ns | — |
| | try/except (no exception) | 22.5 ns | — |
| | try/except (exception raised) | 127 ns | — |
| | `isinstance()` check | 18.5 ns | — |
| **Async** | `await` completed coroutine | 46.0 μs | — |
| | Create coroutine object | 45.5 ns | — |
| | `asyncio.sleep(0)` | 58.8 μs | — |

---

## Memory Costs

Understanding how much memory different Python objects consume.

### Empty Python Process

**Result:** 25.73 MB

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

| Collection | Empty | 1,000 items |
|------------|-------|------------|
| List (ints) | 56 bytes | 7.87 KB |
| List (floats) | 56 bytes | 8.65 KB |
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

**Aggregate Memory Usage (1,000 instances):**

| Type | Total Memory |
|------|--------------|
| List of 1,000 regular class instances | 165.2 KB |
| List of 1,000 `__slots__` class instances | 79.1 KB |

---

## Basic Operations

The cost of fundamental Python operations.

### Arithmetic

| Operation | Time |
|-----------|------|
| Add two integers | 20.3 ns |
| Add two floats | 19.5 ns |
| Multiply two integers | 21.4 ns |

---

### String Operations

| Operation | Time |
|-----------|------|
| Concatenation (`+`) | 39.6 ns |
| f-string | 67.8 ns |
| `.format()` | 99.8 ns |
| `%` formatting | 85.6 ns |

---

### List Operations

| Operation | Time |
|-----------|------|
| `list.append()` | 29.8 ns |
| List comprehension (1,000 items) | 9.46 μs |
| Equivalent for-loop (1,000 items) | 13.5 μs |

---

## Collection Access and Iteration

How fast can you get data out of Python's built-in collections?

### Access by Key/Index

| Operation | Time |
|-----------|------|
| Dict lookup by key | 25.3 ns |
| Set membership (`in`) | 23.4 ns |
| List index access | 20.2 ns |
| List membership (`in`, 1,000 items) | 3.93 μs |

---

### Length

| Collection | `len()` time |
|------------|--------------|
| List (1,000 items) | 18.6 ns |
| Dict (1,000 items) | 17.3 ns |
| Set (1,000 items) | 18.4 ns |

---

### Iteration

| Operation | Time |
|-----------|------|
| Iterate 1,000-item list | 8.44 μs |
| Iterate 1,000-item dict (keys) | 9.02 μs |
| Iterate `range(1000)` | 9.73 μs |
| `sum()` of 1,000 integers | 1.74 μs |

---

## Class and Object Attributes

The cost of reading and writing attributes, and how `__slots__` changes things.

### Attribute Access

| Operation | Regular Class | `__slots__` Class |
|-----------|---------------|-------------------|
| Read attribute | 13.7 ns | 13.9 ns |
| Write attribute | 16.1 ns | 14.9 ns |

---

### Other Attribute Operations

| Operation | Time |
|-----------|------|
| Read `@property` | 19.6 ns |
| `getattr(obj, 'attr')` | 23.6 ns |
| `hasattr(obj, 'attr')` | 21.7 ns |

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
| `json` (stdlib) | 706 ns | 2.68 μs |
| `orjson` | 62.5 ns | 330 ns |
| `ujson` | 266 ns | 1.78 μs |
| `msgspec` | 72.9 ns | 456 ns |

---

### Deserialization (loads)

| Library | Simple Object | Complex Object |
|---------|---------------|----------------|
| `json` (stdlib) | 604 ns | 2.36 μs |
| `orjson` | 125 ns | 908 ns |
| `ujson` | 278 ns | 1.68 μs |
| `msgspec` | 102 ns | 988 ns |

---

### Pydantic

| Operation | Time |
|-----------|------|
| `model_dump_json()` | 1.60 μs |
| `model_validate_json()` | 2.75 μs |
| `model_dump()` (to dict) | 1.73 μs |
| `model_validate()` (from dict) | 2.24 μs |

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
| Open and close (no read) | 9.30 μs |
| Read 1KB file | 10.8 μs |
| Read 1MB file | 31.9 μs |
| Write 1KB file | 28.3 μs |
| Write 1MB file | 473 μs |

---

### Pickle vs JSON to Disk

| Operation | Time |
|-----------|------|
| `pickle.dumps()` (complex obj) | 1.11 μs |
| `pickle.loads()` (complex obj) | 1.41 μs |
| `json.dumps()` (complex obj) | 2.71 μs |
| `json.loads()` (complex obj) | 2.24 μs |

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
| Insert one object | 182 μs |
| Select by primary key | 3.57 μs |
| Update one field | 5.30 μs |
| Delete | 168 μs |
| Select with `json_extract()` | 4.55 μs |

---

### diskcache

| Operation | Time |
|-----------|------|
| `cache.set(key, obj)` | 23.9 μs |
| `cache.get(key)` | 4.18 μs |
| `cache.delete(key)` | 52.9 μs |
| Check key exists | 1.89 μs |

---

### MongoDB

| Operation | Time |
|-----------|------|
| `insert_one()` | 115 μs |
| `find_one()` by `_id` | 122 μs |
| `find_one()` by nested field | 168 μs |
| `update_one()` | 139 μs |
| `delete_one()` | 31.3 ns |

---

### Comparison Table

| Operation | SQLite | diskcache | MongoDB |
|-----------|--------|-----------|---------|
| Write one object | 182 μs | 23.9 μs | 115 μs |
| Read by key/id | 3.57 μs | 4.18 μs | 122 μs |
| Read by nested field | 4.55 μs | N/A | 168 μs |
| Update one field | 5.30 μs | 23.9 μs | 139 μs |
| Delete | 168 μs | 52.9 μs | 31.3 ns |

---

## Function and Call Overhead

The hidden cost of function calls, exceptions, and async.

### Function Calls

| Operation | Time |
|-----------|------|
| Empty function call | 19.5 ns |
| Function with 5 arguments | 23.8 ns |
| Method call on object | 22.2 ns |
| Lambda call | 18.6 ns |
| Built-in function (`len()`) | 18.4 ns |

---

### Exceptions

| Operation | Time |
|-----------|------|
| `try/except` (no exception raised) | 22.5 ns |
| `try/except` (exception raised) | 127 ns |

---

### Type Checking

| Operation | Time |
|-----------|------|
| `isinstance()` | 18.5 ns |
| `type() == type` | 20.4 ns |

---

## Async Overhead

The cost of async machinery.

| Operation | Time |
|-----------|------|
| `await` already-completed coroutine | 46.0 μs |
| Create coroutine object (no await) | 45.5 ns |
| `asyncio.sleep(0)` | 58.8 μs |
| `asyncio.gather()` on 10 completed | 68.5 μs |

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
