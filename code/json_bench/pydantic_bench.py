"""
Pydantic serialization/validation benchmarks.

Measures:
- model_dump_json()
- model_validate_json()
- model_dump() (to dict)
- model_validate() (from dict)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.benchmark import (
    BenchmarkResult,
    collect_results,
    print_header,
    print_result,
    print_skip_message,
    print_subheader,
    time_operation,
    try_import,
)

CATEGORY = "pydantic_serialization"


def run_benchmarks() -> list[BenchmarkResult]:
    """Run all Pydantic benchmarks."""
    results = []

    print_header("Pydantic Serialization Benchmarks")

    pydantic = try_import("pydantic")

    if not pydantic:
        print_skip_message("pydantic")
        return results

    from pydantic import BaseModel

    # -------------------------------------------------------------------------
    # Define Pydantic Models
    # -------------------------------------------------------------------------

    class SimpleModel(BaseModel):
        id: int
        name: str
        active: bool

    class PostModel(BaseModel):
        id: int
        title: str
        tags: list[str]
        views: int

    class ProfileModel(BaseModel):
        bio: str
        location: str
        website: str
        joined: str

    class SettingsModel(BaseModel):
        theme: str
        notifications: bool
        email_frequency: str

    class ComplexModel(BaseModel):
        id: int
        username: str
        email: str
        profile: ProfileModel
        posts: list[PostModel]
        settings: SettingsModel

    # Create test instances
    simple_instance = SimpleModel(id=123, name="Alice", active=True)

    complex_instance = ComplexModel(
        id=12345,
        username="alice_dev",
        email="alice@example.com",
        profile=ProfileModel(
            bio="Software engineer who loves Python",
            location="Portland, OR",
            website="https://alice.dev",
            joined="2020-03-15T08:30:00Z",
        ),
        posts=[
            PostModel(id=1, title="First Post", tags=["python", "tutorial"], views=1520),
            PostModel(id=2, title="Second Post", tags=["rust", "wasm"], views=843),
            PostModel(id=3, title="Third Post", tags=["python", "async"], views=2341),
        ],
        settings=SettingsModel(
            theme="dark",
            notifications=True,
            email_frequency="weekly",
        ),
    )

    # Pre-create dicts and JSON for validation benchmarks
    simple_dict = {"id": 123, "name": "Alice", "active": True}
    complex_dict = {
        "id": 12345,
        "username": "alice_dev",
        "email": "alice@example.com",
        "profile": {
            "bio": "Software engineer who loves Python",
            "location": "Portland, OR",
            "website": "https://alice.dev",
            "joined": "2020-03-15T08:30:00Z",
        },
        "posts": [
            {"id": 1, "title": "First Post", "tags": ["python", "tutorial"], "views": 1520},
            {"id": 2, "title": "Second Post", "tags": ["rust", "wasm"], "views": 843},
            {"id": 3, "title": "Third Post", "tags": ["python", "async"], "views": 2341},
        ],
        "settings": {
            "theme": "dark",
            "notifications": True,
            "email_frequency": "weekly",
        },
    }

    simple_json = json.dumps(simple_dict)
    complex_json = json.dumps(complex_dict)

    # -------------------------------------------------------------------------
    # model_dump() - to dict
    # -------------------------------------------------------------------------
    print_subheader("model_dump() - to dict")

    def model_dump_simple():
        return simple_instance.model_dump()

    time_ms = time_operation(model_dump_simple, iterations=5000)
    results.append(BenchmarkResult("model_dump() - simple", time_ms, category=CATEGORY))
    print_result("model_dump() - simple", time_ms)

    def model_dump_complex():
        return complex_instance.model_dump()

    time_ms = time_operation(model_dump_complex, iterations=5000)
    results.append(BenchmarkResult("model_dump() - complex", time_ms, category=CATEGORY))
    print_result("model_dump() - complex", time_ms)

    # -------------------------------------------------------------------------
    # model_dump_json() - to JSON string
    # -------------------------------------------------------------------------
    print_subheader("model_dump_json() - to JSON")

    def model_dump_json_simple():
        return simple_instance.model_dump_json()

    time_ms = time_operation(model_dump_json_simple, iterations=5000)
    results.append(BenchmarkResult("model_dump_json() - simple", time_ms, category=CATEGORY))
    print_result("model_dump_json() - simple", time_ms)

    def model_dump_json_complex():
        return complex_instance.model_dump_json()

    time_ms = time_operation(model_dump_json_complex, iterations=5000)
    results.append(BenchmarkResult("model_dump_json() - complex", time_ms, category=CATEGORY))
    print_result("model_dump_json() - complex", time_ms)

    # -------------------------------------------------------------------------
    # model_validate() - from dict
    # -------------------------------------------------------------------------
    print_subheader("model_validate() - from dict")

    def model_validate_simple():
        return SimpleModel.model_validate(simple_dict)

    time_ms = time_operation(model_validate_simple, iterations=5000)
    results.append(BenchmarkResult("model_validate() - simple", time_ms, category=CATEGORY))
    print_result("model_validate() - simple", time_ms)

    def model_validate_complex():
        return ComplexModel.model_validate(complex_dict)

    time_ms = time_operation(model_validate_complex, iterations=5000)
    results.append(BenchmarkResult("model_validate() - complex", time_ms, category=CATEGORY))
    print_result("model_validate() - complex", time_ms)

    # -------------------------------------------------------------------------
    # model_validate_json() - from JSON string
    # -------------------------------------------------------------------------
    print_subheader("model_validate_json() - from JSON")

    def model_validate_json_simple():
        return SimpleModel.model_validate_json(simple_json)

    time_ms = time_operation(model_validate_json_simple, iterations=5000)
    results.append(BenchmarkResult("model_validate_json() - simple", time_ms, category=CATEGORY))
    print_result("model_validate_json() - simple", time_ms)

    def model_validate_json_complex():
        return ComplexModel.model_validate_json(complex_json)

    time_ms = time_operation(model_validate_json_complex, iterations=5000)
    results.append(BenchmarkResult("model_validate_json() - complex", time_ms, category=CATEGORY))
    print_result("model_validate_json() - complex", time_ms)

    # -------------------------------------------------------------------------
    # Comparison: dict() vs model_dump()
    # -------------------------------------------------------------------------
    print_subheader("Comparison")

    # Compare to plain json.dumps on the dict
    def json_dumps_dict():
        return json.dumps(complex_dict)

    time_ms = time_operation(json_dumps_dict, iterations=5000)
    results.append(BenchmarkResult("json.dumps(dict) - comparison", time_ms, category=CATEGORY))
    print_result("json.dumps(dict) - comparison", time_ms)

    return results


def main():
    """Run benchmarks and output results."""
    results = run_benchmarks()
    output = collect_results(CATEGORY, results)

    print()
    print(f"Total benchmarks: {len(results)}")

    return output


if __name__ == "__main__":
    main()
