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
| [**Basic Ops**](#basic-operations) | Add two integers | 20.1 ns (49.7M ops/sec) | — |
| | Add two floats | 20.3 ns (49.3M ops/sec) | — |
| | String concatenation (small) | 40.2 ns (24.9M ops/sec) | — |
| | f-string formatting | 69.8 ns (14.3M ops/sec) | — |
| | `.format()` | 105 ns (9.5M ops/sec) | — |
| | `%` formatting | 91.1 ns (11.0M ops/sec) | — |
| | List append | 30.0 ns (33.3M ops/sec) | — |
| | List comprehension (1,000 items) | 9.59 μs (104.3k ops/sec) | — |
| | Equivalent for-loop (1,000 items) | 11.9 μs (84.0k ops/sec) | — |
| [**Collections**](#collection-access-and-iteration) | Dict lookup by key | 20.2 ns (49.6M ops/sec) | — |
| | Set membership check | 19.6 ns (51.1M ops/sec) | — |
| | List index access | 18.6 ns (53.7M ops/sec) | — |
| | List membership check (1,000 items) | 4.08 μs (245.1k ops/sec) | — |
| | `len()` on list | 19.6 ns (51.0M ops/sec) | — |
| | Iterate 1,000-item list | 7.84 μs (127.6k ops/sec) | — |
| | Iterate 1,000-item dict | 9.15 μs (109.2k ops/sec) | — |
| | `range(1000)` iteration | 9.70 μs (103.1k ops/sec) | — |
| | `sum()` of 1,000 ints | 1.84 μs (544.2k ops/sec) | — |
| [**Attributes**](#class-and-object-attributes) | Read from regular class | 14.5 ns (69.0M ops/sec) | — |
| | Write to regular class | 16.3 ns (61.2M ops/sec) | — |
| | Read from `__slots__` class | 14.0 ns (71.3M ops/sec) | — |
| | Write to `__slots__` class | 15.4 ns (65.0M ops/sec) | — |
| | Read from `@property` | 21.0 ns (47.6M ops/sec) | — |
| | `getattr()` | 24.7 ns (40.4M ops/sec) | — |
| | `hasattr()` | 23.9 ns (41.8M ops/sec) | — |
| [**JSON**](#json-and-serialization) | `json.dumps()` (simple) | 732 ns (1.4M ops/sec) | — |
| | `json.loads()` (simple) | 536 ns (1.9M ops/sec) | — |
| | `json.dumps()` (complex) | 2.66 μs (375.4k ops/sec) | — |
| | `json.loads()` (complex) | 2.25 μs (444.2k ops/sec) | — |
| | `orjson.dumps()` (complex) | 321 ns (3.1M ops/sec) | — |
| | `orjson.loads()` (complex) | 923 ns (1.1M ops/sec) | — |
| | `ujson.dumps()` (complex) | 1.68 μs (594.4k ops/sec) | — |
| | `msgspec` encode (complex) | 430 ns (2.3M ops/sec) | — |
| | Pydantic `model_dump_json()` | 1.57 μs (637.5k ops/sec) | — |
| | Pydantic `model_validate_json()` | 2.85 μs (351.2k ops/sec) | — |
| [**Web Frameworks**](#web-frameworks) | Flask (return JSON) | 50.6k req/sec | — |
| | Django (return JSON) | 37.2k req/sec | — |
| | FastAPI (return JSON) | 27.8k req/sec | — |
| | Starlette (return JSON) | 160.5k req/sec | — |
| | Litestar (return JSON) | 133.0k req/sec | — |
| [**File I/O**](#file-io) | Open and close file | 9.13 μs (109.5k ops/sec) | — |
| | Read 1KB file | 9.98 μs (100.2k ops/sec) | — |
| | Write 1KB file | 30.3 μs (33.0k ops/sec) | — |
| | Write 1MB file | 450 μs (2.2k ops/sec) | — |
| | `pickle.dumps()` | 1.56 μs (639.8k ops/sec) | — |
| | `pickle.loads()` | 1.41 μs (711.2k ops/sec) | — |
| [**Database**](#database-and-persistence) | SQLite insert (JSON blob) | 165 μs (6.1k ops/sec) | — |
| | SQLite select by PK | 3.54 μs (282.7k ops/sec) | — |
| | SQLite update one field | 5.18 μs (192.9k ops/sec) | — |
| | diskcache set | 24.4 μs (41.0k ops/sec) | — |
| | diskcache get | 4.48 μs (223.2k ops/sec) | — |
| | MongoDB insert_one | 107 μs (9.3k ops/sec) | — |
| | MongoDB find_one by _id | 116 μs (8.7k ops/sec) | — |
| | MongoDB find_one by nested field | 120 μs (8.3k ops/sec) | — |
| [**Functions**](#function-and-call-overhead) | Empty function call | 18.2 ns (55.0M ops/sec) | — |
| | Function with 5 args | 24.4 ns (41.0M ops/sec) | — |
| | Method call | 22.7 ns (44.0M ops/sec) | — |
| | Lambda call | 21.4 ns (46.6M ops/sec) | — |
| | try/except (no exception) | 22.0 ns (45.5M ops/sec) | — |
| | try/except (exception raised) | 134 ns (7.5M ops/sec) | — |
| | `isinstance()` check | 19.3 ns (51.8M ops/sec) | — |
| [**Async**](#async-overhead) | `await` completed coroutine | 46.1 μs (21.7k ops/sec) | — |
| | Create coroutine object | 44.9 ns (22.3M ops/sec) | — |
| | `asyncio.sleep(0)` | 58.1 μs (17.2k ops/sec) | — |

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
| Add two integers | 20.1 ns (49.7M ops/sec) |
| Add two floats | 20.3 ns (49.3M ops/sec) |
| Multiply two integers | 20.3 ns (49.2M ops/sec) |

---

### String Operations

| Operation | Time |
|-----------|------|
| Concatenation (`+`) | 40.2 ns (24.9M ops/sec) |
| f-string | 69.8 ns (14.3M ops/sec) |
| `.format()` | 105 ns (9.5M ops/sec) |
| `%` formatting | 91.1 ns (11.0M ops/sec) |

---

### List Operations

| Operation | Time |
|-----------|------|
| `list.append()` | 30.0 ns (33.3M ops/sec) |
| List comprehension (1,000 items) | 9.59 μs (104.3k ops/sec) |
| Equivalent for-loop (1,000 items) | 11.9 μs (84.0k ops/sec) |

---

## Collection Access and Iteration

How fast can you get data out of Python's built-in collections?

### Access by Key/Index

| Operation | Time |
|-----------|------|
| Dict lookup by key | 20.2 ns (49.6M ops/sec) |
| Set membership (`in`) | 19.6 ns (51.1M ops/sec) |
| List index access | 18.6 ns (53.7M ops/sec) |
| List membership (`in`, 1,000 items) | 4.08 μs (245.1k ops/sec) |

---

### Length

| Collection | `len()` time |
|------------|--------------|
| List (1,000 items) | 19.6 ns (51.0M ops/sec) |
| Dict (1,000 items) | 19.4 ns (51.6M ops/sec) |
| Set (1,000 items) | 19.0 ns (52.6M ops/sec) |

---

### Iteration

| Operation | Time |
|-----------|------|
| Iterate 1,000-item list | 7.84 μs (127.6k ops/sec) |
| Iterate 1,000-item dict (keys) | 9.15 μs (109.2k ops/sec) |
| Iterate `range(1000)` | 9.70 μs (103.1k ops/sec) |
| `sum()` of 1,000 integers | 1.84 μs (544.2k ops/sec) |

---

## Class and Object Attributes

The cost of reading and writing attributes, and how `__slots__` changes things.

### Attribute Access

| Operation | Regular Class | `__slots__` Class |
|-----------|---------------|-------------------|
| Read attribute | 14.5 ns (69.0M ops/sec) | 14.0 ns (71.3M ops/sec) |
| Write attribute | 16.3 ns (61.2M ops/sec) | 15.4 ns (65.0M ops/sec) |

---

### Other Attribute Operations

| Operation | Time |
|-----------|------|
| Read `@property` | 21.0 ns (47.6M ops/sec) |
| `getattr(obj, 'attr')` | 24.7 ns (40.4M ops/sec) |
| `hasattr(obj, 'attr')` | 23.9 ns (41.8M ops/sec) |

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
| `json` (stdlib) | 732 ns (1.4M ops/sec) | 2.66 μs (375.4k ops/sec) |
| `orjson` | 65.0 ns (15.4M ops/sec) | 321 ns (3.1M ops/sec) |
| `ujson` | 256 ns (3.9M ops/sec) | 1.68 μs (594.4k ops/sec) |
| `msgspec` | 83.7 ns (11.9M ops/sec) | 430 ns (2.3M ops/sec) |

---

### Deserialization (loads)

| Library | Simple Object | Complex Object |
|---------|---------------|----------------|
| `json` (stdlib) | 536 ns (1.9M ops/sec) | 2.25 μs (444.2k ops/sec) |
| `orjson` | 124 ns (8.0M ops/sec) | 923 ns (1.1M ops/sec) |
| `ujson` | 293 ns (3.4M ops/sec) | 1.57 μs (635.7k ops/sec) |
| `msgspec` | 110 ns (9.1M ops/sec) | 906 ns (1.1M ops/sec) |

---

### Pydantic

| Operation | Time |
|-----------|------|
| `model_dump_json()` | 1.57 μs (637.5k ops/sec) |
| `model_validate_json()` | 2.85 μs (351.2k ops/sec) |
| `model_dump()` (to dict) | 1.73 μs (578.7k ops/sec) |
| `model_validate()` (from dict) | 2.27 μs (439.9k ops/sec) |

---

## Web Frameworks

Returning a simple JSON response. Benchmarked with `wrk` or `hey` against localhost.

### Test Setup

Each framework returns the same JSON payload from a minimal endpoint.

### Results

| Framework | Requests/sec | Latency (p50) | Latency (p99) |
|-----------|--------------|---------------|---------------|
| Flask | 50.6k req/sec | {{WEB.FLASK_LATENCY_P50}} | 7.240 ms (138.1 ops/sec) |
| Django | 37.2k req/sec | {{WEB.DJANGO_LATENCY_P50}} | 16.92 ms (59.1 ops/sec) |
| FastAPI | 27.8k req/sec | {{WEB.FASTAPI_LATENCY_P50}} | 8.030 ms (124.5 ops/sec) |
| Starlette | 160.5k req/sec | {{WEB.STARLETTE_LATENCY_P50}} | 1.630 ms (613.5 ops/sec) |
| Litestar | 133.0k req/sec | {{WEB.LITESTAR_LATENCY_P50}} | 2.370 ms (421.9 ops/sec) |

---

## File I/O

Reading and writing files of various sizes.

### Basic Operations

| Operation | Time |
|-----------|------|
| Open and close (no read) | 9.13 μs (109.5k ops/sec) |
| Read 1KB file | 9.98 μs (100.2k ops/sec) |
| Read 1MB file | 32.9 μs (30.4k ops/sec) |
| Write 1KB file | 30.3 μs (33.0k ops/sec) |
| Write 1MB file | 450 μs (2.2k ops/sec) |

---

### Pickle vs JSON to Disk

| Operation | Time |
|-----------|------|
| `pickle.dumps()` (complex obj) | 1.56 μs (639.8k ops/sec) |
| `pickle.loads()` (complex obj) | 1.41 μs (711.2k ops/sec) |
| `json.dumps()` (complex obj) | 2.72 μs (367.6k ops/sec) |
| `json.loads()` (complex obj) | 2.20 μs (455.0k ops/sec) |

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
| Insert one object | 165 μs (6.1k ops/sec) |
| Select by primary key | 3.54 μs (282.7k ops/sec) |
| Update one field | 5.18 μs (192.9k ops/sec) |
| Delete | 168 μs (5.9k ops/sec) |
| Select with `json_extract()` | 4.27 μs (234.2k ops/sec) |

---

### diskcache

| Operation | Time |
|-----------|------|
| `cache.set(key, obj)` | 24.4 μs (41.0k ops/sec) |
| `cache.get(key)` | 4.48 μs (223.2k ops/sec) |
| `cache.delete(key)` | 52.8 μs (18.9k ops/sec) |
| Check key exists | 1.92 μs (521.9k ops/sec) |

---

### MongoDB

| Operation | Time |
|-----------|------|
| `insert_one()` | 107 μs (9.3k ops/sec) |
| `find_one()` by `_id` | 116 μs (8.7k ops/sec) |
| `find_one()` by nested field | 120 μs (8.3k ops/sec) |
| `update_one()` | 103 μs (9.7k ops/sec) |
| `delete_one()` | 31.2 ns (32.0M ops/sec) |

---

### Comparison Table

| Operation | SQLite | diskcache | MongoDB |
|-----------|--------|-----------|---------|
| Write one object | 165 μs (6.1k ops/sec) | 24.4 μs (41.0k ops/sec) | 107 μs (9.3k ops/sec) |
| Read by key/id | 3.54 μs (282.7k ops/sec) | 4.48 μs (223.2k ops/sec) | 116 μs (8.7k ops/sec) |
| Read by nested field | 4.27 μs (234.2k ops/sec) | N/A | 120 μs (8.3k ops/sec) |
| Update one field | 5.18 μs (192.9k ops/sec) | 24.4 μs (41.0k ops/sec) | 103 μs (9.7k ops/sec) |
| Delete | 168 μs (5.9k ops/sec) | 52.8 μs (18.9k ops/sec) | 31.2 ns (32.0M ops/sec) |

---

## Function and Call Overhead

The hidden cost of function calls, exceptions, and async.

### Function Calls

| Operation | Time |
|-----------|------|
| Empty function call | 18.2 ns (55.0M ops/sec) |
| Function with 5 arguments | 24.4 ns (41.0M ops/sec) |
| Method call on object | 22.7 ns (44.0M ops/sec) |
| Lambda call | 21.4 ns (46.6M ops/sec) |
| Built-in function (`len()`) | 18.2 ns (54.9M ops/sec) |

---

### Exceptions

| Operation | Time |
|-----------|------|
| `try/except` (no exception raised) | 22.0 ns (45.5M ops/sec) |
| `try/except` (exception raised) | 134 ns (7.5M ops/sec) |

---

### Type Checking

| Operation | Time |
|-----------|------|
| `isinstance()` | 19.3 ns (51.8M ops/sec) |
| `type() == type` | 20.6 ns (48.6M ops/sec) |

---

## Async Overhead

The cost of async machinery.

| Operation | Time |
|-----------|------|
| `await` already-completed coroutine | 46.1 μs (21.7k ops/sec) |
| Create coroutine object (no await) | 44.9 ns (22.3M ops/sec) |
| `asyncio.sleep(0)` | 58.1 μs (17.2k ops/sec) |
| `asyncio.gather()` on 10 completed | 67.6 μs (14.8k ops/sec) |

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
