# Python Numbers Every Programmer Should Know

*Inspired by "Latency Numbers Every Programmer Should Know" -- but for Python.*

A practical reference for understanding the cost of common Python operations. All benchmarks run on macOS-26.2-arm64-arm-64bit-Mach-O with Python 3.14.2.

---

## Quick Reference Table

| Category | Operation | Time | Memory |
|----------|-----------|------|--------|
| [**💾 Memory**](#memory-costs) | Empty Python process | — | 15.73 MB |
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
| [**⚙️ Basic Ops**](#basic-operations) | Add two integers | 19.0 ns (52.7M ops/sec) | — |
| | Add two floats | 18.4 ns (54.4M ops/sec) | — |
| | String concatenation (small) | 39.1 ns (25.6M ops/sec) | — |
| | f-string formatting | 64.9 ns (15.4M ops/sec) | — |
| | `.format()` | 103 ns (9.7M ops/sec) | — |
| | `%` formatting | 89.8 ns (11.1M ops/sec) | — |
| | List append | 28.7 ns (34.8M ops/sec) | — |
| | List comprehension (1,000 items) | 9.45 μs (105.8k ops/sec) | — |
| | Equivalent for-loop (1,000 items) | 11.9 μs (83.9k ops/sec) | — |
| [**📦 Collections**](#collection-access-and-iteration) | Dict lookup by key | 21.9 ns (45.7M ops/sec) | — |
| | Set membership check | 19.0 ns (52.7M ops/sec) | — |
| | List index access | 17.6 ns (56.8M ops/sec) | — |
| | List membership check (1,000 items) | 3.85 μs (259.6k ops/sec) | — |
| | `len()` on list | 18.8 ns (53.3M ops/sec) | — |
| | Iterate 1,000-item list | 7.87 μs (127.0k ops/sec) | — |
| | Iterate 1,000-item dict | 8.74 μs (114.5k ops/sec) | — |
| | `range(1000)` iteration | {{COLLECTIONS.FOR_I_IN_RANGE_1000}} | — |
| | `sum()` of 1,000 ints | 1.87 μs (534.8k ops/sec) | — |
| [**🏷️ Attributes**](#class-and-object-attributes) | Read from regular class | 14.1 ns (70.9M ops/sec) | — |
| | Write to regular class | 15.7 ns (63.6M ops/sec) | — |
| | Read from `__slots__` class | 14.1 ns (70.7M ops/sec) | — |
| | Write to `__slots__` class | 16.4 ns (60.8M ops/sec) | — |
| | Read from `@property` | 19.0 ns (52.8M ops/sec) | — |
| | `getattr()` | 13.8 ns (72.7M ops/sec) | — |
| | `hasattr()` | 23.8 ns (41.9M ops/sec) | — |
| [**📄 JSON**](#json-and-serialization) | `json.dumps()` (simple) | 708 ns (1.4M ops/sec) | — |
| | `json.loads()` (simple) | 714 ns (1.4M ops/sec) | — |
| | `json.dumps()` (complex) | 2.65 μs (376.8k ops/sec) | — |
| | `json.loads()` (complex) | 2.22 μs (449.9k ops/sec) | — |
| | `orjson.dumps()` (complex) | 310 ns (3.2M ops/sec) | — |
| | `orjson.loads()` (complex) | 839 ns (1.2M ops/sec) | — |
| | `ujson.dumps()` (complex) | 1.64 μs (611.2k ops/sec) | — |
| | `msgspec` encode (complex) | 445 ns (2.2M ops/sec) | — |
| | Pydantic `model_dump_json()` | 1.54 μs (647.8k ops/sec) | — |
| | Pydantic `model_validate_json()` | 2.99 μs (334.7k ops/sec) | — |
| [**🌐 Web Frameworks**](#web-frameworks) | Flask (return JSON) | 16.5 μs (60.7k req/sec) | — |
| | Django (return JSON) | 18.1 μs (55.4k req/sec) | — |
| | FastAPI (return JSON) | 8.63 μs (115.9k req/sec) | — |
| | Starlette (return JSON) | 8.01 μs (124.8k req/sec) | — |
| | Litestar (return JSON) | 8.19 μs (122.1k req/sec) | — |
| [**📁 File I/O**](#file-io) | Open and close file | 9.05 μs (110.5k ops/sec) | — |
| | Read 1KB file | 10.0 μs (99.5k ops/sec) | — |
| | Write 1KB file | 35.1 μs (28.5k ops/sec) | — |
| | Write 1MB file | 207 μs (4.8k ops/sec) | — |
| | `pickle.dumps()` | 1.30 μs (769.6k ops/sec) | — |
| | `pickle.loads()` | 1.44 μs (695.2k ops/sec) | — |
| [**🗄️ Database**](#database-and-persistence) | SQLite insert (JSON blob) | 192 μs (5.2k ops/sec) | — |
| | SQLite select by PK | 3.57 μs (280.3k ops/sec) | — |
| | SQLite update one field | 5.22 μs (191.7k ops/sec) | — |
| | diskcache set | 23.9 μs (41.8k ops/sec) | — |
| | diskcache get | 4.25 μs (235.5k ops/sec) | — |
| | MongoDB insert_one | 119 μs (8.4k ops/sec) | — |
| | MongoDB find_one by _id | 121 μs (8.2k ops/sec) | — |
| | MongoDB find_one by nested field | 124 μs (8.1k ops/sec) | — |
| [**📞 Functions**](#function-and-call-overhead) | Empty function call | 22.4 ns (44.6M ops/sec) | — |
| | Function with 5 args | 24.0 ns (41.7M ops/sec) | — |
| | Method call | 23.3 ns (42.9M ops/sec) | — |
| | Lambda call | 19.7 ns (50.9M ops/sec) | — |
| | try/except (no exception) | 21.5 ns (46.5M ops/sec) | — |
| | try/except (exception raised) | 139 ns (7.2M ops/sec) | — |
| | `isinstance()` check | 18.3 ns (54.7M ops/sec) | — |
| [**⏱️ Async**](#async-overhead) | Create coroutine object | 47.0 ns (21.3M ops/sec) | — |
| | `run_until_complete(empty)` | 27.6 μs (36.2k ops/sec) | — |
| | `asyncio.sleep(0)` | 39.4 μs (25.4k ops/sec) | — |
| | `gather()` 10 coroutines | 55.0 μs (18.2k ops/sec) | — |
| | `create_task()` + await | 52.8 μs (18.9k ops/sec) | — |
| | `async with` (context manager) | 29.5 μs (33.9k ops/sec) | — |

---

## Memory Costs

Understanding how much memory different Python objects consume.

### Empty Python Process

**Result:** 15.73 MB

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
| Add two integers | 19.0 ns (52.7M ops/sec) |
| Add two floats | 18.4 ns (54.4M ops/sec) |
| Multiply two integers | 19.4 ns (51.6M ops/sec) |

---

### String Operations

| Operation | Time |
|-----------|------|
| Concatenation (`+`) | 39.1 ns (25.6M ops/sec) |
| f-string | 64.9 ns (15.4M ops/sec) |
| `.format()` | 103 ns (9.7M ops/sec) |
| `%` formatting | 89.8 ns (11.1M ops/sec) |

---

### List Operations

| Operation | Time |
|-----------|------|
| `list.append()` | 28.7 ns (34.8M ops/sec) |
| List comprehension (1,000 items) | 9.45 μs (105.8k ops/sec) |
| Equivalent for-loop (1,000 items) | 11.9 μs (83.9k ops/sec) |

---

## Collection Access and Iteration

How fast can you get data out of Python's built-in collections?

### Access by Key/Index

| Operation | Time |
|-----------|------|
| Dict lookup by key | 21.9 ns (45.7M ops/sec) |
| Set membership (`in`) | 19.0 ns (52.7M ops/sec) |
| List index access | 17.6 ns (56.8M ops/sec) |
| List membership (`in`, 1,000 items) | 3.85 μs (259.6k ops/sec) |

---

### Length

| Collection | `len()` time |
|------------|--------------|
| List (1,000 items) | 18.8 ns (53.3M ops/sec) |
| Dict (1,000 items) | 17.6 ns (56.9M ops/sec) |
| Set (1,000 items) | 18.0 ns (55.5M ops/sec) |

---

### Iteration

| Operation | Time |
|-----------|------|
| Iterate 1,000-item list | 7.87 μs (127.0k ops/sec) |
| Iterate 1,000-item dict (keys) | 8.74 μs (114.5k ops/sec) |
| Iterate `range(1000)` | {{COLLECTIONS.FOR_I_IN_RANGE_1000}} |
| `sum()` of 1,000 integers | 1.87 μs (534.8k ops/sec) |

---

## Class and Object Attributes

The cost of reading and writing attributes, and how `__slots__` changes things.

### Attribute Access

| Operation | Regular Class | `__slots__` Class |
|-----------|---------------|-------------------|
| Read attribute | 14.1 ns (70.9M ops/sec) | 14.1 ns (70.7M ops/sec) |
| Write attribute | 15.7 ns (63.6M ops/sec) | 16.4 ns (60.8M ops/sec) |

---

### Other Attribute Operations

| Operation | Time |
|-----------|------|
| Read `@property` | 19.0 ns (52.8M ops/sec) |
| `getattr(obj, 'attr')` | 13.8 ns (72.7M ops/sec) |
| `hasattr(obj, 'attr')` | 23.8 ns (41.9M ops/sec) |

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
| `json` (stdlib) | 708 ns (1.4M ops/sec) | 2.65 μs (376.8k ops/sec) |
| `orjson` | 60.9 ns (16.4M ops/sec) | 310 ns (3.2M ops/sec) |
| `ujson` | 264 ns (3.8M ops/sec) | 1.64 μs (611.2k ops/sec) |
| `msgspec` | 92.3 ns (10.8M ops/sec) | 445 ns (2.2M ops/sec) |

---

### Deserialization (loads)

| Library | Simple Object | Complex Object |
|---------|---------------|----------------|
| `json` (stdlib) | 714 ns (1.4M ops/sec) | 2.22 μs (449.9k ops/sec) |
| `orjson` | 106 ns (9.4M ops/sec) | 839 ns (1.2M ops/sec) |
| `ujson` | 268 ns (3.7M ops/sec) | 1.46 μs (682.8k ops/sec) |
| `msgspec` | 101 ns (9.9M ops/sec) | 850 ns (1.2M ops/sec) |

---

### Pydantic

| Operation | Time |
|-----------|------|
| `model_dump_json()` | 1.54 μs (647.8k ops/sec) |
| `model_validate_json()` | 2.99 μs (334.7k ops/sec) |
| `model_dump()` (to dict) | 1.71 μs (585.2k ops/sec) |
| `model_validate()` (from dict) | 2.30 μs (435.5k ops/sec) |

---

## Web Frameworks

Returning a simple JSON response. Benchmarked with `wrk` or `hey` against localhost.

### Test Setup

Each framework returns the same JSON payload from a minimal endpoint.

### Results

| Framework | Requests/sec | Latency (p99) |
|-----------|--------------|---------------|
| Flask | 16.5 μs (60.7k req/sec) | 20.85 ms (48.0 ops/sec) |
| Django | 18.1 μs (55.4k req/sec) | 170.3 ms (5.9 ops/sec) |
| FastAPI | 8.63 μs (115.9k req/sec) | 1.530 ms (653.6 ops/sec) |
| Starlette | 8.01 μs (124.8k req/sec) | 930 μs (1.1k ops/sec) |
| Litestar | 8.19 μs (122.1k req/sec) | 1.010 ms (990.1 ops/sec) |

---

## File I/O

Reading and writing files of various sizes.

### Basic Operations

| Operation | Time |
|-----------|------|
| Open and close (no read) | 9.05 μs (110.5k ops/sec) |
| Read 1KB file | 10.0 μs (99.5k ops/sec) |
| Read 1MB file | 33.6 μs (29.8k ops/sec) |
| Write 1KB file | 35.1 μs (28.5k ops/sec) |
| Write 1MB file | 207 μs (4.8k ops/sec) |

---

### Pickle vs JSON to Disk

| Operation | Time |
|-----------|------|
| `pickle.dumps()` (complex obj) | 1.30 μs (769.6k ops/sec) |
| `pickle.loads()` (complex obj) | 1.44 μs (695.2k ops/sec) |
| `json.dumps()` (complex obj) | 2.72 μs (367.1k ops/sec) |
| `json.loads()` (complex obj) | 2.35 μs (425.9k ops/sec) |

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
| Insert one object | 192 μs (5.2k ops/sec) |
| Select by primary key | 3.57 μs (280.3k ops/sec) |
| Update one field | 5.22 μs (191.7k ops/sec) |
| Delete | 191 μs (5.2k ops/sec) |
| Select with `json_extract()` | 4.27 μs (234.2k ops/sec) |

---

### diskcache

| Operation | Time |
|-----------|------|
| `cache.set(key, obj)` | 23.9 μs (41.8k ops/sec) |
| `cache.get(key)` | 4.25 μs (235.5k ops/sec) |
| `cache.delete(key)` | 51.9 μs (19.3k ops/sec) |
| Check key exists | 1.91 μs (523.2k ops/sec) |

---

### MongoDB

| Operation | Time |
|-----------|------|
| `insert_one()` | 119 μs (8.4k ops/sec) |
| `find_one()` by `_id` | 121 μs (8.2k ops/sec) |
| `find_one()` by nested field | 124 μs (8.1k ops/sec) |
| `update_one()` | 115 μs (8.7k ops/sec) |
| `delete_one()` | 30.4 ns (32.9M ops/sec) |

---

### Comparison Table

| Operation | SQLite | diskcache | MongoDB |
|-----------|--------|-----------|---------|
| Write one object | 192 μs (5.2k ops/sec) | 23.9 μs (41.8k ops/sec) | 119 μs (8.4k ops/sec) |
| Read by key/id | 3.57 μs (280.3k ops/sec) | 4.25 μs (235.5k ops/sec) | 121 μs (8.2k ops/sec) |
| Read by nested field | 4.27 μs (234.2k ops/sec) | N/A | 124 μs (8.1k ops/sec) |
| Update one field | 5.22 μs (191.7k ops/sec) | 23.9 μs (41.8k ops/sec) | 115 μs (8.7k ops/sec) |
| Delete | 191 μs (5.2k ops/sec) | 51.9 μs (19.3k ops/sec) | 30.4 ns (32.9M ops/sec) |

---

## Function and Call Overhead

The hidden cost of function calls, exceptions, and async.

### Function Calls

| Operation | Time |
|-----------|------|
| Empty function call | 22.4 ns (44.6M ops/sec) |
| Function with 5 arguments | 24.0 ns (41.7M ops/sec) |
| Method call on object | 23.3 ns (42.9M ops/sec) |
| Lambda call | 19.7 ns (50.9M ops/sec) |
| Built-in function (`len()`) | 17.1 ns (58.4M ops/sec) |

---

### Exceptions

| Operation | Time |
|-----------|------|
| `try/except` (no exception raised) | 21.5 ns (46.5M ops/sec) |
| `try/except` (exception raised) | 139 ns (7.2M ops/sec) |

---

### Type Checking

| Operation | Time |
|-----------|------|
| `isinstance()` | 18.3 ns (54.7M ops/sec) |
| `type() == type` | 21.8 ns (46.0M ops/sec) |

---

## Async Overhead

The cost of async machinery.

### Coroutine Creation

| Operation | Time |
|-----------|------|
| Create coroutine object (no await) | 47.0 ns (21.3M ops/sec) |
| Create coroutine (with return value) | 45.3 ns (22.1M ops/sec) |

---

### Running Coroutines

| Operation | Time |
|-----------|------|
| `run_until_complete(empty)` | 27.6 μs (36.2k ops/sec) |
| `run_until_complete(return value)` | 26.6 μs (37.5k ops/sec) |
| Run nested await | 28.9 μs (34.6k ops/sec) |
| Run 3 sequential awaits | 27.9 μs (35.8k ops/sec) |

---

### asyncio.sleep()

| Operation | Time |
|-----------|------|
| `asyncio.sleep(0)` | 39.4 μs (25.4k ops/sec) |
| Coroutine with `sleep(0)` | 41.8 μs (23.9k ops/sec) |

---

### asyncio.gather()

| Operation | Time |
|-----------|------|
| `gather()` 5 coroutines | 49.7 μs (20.1k ops/sec) |
| `gather()` 10 coroutines | 55.0 μs (18.2k ops/sec) |
| `gather()` 100 coroutines | 155 μs (6.5k ops/sec) |

---

### Task Creation

| Operation | Time |
|-----------|------|
| `create_task()` + await | 52.8 μs (18.9k ops/sec) |
| Create 10 tasks + gather | 85.5 μs (11.7k ops/sec) |

---

### Async Context Managers & Iteration

| Operation | Time |
|-----------|------|
| `async with` (context manager) | 29.5 μs (33.9k ops/sec) |
| `async for` (5 items) | 30.0 μs (33.3k ops/sec) |
| `async for` (100 items) | 36.4 μs (27.5k ops/sec) |

---

### Sync vs Async Comparison

| Operation | Time |
|-----------|------|
| Sync function call | 20.3 ns (49.2M ops/sec) |
| Async equivalent (`run_until_complete`) | 28.2 μs (35.5k ops/sec) |

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
- **CPU:** arm - 14 cores (14 logical)
- **RAM:** 24.0 GB

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

*Last updated: 2025-12-30*
