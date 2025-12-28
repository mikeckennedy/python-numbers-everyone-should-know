# Python Numbers Every Programmer Should Know

*Inspired by "Latency Numbers Every Programmer Should Know" -- but for Python.*

A practical reference for understanding the cost of common Python operations. All benchmarks run on macOS-26.2-arm64-arm-64bit-Mach-O with Python 3.14.2.

---

## Quick Reference Table

| Category | Operation | Time | Memory |
|----------|-----------|------|--------|
| [**Memory**](#memory-costs) | Empty Python process | — | 27.14 MB |
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
| [**Basic Ops**](#basic-operations) | Add two integers | 20.6 ns (48.5M ops/sec) | — |
| | Add two floats | 19.1 ns (52.5M ops/sec) | — |
| | String concatenation (small) | 42.2 ns (23.7M ops/sec) | — |
| | f-string formatting | 74.2 ns (13.5M ops/sec) | — |
| | `.format()` | 103 ns (9.7M ops/sec) | — |
| | `%` formatting | 84.6 ns (11.8M ops/sec) | — |
| | List append | 31.5 ns (31.8M ops/sec) | — |
| | List comprehension (1,000 items) | 9.68 μs (103.3k ops/sec) | — |
| | Equivalent for-loop (1,000 items) | 12.2 μs (82.3k ops/sec) | — |
| [**Collections**](#collection-access-and-iteration) | Dict lookup by key | 21.7 ns (46.2M ops/sec) | — |
| | Set membership check | 18.9 ns (53.0M ops/sec) | — |
| | List index access | 18.4 ns (54.3M ops/sec) | — |
| | List membership check (1,000 items) | 4.11 μs (243.5k ops/sec) | — |
| | `len()` on list | 19.4 ns (51.5M ops/sec) | — |
| | Iterate 1,000-item list | 7.93 μs (126.1k ops/sec) | — |
| | Iterate 1,000-item dict | 8.75 μs (114.3k ops/sec) | — |
| | `range(1000)` iteration | 9.95 μs (100.5k ops/sec) | — |
| | `sum()` of 1,000 ints | 1.86 μs (538.4k ops/sec) | — |
| [**Attributes**](#class-and-object-attributes) | Read from regular class | 15.1 ns (66.4M ops/sec) | — |
| | Write to regular class | 16.8 ns (59.6M ops/sec) | — |
| | Read from `__slots__` class | 15.0 ns (66.6M ops/sec) | — |
| | Write to `__slots__` class | 16.0 ns (62.4M ops/sec) | — |
| | Read from `@property` | 22.1 ns (45.3M ops/sec) | — |
| | `getattr()` | 23.9 ns (41.9M ops/sec) | — |
| | `hasattr()` | 23.8 ns (42.0M ops/sec) | — |
| [**JSON**](#json-and-serialization) | `json.dumps()` (simple) | 717 ns (1.4M ops/sec) | — |
| | `json.loads()` (simple) | 566 ns (1.8M ops/sec) | — |
| | `json.dumps()` (complex) | 2.69 μs (372.1k ops/sec) | — |
| | `json.loads()` (complex) | 2.35 μs (425.9k ops/sec) | — |
| | `orjson.dumps()` (complex) | 320 ns (3.1M ops/sec) | — |
| | `orjson.loads()` (complex) | 958 ns (1.0M ops/sec) | — |
| | `ujson.dumps()` (complex) | 1.70 μs (588.9k ops/sec) | — |
| | `msgspec` encode (complex) | 449 ns (2.2M ops/sec) | — |
| | Pydantic `model_dump_json()` | 1.61 μs (621.4k ops/sec) | — |
| | Pydantic `model_validate_json()` | 2.75 μs (364.2k ops/sec) | — |
| [**Web Frameworks**](#web-frameworks) | Flask (return JSON) | 47.7k req/sec | — |
| | Django (return JSON) | 42.8k req/sec | — |
| | FastAPI (return JSON) | 26.9k req/sec | — |
| | Starlette (return JSON) | 157.4k req/sec | — |
| | Litestar (return JSON) | 118.8k req/sec | — |
| [**File I/O**](#file-io) | Open and close file | 8.99 μs (111.2k ops/sec) | — |
| | Read 1KB file | 9.94 μs (100.6k ops/sec) | — |
| | Write 1KB file | 30.9 μs (32.4k ops/sec) | — |
| | Write 1MB file | 488 μs (2.0k ops/sec) | — |
| | `pickle.dumps()` | 1.59 μs (628.7k ops/sec) | — |
| | `pickle.loads()` | 1.42 μs (702.6k ops/sec) | — |
| [**Database**](#database-and-persistence) | SQLite insert (JSON blob) | 164 μs (6.1k ops/sec) | — |
| | SQLite select by PK | 3.59 μs (278.6k ops/sec) | — |
| | SQLite update one field | 5.49 μs (182.0k ops/sec) | — |
| | diskcache set | 24.6 μs (40.7k ops/sec) | — |
| | diskcache get | 4.31 μs (232.2k ops/sec) | — |
| | MongoDB insert_one | 108 μs (9.3k ops/sec) | — |
| | MongoDB find_one by _id | 115 μs (8.7k ops/sec) | — |
| | MongoDB find_one by nested field | 120 μs (8.3k ops/sec) | — |
| [**Functions**](#function-and-call-overhead) | Empty function call | 20.1 ns (49.7M ops/sec) | — |
| | Function with 5 args | 25.7 ns (38.9M ops/sec) | — |
| | Method call | 24.0 ns (41.7M ops/sec) | — |
| | Lambda call | 21.0 ns (47.6M ops/sec) | — |
| | try/except (no exception) | 23.5 ns (42.5M ops/sec) | — |
| | try/except (exception raised) | 159 ns (6.3M ops/sec) | — |
| | `isinstance()` check | 19.6 ns (50.9M ops/sec) | — |
| [**Async**](#async-overhead) | `await` completed coroutine | 45.6 μs (21.9k ops/sec) | — |
| | Create coroutine object | 46.8 ns (21.4M ops/sec) | — |
| | `asyncio.sleep(0)` | 58.2 μs (17.2k ops/sec) | — |

---

## Memory Costs

Understanding how much memory different Python objects consume.

### Empty Python Process

**Result:** 27.14 MB

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
| Add two floats | 19.1 ns (52.5M ops/sec) |
| Multiply two integers | 20.1 ns (49.9M ops/sec) |

---

### String Operations

| Operation | Time |
|-----------|------|
| Concatenation (`+`) | 42.2 ns (23.7M ops/sec) |
| f-string | 74.2 ns (13.5M ops/sec) |
| `.format()` | 103 ns (9.7M ops/sec) |
| `%` formatting | 84.6 ns (11.8M ops/sec) |

---

### List Operations

| Operation | Time |
|-----------|------|
| `list.append()` | 31.5 ns (31.8M ops/sec) |
| List comprehension (1,000 items) | 9.68 μs (103.3k ops/sec) |
| Equivalent for-loop (1,000 items) | 12.2 μs (82.3k ops/sec) |

---

## Collection Access and Iteration

How fast can you get data out of Python's built-in collections?

### Access by Key/Index

| Operation | Time |
|-----------|------|
| Dict lookup by key | 21.7 ns (46.2M ops/sec) |
| Set membership (`in`) | 18.9 ns (53.0M ops/sec) |
| List index access | 18.4 ns (54.3M ops/sec) |
| List membership (`in`, 1,000 items) | 4.11 μs (243.5k ops/sec) |

---

### Length

| Collection | `len()` time |
|------------|--------------|
| List (1,000 items) | 19.4 ns (51.5M ops/sec) |
| Dict (1,000 items) | 19.7 ns (50.9M ops/sec) |
| Set (1,000 items) | 20.8 ns (48.1M ops/sec) |

---

### Iteration

| Operation | Time |
|-----------|------|
| Iterate 1,000-item list | 7.93 μs (126.1k ops/sec) |
| Iterate 1,000-item dict (keys) | 8.75 μs (114.3k ops/sec) |
| Iterate `range(1000)` | 9.95 μs (100.5k ops/sec) |
| `sum()` of 1,000 integers | 1.86 μs (538.4k ops/sec) |

---

## Class and Object Attributes

The cost of reading and writing attributes, and how `__slots__` changes things.

### Attribute Access

| Operation | Regular Class | `__slots__` Class |
|-----------|---------------|-------------------|
| Read attribute | 15.1 ns (66.4M ops/sec) | 15.0 ns (66.6M ops/sec) |
| Write attribute | 16.8 ns (59.6M ops/sec) | 16.0 ns (62.4M ops/sec) |

---

### Other Attribute Operations

| Operation | Time |
|-----------|------|
| Read `@property` | 22.1 ns (45.3M ops/sec) |
| `getattr(obj, 'attr')` | 23.9 ns (41.9M ops/sec) |
| `hasattr(obj, 'attr')` | 23.8 ns (42.0M ops/sec) |

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
| `json` (stdlib) | 717 ns (1.4M ops/sec) | 2.69 μs (372.1k ops/sec) |
| `orjson` | 63.5 ns (15.7M ops/sec) | 320 ns (3.1M ops/sec) |
| `ujson` | 253 ns (3.9M ops/sec) | 1.70 μs (588.9k ops/sec) |
| `msgspec` | 75.5 ns (13.2M ops/sec) | 449 ns (2.2M ops/sec) |

---

### Deserialization (loads)

| Library | Simple Object | Complex Object |
|---------|---------------|----------------|
| `json` (stdlib) | 566 ns (1.8M ops/sec) | 2.35 μs (425.9k ops/sec) |
| `orjson` | 113 ns (8.8M ops/sec) | 958 ns (1.0M ops/sec) |
| `ujson` | 291 ns (3.4M ops/sec) | 1.64 μs (611.6k ops/sec) |
| `msgspec` | 108 ns (9.3M ops/sec) | 957 ns (1.0M ops/sec) |

---

### Pydantic

| Operation | Time |
|-----------|------|
| `model_dump_json()` | 1.61 μs (621.4k ops/sec) |
| `model_validate_json()` | 2.75 μs (364.2k ops/sec) |
| `model_dump()` (to dict) | 1.72 μs (580.7k ops/sec) |
| `model_validate()` (from dict) | 2.19 μs (456.5k ops/sec) |

---

## Web Frameworks

Returning a simple JSON response. Benchmarked with `wrk` or `hey` against localhost.

### Test Setup

Each framework returns the same JSON payload from a minimal endpoint.

### Results

| Framework | Requests/sec | Latency (p50) | Latency (p99) |
|-----------|--------------|---------------|---------------|
| Flask | 47.7k req/sec | 2.370 ms (421.9 ops/sec) | 10.14 ms (98.6 ops/sec) |
| Django | 42.8k req/sec | 2.390 ms (418.4 ops/sec) | 6.170 ms (162.1 ops/sec) |
| FastAPI | 27.0k req/sec | 3.720 ms (268.8 ops/sec) | 8.320 ms (120.2 ops/sec) |
| Starlette | 157.4k req/sec | 634 μs (1.6k ops/sec) | 1.780 ms (561.8 ops/sec) |
| Litestar | 118.8k req/sec | 890 μs (1.1k ops/sec) | 3.180 ms (314.5 ops/sec) |

---

## File I/O

Reading and writing files of various sizes.

### Basic Operations

| Operation | Time |
|-----------|------|
| Open and close (no read) | 8.99 μs (111.2k ops/sec) |
| Read 1KB file | 9.94 μs (100.6k ops/sec) |
| Read 1MB file | 32.9 μs (30.4k ops/sec) |
| Write 1KB file | 30.9 μs (32.4k ops/sec) |
| Write 1MB file | 488 μs (2.0k ops/sec) |

---

### Pickle vs JSON to Disk

| Operation | Time |
|-----------|------|
| `pickle.dumps()` (complex obj) | 1.59 μs (628.7k ops/sec) |
| `pickle.loads()` (complex obj) | 1.42 μs (702.6k ops/sec) |
| `json.dumps()` (complex obj) | 2.64 μs (378.9k ops/sec) |
| `json.loads()` (complex obj) | 2.29 μs (437.1k ops/sec) |

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
| Insert one object | 164 μs (6.1k ops/sec) |
| Select by primary key | 3.59 μs (278.6k ops/sec) |
| Update one field | 5.49 μs (182.0k ops/sec) |
| Delete | 172 μs (5.8k ops/sec) |
| Select with `json_extract()` | 4.21 μs (237.7k ops/sec) |

---

### diskcache

| Operation | Time |
|-----------|------|
| `cache.set(key, obj)` | 24.6 μs (40.7k ops/sec) |
| `cache.get(key)` | 4.31 μs (232.2k ops/sec) |
| `cache.delete(key)` | 53.1 μs (18.8k ops/sec) |
| Check key exists | 1.95 μs (512.0k ops/sec) |

---

### MongoDB

| Operation | Time |
|-----------|------|
| `insert_one()` | 108 μs (9.3k ops/sec) |
| `find_one()` by `_id` | 115 μs (8.7k ops/sec) |
| `find_one()` by nested field | 120 μs (8.3k ops/sec) |
| `update_one()` | 106 μs (9.5k ops/sec) |
| `delete_one()` | 32.5 ns (30.8M ops/sec) |

---

### Comparison Table

| Operation | SQLite | diskcache | MongoDB |
|-----------|--------|-----------|---------|
| Write one object | 164 μs (6.1k ops/sec) | 24.6 μs (40.7k ops/sec) | 108 μs (9.3k ops/sec) |
| Read by key/id | 3.59 μs (278.6k ops/sec) | 4.31 μs (232.2k ops/sec) | 115 μs (8.7k ops/sec) |
| Read by nested field | 4.21 μs (237.7k ops/sec) | N/A | 120 μs (8.3k ops/sec) |
| Update one field | 5.49 μs (182.0k ops/sec) | 24.6 μs (40.7k ops/sec) | 106 μs (9.5k ops/sec) |
| Delete | 172 μs (5.8k ops/sec) | 53.1 μs (18.8k ops/sec) | 32.5 ns (30.8M ops/sec) |

---

## Function and Call Overhead

The hidden cost of function calls, exceptions, and async.

### Function Calls

| Operation | Time |
|-----------|------|
| Empty function call | 20.1 ns (49.7M ops/sec) |
| Function with 5 arguments | 25.7 ns (38.9M ops/sec) |
| Method call on object | 24.0 ns (41.7M ops/sec) |
| Lambda call | 21.0 ns (47.6M ops/sec) |
| Built-in function (`len()`) | 18.6 ns (53.9M ops/sec) |

---

### Exceptions

| Operation | Time |
|-----------|------|
| `try/except` (no exception raised) | 23.5 ns (42.5M ops/sec) |
| `try/except` (exception raised) | 159 ns (6.3M ops/sec) |

---

### Type Checking

| Operation | Time |
|-----------|------|
| `isinstance()` | 19.6 ns (50.9M ops/sec) |
| `type() == type` | 21.2 ns (47.1M ops/sec) |

---

## Async Overhead

The cost of async machinery.

| Operation | Time |
|-----------|------|
| `await` already-completed coroutine | 45.6 μs (21.9k ops/sec) |
| Create coroutine object (no await) | 46.8 ns (21.4M ops/sec) |
| `asyncio.sleep(0)` | 58.2 μs (17.2k ops/sec) |
| `asyncio.gather()` on 10 completed | 68.2 μs (14.7k ops/sec) |

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

*Last updated: 2025-12-27*
