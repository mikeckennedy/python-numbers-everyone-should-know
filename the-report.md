# Python Numbers Every Programmer Should Know

*Inspired by "Latency Numbers Every Programmer Should Know" -- but for Python.*

A practical reference for understanding the cost of common Python operations. All benchmarks run on macOS-26.1-arm64-arm-64bit-Mach-O with Python 3.14.2.

---

## Quick Reference Table

| Category | Operation | Time | Memory |
|----------|-----------|------|--------|
| [**💾 Memory**](#memory-costs) | Empty Python process | — | 15.61 MB |
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
| [**⚙️ Basic Ops**](#basic-operations) | Add two integers | 19.6 ns (50.9M ops/sec) | — |
| | Add two floats | 18.8 ns (53.2M ops/sec) | — |
| | String concatenation (small) | 42.0 ns (23.8M ops/sec) | — |
| | f-string formatting | 65.7 ns (15.2M ops/sec) | — |
| | `.format()` | 106 ns (9.5M ops/sec) | — |
| | `%` formatting | 88.2 ns (11.3M ops/sec) | — |
| | List append | 88.6 ns (11.3M ops/sec) | — |
| | List comprehension (1,000 items) | 9.19 μs (108.8k ops/sec) | — |
| | Equivalent for-loop (1,000 items) | 11.7 μs (85.8k ops/sec) | — |
| [**📦 Collections**](#collection-access-and-iteration) | Dict lookup by key | 23.9 ns (41.8M ops/sec) | — |
| | Set membership check | 19.2 ns (52.1M ops/sec) | — |
| | List index access | 18.2 ns (55.1M ops/sec) | — |
| | List membership check (1,000 items) | 3.90 μs (256.4k ops/sec) | — |
| | `len()` on list | 18.3 ns (54.8M ops/sec) | — |
| | Iterate 1,000-item list | 7.76 μs (128.9k ops/sec) | — |
| | Iterate 1,000-item dict | 8.64 μs (115.8k ops/sec) | — |
| | `range(1000)` iteration | {{COLLECTIONS.FOR_I_IN_RANGE_1000}} | — |
| | `sum()` of 1,000 ints | 1.80 μs (557.0k ops/sec) | — |
| [**🏷️ Attributes**](#class-and-object-attributes) | Read from regular class | 15.9 ns (63.0M ops/sec) | — |
| | Write to regular class | 16.0 ns (62.4M ops/sec) | — |
| | Read from `__slots__` class | 14.9 ns (67.1M ops/sec) | — |
| | Write to `__slots__` class | 14.9 ns (67.1M ops/sec) | — |
| | Read from `@property` | 21.8 ns (46.0M ops/sec) | — |
| | `getattr()` | 15.4 ns (64.9M ops/sec) | — |
| | `hasattr()` | 23.5 ns (42.6M ops/sec) | — |
| [**📄 JSON**](#json-and-serialization) | `json.dumps()` (simple) | 689 ns (1.5M ops/sec) | — |
| | `json.loads()` (simple) | 590 ns (1.7M ops/sec) | — |
| | `json.dumps()` (complex) | 2.59 μs (386.7k ops/sec) | — |
| | `json.loads()` (complex) | 2.24 μs (445.8k ops/sec) | — |
| | `orjson.dumps()` (complex) | 298 ns (3.4M ops/sec) | — |
| | `orjson.loads()` (complex) | 942 ns (1.1M ops/sec) | — |
| | `ujson.dumps()` (complex) | 1.60 μs (623.7k ops/sec) | — |
| | `msgspec` encode (complex) | 422 ns (2.4M ops/sec) | — |
| | Pydantic `model_dump_json()` | 1.50 μs (665.3k ops/sec) | — |
| | Pydantic `model_validate_json()` | 2.79 μs (359.0k ops/sec) | — |
| [**🌐 Web Frameworks**](#web-frameworks) | Flask (return JSON) | 19.6 μs (51.1k req/sec) | — |
| | Django (return JSON) | 21.6 μs (46.3k req/sec) | — |
| | FastAPI (return JSON) | 34.8 μs (28.7k req/sec) | — |
| | Starlette (return JSON) | 6.43 μs (155.5k req/sec) | — |
| | Litestar (return JSON) | 7.67 μs (130.4k req/sec) | — |
| [**📁 File I/O**](#file-io) | Open and close file | 9.19 μs (108.8k ops/sec) | — |
| | Read 1KB file | 10.2 μs (98.4k ops/sec) | — |
| | Write 1KB file | 31.8 μs (31.4k ops/sec) | — |
| | Write 1MB file | 658 μs (1.5k ops/sec) | — |
| | `pickle.dumps()` | 1.10 μs (906.8k ops/sec) | — |
| | `pickle.loads()` | 1.33 μs (752.1k ops/sec) | — |
| [**🗄️ Database**](#database-and-persistence) | SQLite insert (JSON blob) | 183 μs (5.5k ops/sec) | — |
| | SQLite select by PK | 3.60 μs (277.6k ops/sec) | — |
| | SQLite update one field | 5.07 μs (197.2k ops/sec) | — |
| | diskcache set | 24.4 μs (40.9k ops/sec) | — |
| | diskcache get | 4.31 μs (231.9k ops/sec) | — |
| | MongoDB insert_one | 106 μs (9.4k ops/sec) | — |
| | MongoDB find_one by _id | 114 μs (8.8k ops/sec) | — |
| | MongoDB find_one by nested field | 119 μs (8.4k ops/sec) | — |
| [**📞 Functions**](#function-and-call-overhead) | Empty function call | 20.0 ns (49.9M ops/sec) | — |
| | Function with 5 args | 25.3 ns (39.6M ops/sec) | — |
| | Method call | 23.2 ns (43.1M ops/sec) | — |
| | Lambda call | 20.9 ns (47.8M ops/sec) | — |
| | try/except (no exception) | 21.4 ns (46.7M ops/sec) | — |
| | try/except (exception raised) | 149 ns (6.7M ops/sec) | — |
| | `isinstance()` check | 18.5 ns (54.2M ops/sec) | — |
| [**⏱️ Async**](#async-overhead) | Create coroutine object | 46.7 ns (21.4M ops/sec) | — |
| | `run_until_complete(empty)` | 26.7 μs (37.5k ops/sec) | — |
| | `asyncio.sleep(0)` | 39.0 μs (25.6k ops/sec) | — |
| | `gather()` 10 coroutines | 52.8 μs (18.9k ops/sec) | — |
| | `create_task()` + await | 50.4 μs (19.8k ops/sec) | — |
| | `async with` (context manager) | 27.7 μs (36.0k ops/sec) | — |

---

## Memory Costs

Understanding how much memory different Python objects consume.

### Empty Python Process

**Result:** 15.61 MB

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
| Add two integers | 19.6 ns (50.9M ops/sec) |
| Add two floats | 18.8 ns (53.2M ops/sec) |
| Multiply two integers | 19.7 ns (50.6M ops/sec) |

---

### String Operations

| Operation | Time |
|-----------|------|
| Concatenation (`+`) | 42.0 ns (23.8M ops/sec) |
| f-string | 65.7 ns (15.2M ops/sec) |
| `.format()` | 106 ns (9.5M ops/sec) |
| `%` formatting | 88.2 ns (11.3M ops/sec) |

---

### List Operations

| Operation | Time |
|-----------|------|
| `list.append()` | 88.6 ns (11.3M ops/sec) |
| List comprehension (1,000 items) | 9.19 μs (108.8k ops/sec) |
| Equivalent for-loop (1,000 items) | 11.7 μs (85.8k ops/sec) |

---

## Collection Access and Iteration

How fast can you get data out of Python's built-in collections?

### Access by Key/Index

| Operation | Time |
|-----------|------|
| Dict lookup by key | 23.9 ns (41.8M ops/sec) |
| Set membership (`in`) | 19.2 ns (52.1M ops/sec) |
| List index access | 18.2 ns (55.1M ops/sec) |
| List membership (`in`, 1,000 items) | 3.90 μs (256.4k ops/sec) |

---

### Length

| Collection | `len()` time |
|------------|--------------|
| List (1,000 items) | 18.3 ns (54.8M ops/sec) |
| Dict (1,000 items) | 18.7 ns (53.4M ops/sec) |
| Set (1,000 items) | 18.1 ns (55.2M ops/sec) |

---

### Iteration

| Operation | Time |
|-----------|------|
| Iterate 1,000-item list | 7.76 μs (128.9k ops/sec) |
| Iterate 1,000-item dict (keys) | 8.64 μs (115.8k ops/sec) |
| Iterate `range(1000)` | {{COLLECTIONS.FOR_I_IN_RANGE_1000}} |
| `sum()` of 1,000 integers | 1.80 μs (557.0k ops/sec) |

---

## Class and Object Attributes

The cost of reading and writing attributes, and how `__slots__` changes things.

### Attribute Access

| Operation | Regular Class | `__slots__` Class |
|-----------|---------------|-------------------|
| Read attribute | 15.9 ns (63.0M ops/sec) | 14.9 ns (67.1M ops/sec) |
| Write attribute | 16.0 ns (62.4M ops/sec) | 14.9 ns (67.1M ops/sec) |

---

### Other Attribute Operations

| Operation | Time |
|-----------|------|
| Read `@property` | 21.8 ns (46.0M ops/sec) |
| `getattr(obj, 'attr')` | 15.4 ns (64.9M ops/sec) |
| `hasattr(obj, 'attr')` | 23.5 ns (42.6M ops/sec) |

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
| `json` (stdlib) | 689 ns (1.5M ops/sec) | 2.59 μs (386.7k ops/sec) |
| `orjson` | 63.3 ns (15.8M ops/sec) | 298 ns (3.4M ops/sec) |
| `ujson` | 263 ns (3.8M ops/sec) | 1.60 μs (623.7k ops/sec) |
| `msgspec` | 83.7 ns (11.9M ops/sec) | 422 ns (2.4M ops/sec) |

---

### Deserialization (loads)

| Library | Simple Object | Complex Object |
|---------|---------------|----------------|
| `json` (stdlib) | 590 ns (1.7M ops/sec) | 2.24 μs (445.8k ops/sec) |
| `orjson` | 112 ns (9.0M ops/sec) | 942 ns (1.1M ops/sec) |
| `ujson` | 311 ns (3.2M ops/sec) | 1.49 μs (672.4k ops/sec) |
| `msgspec` | 108 ns (9.3M ops/sec) | 896 ns (1.1M ops/sec) |

---

### Pydantic

| Operation | Time |
|-----------|------|
| `model_dump_json()` | 1.50 μs (665.3k ops/sec) |
| `model_validate_json()` | 2.79 μs (359.0k ops/sec) |
| `model_dump()` (to dict) | 1.64 μs (610.0k ops/sec) |
| `model_validate()` (from dict) | 2.15 μs (466.0k ops/sec) |

---

## Web Frameworks

Returning a simple JSON response. Benchmarked with `wrk` or `hey` against localhost.

### Test Setup

Each framework returns the same JSON payload from a minimal endpoint.

### Results

| Framework | Requests/sec | Latency (p50) | Latency (p99) |
|-----------|--------------|---------------|---------------|
| Flask | 19.6 μs (51.1k req/sec) | {{WEB.FLASK_LATENCY_P50}} | 7.210 ms (138.7 ops/sec) |
| Django | 21.6 μs (46.3k req/sec) | {{WEB.DJANGO_LATENCY_P50}} | 7.380 ms (135.5 ops/sec) |
| FastAPI | 34.8 μs (28.7k req/sec) | {{WEB.FASTAPI_LATENCY_P50}} | 6.230 ms (160.5 ops/sec) |
| Starlette | 6.43 μs (155.5k req/sec) | {{WEB.STARLETTE_LATENCY_P50}} | 1.720 ms (581.4 ops/sec) |
| Litestar | 7.67 μs (130.4k req/sec) | {{WEB.LITESTAR_LATENCY_P50}} | 1.820 ms (549.5 ops/sec) |

---

## File I/O

Reading and writing files of various sizes.

### Basic Operations

| Operation | Time |
|-----------|------|
| Open and close (no read) | 9.19 μs (108.8k ops/sec) |
| Read 1KB file | 10.2 μs (98.4k ops/sec) |
| Read 1MB file | 34.6 μs (28.9k ops/sec) |
| Write 1KB file | 31.8 μs (31.4k ops/sec) |
| Write 1MB file | 658 μs (1.5k ops/sec) |

---

### Pickle vs JSON to Disk

| Operation | Time |
|-----------|------|
| `pickle.dumps()` (complex obj) | 1.10 μs (906.8k ops/sec) |
| `pickle.loads()` (complex obj) | 1.33 μs (752.1k ops/sec) |
| `json.dumps()` (complex obj) | 2.69 μs (372.3k ops/sec) |
| `json.loads()` (complex obj) | 2.27 μs (440.3k ops/sec) |

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
| Insert one object | 183 μs (5.5k ops/sec) |
| Select by primary key | 3.60 μs (277.6k ops/sec) |
| Update one field | 5.07 μs (197.2k ops/sec) |
| Delete | 188 μs (5.3k ops/sec) |
| Select with `json_extract()` | 4.21 μs (237.7k ops/sec) |

---

### diskcache

| Operation | Time |
|-----------|------|
| `cache.set(key, obj)` | 24.4 μs (40.9k ops/sec) |
| `cache.get(key)` | 4.31 μs (231.9k ops/sec) |
| `cache.delete(key)` | 56.2 μs (17.8k ops/sec) |
| Check key exists | 1.96 μs (510.7k ops/sec) |

---

### MongoDB

| Operation | Time |
|-----------|------|
| `insert_one()` | 106 μs (9.4k ops/sec) |
| `find_one()` by `_id` | 114 μs (8.8k ops/sec) |
| `find_one()` by nested field | 119 μs (8.4k ops/sec) |
| `update_one()` | 105 μs (9.5k ops/sec) |
| `delete_one()` | 26.9 ns (37.2M ops/sec) |

---

### Comparison Table

| Operation | SQLite | diskcache | MongoDB |
|-----------|--------|-----------|---------|
| Write one object | 183 μs (5.5k ops/sec) | 24.4 μs (40.9k ops/sec) | 106 μs (9.4k ops/sec) |
| Read by key/id | 3.60 μs (277.6k ops/sec) | 4.31 μs (231.9k ops/sec) | 114 μs (8.8k ops/sec) |
| Read by nested field | 4.21 μs (237.7k ops/sec) | N/A | 119 μs (8.4k ops/sec) |
| Update one field | 5.07 μs (197.2k ops/sec) | 24.4 μs (40.9k ops/sec) | 105 μs (9.5k ops/sec) |
| Delete | 188 μs (5.3k ops/sec) | 56.2 μs (17.8k ops/sec) | 26.9 ns (37.2M ops/sec) |

---

## Function and Call Overhead

The hidden cost of function calls, exceptions, and async.

### Function Calls

| Operation | Time |
|-----------|------|
| Empty function call | 20.0 ns (49.9M ops/sec) |
| Function with 5 arguments | 25.3 ns (39.6M ops/sec) |
| Method call on object | 23.2 ns (43.1M ops/sec) |
| Lambda call | 20.9 ns (47.8M ops/sec) |
| Built-in function (`len()`) | 18.0 ns (55.7M ops/sec) |

---

### Exceptions

| Operation | Time |
|-----------|------|
| `try/except` (no exception raised) | 21.4 ns (46.7M ops/sec) |
| `try/except` (exception raised) | 149 ns (6.7M ops/sec) |

---

### Type Checking

| Operation | Time |
|-----------|------|
| `isinstance()` | 18.5 ns (54.2M ops/sec) |
| `type() == type` | 22.2 ns (45.1M ops/sec) |

---

## Async Overhead

The cost of async machinery.

### Coroutine Creation

| Operation | Time |
|-----------|------|
| Create coroutine object (no await) | 46.7 ns (21.4M ops/sec) |
| Create coroutine (with return value) | 46.9 ns (21.3M ops/sec) |

---

### Running Coroutines

| Operation | Time |
|-----------|------|
| `run_until_complete(empty)` | 26.7 μs (37.5k ops/sec) |
| `run_until_complete(return value)` | 27.0 μs (37.1k ops/sec) |
| Run nested await | 27.1 μs (36.9k ops/sec) |
| Run 3 sequential awaits | 27.8 μs (35.9k ops/sec) |

---

### asyncio.sleep()

| Operation | Time |
|-----------|------|
| `asyncio.sleep(0)` | 39.0 μs (25.6k ops/sec) |
| Coroutine with `sleep(0)` | 38.9 μs (25.7k ops/sec) |

---

### asyncio.gather()

| Operation | Time |
|-----------|------|
| `gather()` 5 coroutines | 47.0 μs (21.3k ops/sec) |
| `gather()` 10 coroutines | 52.8 μs (18.9k ops/sec) |
| `gather()` 100 coroutines | 152 μs (6.6k ops/sec) |

---

### Task Creation

| Operation | Time |
|-----------|------|
| `create_task()` + await | 50.4 μs (19.8k ops/sec) |
| Create 10 tasks + gather | 81.7 μs (12.2k ops/sec) |

---

### Async Context Managers & Iteration

| Operation | Time |
|-----------|------|
| `async with` (context manager) | 27.7 μs (36.0k ops/sec) |
| `async for` (5 items) | 29.1 μs (34.3k ops/sec) |
| `async for` (100 items) | 34.9 μs (28.6k ops/sec) |

---

### Sync vs Async Comparison

| Operation | Time |
|-----------|------|
| Sync function call | 21.2 ns (47.1M ops/sec) |
| Async equivalent (`run_until_complete`) | 27.1 μs (36.9k ops/sec) |

---

## Methodology

### Benchmarking Approach

- All benchmarks run multiple times with warmup
- Timing uses `timeit` or `perf_counter_ns` as appropriate
- Memory measured with `sys.getsizeof()` and `tracemalloc`
- Results are median of N runs

### Environment

- **OS:** macOS-26.1-arm64-arm-64bit-Mach-O
- **Python:** 3.14.2 (CPython)
- **CPU:** arm - 10 cores (10 logical)
- **RAM:** 16.0 GB

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

*Last updated: 2025-12-28*
