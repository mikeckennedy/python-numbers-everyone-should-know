# Python Numbers Everyone Should Know

*Inspired by "Latency Numbers Every Programmer Should Know" — but for Python.*

A practical reference for understanding the cost of common Python operations. All benchmarks run on [YOUR MACHINE SPECS HERE] with Python [VERSION].

---

## Quick Reference Table

| Category | Operation | Time | Memory |
|----------|-----------|------|--------|
| **Memory** | Empty Python process | ? MB | — |
| | Empty string | — | ? bytes |
| | 100-char string | — | ? bytes |
| | Small int (0-256) | — | ? bytes |
| | Large int | — | ? bytes |
| | Float | — | ? bytes |
| | Empty list | — | ? bytes |
| | List with 1000 ints | — | ? bytes |
| | Empty dict | — | ? bytes |
| | Dict with 1000 items | — | ? bytes |
| | Empty set | — | ? bytes |
| | Regular class instance (5 attrs) | — | ? bytes |
| | `__slots__` class instance (5 attrs) | — | ? bytes |
| | dataclass instance | — | ? bytes |
| | namedtuple instance | — | ? bytes |
| **Basic Ops** | Add two integers | ? ns | — |
| | Add two floats | ? ns | — |
| | String concatenation (small) | ? ns | — |
| | f-string formatting | ? ns | — |
| | `.format()` | ? ns | — |
| | `%` formatting | ? ns | — |
| | List append | ? ns | — |
| | List comprehension (1000 items) | ? μs | — |
| | Equivalent for-loop | ? μs | — |
| **Collections** | Dict lookup by key | ? ns | — |
| | Set membership check | ? ns | — |
| | List index access | ? ns | — |
| | List membership check (1000 items) | ? μs | — |
| | `len()` on list | ? ns | — |
| | Iterate 1000-item list | ? μs | — |
| | Iterate 1000-item dict | ? μs | — |
| | `range(1000)` iteration | ? μs | — |
| | `sum()` of 1000 ints | ? μs | — |
| **Attributes** | Read from regular class | ? ns | — |
| | Write to regular class | ? ns | — |
| | Read from `__slots__` class | ? ns | — |
| | Write to `__slots__` class | ? ns | — |
| | Read from `@property` | ? ns | — |
| | `getattr()` | ? ns | — |
| | `hasattr()` | ? ns | — |
| **JSON** | `json.dumps()` (simple) | ? μs | — |
| | `json.loads()` (simple) | ? μs | — |
| | `json.dumps()` (complex) | ? μs | — |
| | `json.loads()` (complex) | ? μs | — |
| | `orjson.dumps()` (complex) | ? μs | — |
| | `orjson.loads()` (complex) | ? μs | — |
| | `ujson.dumps()` (complex) | ? μs | — |
| | `msgspec` encode (complex) | ? μs | — |
| | Pydantic `model_dump_json()` | ? μs | — |
| | Pydantic `model_validate_json()` | ? μs | — |
| **Web Frameworks** | Flask (return JSON) | ? μs | — |
| | Django (return JSON) | ? μs | — |
| | FastAPI async (return JSON) | ? μs | — |
| | FastAPI sync (return JSON) | ? μs | — |
| | Starlette (return JSON) | ? μs | — |
| **File I/O** | Open and close file | ? μs | — |
| | Read 1KB file | ? μs | — |
| | Write 1KB file | ? μs | — |
| | Write 1MB file | ? ms | — |
| | `pickle.dumps()` | ? μs | — |
| | `pickle.loads()` | ? μs | — |
| **Database** | SQLite insert (JSON blob) | ? μs | — |
| | SQLite select by PK | ? μs | — |
| | SQLite update one field | ? μs | — |
| | diskcache set | ? μs | — |
| | diskcache get | ? μs | — |
| | MongoDB insert_one | ? μs | — |
| | MongoDB find_one by _id | ? μs | — |
| | MongoDB find_one by nested field | ? μs | — |
| **Functions** | Empty function call | ? ns | — |
| | Function with 5 args | ? ns | — |
| | Method call | ? ns | — |
| | Lambda call | ? ns | — |
| | try/except (no exception) | ? ns | — |
| | try/except (exception raised) | ? μs | — |
| | `isinstance()` check | ? ns | — |
| **Async** | `await` completed coroutine | ? ns | — |
| | Create coroutine object | ? ns | — |
| | `asyncio.sleep(0)` | ? μs | — |

---

## Memory Costs

Understanding how much memory different Python objects consume.

### Empty Python Process

```python
# TODO: Benchmark code
```

**Result:** ? MB

---

### Strings

```python
# TODO: Benchmark code
```

| String | Size |
|--------|------|
| Empty string `""` | ? bytes |
| 1-char string `"a"` | ? bytes |
| 100-char string | ? bytes |

---

### Numbers

```python
# TODO: Benchmark code
```

| Type | Size |
|------|------|
| Small int (0-256, cached) | ? bytes |
| Large int (1000) | ? bytes |
| Very large int (10**100) | ? bytes |
| Float | ? bytes |

---

### Collections

```python
# TODO: Benchmark code
```

| Collection | Empty | 1000 items |
|------------|-------|------------|
| List | ? bytes | ? bytes |
| Dict | ? bytes | ? bytes |
| Set | ? bytes | ? bytes |

---

### Classes and Instances

```python
# TODO: Benchmark code
```

| Type | Empty | 5 attributes |
|------|-------|--------------|
| Regular class | ? bytes | ? bytes |
| `__slots__` class | ? bytes | ? bytes |
| dataclass | ? bytes | ? bytes |
| `@dataclass(slots=True)` | ? bytes | ? bytes |
| namedtuple | — | ? bytes |

---

## Basic Operations

The cost of fundamental Python operations.

### Arithmetic

```python
# TODO: Benchmark code
```

| Operation | Time |
|-----------|------|
| Add two integers | ? ns |
| Add two floats | ? ns |
| Multiply two integers | ? ns |

---

### String Operations

```python
# TODO: Benchmark code
```

| Operation | Time |
|-----------|------|
| Concatenation (`+`) | ? ns |
| f-string | ? ns |
| `.format()` | ? ns |
| `%` formatting | ? ns |

---

### List Operations

```python
# TODO: Benchmark code
```

| Operation | Time |
|-----------|------|
| `list.append()` | ? ns |
| List comprehension (1000 items) | ? μs |
| Equivalent for-loop (1000 items) | ? μs |

---

## Collection Access and Iteration

How fast can you get data out of Python's built-in collections?

### Access by Key/Index

```python
# TODO: Benchmark code
```

| Operation | Time |
|-----------|------|
| Dict lookup by key | ? ns |
| Set membership (`in`) | ? ns |
| List index access | ? ns |
| List membership (`in`, 1000 items) | ? μs |

---

### Length

```python
# TODO: Benchmark code
```

| Collection | `len()` time |
|------------|--------------|
| List (1000 items) | ? ns |
| Dict (1000 items) | ? ns |
| Set (1000 items) | ? ns |

---

### Iteration

```python
# TODO: Benchmark code
```

| Operation | Time |
|-----------|------|
| Iterate 1000-item list | ? μs |
| Iterate 1000-item dict (keys) | ? μs |
| Iterate `range(1000)` | ? μs |
| `sum()` of 1000 integers | ? μs |

---

## Class and Object Attributes

The cost of reading and writing attributes, and how `__slots__` changes things.

### Attribute Access

```python
# TODO: Benchmark code
```

| Operation | Regular Class | `__slots__` Class |
|-----------|---------------|-------------------|
| Read attribute | ? ns | ? ns |
| Write attribute | ? ns | ? ns |

---

### Other Attribute Operations

```python
# TODO: Benchmark code
```

| Operation | Time |
|-----------|------|
| Read `@property` | ? ns |
| `getattr(obj, 'attr')` | ? ns |
| `hasattr(obj, 'attr')` | ? ns |

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

```python
# TODO: Benchmark code
```

| Library | Simple Object | Complex Object |
|---------|---------------|----------------|
| `json` (stdlib) | ? μs | ? μs |
| `orjson` | ? μs | ? μs |
| `ujson` | ? μs | ? μs |
| `msgspec` | ? μs | ? μs |

---

### Deserialization (loads)

```python
# TODO: Benchmark code
```

| Library | Simple Object | Complex Object |
|---------|---------------|----------------|
| `json` (stdlib) | ? μs | ? μs |
| `orjson` | ? μs | ? μs |
| `ujson` | ? μs | ? μs |
| `msgspec` | ? μs | ? μs |

---

### Pydantic

```python
# TODO: Benchmark code
```

| Operation | Time |
|-----------|------|
| `model_dump_json()` | ? μs |
| `model_validate_json()` | ? μs |
| `model_dump()` (to dict) | ? μs |
| `model_validate()` (from dict) | ? μs |

---

## Web Frameworks

Returning a simple JSON response. Benchmarked with `wrk` or `hey` against localhost.

### Test Setup

Each framework returns the same JSON payload from a minimal endpoint.

```python
# TODO: Endpoint code for each framework
```

### Results

```python
# TODO: Benchmark methodology
```

| Framework | Requests/sec | Latency (p50) | Latency (p99) |
|-----------|--------------|---------------|---------------|
| Flask | ? | ? μs | ? μs |
| Django | ? | ? μs | ? μs |
| FastAPI (async) | ? | ? μs | ? μs |
| FastAPI (sync) | ? | ? μs | ? μs |
| Starlette | ? | ? μs | ? μs |
| Falcon | ? | ? μs | ? μs |

---

## File I/O

Reading and writing files of various sizes.

### Basic Operations

```python
# TODO: Benchmark code
```

| Operation | Time |
|-----------|------|
| Open and close (no read) | ? μs |
| Read 1KB file | ? μs |
| Read 1MB file | ? ms |
| Write 1KB file | ? μs |
| Write 1MB file | ? ms |

---

### Pickle vs JSON to Disk

```python
# TODO: Benchmark code
```

| Operation | Time |
|-----------|------|
| `pickle.dumps()` (complex obj) | ? μs |
| `pickle.loads()` (complex obj) | ? μs |
| `json.dumps()` (complex obj) | ? μs |
| `json.loads()` (complex obj) | ? μs |

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

```python
# TODO: Benchmark code
```

| Operation | Time |
|-----------|------|
| Insert one object | ? μs |
| Select by primary key | ? μs |
| Update one field | ? μs |
| Delete | ? μs |
| Select with `json_extract()` | ? μs |

---

### diskcache

```python
# TODO: Benchmark code
```

| Operation | Time |
|-----------|------|
| `cache.set(key, obj)` | ? μs |
| `cache.get(key)` | ? μs |
| `cache.delete(key)` | ? μs |
| Check key exists | ? μs |

---

### MongoDB

```python
# TODO: Benchmark code
```

| Operation | Time |
|-----------|------|
| `insert_one()` | ? μs |
| `find_one()` by `_id` | ? μs |
| `find_one()` by nested field | ? μs |
| `update_one()` | ? μs |
| `delete_one()` | ? μs |

---

### Comparison Table

| Operation | SQLite | diskcache | MongoDB |
|-----------|--------|-----------|---------|
| Write one object | ? μs | ? μs | ? μs |
| Read by key/id | ? μs | ? μs | ? μs |
| Read by nested field | ? μs | N/A | ? μs |
| Update one field | ? μs | ? μs | ? μs |
| Delete | ? μs | ? μs | ? μs |

---

## Function and Call Overhead

The hidden cost of function calls, exceptions, and async.

### Function Calls

```python
# TODO: Benchmark code
```

| Operation | Time |
|-----------|------|
| Empty function call | ? ns |
| Function with 5 arguments | ? ns |
| Method call on object | ? ns |
| Lambda call | ? ns |
| Built-in function (`len()`) | ? ns |

---

### Exceptions

```python
# TODO: Benchmark code
```

| Operation | Time |
|-----------|------|
| `try/except` (no exception raised) | ? ns |
| `try/except` (exception raised) | ? μs |

---

### Type Checking

```python
# TODO: Benchmark code
```

| Operation | Time |
|-----------|------|
| `isinstance()` | ? ns |
| `type() == type` | ? ns |

---

## Async Overhead

The cost of async machinery.

```python
# TODO: Benchmark code
```

| Operation | Time |
|-----------|------|
| `await` already-completed coroutine | ? ns |
| Create coroutine object (no await) | ? ns |
| `asyncio.sleep(0)` | ? μs |
| `asyncio.gather()` on 10 completed | ? μs |

---

## Methodology

### Benchmarking Approach

- All benchmarks run multiple times with warmup
- Timing uses `timeit` or `perf_counter_ns` as appropriate
- Memory measured with `sys.getsizeof()` and `tracemalloc`
- Results are median of N runs

### Environment

- **OS:** [TODO]
- **Python:** [TODO]
- **CPU:** [TODO]
- **RAM:** [TODO]

### Code Repository

All benchmark code available at: [TODO: GitHub link]

---

## Key Takeaways

1. **TODO:** First insight
2. **TODO:** Second insight
3. **TODO:** Third insight

---

## Acknowledgments

Inspired by [Latency Numbers Every Programmer Should Know](https://gist.github.com/jboner/2841832) and similar resources.

---

*Last updated: [DATE]*
