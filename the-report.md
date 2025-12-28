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
| [**⚙️ Basic Ops**](#basic-operations) | Add two integers | 20.6 ns (48.5M ops/sec) | — |
| | Add two floats | 20.0 ns (50.0M ops/sec) | — |
| | String concatenation (small) | 40.0 ns (25.0M ops/sec) | — |
| | f-string formatting | 64.2 ns (15.6M ops/sec) | — |
| | `.format()` | 104 ns (9.6M ops/sec) | — |
| | `%` formatting | 82.2 ns (12.2M ops/sec) | — |
| | List append | 28.7 ns (34.8M ops/sec) | — |
| | List comprehension (1,000 items) | 9.56 μs (104.6k ops/sec) | — |
| | Equivalent for-loop (1,000 items) | 12.0 μs (83.3k ops/sec) | — |
| [**📦 Collections**](#collection-access-and-iteration) | Dict lookup by key | 23.8 ns (42.1M ops/sec) | — |
| | Set membership check | 19.9 ns (50.1M ops/sec) | — |
| | List index access | 17.7 ns (56.6M ops/sec) | — |
| | List membership check (1,000 items) | 4.09 μs (244.4k ops/sec) | — |
| | `len()` on list | 19.6 ns (51.0M ops/sec) | — |
| | Iterate 1,000-item list | 8.20 μs (122.0k ops/sec) | — |
| | Iterate 1,000-item dict | 8.97 μs (111.5k ops/sec) | — |
| | `range(1000)` iteration | {{COLLECTIONS.FOR_I_IN_RANGE_1000}} | — |
| | `sum()` of 1,000 ints | 1.84 μs (542.6k ops/sec) | — |
| [**🏷️ Attributes**](#class-and-object-attributes) | Read from regular class | 15.4 ns (65.0M ops/sec) | — |
| | Write to regular class | 16.8 ns (59.5M ops/sec) | — |
| | Read from `__slots__` class | 15.5 ns (64.6M ops/sec) | — |
| | Write to `__slots__` class | 15.5 ns (64.7M ops/sec) | — |
| | Read from `@property` | 21.0 ns (47.6M ops/sec) | — |
| | `getattr()` | 16.3 ns (61.5M ops/sec) | — |
| | `hasattr()` | 24.6 ns (40.6M ops/sec) | — |
| [**📄 JSON**](#json-and-serialization) | `json.dumps()` (simple) | 724 ns (1.4M ops/sec) | — |
| | `json.loads()` (simple) | 562 ns (1.8M ops/sec) | — |
| | `json.dumps()` (complex) | 2.78 μs (359.9k ops/sec) | — |
| | `json.loads()` (complex) | 2.29 μs (437.6k ops/sec) | — |
| | `orjson.dumps()` (complex) | 321 ns (3.1M ops/sec) | — |
| | `orjson.loads()` (complex) | 925 ns (1.1M ops/sec) | — |
| | `ujson.dumps()` (complex) | 1.70 μs (587.1k ops/sec) | — |
| | `msgspec` encode (complex) | 451 ns (2.2M ops/sec) | — |
| | Pydantic `model_dump_json()` | 1.58 μs (631.2k ops/sec) | — |
| | Pydantic `model_validate_json()` | 2.90 μs (345.0k ops/sec) | — |
| [**🌐 Web Frameworks**](#web-frameworks) | Flask (return JSON) | 19.5 μs (51.4k req/sec) | — |
| | Django (return JSON) | 21.1 μs (47.4k req/sec) | — |
| | FastAPI (return JSON) | 10.2 μs (98.4k req/sec) | — |
| | Starlette (return JSON) | 6.45 μs (155.1k req/sec) | — |
| | Litestar (return JSON) | 7.93 μs (126.1k req/sec) | — |
| [**📁 File I/O**](#file-io) | Open and close file | 9.13 μs (109.5k ops/sec) | — |
| | Read 1KB file | 10.1 μs (99.0k ops/sec) | — |
| | Write 1KB file | 29.4 μs (34.0k ops/sec) | — |
| | Write 1MB file | 646 μs (1.5k ops/sec) | — |
| | `pickle.dumps()` | 1.21 μs (824.3k ops/sec) | — |
| | `pickle.loads()` | 1.34 μs (743.7k ops/sec) | — |
| [**🗄️ Database**](#database-and-persistence) | SQLite insert (JSON blob) | 195 μs (5.1k ops/sec) | — |
| | SQLite select by PK | 3.51 μs (284.9k ops/sec) | — |
| | SQLite update one field | 5.10 μs (195.9k ops/sec) | — |
| | diskcache set | 24.8 μs (40.3k ops/sec) | — |
| | diskcache get | 4.14 μs (241.6k ops/sec) | — |
| | MongoDB insert_one | 110 μs (9.1k ops/sec) | — |
| | MongoDB find_one by _id | 116 μs (8.6k ops/sec) | — |
| | MongoDB find_one by nested field | 119 μs (8.4k ops/sec) | — |
| [**📞 Functions**](#function-and-call-overhead) | Empty function call | 22.2 ns (45.0M ops/sec) | — |
| | Function with 5 args | 26.0 ns (38.4M ops/sec) | — |
| | Method call | 23.5 ns (42.5M ops/sec) | — |
| | Lambda call | 22.3 ns (44.8M ops/sec) | — |
| | try/except (no exception) | 22.9 ns (43.7M ops/sec) | — |
| | try/except (exception raised) | 129 ns (7.7M ops/sec) | — |
| | `isinstance()` check | 18.8 ns (53.2M ops/sec) | — |
| [**⏱️ Async**](#async-overhead) | Create coroutine object | 47.9 ns (20.9M ops/sec) | — |
| | `run_until_complete(empty)` | 25.6 μs (39.0k ops/sec) | — |
| | `asyncio.sleep(0)` | 37.7 μs (26.6k ops/sec) | — |
| | `gather()` 10 coroutines | 53.4 μs (18.7k ops/sec) | — |
| | `create_task()` + await | 49.9 μs (20.0k ops/sec) | — |
| | `async with` (context manager) | 25.5 μs (39.2k ops/sec) | — |

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
| Add two integers | 20.6 ns (48.5M ops/sec) |
| Add two floats | 20.0 ns (50.0M ops/sec) |
| Multiply two integers | 20.6 ns (48.5M ops/sec) |

---

### String Operations

| Operation | Time |
|-----------|------|
| Concatenation (`+`) | 40.0 ns (25.0M ops/sec) |
| f-string | 64.2 ns (15.6M ops/sec) |
| `.format()` | 104 ns (9.6M ops/sec) |
| `%` formatting | 82.2 ns (12.2M ops/sec) |

---

### List Operations

| Operation | Time |
|-----------|------|
| `list.append()` | 28.7 ns (34.8M ops/sec) |
| List comprehension (1,000 items) | 9.56 μs (104.6k ops/sec) |
| Equivalent for-loop (1,000 items) | 12.0 μs (83.3k ops/sec) |

---

## Collection Access and Iteration

How fast can you get data out of Python's built-in collections?

### Access by Key/Index

| Operation | Time |
|-----------|------|
| Dict lookup by key | 23.8 ns (42.1M ops/sec) |
| Set membership (`in`) | 19.9 ns (50.1M ops/sec) |
| List index access | 17.7 ns (56.6M ops/sec) |
| List membership (`in`, 1,000 items) | 4.09 μs (244.4k ops/sec) |

---

### Length

| Collection | `len()` time |
|------------|--------------|
| List (1,000 items) | 19.6 ns (51.0M ops/sec) |
| Dict (1,000 items) | 19.8 ns (50.5M ops/sec) |
| Set (1,000 items) | 19.8 ns (50.6M ops/sec) |

---

### Iteration

| Operation | Time |
|-----------|------|
| Iterate 1,000-item list | 8.20 μs (122.0k ops/sec) |
| Iterate 1,000-item dict (keys) | 8.97 μs (111.5k ops/sec) |
| Iterate `range(1000)` | {{COLLECTIONS.FOR_I_IN_RANGE_1000}} |
| `sum()` of 1,000 integers | 1.84 μs (542.6k ops/sec) |

---

## Class and Object Attributes

The cost of reading and writing attributes, and how `__slots__` changes things.

### Attribute Access

| Operation | Regular Class | `__slots__` Class |
|-----------|---------------|-------------------|
| Read attribute | 15.4 ns (65.0M ops/sec) | 15.5 ns (64.6M ops/sec) |
| Write attribute | 16.8 ns (59.5M ops/sec) | 15.5 ns (64.7M ops/sec) |

---

### Other Attribute Operations

| Operation | Time |
|-----------|------|
| Read `@property` | 21.0 ns (47.6M ops/sec) |
| `getattr(obj, 'attr')` | 16.3 ns (61.5M ops/sec) |
| `hasattr(obj, 'attr')` | 24.6 ns (40.6M ops/sec) |

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
| `json` (stdlib) | 724 ns (1.4M ops/sec) | 2.78 μs (359.9k ops/sec) |
| `orjson` | 63.1 ns (15.8M ops/sec) | 321 ns (3.1M ops/sec) |
| `ujson` | 252 ns (4.0M ops/sec) | 1.70 μs (587.1k ops/sec) |
| `msgspec` | 82.5 ns (12.1M ops/sec) | 451 ns (2.2M ops/sec) |

---

### Deserialization (loads)

| Library | Simple Object | Complex Object |
|---------|---------------|----------------|
| `json` (stdlib) | 562 ns (1.8M ops/sec) | 2.29 μs (437.6k ops/sec) |
| `orjson` | 113 ns (8.9M ops/sec) | 925 ns (1.1M ops/sec) |
| `ujson` | 291 ns (3.4M ops/sec) | 1.55 μs (644.6k ops/sec) |
| `msgspec` | 108 ns (9.2M ops/sec) | 919 ns (1.1M ops/sec) |

---

### Pydantic

| Operation | Time |
|-----------|------|
| `model_dump_json()` | 1.58 μs (631.2k ops/sec) |
| `model_validate_json()` | 2.90 μs (345.0k ops/sec) |
| `model_dump()` (to dict) | 1.73 μs (578.6k ops/sec) |
| `model_validate()` (from dict) | 2.32 μs (431.6k ops/sec) |

---

## Web Frameworks

Returning a simple JSON response. Benchmarked with `wrk` or `hey` against localhost.

### Test Setup

Each framework returns the same JSON payload from a minimal endpoint.

### Results

| Framework | Requests/sec | Latency (p50) | Latency (p99) |
|-----------|--------------|---------------|---------------|
| Flask | 19.5 μs (51.4k req/sec) | {{WEB.FLASK_LATENCY_P50}} | 7.260 ms (137.7 ops/sec) |
| Django | 21.1 μs (47.4k req/sec) | {{WEB.DJANGO_LATENCY_P50}} | 64.83 ms (15.4 ops/sec) |
| FastAPI | 10.2 μs (98.4k req/sec) | {{WEB.FASTAPI_LATENCY_P50}} | 2.660 ms (375.9 ops/sec) |
| Starlette | 6.45 μs (155.1k req/sec) | {{WEB.STARLETTE_LATENCY_P50}} | 1.420 ms (704.2 ops/sec) |
| Litestar | 7.93 μs (126.1k req/sec) | {{WEB.LITESTAR_LATENCY_P50}} | 2.640 ms (378.8 ops/sec) |

---

## File I/O

Reading and writing files of various sizes.

### Basic Operations

| Operation | Time |
|-----------|------|
| Open and close (no read) | 9.13 μs (109.5k ops/sec) |
| Read 1KB file | 10.1 μs (99.0k ops/sec) |
| Read 1MB file | 35.8 μs (27.9k ops/sec) |
| Write 1KB file | 29.4 μs (34.0k ops/sec) |
| Write 1MB file | 646 μs (1.5k ops/sec) |

---

### Pickle vs JSON to Disk

| Operation | Time |
|-----------|------|
| `pickle.dumps()` (complex obj) | 1.21 μs (824.3k ops/sec) |
| `pickle.loads()` (complex obj) | 1.34 μs (743.7k ops/sec) |
| `json.dumps()` (complex obj) | 2.60 μs (384.4k ops/sec) |
| `json.loads()` (complex obj) | 2.29 μs (437.2k ops/sec) |

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
| Insert one object | 195 μs (5.1k ops/sec) |
| Select by primary key | 3.51 μs (284.9k ops/sec) |
| Update one field | 5.10 μs (195.9k ops/sec) |
| Delete | 183 μs (5.5k ops/sec) |
| Select with `json_extract()` | 4.20 μs (237.8k ops/sec) |

---

### diskcache

| Operation | Time |
|-----------|------|
| `cache.set(key, obj)` | 24.8 μs (40.3k ops/sec) |
| `cache.get(key)` | 4.14 μs (241.6k ops/sec) |
| `cache.delete(key)` | 54.6 μs (18.3k ops/sec) |
| Check key exists | 1.83 μs (545.8k ops/sec) |

---

### MongoDB

| Operation | Time |
|-----------|------|
| `insert_one()` | 110 μs (9.1k ops/sec) |
| `find_one()` by `_id` | 116 μs (8.6k ops/sec) |
| `find_one()` by nested field | 119 μs (8.4k ops/sec) |
| `update_one()` | 104 μs (9.6k ops/sec) |
| `delete_one()` | 27.5 ns (36.4M ops/sec) |

---

### Comparison Table

| Operation | SQLite | diskcache | MongoDB |
|-----------|--------|-----------|---------|
| Write one object | 195 μs (5.1k ops/sec) | 24.8 μs (40.3k ops/sec) | 110 μs (9.1k ops/sec) |
| Read by key/id | 3.51 μs (284.9k ops/sec) | 4.14 μs (241.6k ops/sec) | 116 μs (8.6k ops/sec) |
| Read by nested field | 4.20 μs (237.8k ops/sec) | N/A | 119 μs (8.4k ops/sec) |
| Update one field | 5.10 μs (195.9k ops/sec) | 24.8 μs (40.3k ops/sec) | 104 μs (9.6k ops/sec) |
| Delete | 183 μs (5.5k ops/sec) | 54.6 μs (18.3k ops/sec) | 27.5 ns (36.4M ops/sec) |

---

## Function and Call Overhead

The hidden cost of function calls, exceptions, and async.

### Function Calls

| Operation | Time |
|-----------|------|
| Empty function call | 22.2 ns (45.0M ops/sec) |
| Function with 5 arguments | 26.0 ns (38.4M ops/sec) |
| Method call on object | 23.5 ns (42.5M ops/sec) |
| Lambda call | 22.3 ns (44.8M ops/sec) |
| Built-in function (`len()`) | 20.6 ns (48.5M ops/sec) |

---

### Exceptions

| Operation | Time |
|-----------|------|
| `try/except` (no exception raised) | 22.9 ns (43.7M ops/sec) |
| `try/except` (exception raised) | 129 ns (7.7M ops/sec) |

---

### Type Checking

| Operation | Time |
|-----------|------|
| `isinstance()` | 18.8 ns (53.2M ops/sec) |
| `type() == type` | 22.1 ns (45.3M ops/sec) |

---

## Async Overhead

The cost of async machinery.

### Coroutine Creation

| Operation | Time |
|-----------|------|
| Create coroutine object (no await) | 47.9 ns (20.9M ops/sec) |
| Create coroutine (with return value) | 45.8 ns (21.8M ops/sec) |

---

### Running Coroutines

| Operation | Time |
|-----------|------|
| `run_until_complete(empty)` | 25.6 μs (39.0k ops/sec) |
| `run_until_complete(return value)` | 25.5 μs (39.2k ops/sec) |
| Run nested await | 25.5 μs (39.2k ops/sec) |
| Run 3 sequential awaits | 25.6 μs (39.1k ops/sec) |

---

### asyncio.sleep()

| Operation | Time |
|-----------|------|
| `asyncio.sleep(0)` | 37.7 μs (26.6k ops/sec) |
| Coroutine with `sleep(0)` | 39.1 μs (25.6k ops/sec) |

---

### asyncio.gather()

| Operation | Time |
|-----------|------|
| `gather()` 5 coroutines | 47.2 μs (21.2k ops/sec) |
| `gather()` 10 coroutines | 53.4 μs (18.7k ops/sec) |
| `gather()` 100 coroutines | 152 μs (6.6k ops/sec) |

---

### Task Creation

| Operation | Time |
|-----------|------|
| `create_task()` + await | 49.9 μs (20.0k ops/sec) |
| Create 10 tasks + gather | 81.8 μs (12.2k ops/sec) |

---

### Async Context Managers & Iteration

| Operation | Time |
|-----------|------|
| `async with` (context manager) | 25.5 μs (39.2k ops/sec) |
| `async for` (5 items) | 27.2 μs (36.8k ops/sec) |
| `async for` (100 items) | 35.3 μs (28.3k ops/sec) |

---

### Sync vs Async Comparison

| Operation | Time |
|-----------|------|
| Sync function call | 21.1 ns (47.4M ops/sec) |
| Async equivalent (`run_until_complete`) | 26.2 μs (38.2k ops/sec) |

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
