import marimo

__generated_with = "0.18.4"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import notebook_utils as utils
    return mo, utils


@app.cell(hide_code=True)
def _(utils):
    metadata, categories = utils.load_benchmark_results()
    return categories, metadata


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
    ## 🎯 Quick Reference Dashboard

    Navigate to any section to explore detailed visualizations:
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
    fig, savings_pct, savings_kb = utils.create_aggregate_class_memory_chart(memory_results)

    mo.vstack(
        [
            fig,
            mo.callout(
                mo.md(f"""
            **__slots__ Memory Savings:** {savings_pct:.1f}% less memory 
            ({savings_kb:.1f} KB saved for 1,000 instances)
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

    *This is a streamlined version of the notebook focused on memory and basic operations.*

    **The full notebook with all visualizations for collections, JSON, web frameworks,
    database, functions, async, and imports can be expanded as needed.**

    ---

    ## 🎓 Key Takeaways

    Performance rules of thumb for Python developers.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### 1. 🏃 Use Dict/Set for Membership Checks

    Dictionary and set lookups are **O(1)** - extremely fast regardless of size.
    List membership checks are **O(n)** - slow for large lists.

    **Rule:** If you're checking `if x in collection` frequently, use a set or dict, not a list!
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### 2. 🐌 Avoid Exceptions in Hot Loops

    Raising and catching exceptions is **~6-7x slower** than normal execution.

    **Rule:** Use exceptions for exceptional cases, not control flow.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### 3. 📦 Use __slots__ for Many Instances

    `__slots__` classes use **~50% less memory** when you have many instances.
    Speed difference is minimal.

    **Rule:** Use `__slots__` when creating thousands of similar objects.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### 4. ⚡ Consider orjson or msgspec for JSON

    Alternative JSON libraries are **3-8x faster** than stdlib `json`.

    **Rule:** For high-throughput APIs or data processing, use `orjson` or `msgspec`.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### 5. 🔄 Async Only for I/O-Bound Work

    Async/await adds **~2000x overhead** for simple operations.

    **Rule:** Only use async when you have actual I/O operations (network, disk, database).
    Don't use async for CPU-bound or simple synchronous code.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### 6. 📝 List Comprehensions Are Faster

    List comprehensions are **~20% faster** than equivalent for-loops.

    **Rule:** Use comprehensions when appropriate - they're both faster and more Pythonic.
    """)
    return


@app.cell
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


if __name__ == "__main__":
    app.run()
