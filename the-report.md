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
| **Basic Ops** | Add two integers | 20.3 ns (49.2M ops/sec) | — |
| | Add two floats | 19.5 ns (51.3M ops/sec) | — |
| | String concatenation (small) | 39.6 ns (25.3M ops/sec) | — |
| | f-string formatting | 67.8 ns (14.7M ops/sec) | — |
| | `.format()` | 99.8 ns (10.0M ops/sec) | — |
| | `%` formatting | 85.6 ns (11.7M ops/sec) | — |
| | List append | 29.8 ns (33.5M ops/sec) | — |
| | List comprehension (1,000 items) | 9.46 μs (105.7k ops/sec) | — |
| | Equivalent for-loop (1,000 items) | 13.5 μs (74.1k ops/sec) | — |
| **Collections** | Dict lookup by key | 25.3 ns (39.6M ops/sec) | — |
| | Set membership check | 23.4 ns (42.8M ops/sec) | — |
| | List index access | 20.2 ns (49.6M ops/sec) | — |
| | List membership check (1,000 items) | 3.93 μs (254.4k ops/sec) | — |
| | `len()` on list | 18.6 ns (53.8M ops/sec) | — |
| | Iterate 1,000-item list | 8.44 μs (118.5k ops/sec) | — |
| | Iterate 1,000-item dict | 9.02 μs (110.9k ops/sec) | — |
| | `range(1000)` iteration | 9.73 μs (102.8k ops/sec) | — |
| | `sum()` of 1,000 ints | 1.74 μs (574.3k ops/sec) | — |
| **Attributes** | Read from regular class | 13.7 ns (73.1M ops/sec) | — |
| | Write to regular class | 16.1 ns (62.2M ops/sec) | — |
| | Read from `__slots__` class | 13.9 ns (72.0M ops/sec) | — |
| | Write to `__slots__` class | 14.9 ns (67.2M ops/sec) | — |
| | Read from `@property` | 19.6 ns (51.0M ops/sec) | — |
| | `getattr()` | 23.6 ns (42.4M ops/sec) | — |
| | `hasattr()` | 21.7 ns (46.2M ops/sec) | — |
| **JSON** | `json.dumps()` (simple) | 706 ns (1.4M ops/sec) | — |
| | `json.loads()` (simple) | 604 ns (1.7M ops/sec) | — |
| | `json.dumps()` (complex) | 2.68 μs (373.0k ops/sec) | — |
| | `json.loads()` (complex) | 2.36 μs (424.1k ops/sec) | — |
| | `orjson.dumps()` (complex) | 330 ns (3.0M ops/sec) | — |
| | `orjson.loads()` (complex) | 908 ns (1.1M ops/sec) | — |
| | `ujson.dumps()` (complex) | 1.78 μs (561.5k ops/sec) | — |
| | `msgspec` encode (complex) | 456 ns (2.2M ops/sec) | — |
| | Pydantic `model_dump_json()` | 1.60 μs (625.2k ops/sec) | — |
| | Pydantic `model_validate_json()` | 2.75 μs (364.3k ops/sec) | — |
| **Web Frameworks** | Flask (return JSON) | {{WEB.FLASK_RETURN_JSON}} | — |
| | Django (return JSON) | {{WEB.DJANGO_RETURN_JSON}} | — |
| | FastAPI async (return JSON) | {{WEB.FASTAPI_ASYNC_RETURN_JSON}} | — |
| | FastAPI sync (return JSON) | {{WEB.FASTAPI_SYNC_RETURN_JSON}} | — |
| | Starlette (return JSON) | {{WEB.STARLETTE_RETURN_JSON}} | — |
| **File I/O** | Open and close file | 9.30 μs (107.5k ops/sec) | — |
| | Read 1KB file | 10.8 μs (92.8k ops/sec) | — |
| | Write 1KB file | 28.3 μs (35.4k ops/sec) | — |
| | Write 1MB file | 473 μs (2.1k ops/sec) | — |
| | `pickle.dumps()` | 1.11 μs (897.4k ops/sec) | — |
| | `pickle.loads()` | 1.41 μs (708.6k ops/sec) | — |
| **Database** | SQLite insert (JSON blob) | 182 μs (5.5k ops/sec) | — |
| | SQLite select by PK | 3.57 μs (280.5k ops/sec) | — |
| | SQLite update one field | 5.30 μs (188.6k ops/sec) | — |
| | diskcache set | 23.9 μs (41.8k ops/sec) | — |
| | diskcache get | 4.18 μs (239.0k ops/sec) | — |
| | MongoDB insert_one | 115 μs (8.7k ops/sec) | — |
| | MongoDB find_one by _id | 122 μs (8.2k ops/sec) | — |
| | MongoDB find_one by nested field | 168 μs (5.9k ops/sec) | — |
| **Functions** | Empty function call | 19.5 ns (51.4M ops/sec) | — |
| | Function with 5 args | 23.8 ns (42.1M ops/sec) | — |
| | Method call | 22.2 ns (45.1M ops/sec) | — |
| | Lambda call | 18.6 ns (53.6M ops/sec) | — |
| | try/except (no exception) | 22.5 ns (44.4M ops/sec) | — |
| | try/except (exception raised) | 127 ns (7.9M ops/sec) | — |
| | `isinstance()` check | 18.5 ns (54.0M ops/sec) | — |
| **Async** | `await` completed coroutine | 46.0 μs (21.7k ops/sec) | — |
| | Create coroutine object | 45.5 ns (22.0M ops/sec) | — |
| | `asyncio.sleep(0)` | 58.8 μs (17.0k ops/sec) | — |

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
| Add two integers | 20.3 ns (49.2M ops/sec) |
| Add two floats | 19.5 ns (51.3M ops/sec) |
| Multiply two integers | 21.4 ns (46.7M ops/sec) |

---

### String Operations

| Operation | Time |
|-----------|------|
| Concatenation (`+`) | 39.6 ns (25.3M ops/sec) |
| f-string | 67.8 ns (14.7M ops/sec) |
| `.format()` | 99.8 ns (10.0M ops/sec) |
| `%` formatting | 85.6 ns (11.7M ops/sec) |

---

### List Operations

| Operation | Time |
|-----------|------|
| `list.append()` | 29.8 ns (33.5M ops/sec) |
| List comprehension (1,000 items) | 9.46 μs (105.7k ops/sec) |
| Equivalent for-loop (1,000 items) | 13.5 μs (74.1k ops/sec) |

---

## Collection Access and Iteration

How fast can you get data out of Python's built-in collections?

### Access by Key/Index

| Operation | Time |
|-----------|------|
| Dict lookup by key | 25.3 ns (39.6M ops/sec) |
| Set membership (`in`) | 23.4 ns (42.8M ops/sec) |
| List index access | 20.2 ns (49.6M ops/sec) |
| List membership (`in`, 1,000 items) | 3.93 μs (254.4k ops/sec) |

---

### Length

| Collection | `len()` time |
|------------|--------------|
| List (1,000 items) | 18.6 ns (53.8M ops/sec) |
| Dict (1,000 items) | 17.3 ns (57.8M ops/sec) |
| Set (1,000 items) | 18.4 ns (54.3M ops/sec) |

---

### Iteration

| Operation | Time |
|-----------|------|
| Iterate 1,000-item list | 8.44 μs (118.5k ops/sec) |
| Iterate 1,000-item dict (keys) | 9.02 μs (110.9k ops/sec) |
| Iterate `range(1000)` | 9.73 μs (102.8k ops/sec) |
| `sum()` of 1,000 integers | 1.74 μs (574.3k ops/sec) |

---

## Class and Object Attributes

The cost of reading and writing attributes, and how `__slots__` changes things.

### Attribute Access

| Operation | Regular Class | `__slots__` Class |
|-----------|---------------|-------------------|
| Read attribute | 13.7 ns (73.1M ops/sec) | 13.9 ns (72.0M ops/sec) |
| Write attribute | 16.1 ns (62.2M ops/sec) | 14.9 ns (67.2M ops/sec) |

---

### Other Attribute Operations

| Operation | Time |
|-----------|------|
| Read `@property` | 19.6 ns (51.0M ops/sec) |
| `getattr(obj, 'attr')` | 23.6 ns (42.4M ops/sec) |
| `hasattr(obj, 'attr')` | 21.7 ns (46.2M ops/sec) |

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
| `json` (stdlib) | 706 ns (1.4M ops/sec) | 2.68 μs (373.0k ops/sec) |
| `orjson` | 62.5 ns (16.0M ops/sec) | 330 ns (3.0M ops/sec) |
| `ujson` | 266 ns (3.8M ops/sec) | 1.78 μs (561.5k ops/sec) |
| `msgspec` | 72.9 ns (13.7M ops/sec) | 456 ns (2.2M ops/sec) |

---

### Deserialization (loads)

| Library | Simple Object | Complex Object |
|---------|---------------|----------------|
| `json` (stdlib) | 604 ns (1.7M ops/sec) | 2.36 μs (424.1k ops/sec) |
| `orjson` | 125 ns (8.0M ops/sec) | 908 ns (1.1M ops/sec) |
| `ujson` | 278 ns (3.6M ops/sec) | 1.68 μs (596.6k ops/sec) |
| `msgspec` | 102 ns (9.8M ops/sec) | 988 ns (1.0M ops/sec) |

---

### Pydantic

| Operation | Time |
|-----------|------|
| `model_dump_json()` | 1.60 μs (625.2k ops/sec) |
| `model_validate_json()` | 2.75 μs (364.3k ops/sec) |
| `model_dump()` (to dict) | 1.73 μs (576.4k ops/sec) |
| `model_validate()` (from dict) | 2.24 μs (446.5k ops/sec) |

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
| Open and close (no read) | 9.30 μs (107.5k ops/sec) |
| Read 1KB file | 10.8 μs (92.8k ops/sec) |
| Read 1MB file | 31.9 μs (31.3k ops/sec) |
| Write 1KB file | 28.3 μs (35.4k ops/sec) |
| Write 1MB file | 473 μs (2.1k ops/sec) |

---

### Pickle vs JSON to Disk

| Operation | Time |
|-----------|------|
| `pickle.dumps()` (complex obj) | 1.11 μs (897.4k ops/sec) |
| `pickle.loads()` (complex obj) | 1.41 μs (708.6k ops/sec) |
| `json.dumps()` (complex obj) | 2.71 μs (368.5k ops/sec) |
| `json.loads()` (complex obj) | 2.24 μs (446.3k ops/sec) |

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
| Insert one object | 182 μs (5.5k ops/sec) |
| Select by primary key | 3.57 μs (280.5k ops/sec) |
| Update one field | 5.30 μs (188.6k ops/sec) |
| Delete | 168 μs (6.0k ops/sec) |
| Select with `json_extract()` | 4.55 μs (220.0k ops/sec) |

---

### diskcache

| Operation | Time |
|-----------|------|
| `cache.set(key, obj)` | 23.9 μs (41.8k ops/sec) |
| `cache.get(key)` | 4.18 μs (239.0k ops/sec) |
| `cache.delete(key)` | 52.9 μs (18.9k ops/sec) |
| Check key exists | 1.89 μs (529.4k ops/sec) |

---

### MongoDB

| Operation | Time |
|-----------|------|
| `insert_one()` | 115 μs (8.7k ops/sec) |
| `find_one()` by `_id` | 122 μs (8.2k ops/sec) |
| `find_one()` by nested field | 168 μs (5.9k ops/sec) |
| `update_one()` | 139 μs (7.2k ops/sec) |
| `delete_one()` | 31.3 ns (31.9M ops/sec) |

---

### Comparison Table

| Operation | SQLite | diskcache | MongoDB |
|-----------|--------|-----------|---------|
| Write one object | 182 μs (5.5k ops/sec) | 23.9 μs (41.8k ops/sec) | 115 μs (8.7k ops/sec) |
| Read by key/id | 3.57 μs (280.5k ops/sec) | 4.18 μs (239.0k ops/sec) | 122 μs (8.2k ops/sec) |
| Read by nested field | 4.55 μs (220.0k ops/sec) | N/A | 168 μs (5.9k ops/sec) |
| Update one field | 5.30 μs (188.6k ops/sec) | 23.9 μs (41.8k ops/sec) | 139 μs (7.2k ops/sec) |
| Delete | 168 μs (6.0k ops/sec) | 52.9 μs (18.9k ops/sec) | 31.3 ns (31.9M ops/sec) |

---

## Function and Call Overhead

The hidden cost of function calls, exceptions, and async.

### Function Calls

| Operation | Time |
|-----------|------|
| Empty function call | 19.5 ns (51.4M ops/sec) |
| Function with 5 arguments | 23.8 ns (42.1M ops/sec) |
| Method call on object | 22.2 ns (45.1M ops/sec) |
| Lambda call | 18.6 ns (53.6M ops/sec) |
| Built-in function (`len()`) | 18.4 ns (54.5M ops/sec) |

---

### Exceptions

| Operation | Time |
|-----------|------|
| `try/except` (no exception raised) | 22.5 ns (44.4M ops/sec) |
| `try/except` (exception raised) | 127 ns (7.9M ops/sec) |

---

### Type Checking

| Operation | Time |
|-----------|------|
| `isinstance()` | 18.5 ns (54.0M ops/sec) |
| `type() == type` | 20.4 ns (49.0M ops/sec) |

---

## Async Overhead

The cost of async machinery.

| Operation | Time |
|-----------|------|
| `await` already-completed coroutine | 46.0 μs (21.7k ops/sec) |
| Create coroutine object (no await) | 45.5 ns (22.0M ops/sec) |
| `asyncio.sleep(0)` | 58.8 μs (17.0k ops/sec) |
| `asyncio.gather()` on 10 completed | 68.5 μs (14.6k ops/sec) |

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
