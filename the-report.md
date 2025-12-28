# Python Numbers Every Programmer Should Know

*Inspired by "Latency Numbers Every Programmer Should Know" -- but for Python.*

A practical reference for understanding the cost of common Python operations. All benchmarks run on macOS-26.1-arm64-arm-64bit-Mach-O with Python 3.14.2.

---

## Quick Reference Table

| Category | Operation | Time | Memory |
|----------|-----------|------|--------|
| [**💾 Memory**](#memory-costs) | Empty Python process | — | 26.81 MB |
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
| [**⚙️ Basic Ops**](#basic-operations) | Add two integers | 20.2 ns (49.5M ops/sec) | — |
| | Add two floats | 19.6 ns (50.9M ops/sec) | — |
| | String concatenation (small) | 40.0 ns (25.0M ops/sec) | — |
| | f-string formatting | 64.7 ns (15.5M ops/sec) | — |
| | `.format()` | 102 ns (9.8M ops/sec) | — |
| | `%` formatting | 82.5 ns (12.1M ops/sec) | — |
| | List append | 28.8 ns (34.7M ops/sec) | — |
| | List comprehension (1,000 items) | 9.48 μs (105.5k ops/sec) | — |
| | Equivalent for-loop (1,000 items) | 12.1 μs (82.9k ops/sec) | — |
| [**📦 Collections**](#collection-access-and-iteration) | Dict lookup by key | 19.0 ns (52.7M ops/sec) | — |
| | Set membership check | 19.1 ns (52.4M ops/sec) | — |
| | List index access | 17.9 ns (56.0M ops/sec) | — |
| | List membership check (1,000 items) | 3.92 μs (254.8k ops/sec) | — |
| | `len()` on list | 20.1 ns (49.8M ops/sec) | — |
| | Iterate 1,000-item list | 7.82 μs (127.8k ops/sec) | — |
| | Iterate 1,000-item dict | 8.68 μs (115.1k ops/sec) | — |
| | `range(1000)` iteration | 9.89 μs (101.1k ops/sec) | — |
| | `sum()` of 1,000 ints | 1.74 μs (576.4k ops/sec) | — |
| [**🏷️ Attributes**](#class-and-object-attributes) | Read from regular class | 13.6 ns (73.6M ops/sec) | — |
| | Write to regular class | 15.3 ns (65.4M ops/sec) | — |
| | Read from `__slots__` class | 14.2 ns (70.4M ops/sec) | — |
| | Write to `__slots__` class | 16.4 ns (60.8M ops/sec) | — |
| | Read from `@property` | 19.2 ns (52.2M ops/sec) | — |
| | `getattr()` | 23.6 ns (42.3M ops/sec) | — |
| | `hasattr()` | 22.7 ns (44.1M ops/sec) | — |
| [**📄 JSON**](#json-and-serialization) | `json.dumps()` (simple) | 730 ns (1.4M ops/sec) | — |
| | `json.loads()` (simple) | 554 ns (1.8M ops/sec) | — |
| | `json.dumps()` (complex) | 2.60 μs (385.2k ops/sec) | — |
| | `json.loads()` (complex) | 2.07 μs (482.5k ops/sec) | — |
| | `orjson.dumps()` (complex) | 314 ns (3.2M ops/sec) | — |
| | `orjson.loads()` (complex) | 833 ns (1.2M ops/sec) | — |
| | `ujson.dumps()` (complex) | 1.66 μs (601.6k ops/sec) | — |
| | `msgspec` encode (complex) | 414 ns (2.4M ops/sec) | — |
| | Pydantic `model_dump_json()` | 1.58 μs (634.8k ops/sec) | — |
| | Pydantic `model_validate_json()` | 2.86 μs (350.0k ops/sec) | — |
| [**🌐 Web Frameworks**](#web-frameworks) | Flask (return JSON) | 18.9 μs (52.8k req/sec) | — |
| | Django (return JSON) | 21.5 μs (46.6k req/sec) | — |
| | FastAPI (return JSON) | 35.8 μs (27.9k req/sec) | — |
| | Starlette (return JSON) | 6.48 μs (154.2k req/sec) | — |
| | Litestar (return JSON) | 8.05 μs (124.3k req/sec) | — |
| [**📁 File I/O**](#file-io) | Open and close file | 9.14 μs (109.4k ops/sec) | — |
| | Read 1KB file | 10.1 μs (99.1k ops/sec) | — |
| | Write 1KB file | 29.6 μs (33.7k ops/sec) | — |
| | Write 1MB file | 648 μs (1.5k ops/sec) | — |
| | `pickle.dumps()` | 1.52 μs (659.2k ops/sec) | — |
| | `pickle.loads()` | 1.34 μs (746.8k ops/sec) | — |
| [**🗄️ Database**](#database-and-persistence) | SQLite insert (JSON blob) | 206 μs (4.9k ops/sec) | — |
| | SQLite select by PK | 3.54 μs (282.7k ops/sec) | — |
| | SQLite update one field | 5.31 μs (188.4k ops/sec) | — |
| | diskcache set | 25.1 μs (39.9k ops/sec) | — |
| | diskcache get | 4.25 μs (235.5k ops/sec) | — |
| | MongoDB insert_one | 106 μs (9.4k ops/sec) | — |
| | MongoDB find_one by _id | 114 μs (8.8k ops/sec) | — |
| | MongoDB find_one by nested field | 119 μs (8.4k ops/sec) | — |
| [**📞 Functions**](#function-and-call-overhead) | Empty function call | 19.3 ns (51.8M ops/sec) | — |
| | Function with 5 args | 26.1 ns (38.3M ops/sec) | — |
| | Method call | 23.4 ns (42.7M ops/sec) | — |
| | Lambda call | 19.4 ns (51.7M ops/sec) | — |
| | try/except (no exception) | 20.9 ns (47.8M ops/sec) | — |
| | try/except (exception raised) | 152 ns (6.6M ops/sec) | — |
| | `isinstance()` check | 18.5 ns (54.1M ops/sec) | — |
| [**⏱️ Async**](#async-overhead) | `await` completed coroutine | 44.8 μs (22.3k ops/sec) | — |
| | Create coroutine object | 44.7 ns (22.4M ops/sec) | — |
| | `asyncio.sleep(0)` | 57.0 μs (17.6k ops/sec) | — |

---

## Memory Costs

Understanding how much memory different Python objects consume.

### Empty Python Process

**Result:** 26.81 MB

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
| Add two integers | 20.2 ns (49.5M ops/sec) |
| Add two floats | 19.6 ns (50.9M ops/sec) |
| Multiply two integers | 20.5 ns (48.7M ops/sec) |

---

### String Operations

| Operation | Time |
|-----------|------|
| Concatenation (`+`) | 40.0 ns (25.0M ops/sec) |
| f-string | 64.7 ns (15.5M ops/sec) |
| `.format()` | 102 ns (9.8M ops/sec) |
| `%` formatting | 82.5 ns (12.1M ops/sec) |

---

### List Operations

| Operation | Time |
|-----------|------|
| `list.append()` | 28.8 ns (34.7M ops/sec) |
| List comprehension (1,000 items) | 9.48 μs (105.5k ops/sec) |
| Equivalent for-loop (1,000 items) | 12.1 μs (82.9k ops/sec) |

---

## Collection Access and Iteration

How fast can you get data out of Python's built-in collections?

### Access by Key/Index

| Operation | Time |
|-----------|------|
| Dict lookup by key | 19.0 ns (52.7M ops/sec) |
| Set membership (`in`) | 19.1 ns (52.4M ops/sec) |
| List index access | 17.9 ns (56.0M ops/sec) |
| List membership (`in`, 1,000 items) | 3.92 μs (254.8k ops/sec) |

---

### Length

| Collection | `len()` time |
|------------|--------------|
| List (1,000 items) | 20.1 ns (49.8M ops/sec) |
| Dict (1,000 items) | 18.9 ns (52.8M ops/sec) |
| Set (1,000 items) | 21.8 ns (45.9M ops/sec) |

---

### Iteration

| Operation | Time |
|-----------|------|
| Iterate 1,000-item list | 7.82 μs (127.8k ops/sec) |
| Iterate 1,000-item dict (keys) | 8.68 μs (115.1k ops/sec) |
| Iterate `range(1000)` | 9.89 μs (101.1k ops/sec) |
| `sum()` of 1,000 integers | 1.74 μs (576.4k ops/sec) |

---

## Class and Object Attributes

The cost of reading and writing attributes, and how `__slots__` changes things.

### Attribute Access

| Operation | Regular Class | `__slots__` Class |
|-----------|---------------|-------------------|
| Read attribute | 13.6 ns (73.6M ops/sec) | 14.2 ns (70.4M ops/sec) |
| Write attribute | 15.3 ns (65.4M ops/sec) | 16.4 ns (60.8M ops/sec) |

---

### Other Attribute Operations

| Operation | Time |
|-----------|------|
| Read `@property` | 19.2 ns (52.2M ops/sec) |
| `getattr(obj, 'attr')` | 23.6 ns (42.3M ops/sec) |
| `hasattr(obj, 'attr')` | 22.7 ns (44.1M ops/sec) |

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
| `json` (stdlib) | 730 ns (1.4M ops/sec) | 2.60 μs (385.2k ops/sec) |
| `orjson` | 63.5 ns (15.8M ops/sec) | 314 ns (3.2M ops/sec) |
| `ujson` | 255 ns (3.9M ops/sec) | 1.66 μs (601.6k ops/sec) |
| `msgspec` | 84.8 ns (11.8M ops/sec) | 414 ns (2.4M ops/sec) |

---

### Deserialization (loads)

| Library | Simple Object | Complex Object |
|---------|---------------|----------------|
| `json` (stdlib) | 554 ns (1.8M ops/sec) | 2.07 μs (482.5k ops/sec) |
| `orjson` | 118 ns (8.4M ops/sec) | 833 ns (1.2M ops/sec) |
| `ujson` | 271 ns (3.7M ops/sec) | 1.41 μs (708.5k ops/sec) |
| `msgspec` | 98.6 ns (10.1M ops/sec) | 841 ns (1.2M ops/sec) |

---

### Pydantic

| Operation | Time |
|-----------|------|
| `model_dump_json()` | 1.58 μs (634.8k ops/sec) |
| `model_validate_json()` | 2.86 μs (350.0k ops/sec) |
| `model_dump()` (to dict) | 1.79 μs (559.8k ops/sec) |
| `model_validate()` (from dict) | 2.14 μs (466.9k ops/sec) |

---

## Web Frameworks

Returning a simple JSON response. Benchmarked with `wrk` or `hey` against localhost.

### Test Setup

Each framework returns the same JSON payload from a minimal endpoint.

### Results

| Framework | Requests/sec | Latency (p50) | Latency (p99) |
|-----------|--------------|---------------|---------------|
| Flask | 18.9 μs (52.8k req/sec) | {{WEB.FLASK_LATENCY_P50}} | 432.6 ms (2.3 ops/sec) |
| Django | 21.5 μs (46.6k req/sec) | {{WEB.DJANGO_LATENCY_P50}} | 10.10 ms (99.0 ops/sec) |
| FastAPI | 35.8 μs (27.9k req/sec) | {{WEB.FASTAPI_LATENCY_P50}} | 7.680 ms (130.2 ops/sec) |
| Starlette | 6.48 μs (154.2k req/sec) | {{WEB.STARLETTE_LATENCY_P50}} | 1.670 ms (598.8 ops/sec) |
| Litestar | 8.05 μs (124.3k req/sec) | {{WEB.LITESTAR_LATENCY_P50}} | 2.770 ms (361.0 ops/sec) |

---

## File I/O

Reading and writing files of various sizes.

### Basic Operations

| Operation | Time |
|-----------|------|
| Open and close (no read) | 9.14 μs (109.4k ops/sec) |
| Read 1KB file | 10.1 μs (99.1k ops/sec) |
| Read 1MB file | 35.2 μs (28.4k ops/sec) |
| Write 1KB file | 29.6 μs (33.7k ops/sec) |
| Write 1MB file | 648 μs (1.5k ops/sec) |

---

### Pickle vs JSON to Disk

| Operation | Time |
|-----------|------|
| `pickle.dumps()` (complex obj) | 1.52 μs (659.2k ops/sec) |
| `pickle.loads()` (complex obj) | 1.34 μs (746.8k ops/sec) |
| `json.dumps()` (complex obj) | 2.68 μs (372.9k ops/sec) |
| `json.loads()` (complex obj) | 2.23 μs (447.7k ops/sec) |

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
| Insert one object | 206 μs (4.9k ops/sec) |
| Select by primary key | 3.54 μs (282.7k ops/sec) |
| Update one field | 5.31 μs (188.4k ops/sec) |
| Delete | 183 μs (5.5k ops/sec) |
| Select with `json_extract()` | 4.18 μs (239.3k ops/sec) |

---

### diskcache

| Operation | Time |
|-----------|------|
| `cache.set(key, obj)` | 25.1 μs (39.9k ops/sec) |
| `cache.get(key)` | 4.25 μs (235.5k ops/sec) |
| `cache.delete(key)` | 55.6 μs (18.0k ops/sec) |
| Check key exists | 1.87 μs (534.3k ops/sec) |

---

### MongoDB

| Operation | Time |
|-----------|------|
| `insert_one()` | 106 μs (9.4k ops/sec) |
| `find_one()` by `_id` | 114 μs (8.8k ops/sec) |
| `find_one()` by nested field | 119 μs (8.4k ops/sec) |
| `update_one()` | 106 μs (9.4k ops/sec) |
| `delete_one()` | 30.5 ns (32.7M ops/sec) |

---

### Comparison Table

| Operation | SQLite | diskcache | MongoDB |
|-----------|--------|-----------|---------|
| Write one object | 206 μs (4.9k ops/sec) | 25.1 μs (39.9k ops/sec) | 106 μs (9.4k ops/sec) |
| Read by key/id | 3.54 μs (282.7k ops/sec) | 4.25 μs (235.5k ops/sec) | 114 μs (8.8k ops/sec) |
| Read by nested field | 4.18 μs (239.3k ops/sec) | N/A | 119 μs (8.4k ops/sec) |
| Update one field | 5.31 μs (188.4k ops/sec) | 25.1 μs (39.9k ops/sec) | 106 μs (9.4k ops/sec) |
| Delete | 183 μs (5.5k ops/sec) | 55.6 μs (18.0k ops/sec) | 30.5 ns (32.7M ops/sec) |

---

## Function and Call Overhead

The hidden cost of function calls, exceptions, and async.

### Function Calls

| Operation | Time |
|-----------|------|
| Empty function call | 19.3 ns (51.8M ops/sec) |
| Function with 5 arguments | 26.1 ns (38.3M ops/sec) |
| Method call on object | 23.4 ns (42.7M ops/sec) |
| Lambda call | 19.4 ns (51.7M ops/sec) |
| Built-in function (`len()`) | 18.3 ns (54.7M ops/sec) |

---

### Exceptions

| Operation | Time |
|-----------|------|
| `try/except` (no exception raised) | 20.9 ns (47.8M ops/sec) |
| `try/except` (exception raised) | 152 ns (6.6M ops/sec) |

---

### Type Checking

| Operation | Time |
|-----------|------|
| `isinstance()` | 18.5 ns (54.1M ops/sec) |
| `type() == type` | 21.5 ns (46.6M ops/sec) |

---

## Async Overhead

The cost of async machinery.

| Operation | Time |
|-----------|------|
| `await` already-completed coroutine | 44.8 μs (22.3k ops/sec) |
| Create coroutine object (no await) | 44.7 ns (22.4M ops/sec) |
| `asyncio.sleep(0)` | 57.0 μs (17.6k ops/sec) |
| `asyncio.gather()` on 10 completed | 67.9 μs (14.7k ops/sec) |

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

*Last updated: 2025-12-27*
