# Python Numbers Every Programmer Should Know

*Inspired by "Latency Numbers Every Programmer Should Know" -- but for Python.*

A practical reference for understanding the cost of common Python operations. All benchmarks run on macOS-26.1-arm64-arm-64bit-Mach-O with Python 3.14.2.

---

## Quick Reference Table

| Category | Operation | Time | Memory |
|----------|-----------|------|--------|
| [**💾 Memory**](#memory-costs) | Empty Python process | — | 15.59 MB |
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
| [**⚙️ Basic Ops**](#basic-operations) | Add two integers | 19.0 ns (52.6M ops/sec) | — |
| | Add two floats | 19.1 ns (52.4M ops/sec) | — |
| | String concatenation (small) | 40.3 ns (24.8M ops/sec) | — |
| | f-string formatting | 67.0 ns (14.9M ops/sec) | — |
| | `.format()` | 104 ns (9.6M ops/sec) | — |
| | `%` formatting | 83.4 ns (12.0M ops/sec) | — |
| | List append | 28.5 ns (35.1M ops/sec) | — |
| | List comprehension (1,000 items) | 9.38 μs (106.6k ops/sec) | — |
| | Equivalent for-loop (1,000 items) | 12.3 μs (81.5k ops/sec) | — |
| [**📦 Collections**](#collection-access-and-iteration) | Dict lookup by key | 22.9 ns (43.7M ops/sec) | — |
| | Set membership check | 24.9 ns (40.2M ops/sec) | — |
| | List index access | 17.5 ns (57.1M ops/sec) | — |
| | List membership check (1,000 items) | 4.03 μs (248.1k ops/sec) | — |
| | `len()` on list | 18.7 ns (53.4M ops/sec) | — |
| | Iterate 1,000-item list | 8.02 μs (124.7k ops/sec) | — |
| | Iterate 1,000-item dict | 9.02 μs (110.9k ops/sec) | — |
| | `range(1000)` iteration | {{COLLECTIONS.FOR_I_IN_RANGE_1000}} | — |
| | `sum()` of 1,000 ints | 1.83 μs (546.0k ops/sec) | — |
| [**🏷️ Attributes**](#class-and-object-attributes) | Read from regular class | 14.9 ns (67.3M ops/sec) | — |
| | Write to regular class | 15.1 ns (66.4M ops/sec) | — |
| | Read from `__slots__` class | 13.6 ns (73.6M ops/sec) | — |
| | Write to `__slots__` class | 15.2 ns (65.9M ops/sec) | — |
| | Read from `@property` | 21.6 ns (46.2M ops/sec) | — |
| | `getattr()` | 15.5 ns (64.7M ops/sec) | — |
| | `hasattr()` | 24.7 ns (40.5M ops/sec) | — |
| [**📄 JSON**](#json-and-serialization) | `json.dumps()` (simple) | 726 ns (1.4M ops/sec) | — |
| | `json.loads()` (simple) | 584 ns (1.7M ops/sec) | — |
| | `json.dumps()` (complex) | 2.57 μs (389.6k ops/sec) | — |
| | `json.loads()` (complex) | 2.33 μs (428.6k ops/sec) | — |
| | `orjson.dumps()` (complex) | 323 ns (3.1M ops/sec) | — |
| | `orjson.loads()` (complex) | 913 ns (1.1M ops/sec) | — |
| | `ujson.dumps()` (complex) | 1.60 μs (626.7k ops/sec) | — |
| | `msgspec` encode (complex) | 425 ns (2.4M ops/sec) | — |
| | Pydantic `model_dump_json()` | 1.55 μs (646.2k ops/sec) | — |
| | Pydantic `model_validate_json()` | 2.78 μs (359.7k ops/sec) | — |
| [**🌐 Web Frameworks**](#web-frameworks) | Flask (return JSON) | 19.4 μs (51.6k req/sec) | — |
| | Django (return JSON) | 22.3 μs (44.8k req/sec) | — |
| | FastAPI (return JSON) | 35.7 μs (28.0k req/sec) | — |
| | Starlette (return JSON) | 6.30 μs (158.6k req/sec) | — |
| | Litestar (return JSON) | 7.56 μs (132.3k req/sec) | — |
| [**📁 File I/O**](#file-io) | Open and close file | 9.00 μs (111.1k ops/sec) | — |
| | Read 1KB file | 10.0 μs (99.7k ops/sec) | — |
| | Write 1KB file | 29.7 μs (33.7k ops/sec) | — |
| | Write 1MB file | 640 μs (1.6k ops/sec) | — |
| | `pickle.dumps()` | 1.13 μs (888.6k ops/sec) | — |
| | `pickle.loads()` | 1.46 μs (687.1k ops/sec) | — |
| [**🗄️ Database**](#database-and-persistence) | SQLite insert (JSON blob) | 190 μs (5.3k ops/sec) | — |
| | SQLite select by PK | 3.57 μs (279.8k ops/sec) | — |
| | SQLite update one field | 5.20 μs (192.4k ops/sec) | — |
| | diskcache set | 24.5 μs (40.9k ops/sec) | — |
| | diskcache get | 4.30 μs (232.3k ops/sec) | — |
| | MongoDB insert_one | 107 μs (9.3k ops/sec) | — |
| | MongoDB find_one by _id | 115 μs (8.7k ops/sec) | — |
| | MongoDB find_one by nested field | 118 μs (8.4k ops/sec) | — |
| [**📞 Functions**](#function-and-call-overhead) | Empty function call | 22.4 ns (44.6M ops/sec) | — |
| | Function with 5 args | 26.0 ns (38.4M ops/sec) | — |
| | Method call | 23.5 ns (42.6M ops/sec) | — |
| | Lambda call | 22.1 ns (45.2M ops/sec) | — |
| | try/except (no exception) | 21.7 ns (46.2M ops/sec) | — |
| | try/except (exception raised) | 143 ns (7.0M ops/sec) | — |
| | `isinstance()` check | 18.6 ns (53.9M ops/sec) | — |
| [**⏱️ Async**](#async-overhead) | Create coroutine object | 46.2 ns (21.6M ops/sec) | — |
| | `run_until_complete(empty)` | 25.6 μs (39.1k ops/sec) | — |
| | `asyncio.sleep(0)` | 38.3 μs (26.1k ops/sec) | — |
| | `gather()` 10 coroutines | 52.9 μs (18.9k ops/sec) | — |
| | `create_task()` + await | 49.9 μs (20.1k ops/sec) | — |
| | `async with` (context manager) | 26.4 μs (37.9k ops/sec) | — |

---

## Memory Costs

Understanding how much memory different Python objects consume.

### Empty Python Process

**Result:** 15.59 MB

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
| Add two integers | 19.0 ns (52.6M ops/sec) |
| Add two floats | 19.1 ns (52.4M ops/sec) |
| Multiply two integers | 18.8 ns (53.3M ops/sec) |

---

### String Operations

| Operation | Time |
|-----------|------|
| Concatenation (`+`) | 40.3 ns (24.8M ops/sec) |
| f-string | 67.0 ns (14.9M ops/sec) |
| `.format()` | 104 ns (9.6M ops/sec) |
| `%` formatting | 83.4 ns (12.0M ops/sec) |

---

### List Operations

| Operation | Time |
|-----------|------|
| `list.append()` | 28.5 ns (35.1M ops/sec) |
| List comprehension (1,000 items) | 9.38 μs (106.6k ops/sec) |
| Equivalent for-loop (1,000 items) | 12.3 μs (81.5k ops/sec) |

---

## Collection Access and Iteration

How fast can you get data out of Python's built-in collections?

### Access by Key/Index

| Operation | Time |
|-----------|------|
| Dict lookup by key | 22.9 ns (43.7M ops/sec) |
| Set membership (`in`) | 24.9 ns (40.2M ops/sec) |
| List index access | 17.5 ns (57.1M ops/sec) |
| List membership (`in`, 1,000 items) | 4.03 μs (248.1k ops/sec) |

---

### Length

| Collection | `len()` time |
|------------|--------------|
| List (1,000 items) | 18.7 ns (53.4M ops/sec) |
| Dict (1,000 items) | 19.3 ns (51.8M ops/sec) |
| Set (1,000 items) | 19.7 ns (50.8M ops/sec) |

---

### Iteration

| Operation | Time |
|-----------|------|
| Iterate 1,000-item list | 8.02 μs (124.7k ops/sec) |
| Iterate 1,000-item dict (keys) | 9.02 μs (110.9k ops/sec) |
| Iterate `range(1000)` | {{COLLECTIONS.FOR_I_IN_RANGE_1000}} |
| `sum()` of 1,000 integers | 1.83 μs (546.0k ops/sec) |

---

## Class and Object Attributes

The cost of reading and writing attributes, and how `__slots__` changes things.

### Attribute Access

| Operation | Regular Class | `__slots__` Class |
|-----------|---------------|-------------------|
| Read attribute | 14.9 ns (67.3M ops/sec) | 13.6 ns (73.6M ops/sec) |
| Write attribute | 15.1 ns (66.4M ops/sec) | 15.2 ns (65.9M ops/sec) |

---

### Other Attribute Operations

| Operation | Time |
|-----------|------|
| Read `@property` | 21.6 ns (46.2M ops/sec) |
| `getattr(obj, 'attr')` | 15.5 ns (64.7M ops/sec) |
| `hasattr(obj, 'attr')` | 24.7 ns (40.5M ops/sec) |

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
| `json` (stdlib) | 726 ns (1.4M ops/sec) | 2.57 μs (389.6k ops/sec) |
| `orjson` | 61.0 ns (16.4M ops/sec) | 323 ns (3.1M ops/sec) |
| `ujson` | 239 ns (4.2M ops/sec) | 1.60 μs (626.7k ops/sec) |
| `msgspec` | 79.0 ns (12.7M ops/sec) | 425 ns (2.4M ops/sec) |

---

### Deserialization (loads)

| Library | Simple Object | Complex Object |
|---------|---------------|----------------|
| `json` (stdlib) | 584 ns (1.7M ops/sec) | 2.33 μs (428.6k ops/sec) |
| `orjson` | 117 ns (8.6M ops/sec) | 913 ns (1.1M ops/sec) |
| `ujson` | 283 ns (3.5M ops/sec) | 1.55 μs (644.1k ops/sec) |
| `msgspec` | 109 ns (9.2M ops/sec) | 927 ns (1.1M ops/sec) |

---

### Pydantic

| Operation | Time |
|-----------|------|
| `model_dump_json()` | 1.55 μs (646.2k ops/sec) |
| `model_validate_json()` | 2.78 μs (359.7k ops/sec) |
| `model_dump()` (to dict) | 1.72 μs (581.6k ops/sec) |
| `model_validate()` (from dict) | 2.17 μs (461.5k ops/sec) |

---

## Web Frameworks

Returning a simple JSON response. Benchmarked with `wrk` or `hey` against localhost.

### Test Setup

Each framework returns the same JSON payload from a minimal endpoint.

### Results

| Framework | Requests/sec | Latency (p50) | Latency (p99) |
|-----------|--------------|---------------|---------------|
| Flask | 19.4 μs (51.6k req/sec) | {{WEB.FLASK_LATENCY_P50}} | 7.960 ms (125.6 ops/sec) |
| Django | 22.3 μs (44.8k req/sec) | {{WEB.DJANGO_LATENCY_P50}} | 7.310 ms (136.8 ops/sec) |
| FastAPI | 35.7 μs (28.0k req/sec) | {{WEB.FASTAPI_LATENCY_P50}} | 9.270 ms (107.9 ops/sec) |
| Starlette | 6.30 μs (158.6k req/sec) | {{WEB.STARLETTE_LATENCY_P50}} | 1.440 ms (694.4 ops/sec) |
| Litestar | 7.56 μs (132.3k req/sec) | {{WEB.LITESTAR_LATENCY_P50}} | 1.980 ms (505.1 ops/sec) |

---

## File I/O

Reading and writing files of various sizes.

### Basic Operations

| Operation | Time |
|-----------|------|
| Open and close (no read) | 9.00 μs (111.1k ops/sec) |
| Read 1KB file | 10.0 μs (99.7k ops/sec) |
| Read 1MB file | 33.2 μs (30.1k ops/sec) |
| Write 1KB file | 29.7 μs (33.7k ops/sec) |
| Write 1MB file | 640 μs (1.6k ops/sec) |

---

### Pickle vs JSON to Disk

| Operation | Time |
|-----------|------|
| `pickle.dumps()` (complex obj) | 1.13 μs (888.6k ops/sec) |
| `pickle.loads()` (complex obj) | 1.46 μs (687.1k ops/sec) |
| `json.dumps()` (complex obj) | 2.69 μs (371.1k ops/sec) |
| `json.loads()` (complex obj) | 2.32 μs (430.2k ops/sec) |

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
| Insert one object | 190 μs (5.3k ops/sec) |
| Select by primary key | 3.57 μs (279.8k ops/sec) |
| Update one field | 5.20 μs (192.4k ops/sec) |
| Delete | 183 μs (5.5k ops/sec) |
| Select with `json_extract()` | 4.20 μs (237.9k ops/sec) |

---

### diskcache

| Operation | Time |
|-----------|------|
| `cache.set(key, obj)` | 24.5 μs (40.9k ops/sec) |
| `cache.get(key)` | 4.30 μs (232.3k ops/sec) |
| `cache.delete(key)` | 54.7 μs (18.3k ops/sec) |
| Check key exists | 1.90 μs (526.4k ops/sec) |

---

### MongoDB

| Operation | Time |
|-----------|------|
| `insert_one()` | 107 μs (9.3k ops/sec) |
| `find_one()` by `_id` | 115 μs (8.7k ops/sec) |
| `find_one()` by nested field | 118 μs (8.4k ops/sec) |
| `update_one()` | 106 μs (9.4k ops/sec) |
| `delete_one()` | 28.0 ns (35.7M ops/sec) |

---

### Comparison Table

| Operation | SQLite | diskcache | MongoDB |
|-----------|--------|-----------|---------|
| Write one object | 190 μs (5.3k ops/sec) | 24.5 μs (40.9k ops/sec) | 107 μs (9.3k ops/sec) |
| Read by key/id | 3.57 μs (279.8k ops/sec) | 4.30 μs (232.3k ops/sec) | 115 μs (8.7k ops/sec) |
| Read by nested field | 4.20 μs (237.9k ops/sec) | N/A | 118 μs (8.4k ops/sec) |
| Update one field | 5.20 μs (192.4k ops/sec) | 24.5 μs (40.9k ops/sec) | 106 μs (9.4k ops/sec) |
| Delete | 183 μs (5.5k ops/sec) | 54.7 μs (18.3k ops/sec) | 28.0 ns (35.7M ops/sec) |

---

## Function and Call Overhead

The hidden cost of function calls, exceptions, and async.

### Function Calls

| Operation | Time |
|-----------|------|
| Empty function call | 22.4 ns (44.6M ops/sec) |
| Function with 5 arguments | 26.0 ns (38.4M ops/sec) |
| Method call on object | 23.5 ns (42.6M ops/sec) |
| Lambda call | 22.1 ns (45.2M ops/sec) |
| Built-in function (`len()`) | 18.3 ns (54.6M ops/sec) |

---

### Exceptions

| Operation | Time |
|-----------|------|
| `try/except` (no exception raised) | 21.7 ns (46.2M ops/sec) |
| `try/except` (exception raised) | 143 ns (7.0M ops/sec) |

---

### Type Checking

| Operation | Time |
|-----------|------|
| `isinstance()` | 18.6 ns (53.9M ops/sec) |
| `type() == type` | 21.3 ns (46.9M ops/sec) |

---

## Async Overhead

The cost of async machinery.

### Coroutine Creation

| Operation | Time |
|-----------|------|
| Create coroutine object (no await) | 46.2 ns (21.6M ops/sec) |
| Create coroutine (with return value) | 48.3 ns (20.7M ops/sec) |

---

### Running Coroutines

| Operation | Time |
|-----------|------|
| `run_until_complete(empty)` | 25.6 μs (39.1k ops/sec) |
| `run_until_complete(return value)` | 25.6 μs (39.1k ops/sec) |
| Run nested await | 25.6 μs (39.1k ops/sec) |
| Run 3 sequential awaits | 25.6 μs (39.0k ops/sec) |

---

### asyncio.sleep()

| Operation | Time |
|-----------|------|
| `asyncio.sleep(0)` | 38.3 μs (26.1k ops/sec) |
| Coroutine with `sleep(0)` | 37.8 μs (26.4k ops/sec) |

---

### asyncio.gather()

| Operation | Time |
|-----------|------|
| `gather()` 5 coroutines | 46.9 μs (21.3k ops/sec) |
| `gather()` 10 coroutines | 52.9 μs (18.9k ops/sec) |
| `gather()` 100 coroutines | 151 μs (6.6k ops/sec) |

---

### Task Creation

| Operation | Time |
|-----------|------|
| `create_task()` + await | 49.9 μs (20.1k ops/sec) |
| Create 10 tasks + gather | 81.6 μs (12.2k ops/sec) |

---

### Async Context Managers & Iteration

| Operation | Time |
|-----------|------|
| `async with` (context manager) | 26.4 μs (37.9k ops/sec) |
| `async for` (5 items) | 26.9 μs (37.2k ops/sec) |
| `async for` (100 items) | 34.9 μs (28.7k ops/sec) |

---

### Sync vs Async Comparison

| Operation | Time |
|-----------|------|
| Sync function call | 20.1 ns (49.6M ops/sec) |
| Async equivalent (`run_until_complete`) | 25.6 μs (39.1k ops/sec) |

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
