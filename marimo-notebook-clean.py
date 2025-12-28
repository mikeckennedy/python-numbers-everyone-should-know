import marimo

__generated_with = '0.18.4'
app = marimo.App(width='full')


@app.cell(hide_code=True)
def _():
    import marimo as mo

    import notebook_utils as utils

    metadata, categories = utils.load_benchmark_results()
    return categories, metadata, mo, utils


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # 🐍 Python Numbers Every Programmer Should Know
    ## Interactive Performance Benchmark Dashboard

    *Inspired by "Latency Numbers Every Programmer Should Know" -- but for Python.*

    This interactive notebook visualizes comprehensive benchmarks of common Python operations,
    helping you understand the real cost of different programming choices.
    """)
    return


@app.cell(hide_code=True)
def _(metadata, mo):
    mo.md(f"""
    ## 📊 System Information

    | Property | Value |
    |----------|-------|
    | **Python Version** | {metadata['python_version']} ({metadata['python_implementation']}) |
    | **Platform** | {metadata['platform']} |
    | **Processor** | {metadata['processor']} |
    | **CPU Cores** | {metadata['cpu_cores_physical']} physical / {metadata['cpu_cores_logical']} logical |
    | **RAM** | {metadata['ram_gb']} GB |
    | **Timestamp** | {metadata['timestamp'][:10]} |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 💾 Memory Costs

    Understanding how much memory different Python objects consume.
    """)
    return


@app.cell(hide_code=True)
def _(categories, mo):
    memory_results = categories['memory']['results']
    empty_process = next(r for r in memory_results if r['name'] == 'empty_process')

    mo.callout(
        mo.md(f"""
        ### Empty Python Process Baseline
        **{empty_process['value']:.2f} MB** - This is the memory cost just to start Python!
        """),
        kind='info',
    )
    return (memory_results,)


@app.cell(hide_code=True)
def _(memory_results, utils):
    utils.create_string_memory_chart(memory_results)
    return


@app.cell(hide_code=True)
def _(memory_results, utils):
    utils.create_individual_numbers_chart(memory_results)
    return


@app.cell(hide_code=True)
def _(memory_results, utils):
    utils.create_number_lists_chart(memory_results)
    return


@app.cell(hide_code=True)
def _(memory_results, utils):
    utils.create_empty_collections_chart(memory_results)
    return


@app.cell(hide_code=True)
def _(memory_results, utils):
    utils.create_collection_growth_chart(memory_results)
    return


@app.cell(hide_code=True)
def _(memory_results, utils):
    utils.create_class_memory_chart(memory_results)
    return


@app.cell(hide_code=True)
def _(memory_results, mo, utils):
    fig_agg_class, savings_pct_agg, savings_kb_agg = utils.create_aggregate_class_memory_chart(memory_results)

    mo.vstack(
        [
            fig_agg_class,
            mo.callout(
                mo.md(f"""
            **__slots__ Memory Savings:** {savings_pct_agg:.1f}% less memory 
            ({savings_kb_agg:.1f} KB saved for 1,000 instances)
            """),
                kind='success',
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## ⚡ Basic Operations

    The cost of fundamental Python operations.
    """)
    return


@app.cell(hide_code=True)
def _(categories, utils):
    basic_results = categories['basic_ops']['results']
    utils.create_arithmetic_chart(basic_results)
    return (basic_results,)


@app.cell(hide_code=True)
def _(basic_results, utils):
    utils.create_string_operations_chart(basic_results)
    return


@app.cell(hide_code=True)
def _(basic_results, utils):
    utils.create_list_comp_vs_loop_chart(basic_results)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 📦 Collection Access and Iteration

    How fast can you get data out of Python's built-in collections?
    """)
    return


@app.cell(hide_code=True)
def _(categories, utils):
    coll_results = categories['collections']['results']
    utils.create_collection_access_chart(coll_results)
    return (coll_results,)


@app.cell(hide_code=True)
def _(coll_results, utils):
    utils.create_collection_iteration_chart(coll_results)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Key Takeaway: Use dict/set for membership checks!

    Dictionary and set lookups are O(1) - extremely fast.
    List membership checks are O(n) - slow for large lists.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 🏷️ Class and Object Attributes

    The cost of reading and writing attributes, and how `__slots__` changes things.
    """)
    return


@app.cell(hide_code=True)
def _(categories, utils):
    attr_results = categories['attributes']['results']
    utils.create_attribute_access_chart(attr_results)
    return (attr_results,)


@app.cell(hide_code=True)
def _(attr_results, utils):
    utils.create_other_attribute_ops_chart(attr_results)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md("""
        **Performance Insight:** `__slots__` provides minimal speed improvement (~3-5%) but significant memory savings.
        The real benefit is in memory usage when you have many instances.
        """),
        kind='info',
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 🔄 JSON and Serialization

    Comparing standard library JSON with optimized alternatives.
    """)
    return


@app.cell(hide_code=True)
def _(categories, mo, utils):
    json_results = categories['json']['results']
    fig_ser, ser_df = utils.create_json_serialization_chart(json_results)

    orjson_speedup = ser_df[ser_df['Library'] == 'orjson']['Speedup'].iloc[0]
    msgspec_speedup = ser_df[ser_df['Library'] == 'msgspec']['Speedup'].iloc[0]

    mo.vstack(
        [
            fig_ser,
            mo.callout(
                mo.md(
                    f"""
                **Performance Gains:** orjson is {orjson_speedup:.1f}x faster, 
                msgspec is {msgspec_speedup:.1f}x faster than stdlib json
                """
                ),
                kind='success',
            ),
        ]
    )
    return (json_results,)


@app.cell(hide_code=True)
def _(json_results, mo, utils):
    fig_deser, deser_df = utils.create_json_deserialization_chart(json_results)

    orjson_speedup_deser = deser_df[deser_df['Library'] == 'orjson']['Speedup'].iloc[0]
    msgspec_speedup_deser = deser_df[deser_df['Library'] == 'msgspec']['Speedup'].iloc[0]

    mo.vstack(
        [
            fig_deser,
            mo.callout(
                mo.md(
                    f"""
                **Deserialization:** orjson is {orjson_speedup_deser:.1f}x faster, 
                msgspec is {msgspec_speedup_deser:.1f}x faster
                """
                ),
                kind='success',
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(json_results, mo, utils):
    fig_pydantic = utils.create_pydantic_comparison_chart(json_results)
    if fig_pydantic:
        mo.vstack(
            [
                fig_pydantic,
                mo.callout(
                    mo.md("""
                **Pydantic Performance:** Model validation adds overhead but provides type safety and data validation.
                Use `model_dump_json()` for the fastest JSON serialization from Pydantic models.
                """),
                    kind='info',
                ),
            ]
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 🌐 Web Frameworks

    Comparing request handling performance across popular Python web frameworks.
    """)
    return


@app.cell(hide_code=True)
def _(categories, mo, utils):
    web_results = categories['web']['results']
    if web_results:
        throughput_result = utils.create_web_framework_throughput_chart(web_results)
        latency_result = utils.create_web_framework_latency_chart(web_results)

        if throughput_result and latency_result:
            fig_throughput, throughput_df = throughput_result
            fig_latency, latency_df = latency_result

            fastest_throughput = throughput_df.iloc[-1]['Framework']
            slowest_throughput = throughput_df.iloc[0]['Framework']
            fastest_latency = latency_df.iloc[-1]['Framework']

            web_output = mo.vstack(
                [
                    fig_throughput,
                    fig_latency,
                    mo.callout(
                        mo.md(f"""
                **Performance Insights:**
                - **Highest throughput:** {fastest_throughput} ({throughput_df.iloc[-1]['RPS']:,.0f} req/s)
                - **Lowest latency:** {fastest_latency} ({latency_df.iloc[-1]['Latency']:.2f}ms P99)

                Async frameworks (Starlette, FastAPI, Litestar) excel at I/O-bound workloads
                with many concurrent connections.
                """),
                        kind='success',
                    ),
                ]
            )
        else:
            web_output = mo.callout(
                mo.md("""
                **Web framework benchmarks not yet run.**

                To run these benchmarks, you need `wrk` installed:

                ```bash
                # macOS
                brew install wrk

                # Then run:
                python code/run_all.py --category web
                ```
                """),
                kind='warn',
            )
    else:
        web_output = mo.callout(
            mo.md("""
            **Web framework benchmarks not yet run.**

            To run these benchmarks, you need `wrk` installed:

            ```bash
            # macOS
            brew install wrk

            # Then run:
            python code/run_all.py --category web
            ```
            """),
            kind='warn',
        )
    web_output
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 📁 File I/O

    Reading and writing files of various sizes.
    """)
    return


@app.cell(hide_code=True)
def _(categories, utils):
    file_results = categories['file_io']['results']
    utils.create_file_io_chart(file_results)
    return (file_results,)


@app.cell(hide_code=True)
def _(file_results, mo, utils):
    fig_pickle = utils.create_pickle_vs_json_chart(file_results)
    if fig_pickle:
        mo.vstack(
            [
                fig_pickle,
                mo.callout(
                    mo.md(
                        '**Pickle is faster** than JSON for Python-specific serialization, but JSON is more portable.'
                    ),
                    kind='info',
                ),
            ]
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 🗄️ Database and Persistence

    Comparing SQLite, diskcache, and MongoDB performance.
    """)
    return


@app.cell(hide_code=True)
def _(categories, mo, utils):
    db_results = categories['database']['results']
    fig_db = utils.create_database_comparison_chart(db_results)
    db_output = None
    if fig_db:
        db_output = mo.vstack(
            [
                fig_db,
                mo.callout(
                    mo.md("""
                **Key Insights:** 
                - SQLite is fastest for reads (~4μs)
                - diskcache is faster for writes (~30μs vs SQLite's ~200μs)
                - MongoDB adds network overhead (~100-120μs for both operations)
                
                Choose based on your read/write patterns and whether you need distributed access.
                """),
                    kind='info',
                ),
            ]
        )
    db_output
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 🔧 Function and Call Overhead

    The hidden cost of function calls and exceptions.
    """)
    return


@app.cell(hide_code=True)
def _(categories, utils):
    func_results = categories['functions']['results']
    utils.create_function_calls_chart(func_results)
    return (func_results,)


@app.cell(hide_code=True)
def _(func_results, mo, utils):
    fig_exc, exc_overhead = utils.create_exception_cost_chart(func_results)
    if fig_exc:
        mo.vstack(
            [
                fig_exc,
                mo.callout(
                    mo.md(f"""
                **⚠️ Exception Performance Impact:** Exceptions are {exc_overhead:.0f}x slower!
                Don't use exceptions for control flow in hot paths.
                """),
                    kind='warn',
                ),
            ]
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## ⚡ Async Overhead

    Understanding the cost of async machinery.
    """)
    return


@app.cell(hide_code=True)
def _(categories, mo, utils):
    async_results = categories['async']['results']
    fig_async, async_overhead_value = utils.create_async_overhead_chart(async_results)
    async_output = None
    if fig_async:
        async_output = mo.vstack(
            [
                fig_async,
                mo.callout(
                    mo.md(f"""
                **Async adds ~{async_overhead_value:.0f}x overhead** for simple operations.

                Use async only for I/O-bound work (network, disk, database).
                Avoid for CPU-bound or simple synchronous operations.
                """),
                    kind='warn',
                ),
            ]
        )
    async_output
    return (async_results,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 📦 Import Times

    The cost of importing modules and packages.
    """)
    return


@app.cell(hide_code=True)
def _(categories, mo, utils):
    import_results = categories['imports']['results']
    fig_imports = utils.create_import_times_chart(import_results)

    mo.vstack(
        [
            fig_imports,
            mo.callout(
                mo.md("""
            **Import Optimization Tips:**
            - FastAPI and Litestar have significant import overhead
            - Import expensive modules lazily (inside functions when needed)
            - Consider startup time impact for CLI tools
            """),
                kind='info',
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---

    ## 🎓 Key Takeaways

    Performance rules of thumb for Python developers.
    """)
    return


@app.cell(hide_code=True)
def _(coll_results, mo):
    # Calculate actual speedups from the data
    dict_lookup = next(r['value'] for r in coll_results if r['name'] == 'key in dict (existing)')
    set_lookup = next(r['value'] for r in coll_results if r['name'] == 'item in set (existing)')
    list_lookup_last = next(r['value'] for r in coll_results if r['name'] == 'item in list (last)')
    list_lookup_missing = next(r['value'] for r in coll_results if r['name'] == 'item in list (missing)')

    set_speedup = list_lookup_missing / set_lookup

    mo.md(f"""
    ### 1. 🏃 Use Dict/Set for Membership Checks

    **The Data:** In a 1000-item collection:
    - `x in set`: **{set_lookup * 1000:.2f}μs** (constant time)
    - `x in dict`: **{dict_lookup * 1000:.2f}μs** (constant time)
    - `x in list` (worst case): **{list_lookup_last * 1000:.2f}μs** (linear search)

    **Performance Impact:** Set/dict lookups are **{set_speedup:.0f}x faster** than list membership checks!

    Dictionary and set lookups are **O(1)** using hash tables - extremely fast regardless of size.
    List membership checks are **O(n)** requiring a linear scan through every element.

    **When it matters:** If you're checking membership even 100 times, you've already lost ~400ms with a list 
    vs ~2ms with a set. In a web API handling 1000 requests/sec, this difference could be 
    the bottleneck between 100 requests/sec and smooth operation.

    **Rule:** If you're checking `if x in collection` more than once, use a set or dict, not a list!
    """)
    return


@app.cell(hide_code=True)
def _(func_results, mo):
    # Get actual exception data
    no_exception = next(r['value'] for r in func_results if r['name'] == 'try/except (no exception raised)')
    raise_catch = next(r['value'] for r in func_results if r['name'] == 'raise + catch ValueError')
    normal_call = next(r['value'] for r in func_results if r['name'] == 'function call (no try/except)')

    exception_overhead = raise_catch / no_exception

    mo.md(f"""
    ### 2. 🐌 Avoid Exceptions in Hot Loops

    **The Data:**
    - Normal function call: **{normal_call * 1000:.2f}μs**
    - try/except (no error): **{no_exception * 1000:.2f}μs** (nearly free!)
    - raise + catch exception: **{raise_catch * 1000:.2f}μs**

    **Performance Impact:** Raising an exception is **{exception_overhead:.1f}x slower** than normal execution!

    **The Hidden Cost:** When an exception is raised, Python must:
    1. Create the exception object and populate its attributes
    2. Build the full traceback (stack frames, line numbers, local variables)
    3. Unwind the call stack searching for a matching except clause
    4. Clean up frame objects and references

    Each of these steps takes time. The good news? try/except blocks with no exception raised are essentially free.

    **Real-world impact:** If you're using exceptions for control flow in a tight loop (like validating 
    1000 inputs where 50% fail), you're spending ~7ms on exceptions alone vs ~1ms with conditionals.

    **Rule:** Use exceptions for exceptional cases, not control flow. Prefer `if` checks for expected scenarios.
    """)
    return


@app.cell(hide_code=True)
def _(memory_results, mo):
    # Get memory data for classes
    regular_5attr = next(r['value'] for r in memory_results if r['name'] == 'regular_class_5attr')
    slots_5attr = next(r['value'] for r in memory_results if r['name'] == 'slots_class_5attr')
    regular_1000 = next(r['value'] for r in memory_results if r['name'] == 'list_1000_regular_class')
    slots_1000 = next(r['value'] for r in memory_results if r['name'] == 'list_1000_slots_class')

    single_savings = ((regular_5attr - slots_5attr) / regular_5attr) * 100
    aggregate_savings = ((regular_1000 - slots_1000) / regular_1000) * 100
    slots_savings_kb = (regular_1000 - slots_1000) / 1024
    direction = 'more' if single_savings < 0 else 'less'

    mo.md(f"""
    ### 3. 📦 Use __slots__ for Many Instances

    **The Data (5 attributes per instance):**
    - Regular class: **{regular_5attr} bytes** per instance
    - `__slots__` class: **{slots_5attr} bytes** per instance
    - Memory saved per instance: **{regular_5attr - slots_5attr} bytes** ({abs(single_savings):.1f}% {direction})

    **At Scale (1,000 instances):**
    - Regular classes: **{regular_1000 / 1024:.1f} KB**
    - `__slots__` classes: **{slots_1000 / 1024:.1f} KB**
    - Total savings: **{slots_savings_kb:.1f} KB** ({aggregate_savings:.1f}% reduction)

    **Why the difference?** Regular classes store attributes in a `__dict__` (64 bytes + hash table overhead).
    `__slots__` classes use a fixed array of attribute descriptors - no dict required!

    **Speed difference:** Only ~3-5% faster attribute access. The real win is memory.

    **When it matters:**
    - Loading 10,000 database records as objects? Save ~{slots_savings_kb * 10:.0f} KB
    - Parsing 100,000 JSON records? Save ~{slots_savings_kb * 100 / 1024:.1f} MB
    - Game with 1M entities? Save ~{slots_savings_kb * 1000 / 1024:.0f} MB

    **Trade-off:** You lose dynamic attribute assignment (`obj.new_attr = value` won't work).

    **Rule:** Use `__slots__` when creating thousands of similar objects, especially if memory is constrained.
    """)
    return


@app.cell(hide_code=True)
def _(json_results, mo):
    # Get JSON performance data
    json_ser_complex = next(r['value'] for r in json_results if r['name'] == 'json.dumps() - complex')
    orjson_ser_complex = next(r['value'] for r in json_results if r['name'] == 'orjson.dumps() - complex')
    msgspec_ser_complex = next(r['value'] for r in json_results if r['name'] == 'msgspec.json.encode() - complex')

    json_deser_complex = next(r['value'] for r in json_results if r['name'] == 'json.loads() - complex')
    orjson_deser_complex = next(r['value'] for r in json_results if r['name'] == 'orjson.loads() - complex')
    msgspec_deser_complex = next(r['value'] for r in json_results if r['name'] == 'msgspec.json.decode() - complex')

    orjson_ser_speedup = json_ser_complex / orjson_ser_complex
    msgspec_ser_speedup = json_ser_complex / msgspec_ser_complex
    orjson_deser_speedup = json_deser_complex / orjson_deser_complex
    msgspec_deser_speedup = json_deser_complex / msgspec_deser_complex

    mo.md(f"""
    ### 4. ⚡ Consider orjson or msgspec for JSON

    **The Data (complex nested object):**

    **Serialization (dumps):**
    - `json.dumps()`: **{json_ser_complex * 1000:.2f}μs**
    - `orjson.dumps()`: **{orjson_ser_complex * 1000:.2f}μs** ({orjson_ser_speedup:.1f}x faster)
    - `msgspec.encode()`: **{msgspec_ser_complex * 1000:.2f}μs** ({msgspec_ser_speedup:.1f}x faster)

    **Deserialization (loads):**
    - `json.loads()`: **{json_deser_complex * 1000:.2f}μs**
    - `orjson.loads()`: **{orjson_deser_complex * 1000:.2f}μs** ({orjson_deser_speedup:.1f}x faster)
    - `msgspec.decode()`: **{msgspec_deser_complex * 1000:.2f}μs** ({msgspec_deser_speedup:.1f}x faster)

    **Why so much faster?** These libraries are written in C/Rust with:
    - Optimized parsers avoiding Python's overhead
    - Better memory allocation strategies
    - Specialized string handling
    - Direct C-level data structure access

    **Real-world impact:**
    - **REST API** returning JSON: 1000 requests/sec = 
      save ~{(json_ser_complex - orjson_ser_complex) * 1000:.0f}ms/sec CPU time
    - **Data pipeline** processing 100K records: 
      save ~{(json_ser_complex - orjson_ser_complex) * 100000 / 1000:.1f}s
    - **Microservice** handling 10K messages/sec: reduce latency from 
      {json_deser_complex * 1000:.1f}μs to {orjson_deser_complex * 1000:.1f}μs per message

    **Which to choose?**
    - `orjson`: Fastest, battle-tested, strict RFC 8259 compliance
    - `msgspec`: Includes schema validation, supports MessagePack, excellent type annotations

    **Rule:** For high-throughput APIs or data processing, use `orjson` or `msgspec`. 
    In latency-sensitive APIs, this alone can improve throughput by 20-40%.
    """)
    return


@app.cell(hide_code=True)
def _(async_results, mo):
    # Get async overhead data
    sync_call = next(r['value'] for r in async_results if r['name'] == 'sync function call')
    async_call = next(r['value'] for r in async_results if r['name'] == 'async equivalent (run_until_complete)')

    async_overhead_multiplier = async_call / sync_call
    async_overhead_us = (async_call - sync_call) * 1000

    # Calculate break-even point
    # If an I/O operation takes X ms, async is worth it if you can do other work
    breakeven_io_ms = async_overhead_us / 1000  # Conservative estimate

    mo.md(f"""
    ### 5. 🔄 Async Only for I/O-Bound Work

    **The Data:**
    - Sync function call: **{sync_call * 1000:.2f}μs**
    - Async function call: **{async_call * 1000:.2f}μs**
    - Overhead: **+{async_overhead_us:.2f}μs** ({async_overhead_multiplier:.0f}x slower!)

    **What causes the overhead?**
    1. Event loop management and task scheduling
    2. Coroutine object creation and garbage collection
    3. Context switching between tasks
    4. Frame object allocation for await points

    Each `await` adds scheduling overhead even if there's nothing to wait for.

    **When async pays off:** The break-even point is around **{breakeven_io_ms:.1f}ms** of I/O time.

    **Async WINS:** 🏆
    - Database queries (10-100ms each) - handle 100 concurrent queries instead of 1
    - HTTP requests (50-500ms) - fetch 50 URLs in parallel
    - File I/O (varies) - read multiple files concurrently
    - WebSocket connections - handle thousands of simultaneous connections

    **Async LOSES:** 💸
    - CPU-bound math (`sum()`, parsing, regex) - adds {async_overhead_multiplier:.0f}x overhead with no benefit
    - In-memory operations (dict lookups, list operations)
    - Simple function calls
    - Operations under 1ms

    **Real example:** A FastAPI endpoint that does:
    - 3x database queries (30ms total) + 2x API calls (200ms total) + CPU work (5ms)
    - **Sync:** 235ms (sequential)
    - **Async:** ~50ms (parallel I/O) + 5ms (CPU) + overhead = ~55ms
    - **Speedup:** 4.3x faster! 🚀

    **Rule:** Only use async when you have actual I/O operations (network, disk, database) that 
    can run concurrently. Don't use async for CPU-bound or simple synchronous code.
    """)
    return


@app.cell(hide_code=True)
def _(basic_results, mo):
    # Get list comp vs for loop data
    list_comp_1000 = next(r['value'] for r in basic_results if r['name'] == 'list_comp_1000')
    for_loop_1000 = next(r['value'] for r in basic_results if r['name'] == 'for_loop_1000')

    listcomp_speedup = ((for_loop_1000 - list_comp_1000) / for_loop_1000) * 100
    listcomp_speedup_ratio = for_loop_1000 / list_comp_1000

    mo.md(f"""
    ### 6. 📝 List Comprehensions Are Faster

    **The Data (building 1000-item list):**
    - List comprehension: **{list_comp_1000 * 1000:.2f}μs**
    - For-loop + append: **{for_loop_1000 * 1000:.2f}μs**
    - Speedup: **{listcomp_speedup:.1f}% faster** ({listcomp_speedup_ratio:.2f}x)

    **Why are comprehensions faster?**
    1. **Optimized C implementation** - the interpreter recognizes comprehensions and uses fast paths
    2. **Pre-allocated memory** - Python knows the size for simple ranges and allocates once
    3. **Fewer bytecode operations** - no repeated `list.append` attribute lookups
    4. **Function call overhead** - no `append()` method call per iteration

    Let's look at bytecode:
    ```python
    # For loop: 17 bytecode operations per iteration
    for i in range(1000):
        result.append(i * 2)

    # Comprehension: 10 bytecode operations per iteration
    [i * 2 for i in range(1000)]
    ```

    **Readability bonus:** Comprehensions are also more Pythonic and express intent clearly.

    **When it matters:**
    - Processing 10K records: save ~{(for_loop_1000 - list_comp_1000) * 10:.2f}ms
    - Data transformation pipeline with 5 steps: save {(for_loop_1000 - list_comp_1000) * 5 * 1000:.0f}μs per 1K items
    - Real-time data processing: every microsecond counts

    **Don't overdo it:** Keep comprehensions readable. If you need multiple lines or complex logic, 
    a regular for-loop is fine (and only ~{listcomp_speedup:.0f}% slower).

    **Rule:** Use comprehensions when appropriate - they're both faster and more Pythonic. 
    But readability still trumps micro-optimization.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---

    ## 📚 Data Source

    All visualizations are powered by live data from `results.json`.
    To update these charts, simply re-run the benchmarks:

    ```bash
    cd code
    python run_all.py
    ```

    Then reload this notebook to see updated visualizations!

    ---

    ## 🔗 Resources

    - **Source Code:** [github.com/mkennedy/python-numbers-everyone-should-know](https://github.com/mkennedy/python-numbers-everyone-should-know)
    - **Original Inspiration:** [Latency Numbers Every Programmer Should Know](https://gist.github.com/jboner/2841832)

    ---

    *Built with [marimo](https://marimo.io) - a reactive Python notebook*
    """)
    return


if __name__ == '__main__':
    app.run()
