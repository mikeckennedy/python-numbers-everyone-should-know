# Python Numbers Programmer Should Know

*Inspired by "Latency Numbers Every Programmer Should Know" — but for Python.*

A practical reference for understanding the cost of common Python operations. All benchmarks run on {{METADATA.PLATFORM}} with Python {{METADATA.PYTHON_VERSION}}.

---

## Quick Reference Table

| Category | Operation | Time | Memory |
|----------|-----------|------|--------|
| **Memory** | Empty Python process | — | {{MEMORY.EMPTY_PROCESS}} |
| | Empty string | — | {{MEMORY.EMPTY_STRING}} |
| | 100-char string | — | {{MEMORY.100_CHAR_STRING}} |
| | Small int (0-256) | — | {{MEMORY.SMALL_INT}} |
| | Large int | — | {{MEMORY.LARGE_INT}} |
| | Float | — | {{MEMORY.FLOAT}} |
| | Empty list | — | {{MEMORY.EMPTY_LIST}} |
| | List with 1000 ints | — | {{MEMORY.LIST_1000_CONTAINER}} |
| | Empty dict | — | {{MEMORY.EMPTY_DICT}} |
| | Dict with 1000 items | — | {{MEMORY.DICT_1000_CONTAINER}} |
| | Empty set | — | {{MEMORY.EMPTY_SET}} |
| | Regular class instance (5 attrs) | — | {{MEMORY.REGULAR_CLASS_5ATTR}} |
| | `__slots__` class instance (5 attrs) | — | {{MEMORY.SLOTS_CLASS_5ATTR}} |
| | dataclass instance | — | {{MEMORY.DATACLASS_5ATTR}} |
| | namedtuple instance | — | {{MEMORY.NAMEDTUPLE_5ATTR}} |
| **Basic Ops** | Add two integers | {{BASIC_OPS.INT_ADD}} | — |
| | Add two floats | {{BASIC_OPS.FLOAT_ADD}} | — |
| | String concatenation (small) | {{BASIC_OPS.CONCAT_SMALL}} | — |
| | f-string formatting | {{BASIC_OPS.F_STRING}} | — |
| | `.format()` | {{BASIC_OPS.FORMAT_METHOD}} | — |
| | `%` formatting | {{BASIC_OPS.PERCENT_FORMATTING}} | — |
| | List append | {{BASIC_OPS.LIST_APPEND}} | — |
| | List comprehension (1000 items) | {{BASIC_OPS.LIST_COMP_1000}} | — |
| | Equivalent for-loop | {{BASIC_OPS.FOR_LOOP_1000}} | — |
| **Collections** | Dict lookup by key | {{COLLECTIONS.DICT_KEY_EXISTING}} | — |
| | Set membership check | {{COLLECTIONS.ITEM_IN_SET_EXISTING}} | — |
| | List index access | {{COLLECTIONS.LIST_INDEX}} | — |
| | List membership check (1000 items) | {{COLLECTIONS.ITEM_IN_LIST_LAST}} | — |
| | `len()` on list | {{COLLECTIONS.LEN_LIST_1000_ITEMS}} | — |
| | Iterate 1000-item list | {{COLLECTIONS.FOR_ITEM_IN_LIST}} | — |
| | Iterate 1000-item dict | {{COLLECTIONS.FOR_KEY_IN_DICT}} | — |
| | `range(1000)` iteration | {{COLLECTIONS.FOR_I_IN_RANGE_1000}} | — |
| | `sum()` of 1000 ints | {{COLLECTIONS.SUM_LIST}} | — |
| **Attributes** | Read from regular class | {{ATTRIBUTES.REGULAR_CLASS_READ_ATTR}} | — |
| | Write to regular class | {{ATTRIBUTES.REGULAR_CLASS_WRITE_ATTR}} | — |
| | Read from `__slots__` class | {{ATTRIBUTES.SLOTS_CLASS_READ_ATTR}} | — |
| | Write to `__slots__` class | {{ATTRIBUTES.SLOTS_CLASS_WRITE_ATTR}} | — |
| | Read from `@property` | {{ATTRIBUTES.PROPERTY_READ}} | — |
| | `getattr()` | {{ATTRIBUTES.GETATTR_OBJ_ATTR}} | — |
| | `hasattr()` | {{ATTRIBUTES.HASATTR_OBJ_EXISTING}} | — |
| **JSON** | `json.dumps()` (simple) | {{JSON.JSON_DUMPS_SIMPLE}} | — |
| | `json.loads()` (simple) | {{JSON.JSON_LOADS_SIMPLE}} | — |
| | `json.dumps()` (complex) | {{JSON.JSON_DUMPS_COMPLEX}} | — |
| | `json.loads()` (complex) | {{JSON.JSON_LOADS_COMPLEX}} | — |
| | `orjson.dumps()` (complex) | {{JSON.ORJSON_DUMPS_COMPLEX}} | — |
| | `orjson.loads()` (complex) | {{JSON.ORJSON_LOADS_COMPLEX}} | — |
| | `ujson.dumps()` (complex) | {{JSON.UJSON_DUMPS_COMPLEX}} | — |
| | `msgspec` encode (complex) | {{JSON.MSGSPEC_JSON_ENCODE_COMPLEX}} | — |
| | Pydantic `model_dump_json()` | {{JSON.MODEL_DUMP_JSON_COMPLEX}} | — |
| | Pydantic `model_validate_json()` | {{JSON.MODEL_VALIDATE_JSON_COMPLEX}} | — |
| **Web Frameworks** | Flask (return JSON) | {{WEB.FLASK_RETURN_JSON}} | — |
| | Django (return JSON) | {{WEB.DJANGO_RETURN_JSON}} | — |
| | FastAPI async (return JSON) | {{WEB.FASTAPI_ASYNC_RETURN_JSON}} | — |
| | FastAPI sync (return JSON) | {{WEB.FASTAPI_SYNC_RETURN_JSON}} | — |
| | Starlette (return JSON) | {{WEB.STARLETTE_RETURN_JSON}} | — |
| **File I/O** | Open and close file | {{FILE_IO.OPEN_CLOSE_READ_MODE}} | — |
| | Read 1KB file | {{FILE_IO.READ_1KB_FILE}} | — |
| | Write 1KB file | {{FILE_IO.WRITE_1KB_FILE}} | — |
| | Write 1MB file | {{FILE_IO.WRITE_1MB_FILE}} | — |
| | `pickle.dumps()` | {{FILE_IO.PICKLE_DUMPS}} | — |
| | `pickle.loads()` | {{FILE_IO.PICKLE_LOADS}} | — |
| **Database** | SQLite insert (JSON blob) | {{DATABASE.INSERT_JSON_BLOB}} | — |
| | SQLite select by PK | {{DATABASE.SELECT_BY_PRIMARY_KEY}} | — |
| | SQLite update one field | {{DATABASE.UPDATE_FULL_JSON}} | — |
| | diskcache set | {{DATABASE.CACHE_SET_COMPLEX_OBJ}} | — |
| | diskcache get | {{DATABASE.CACHE_GET_COMPLEX_OBJ}} | — |
| | MongoDB insert_one | {{DATABASE.INSERT_ONE}} | — |
| | MongoDB find_one by _id | {{DATABASE.FIND_ONE_BY_ID}} | — |
| | MongoDB find_one by nested field | {{DATABASE.FIND_ONE_BY_NESTED_FIELD_INDEXED}} | — |
| **Functions** | Empty function call | {{FUNCTIONS.EMPTY_FUNCTION_CALL}} | — |
| | Function with 5 args | {{FUNCTIONS.FUNCTION_WITH_5_ARGS}} | — |
| | Method call | {{FUNCTIONS.INSTANCE_METHOD_CALL}} | — |
| | Lambda call | {{FUNCTIONS.LAMBDA_CALL_NO_ARGS}} | — |
| | try/except (no exception) | {{FUNCTIONS.TRY_EXCEPT_NO_EXCEPTION_RAISED}} | — |
| | try/except (exception raised) | {{FUNCTIONS.RAISE_CATCH_VALUEERROR}} | — |
| | `isinstance()` check | {{FUNCTIONS.ISINSTANCE_EXACT_MATCH}} | — |
| **Async** | `await` completed coroutine | {{ASYNC.RUN_UNTIL_COMPLETE_EMPTY}} | — |
| | Create coroutine object | {{ASYNC.CREATE_COROUTINE_OBJECT}} | — |
| | `asyncio.sleep(0)` | {{ASYNC.ASYNCIO_SLEEP_0}} | — |

---

## Memory Costs

Understanding how much memory different Python objects consume.

### Empty Python Process

**Result:** {{MEMORY.EMPTY_PROCESS}}

---

### Strings

| String | Size |
|--------|------|
| Empty string `""` | {{MEMORY.EMPTY_STRING}} |
| 1-char string `"a"` | {{MEMORY.1_CHAR_STRING}} |
| 100-char string | {{MEMORY.100_CHAR_STRING}} |

---

### Numbers

| Type | Size |
|------|------|
| Small int (0-256, cached) | {{MEMORY.SMALL_INT}} |
| Large int (1000) | {{MEMORY.LARGE_INT}} |
| Very large int (10**100) | {{MEMORY.HUGE_INT_100}} |
| Float | {{MEMORY.FLOAT}} |

---

### Collections

| Collection | Empty | 1000 items |
|------------|-------|------------|
| List | {{MEMORY.EMPTY_LIST}} | {{MEMORY.LIST_1000_CONTAINER}} |
| Dict | {{MEMORY.EMPTY_DICT}} | {{MEMORY.DICT_1000_CONTAINER}} |
| Set | {{MEMORY.EMPTY_SET}} | {{MEMORY.SET_1000_CONTAINER}} |

---

### Classes and Instances

| Type | Empty | 5 attributes |
|------|-------|--------------|
| Regular class | {{MEMORY.REGULAR_CLASS_EMPTY}} | {{MEMORY.REGULAR_CLASS_5ATTR}} |
| `__slots__` class | {{MEMORY.SLOTS_CLASS_EMPTY}} | {{MEMORY.SLOTS_CLASS_5ATTR}} |
| dataclass | — | {{MEMORY.DATACLASS_5ATTR}} |
| `@dataclass(slots=True)` | — | {{MEMORY.SLOTS_DATACLASS_5ATTR}} |
| namedtuple | — | {{MEMORY.NAMEDTUPLE_5ATTR}} |

---

## Basic Operations

The cost of fundamental Python operations.

### Arithmetic

| Operation | Time |
|-----------|------|
| Add two integers | {{BASIC_OPS.INT_ADD}} |
| Add two floats | {{BASIC_OPS.FLOAT_ADD}} |
| Multiply two integers | {{BASIC_OPS.INT_MULTIPLY}} |

---

### String Operations

| Operation | Time |
|-----------|------|
| Concatenation (`+`) | {{BASIC_OPS.CONCAT_SMALL}} |
| f-string | {{BASIC_OPS.F_STRING}} |
| `.format()` | {{BASIC_OPS.FORMAT_METHOD}} |
| `%` formatting | {{BASIC_OPS.PERCENT_FORMATTING}} |

---

### List Operations

| Operation | Time |
|-----------|------|
| `list.append()` | {{BASIC_OPS.LIST_APPEND}} |
| List comprehension (1000 items) | {{BASIC_OPS.LIST_COMP_1000}} |
| Equivalent for-loop (1000 items) | {{BASIC_OPS.FOR_LOOP_1000}} |

---

## Collection Access and Iteration

How fast can you get data out of Python's built-in collections?

### Access by Key/Index

| Operation | Time |
|-----------|------|
| Dict lookup by key | {{COLLECTIONS.DICT_KEY_EXISTING}} |
| Set membership (`in`) | {{COLLECTIONS.ITEM_IN_SET_EXISTING}} |
| List index access | {{COLLECTIONS.LIST_INDEX}} |
| List membership (`in`, 1000 items) | {{COLLECTIONS.ITEM_IN_LIST_LAST}} |

---

### Length

| Collection | `len()` time |
|------------|--------------|
| List (1000 items) | {{COLLECTIONS.LEN_LIST_1000_ITEMS}} |
| Dict (1000 items) | {{COLLECTIONS.LEN_DICT_1000_ITEMS}} |
| Set (1000 items) | {{COLLECTIONS.LEN_SET_1000_ITEMS}} |

---

### Iteration

| Operation | Time |
|-----------|------|
| Iterate 1000-item list | {{COLLECTIONS.FOR_ITEM_IN_LIST}} |
| Iterate 1000-item dict (keys) | {{COLLECTIONS.FOR_KEY_IN_DICT}} |
| Iterate `range(1000)` | {{COLLECTIONS.FOR_I_IN_RANGE_1000}} |
| `sum()` of 1000 integers | {{COLLECTIONS.SUM_LIST}} |

---

## Class and Object Attributes

The cost of reading and writing attributes, and how `__slots__` changes things.

### Attribute Access

| Operation | Regular Class | `__slots__` Class |
|-----------|---------------|-------------------|
| Read attribute | {{ATTRIBUTES.REGULAR_CLASS_READ_ATTR}} | {{ATTRIBUTES.SLOTS_CLASS_READ_ATTR}} |
| Write attribute | {{ATTRIBUTES.REGULAR_CLASS_WRITE_ATTR}} | {{ATTRIBUTES.SLOTS_CLASS_WRITE_ATTR}} |

---

### Other Attribute Operations

| Operation | Time |
|-----------|------|
| Read `@property` | {{ATTRIBUTES.PROPERTY_READ}} |
| `getattr(obj, 'attr')` | {{ATTRIBUTES.GETATTR_OBJ_ATTR}} |
| `hasattr(obj, 'attr')` | {{ATTRIBUTES.HASATTR_OBJ_EXISTING}} |

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
| `json` (stdlib) | {{JSON.JSON_DUMPS_SIMPLE}} | {{JSON.JSON_DUMPS_COMPLEX}} |
| `orjson` | {{JSON.ORJSON_DUMPS_SIMPLE}} | {{JSON.ORJSON_DUMPS_COMPLEX}} |
| `ujson` | {{JSON.UJSON_DUMPS_SIMPLE}} | {{JSON.UJSON_DUMPS_COMPLEX}} |
| `msgspec` | {{JSON.MSGSPEC_JSON_ENCODE_SIMPLE}} | {{JSON.MSGSPEC_JSON_ENCODE_COMPLEX}} |

---

### Deserialization (loads)

| Library | Simple Object | Complex Object |
|---------|---------------|----------------|
| `json` (stdlib) | {{JSON.JSON_LOADS_SIMPLE}} | {{JSON.JSON_LOADS_COMPLEX}} |
| `orjson` | {{JSON.ORJSON_LOADS_SIMPLE}} | {{JSON.ORJSON_LOADS_COMPLEX}} |
| `ujson` | {{JSON.UJSON_LOADS_SIMPLE}} | {{JSON.UJSON_LOADS_COMPLEX}} |
| `msgspec` | {{JSON.MSGSPEC_JSON_DECODE_SIMPLE}} | {{JSON.MSGSPEC_JSON_DECODE_COMPLEX}} |

---

### Pydantic

| Operation | Time |
|-----------|------|
| `model_dump_json()` | {{JSON.MODEL_DUMP_JSON_COMPLEX}} |
| `model_validate_json()` | {{JSON.MODEL_VALIDATE_JSON_COMPLEX}} |
| `model_dump()` (to dict) | {{JSON.MODEL_DUMP_COMPLEX}} |
| `model_validate()` (from dict) | {{JSON.MODEL_VALIDATE_COMPLEX}} |

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
| Open and close (no read) | {{FILE_IO.OPEN_CLOSE_READ_MODE}} |
| Read 1KB file | {{FILE_IO.READ_1KB_FILE}} |
| Read 1MB file | {{FILE_IO.READ_1MB_FILE}} |
| Write 1KB file | {{FILE_IO.WRITE_1KB_FILE}} |
| Write 1MB file | {{FILE_IO.WRITE_1MB_FILE}} |

---

### Pickle vs JSON to Disk

| Operation | Time |
|-----------|------|
| `pickle.dumps()` (complex obj) | {{FILE_IO.PICKLE_DUMPS}} |
| `pickle.loads()` (complex obj) | {{FILE_IO.PICKLE_LOADS}} |
| `json.dumps()` (complex obj) | {{FILE_IO.JSON_DUMPS}} |
| `json.loads()` (complex obj) | {{FILE_IO.JSON_LOADS}} |

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
| Insert one object | {{DATABASE.INSERT_JSON_BLOB}} |
| Select by primary key | {{DATABASE.SELECT_BY_PRIMARY_KEY}} |
| Update one field | {{DATABASE.UPDATE_FULL_JSON}} |
| Delete | {{DATABASE.DELETE_BY_PRIMARY_KEY}} |
| Select with `json_extract()` | {{DATABASE.JSON_EXTRACT_SIMPLE_PATH}} |

---

### diskcache

| Operation | Time |
|-----------|------|
| `cache.set(key, obj)` | {{DATABASE.CACHE_SET_COMPLEX_OBJ}} |
| `cache.get(key)` | {{DATABASE.CACHE_GET_COMPLEX_OBJ}} |
| `cache.delete(key)` | {{DATABASE.CACHE_DELETE}} |
| Check key exists | {{DATABASE.KEY_IN_CACHE_HIT}} |

---

### MongoDB

| Operation | Time |
|-----------|------|
| `insert_one()` | {{DATABASE.INSERT_ONE}} |
| `find_one()` by `_id` | {{DATABASE.FIND_ONE_BY_ID}} |
| `find_one()` by nested field | {{DATABASE.FIND_ONE_BY_NESTED_FIELD_INDEXED}} |
| `update_one()` | {{DATABASE.UPDATE_ONE_BY_ID}} |
| `delete_one()` | {{DATABASE.DELETE_ONE_BY_ID}} |

---

### Comparison Table

| Operation | SQLite | diskcache | MongoDB |
|-----------|--------|-----------|---------|
| Write one object | {{DATABASE.INSERT_JSON_BLOB}} | {{DATABASE.CACHE_SET_COMPLEX_OBJ}} | {{DATABASE.INSERT_ONE}} |
| Read by key/id | {{DATABASE.SELECT_BY_PRIMARY_KEY}} | {{DATABASE.CACHE_GET_COMPLEX_OBJ}} | {{DATABASE.FIND_ONE_BY_ID}} |
| Read by nested field | {{DATABASE.JSON_EXTRACT_SIMPLE_PATH}} | N/A | {{DATABASE.FIND_ONE_BY_NESTED_FIELD_INDEXED}} |
| Update one field | {{DATABASE.UPDATE_FULL_JSON}} | {{DATABASE.CACHE_SET_COMPLEX_OBJ}} | {{DATABASE.UPDATE_ONE_BY_ID}} |
| Delete | {{DATABASE.DELETE_BY_PRIMARY_KEY}} | {{DATABASE.CACHE_DELETE}} | {{DATABASE.DELETE_ONE_BY_ID}} |

---

## Function and Call Overhead

The hidden cost of function calls, exceptions, and async.

### Function Calls

| Operation | Time |
|-----------|------|
| Empty function call | {{FUNCTIONS.EMPTY_FUNCTION_CALL}} |
| Function with 5 arguments | {{FUNCTIONS.FUNCTION_WITH_5_ARGS}} |
| Method call on object | {{FUNCTIONS.INSTANCE_METHOD_CALL}} |
| Lambda call | {{FUNCTIONS.LAMBDA_CALL_NO_ARGS}} |
| Built-in function (`len()`) | {{FUNCTIONS.LEN_ON_LIST}} |

---

### Exceptions

| Operation | Time |
|-----------|------|
| `try/except` (no exception raised) | {{FUNCTIONS.TRY_EXCEPT_NO_EXCEPTION_RAISED}} |
| `try/except` (exception raised) | {{FUNCTIONS.RAISE_CATCH_VALUEERROR}} |

---

### Type Checking

| Operation | Time |
|-----------|------|
| `isinstance()` | {{FUNCTIONS.ISINSTANCE_EXACT_MATCH}} |
| `type() == type` | {{FUNCTIONS.TYPE_X_==_CLASS}} |

---

## Async Overhead

The cost of async machinery.

| Operation | Time |
|-----------|------|
| `await` already-completed coroutine | {{ASYNC.RUN_UNTIL_COMPLETE_EMPTY}} |
| Create coroutine object (no await) | {{ASYNC.CREATE_COROUTINE_OBJECT}} |
| `asyncio.sleep(0)` | {{ASYNC.ASYNCIO_SLEEP_0}} |
| `asyncio.gather()` on 10 completed | {{ASYNC.GATHER_10_COROUTINES}} |

---

## Methodology

### Benchmarking Approach

- All benchmarks run multiple times with warmup
- Timing uses `timeit` or `perf_counter_ns` as appropriate
- Memory measured with `sys.getsizeof()` and `tracemalloc`
- Results are median of N runs

### Environment

- **OS:** {{METADATA.PLATFORM}}
- **Python:** {{METADATA.PYTHON_VERSION}} ({{METADATA.PYTHON_IMPLEMENTATION}})
- **CPU:** {{METADATA.PROCESSOR}}
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

*Last updated: {{METADATA.TIMESTAMP}}*
