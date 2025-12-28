"""
MongoDB benchmarks.

Measures:
- insert_one()
- find_one() by _id
- find_one() by nested field
- update_one()
- delete_one()

Gracefully skips if MongoDB is not running.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.benchmark import (
    USER_DATA,
    BenchmarkResult,
    collect_results,
    print_header,
    print_result,
    print_skip_message,
    print_subheader,
    time_operation,
    try_import,
)

CATEGORY = 'database_mongodb'


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all MongoDB benchmarks."""
    results = []

    print_header('MongoDB Benchmarks')

    # Import pymongo
    pymongo = try_import('pymongo')
    if not pymongo:
        print_skip_message('pymongo', 'not installed (pip install pymongo)')
        return results

    # Try to connect to MongoDB
    try:
        client = pymongo.MongoClient(
            'mongodb://localhost:27017/',
            serverSelectionTimeoutMS=2000,  # 2 second timeout
        )
        # Force connection to check if MongoDB is running
        client.admin.command('ping')
    except Exception as e:
        print_skip_message('MongoDB', f'not running ({e})')
        return results

    # Create test database and collection
    db = client['benchmark_test']
    collection = db['users']

    # Clean up any previous test data
    collection.drop()

    # Create index on nested field for fair comparison
    collection.create_index('profile.location')

    # -------------------------------------------------------------------------
    # Insert Operations
    # -------------------------------------------------------------------------
    print_subheader('Insert Operations')

    inserted_ids = []

    def insert_one():
        result = collection.insert_one(USER_DATA.copy())
        inserted_ids.append(result.inserted_id)

    time_ms = time_operation(insert_one, iterations=1_000)
    results.append(BenchmarkResult('insert_one()', time_ms, category=CATEGORY))
    print_result('insert_one()', time_ms)

    # Insert many for comparison
    def insert_many_10():
        docs = [USER_DATA.copy() for _ in range(10)]
        result = collection.insert_many(docs)
        inserted_ids.extend(result.inserted_ids)

    time_ms = time_operation(insert_many_10, iterations=100)
    results.append(BenchmarkResult('insert_many() 10 docs', time_ms, category=CATEGORY))
    print_result('insert_many() 10 docs', time_ms)

    # -------------------------------------------------------------------------
    # Find Operations
    # -------------------------------------------------------------------------
    print_subheader('Find Operations')

    # Get a test ID
    test_id = inserted_ids[0] if inserted_ids else None

    if test_id:

        def find_by_id():
            return collection.find_one({'_id': test_id})

        time_ms = time_operation(find_by_id, iterations=5_000)
        results.append(BenchmarkResult('find_one() by _id', time_ms, category=CATEGORY))
        print_result('find_one() by _id', time_ms)

    def find_by_field():
        return collection.find_one({'username': 'alice_dev'})

    time_ms = time_operation(find_by_field, iterations=2_000)
    results.append(BenchmarkResult('find_one() by field', time_ms, category=CATEGORY))
    print_result('find_one() by field', time_ms)

    def find_by_nested():
        return collection.find_one({'profile.location': 'Portland, OR'})

    time_ms = time_operation(find_by_nested, iterations=2_000)
    results.append(BenchmarkResult('find_one() by nested field (indexed)', time_ms, category=CATEGORY))
    print_result('find_one() by nested field (indexed)', time_ms)

    # Find with limit
    def find_limit_100():
        return list(collection.find().limit(100))

    time_ms = time_operation(find_limit_100, iterations=500)
    results.append(BenchmarkResult('find().limit(100)', time_ms, category=CATEGORY))
    print_result('find().limit(100)', time_ms)

    # -------------------------------------------------------------------------
    # Update Operations
    # -------------------------------------------------------------------------
    print_subheader('Update Operations')

    if test_id:

        def update_one_by_id():
            collection.update_one({'_id': test_id}, {'$set': {'settings.theme': 'light'}})

        time_ms = time_operation(update_one_by_id, iterations=1_000)
        results.append(BenchmarkResult('update_one() by _id', time_ms, category=CATEGORY))
        print_result('update_one() by _id', time_ms)

    def update_one_by_field():
        collection.update_one({'username': 'alice_dev'}, {'$set': {'settings.theme': 'dark'}})

    time_ms = time_operation(update_one_by_field, iterations=1_000)
    results.append(BenchmarkResult('update_one() by field', time_ms, category=CATEGORY))
    print_result('update_one() by field', time_ms)

    # Update with $inc
    def update_inc():
        collection.update_one({'username': 'alice_dev'}, {'$inc': {'posts.0.views': 1}})

    time_ms = time_operation(update_inc, iterations=1_000)
    results.append(BenchmarkResult('update_one() with $inc', time_ms, category=CATEGORY))
    print_result('update_one() with $inc', time_ms)

    # -------------------------------------------------------------------------
    # Delete Operations
    # -------------------------------------------------------------------------
    print_subheader('Delete Operations')

    # Insert docs to delete
    delete_ids = []
    for _ in range(2000):
        result = collection.insert_one(USER_DATA.copy())
        delete_ids.append(result.inserted_id)

    delete_idx = [0]

    def delete_one_by_id():
        if delete_idx[0] < len(delete_ids):
            collection.delete_one({'_id': delete_ids[delete_idx[0]]})
            delete_idx[0] += 1

    time_ms = time_operation(delete_one_by_id, iterations=1_000)
    results.append(BenchmarkResult('delete_one() by _id', time_ms, category=CATEGORY))
    print_result('delete_one() by _id', time_ms)

    # -------------------------------------------------------------------------
    # Aggregate Operations
    # -------------------------------------------------------------------------
    print_subheader('Aggregate Operations')

    # Simple count
    def count_docs():
        return collection.count_documents({})

    time_ms = time_operation(count_docs, iterations=500)
    results.append(BenchmarkResult('count_documents()', time_ms, category=CATEGORY))
    print_result('count_documents()', time_ms)

    # Aggregate pipeline
    def aggregate_simple():
        return list(collection.aggregate([{'$match': {'settings.theme': 'dark'}}, {'$limit': 10}]))

    time_ms = time_operation(aggregate_simple, iterations=500)
    results.append(BenchmarkResult('aggregate() simple pipeline', time_ms, category=CATEGORY))
    print_result('aggregate() simple pipeline', time_ms)

    # -------------------------------------------------------------------------
    # Statistics
    # -------------------------------------------------------------------------
    print_subheader('Collection Statistics')
    doc_count = collection.count_documents({})
    print(f'  Documents in collection: {doc_count}')

    # Cleanup
    collection.drop()
    client.close()

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
