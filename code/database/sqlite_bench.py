"""
SQLite benchmarks.

Measures:
- Insert one object (JSON blob)
- Select by primary key
- Update one field
- Delete
- Select with json_extract()
"""

import json
import sqlite3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.benchmark import (
    USER_DATA,
    BenchmarkResult,
    collect_results,
    print_header,
    print_result,
    print_subheader,
    time_operation,
)

CATEGORY = 'database_sqlite'


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all SQLite benchmarks."""
    results = []

    print_header('SQLite Benchmarks')

    # Create temporary database file
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / 'test.db'

        # -------------------------------------------------------------------------
        # Setup: Create table
        # -------------------------------------------------------------------------
        conn = sqlite3.connect(db_path)
        conn.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                data TEXT NOT NULL
            )
        """)
        conn.commit()

        # Prepare JSON data
        json_data = json.dumps(USER_DATA)

        # -------------------------------------------------------------------------
        # Insert Operations
        # -------------------------------------------------------------------------
        print_subheader('Insert Operations')

        def insert_one():
            conn.execute('INSERT INTO users (data) VALUES (?)', (json_data,))
            conn.commit()

        time_ms = time_operation(insert_one, iterations=1_000)
        results.append(BenchmarkResult('INSERT (JSON blob)', time_ms, category=CATEGORY))
        print_result('INSERT (JSON blob)', time_ms)

        # Insert without commit for comparison
        def insert_no_commit():
            conn.execute('INSERT INTO users (data) VALUES (?)', (json_data,))

        time_ms = time_operation(insert_no_commit, iterations=1_000)
        conn.commit()  # Commit all the test inserts
        results.append(BenchmarkResult('INSERT (no commit)', time_ms, category=CATEGORY))
        print_result('INSERT (no commit)', time_ms)

        # -------------------------------------------------------------------------
        # Select Operations
        # -------------------------------------------------------------------------
        print_subheader('Select Operations')

        # Get a valid ID to select
        cur = conn.execute('SELECT id FROM users LIMIT 1')
        test_id = cur.fetchone()[0]

        def select_by_pk():
            cur = conn.execute('SELECT * FROM users WHERE id = ?', (test_id,))
            return cur.fetchone()

        time_ms = time_operation(select_by_pk, iterations=5_000)
        results.append(BenchmarkResult('SELECT by primary key', time_ms, category=CATEGORY))
        print_result('SELECT by primary key', time_ms)

        # Select all (limited set)
        def select_limit_100():
            cur = conn.execute('SELECT * FROM users LIMIT 100')
            return cur.fetchall()

        time_ms = time_operation(select_limit_100, iterations=1_000)
        results.append(BenchmarkResult('SELECT LIMIT 100', time_ms, category=CATEGORY))
        print_result('SELECT LIMIT 100', time_ms)

        # -------------------------------------------------------------------------
        # JSON Operations
        # -------------------------------------------------------------------------
        print_subheader('JSON Operations')

        def json_extract_simple():
            cur = conn.execute("SELECT json_extract(data, '$.username') FROM users WHERE id = ?", (test_id,))
            return cur.fetchone()

        time_ms = time_operation(json_extract_simple, iterations=5_000)
        results.append(BenchmarkResult('json_extract() simple path', time_ms, category=CATEGORY))
        print_result('json_extract() simple path', time_ms)

        def json_extract_nested():
            cur = conn.execute("SELECT json_extract(data, '$.profile.location') FROM users WHERE id = ?", (test_id,))
            return cur.fetchone()

        time_ms = time_operation(json_extract_nested, iterations=5_000)
        results.append(BenchmarkResult('json_extract() nested path', time_ms, category=CATEGORY))
        print_result('json_extract() nested path', time_ms)

        def json_extract_array():
            cur = conn.execute("SELECT json_extract(data, '$.posts[0].title') FROM users WHERE id = ?", (test_id,))
            return cur.fetchone()

        time_ms = time_operation(json_extract_array, iterations=5_000)
        results.append(BenchmarkResult('json_extract() array access', time_ms, category=CATEGORY))
        print_result('json_extract() array access', time_ms)

        # -------------------------------------------------------------------------
        # Update Operations
        # -------------------------------------------------------------------------
        print_subheader('Update Operations')

        modified_data = json.dumps({**USER_DATA, 'username': 'bob_dev'})

        def update_one():
            conn.execute('UPDATE users SET data = ? WHERE id = ?', (modified_data, test_id))
            conn.commit()

        time_ms = time_operation(update_one, iterations=1_000)
        results.append(BenchmarkResult('UPDATE (full JSON)', time_ms, category=CATEGORY))
        print_result('UPDATE (full JSON)', time_ms)

        # Update without commit
        def update_no_commit():
            conn.execute('UPDATE users SET data = ? WHERE id = ?', (json_data, test_id))

        time_ms = time_operation(update_no_commit, iterations=1_000)
        conn.commit()
        results.append(BenchmarkResult('UPDATE (no commit)', time_ms, category=CATEGORY))
        print_result('UPDATE (no commit)', time_ms)

        # -------------------------------------------------------------------------
        # Delete Operations
        # -------------------------------------------------------------------------
        print_subheader('Delete Operations')

        # Insert some rows to delete
        for _ in range(1000):
            conn.execute('INSERT INTO users (data) VALUES (?)', (json_data,))
        conn.commit()

        def delete_one():
            cur = conn.execute('SELECT id FROM users LIMIT 1')
            row = cur.fetchone()
            if row:
                conn.execute('DELETE FROM users WHERE id = ?', (row[0],))
                conn.commit()

        time_ms = time_operation(delete_one, iterations=500)
        results.append(BenchmarkResult('DELETE by primary key', time_ms, category=CATEGORY))
        print_result('DELETE by primary key', time_ms)

        # -------------------------------------------------------------------------
        # Transaction Operations
        # -------------------------------------------------------------------------
        print_subheader('Transaction Operations')

        def begin_commit():
            conn.execute('BEGIN')
            conn.execute('INSERT INTO users (data) VALUES (?)', (json_data,))
            conn.commit()

        time_ms = time_operation(begin_commit, iterations=500)
        results.append(BenchmarkResult('BEGIN + INSERT + COMMIT', time_ms, category=CATEGORY))
        print_result('BEGIN + INSERT + COMMIT', time_ms)

        def executemany_10():
            conn.executemany('INSERT INTO users (data) VALUES (?)', [(json_data,)] * 10)
            conn.commit()

        time_ms = time_operation(executemany_10, iterations=200)
        results.append(BenchmarkResult('executemany() 10 rows', time_ms, category=CATEGORY))
        print_result('executemany() 10 rows', time_ms)

        # Cleanup
        conn.close()

    return results


def main():
    """Run benchmarks and output results."""
    results = run_benchmarks()
    output = collect_results(CATEGORY, results)

    print()
    print(f'Total benchmarks: {len(results)}')

    return output


if __name__ == '__main__':
    main()
