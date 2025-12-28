# Python Numbers Every Programmer Should Know

*Inspired by "Latency Numbers Every Programmer Should Know" -- but for Python.*

A practical reference for understanding the cost of common Python operations. All benchmarks run on macOS-26.2-arm64-arm-64bit-Mach-O with Python 3.14.2.

---

## Quick Reference Table

| Category | Operation | Time | Memory |
|----------|-----------|------|--------|
| [**Memory**](#memory-costs) | Empty Python process | — | 26.14 MB |
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
| [**Basic Ops**](#basic-operations) | Add two integers | 19.5 ns (51.4M ops/sec) | — |
| | Add two floats | 18.9 ns (53.0M ops/sec) | — |
| | String concatenation (small) | 40.7 ns (24.6M ops/sec) | — |
| | f-string formatting | 68.0 ns (14.7M ops/sec) | — |
| | `.format()` | 102 ns (9.8M ops/sec) | — |
| | `%` formatting | 83.3 ns (12.0M ops/sec) | — |
| | List append | 31.2 ns (32.0M ops/sec) | — |
| | List comprehension (1,000 items) | 9.66 μs (103.5k ops/sec) | — |
| | Equivalent for-loop (1,000 items) | 12.2 μs (81.7k ops/sec) | — |
| [**Collections**](#collection-access-and-iteration) | Dict lookup by key | 21.5 ns (46.5M ops/sec) | — |
| | Set membership check | 20.0 ns (49.9M ops/sec) | — |
| | List index access | 18.8 ns (53.1M ops/sec) | — |
| | List membership check (1,000 items) | 4.12 μs (242.8k ops/sec) | — |
| | `len()` on list | 18.5 ns (54.2M ops/sec) | — |
| | Iterate 1,000-item list | 7.84 μs (127.6k ops/sec) | — |
| | Iterate 1,000-item dict | 8.79 μs (113.7k ops/sec) | — |
| | `range(1000)` iteration | 10.0 μs (99.6k ops/sec) | — |
| | `sum()` of 1,000 ints | 1.77 μs (565.8k ops/sec) | — |
| [**Attributes**](#class-and-object-attributes) | Read from regular class | 15.5 ns (64.5M ops/sec) | — |
| | Write to regular class | 15.9 ns (63.0M ops/sec) | — |
| | Read from `__slots__` class | 14.9 ns (67.1M ops/sec) | — |
| | Write to `__slots__` class | 15.2 ns (65.8M ops/sec) | — |
| | Read from `@property` | 21.9 ns (45.6M ops/sec) | — |
| | `getattr()` | 25.8 ns (38.8M ops/sec) | — |
| | `hasattr()` | 23.5 ns (42.6M ops/sec) | — |
| [**JSON**](#json-and-serialization) | `json.dumps()` (simple) | 733 ns (1.4M ops/sec) | — |
| | `json.loads()` (simple) | 593 ns (1.7M ops/sec) | — |
| | `json.dumps()` (complex) | 2.68 μs (373.0k ops/sec) | — |
| | `json.loads()` (complex) | 2.28 μs (439.4k ops/sec) | — |
| | `orjson.dumps()` (complex) | 317 ns (3.2M ops/sec) | — |
| | `orjson.loads()` (complex) | 906 ns (1.1M ops/sec) | — |
| | `ujson.dumps()` (complex) | 1.74 μs (574.9k ops/sec) | — |
| | `msgspec` encode (complex) | 437 ns (2.3M ops/sec) | — |
| | Pydantic `model_dump_json()` | 1.64 μs (609.0k ops/sec) | — |
| | Pydantic `model_validate_json()` | 2.94 μs (340.0k ops/sec) | — |
| [**Web Frameworks**](#web-frameworks) | Flask (return JSON) | 2.790 ms (358.4 ops/sec) | — |
| | Django (return JSON) | 3.080 ms (324.7 ops/sec) | — |
| | FastAPI (return JSON) | 6.420 ms (155.8 ops/sec) | — |
| | Starlette (return JSON) | 729 μs (1.4k ops/sec) | — |
| | Litestar (return JSON) | 845 μs (1.2k ops/sec) | — |
| [**File I/O**](#file-io) | Open and close file | 24.1 μs (41.4k ops/sec) | — |
| | Read 1KB file | 37.1 μs (27.0k ops/sec) | — |
| | Write 1KB file | 55.2 μs (18.1k ops/sec) | — |
| | Write 1MB file | 620 μs (1.6k ops/sec) | — |
| | `pickle.dumps()` | 1.23 μs (816.1k ops/sec) | — |
| | `pickle.loads()` | 1.42 μs (706.2k ops/sec) | — |
| [**Database**](#database-and-persistence) | SQLite insert (JSON blob) | 162 μs (6.2k ops/sec) | — |
| | SQLite select by PK | 3.62 μs (276.5k ops/sec) | — |
| | SQLite update one field | 5.26 μs (190.2k ops/sec) | — |
| | diskcache set | 27.0 μs (37.0k ops/sec) | — |
| | diskcache get | 4.35 μs (230.1k ops/sec) | — |
| | MongoDB insert_one | 119 μs (8.4k ops/sec) | — |
| | MongoDB find_one by _id | 121 μs (8.2k ops/sec) | — |
| | MongoDB find_one by nested field | 122 μs (8.2k ops/sec) | — |
| [**Functions**](#function-and-call-overhead) | Empty function call | 19.9 ns (50.2M ops/sec) | — |
| | Function with 5 args | 25.7 ns (39.0M ops/sec) | — |
| | Method call | 23.0 ns (43.5M ops/sec) | — |
| | Lambda call | 20.3 ns (49.3M ops/sec) | — |
| | try/except (no exception) | 23.7 ns (42.3M ops/sec) | — |
| | try/except (exception raised) | 150 ns (6.7M ops/sec) | — |
| | `isinstance()` check | 18.6 ns (53.8M ops/sec) | — |
| [**Async**](#async-overhead) | `await` completed coroutine | 45.8 μs (21.8k ops/sec) | — |
| | Create coroutine object | 46.0 ns (21.7M ops/sec) | — |
| | `asyncio.sleep(0)` | 58.9 μs (17.0k ops/sec) | — |

---

## Memory Costs

Understanding how much memory different Python objects consume.

### Empty Python Process

**Result:** 26.14 MB

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
| Add two integers | 19.5 ns (51.4M ops/sec) |
| Add two floats | 18.9 ns (53.0M ops/sec) |
| Multiply two integers | 19.8 ns (50.6M ops/sec) |

---

### String Operations

| Operation | Time |
|-----------|------|
| Concatenation (`+`) | 40.7 ns (24.6M ops/sec) |
| f-string | 68.0 ns (14.7M ops/sec) |
| `.format()` | 102 ns (9.8M ops/sec) |
| `%` formatting | 83.3 ns (12.0M ops/sec) |

---

### List Operations

| Operation | Time |
|-----------|------|
| `list.append()` | 31.2 ns (32.0M ops/sec) |
| List comprehension (1,000 items) | 9.66 μs (103.5k ops/sec) |
| Equivalent for-loop (1,000 items) | 12.2 μs (81.7k ops/sec) |

---

## Collection Access and Iteration

How fast can you get data out of Python's built-in collections?

### Access by Key/Index

| Operation | Time |
|-----------|------|
| Dict lookup by key | 21.5 ns (46.5M ops/sec) |
| Set membership (`in`) | 20.0 ns (49.9M ops/sec) |
| List index access | 18.8 ns (53.1M ops/sec) |
| List membership (`in`, 1,000 items) | 4.12 μs (242.8k ops/sec) |

---

### Length

| Collection | `len()` time |
|------------|--------------|
| List (1,000 items) | 18.5 ns (54.2M ops/sec) |
| Dict (1,000 items) | 18.6 ns (53.7M ops/sec) |
| Set (1,000 items) | 18.6 ns (53.8M ops/sec) |

---

### Iteration

| Operation | Time |
|-----------|------|
| Iterate 1,000-item list | 7.84 μs (127.6k ops/sec) |
| Iterate 1,000-item dict (keys) | 8.79 μs (113.7k ops/sec) |
| Iterate `range(1000)` | 10.0 μs (99.6k ops/sec) |
| `sum()` of 1,000 integers | 1.77 μs (565.8k ops/sec) |

---

## Class and Object Attributes

The cost of reading and writing attributes, and how `__slots__` changes things.

### Attribute Access

| Operation | Regular Class | `__slots__` Class |
|-----------|---------------|-------------------|
| Read attribute | 15.5 ns (64.5M ops/sec) | 14.9 ns (67.1M ops/sec) |
| Write attribute | 15.9 ns (63.0M ops/sec) | 15.2 ns (65.8M ops/sec) |

---

### Other Attribute Operations

| Operation | Time |
|-----------|------|
| Read `@property` | 21.9 ns (45.6M ops/sec) |
| `getattr(obj, 'attr')` | 25.8 ns (38.8M ops/sec) |
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
| `json` (stdlib) | 733 ns (1.4M ops/sec) | 2.68 μs (373.0k ops/sec) |
| `orjson` | 61.7 ns (16.2M ops/sec) | 317 ns (3.2M ops/sec) |
| `ujson` | 279 ns (3.6M ops/sec) | 1.74 μs (574.9k ops/sec) |
| `msgspec` | 77.1 ns (13.0M ops/sec) | 437 ns (2.3M ops/sec) |

---

### Deserialization (loads)

| Library | Simple Object | Complex Object |
|---------|---------------|----------------|
| `json` (stdlib) | 593 ns (1.7M ops/sec) | 2.28 μs (439.4k ops/sec) |
| `orjson` | 121 ns (8.2M ops/sec) | 906 ns (1.1M ops/sec) |
| `ujson` | 287 ns (3.5M ops/sec) | 1.51 μs (664.2k ops/sec) |
| `msgspec` | 101 ns (9.9M ops/sec) | 877 ns (1.1M ops/sec) |

---

### Pydantic

| Operation | Time |
|-----------|------|
| `model_dump_json()` | 1.64 μs (609.0k ops/sec) |
| `model_validate_json()` | 2.94 μs (340.0k ops/sec) |
| `model_dump()` (to dict) | 1.74 μs (575.9k ops/sec) |
| `model_validate()` (from dict) | 2.29 μs (436.8k ops/sec) |

---

## Web Frameworks

Returning a simple JSON response. Benchmarked with `wrk` or `hey` against localhost.

### Test Setup

Each framework returns the same JSON payload from a minimal endpoint.

### Results

| Framework | Requests/sec | Latency (p50) | Latency (p99) |
|-----------|--------------|---------------|---------------|
| Flask | 43533.72 req/sec | 2.790 ms (358.4 ops/sec) | 13.36 ms (74.9 ops/sec) |
| Django | 39609.27 req/sec | 3.080 ms (324.7 ops/sec) | 15.15 ms (66.0 ops/sec) |
| FastAPI | 18531.53 req/sec | 6.420 ms (155.8 ops/sec) | 37.51 ms (26.7 ops/sec) |
| Starlette | 145839.4 req/sec | 729 μs (1.4k ops/sec) | 2.920 ms (342.5 ops/sec) |
| Litestar | 121409.3 req/sec | 845 μs (1.2k ops/sec) | 2.680 ms (373.1 ops/sec) |

---

## File I/O

Reading and writing files of various sizes.

### Basic Operations

| Operation | Time |
|-----------|------|
| Open and close (no read) | 24.1 μs (41.4k ops/sec) |
| Read 1KB file | 37.1 μs (27.0k ops/sec) |
| Read 1MB file | 58.3 μs (17.2k ops/sec) |
| Write 1KB file | 55.2 μs (18.1k ops/sec) |
| Write 1MB file | 620 μs (1.6k ops/sec) |

---

### Pickle vs JSON to Disk

| Operation | Time |
|-----------|------|
| `pickle.dumps()` (complex obj) | 1.23 μs (816.1k ops/sec) |
| `pickle.loads()` (complex obj) | 1.42 μs (706.2k ops/sec) |
| `json.dumps()` (complex obj) | 2.76 μs (362.3k ops/sec) |
| `json.loads()` (complex obj) | 2.35 μs (425.4k ops/sec) |

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
| Insert one object | 162 μs (6.2k ops/sec) |
| Select by primary key | 3.62 μs (276.5k ops/sec) |
| Update one field | 5.26 μs (190.2k ops/sec) |
| Delete | 174 μs (5.8k ops/sec) |
| Select with `json_extract()` | 4.29 μs (232.9k ops/sec) |

---

### diskcache

| Operation | Time |
|-----------|------|
| `cache.set(key, obj)` | 27.0 μs (37.0k ops/sec) |
| `cache.get(key)` | 4.35 μs (230.1k ops/sec) |
| `cache.delete(key)` | 64.2 μs (15.6k ops/sec) |
| Check key exists | 2.03 μs (491.8k ops/sec) |

---

### MongoDB

| Operation | Time |
|-----------|------|
| `insert_one()` | 119 μs (8.4k ops/sec) |
| `find_one()` by `_id` | 121 μs (8.2k ops/sec) |
| `find_one()` by nested field | 122 μs (8.2k ops/sec) |
| `update_one()` | 111 μs (9.0k ops/sec) |
| `delete_one()` | 36.7 ns (27.3M ops/sec) |

---

### Comparison Table

| Operation | SQLite | diskcache | MongoDB |
|-----------|--------|-----------|---------|
| Write one object | 162 μs (6.2k ops/sec) | 27.0 μs (37.0k ops/sec) | 119 μs (8.4k ops/sec) |
| Read by key/id | 3.62 μs (276.5k ops/sec) | 4.35 μs (230.1k ops/sec) | 121 μs (8.2k ops/sec) |
| Read by nested field | 4.29 μs (232.9k ops/sec) | N/A | 122 μs (8.2k ops/sec) |
| Update one field | 5.26 μs (190.2k ops/sec) | 27.0 μs (37.0k ops/sec) | 111 μs (9.0k ops/sec) |
| Delete | 174 μs (5.8k ops/sec) | 64.2 μs (15.6k ops/sec) | 36.7 ns (27.3M ops/sec) |

---

## Function and Call Overhead

The hidden cost of function calls, exceptions, and async.

### Function Calls

| Operation | Time |
|-----------|------|
| Empty function call | 19.9 ns (50.2M ops/sec) |
| Function with 5 arguments | 25.7 ns (39.0M ops/sec) |
| Method call on object | 23.0 ns (43.5M ops/sec) |
| Lambda call | 20.3 ns (49.3M ops/sec) |
| Built-in function (`len()`) | 17.6 ns (56.9M ops/sec) |

---

### Exceptions

| Operation | Time |
|-----------|------|
| `try/except` (no exception raised) | 23.7 ns (42.3M ops/sec) |
| `try/except` (exception raised) | 150 ns (6.7M ops/sec) |

---

### Type Checking

| Operation | Time |
|-----------|------|
| `isinstance()` | 18.6 ns (53.8M ops/sec) |
| `type() == type` | 20.6 ns (48.6M ops/sec) |

---

## Async Overhead

The cost of async machinery.

| Operation | Time |
|-----------|------|
| `await` already-completed coroutine | 45.8 μs (21.8k ops/sec) |
| Create coroutine object (no await) | 46.0 ns (21.7M ops/sec) |
| `asyncio.sleep(0)` | 58.9 μs (17.0k ops/sec) |
| `asyncio.gather()` on 10 completed | 68.4 μs (14.6k ops/sec) |

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
