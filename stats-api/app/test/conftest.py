"""
Pytest configuration and shared fixtures.
"""

from __future__ import annotations

from pathlib import Path
import pytest
from mongomock import MongoClient as MockMongoClient

from app import create_app

# adjust import if file moved
from app.command.import_csv_to_mongodb import CSVImporter

# ----------------------------
# Paths (stable in Docker/CI)
# ----------------------------


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    # conftest.py location -> tests/fixtures
    return Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(scope="session")
def test_csv_file(fixtures_dir: Path) -> Path:
    return fixtures_dir / "test_csv_file.csv"


# ----------------------------
# Flask app / context (only when needed)
# ----------------------------


@pytest.fixture(scope="session")
def app():
    return create_app("testing")


@pytest.fixture(autouse=True)
def app_ctx(app):
    """
    Push/pop a Flask application context for each test.
    Useful for tests that still use current_app, config, etc.
    If a test doesn't need Flask, this is still cheap and avoids surprises.
    """
    ctx = app.app_context()
    ctx.push()
    yield
    ctx.pop()


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


# ----------------------------
# Mock Mongo (per test)
# ----------------------------


@pytest.fixture()
def mock_mongo_client():
    # mongomock doesn't really need an URI
    return MockMongoClient()


@pytest.fixture()
def db(mock_mongo_client):
    """
    Provides a clean mock database per test.
    """
    db_name = "sales_test"
    database = mock_mongo_client[db_name]

    yield database

    # Cleanup after each test
    mock_mongo_client.drop_database(db_name)


@pytest.fixture()
def collection(db):
    """
    Provides a clean mock collection per test.
    """
    collection_name = "sales_madrid_test"
    col = db[collection_name]

    # Ensure it's empty
    col.delete_many({})
    return col


# ----------------------------
# CSV Importer (independent)
# ----------------------------


@pytest.fixture()
def csv_importer(collection):
    """
    CSVImporter is framework-agnostic: we inject the collection directly.
    """
    return CSVImporter(collection=collection)


@pytest.fixture()
def populated_collection(csv_importer, test_csv_file: Path, collection):
    """
    Pre-populate the collection with the CSV fixture data.
    """
    csv_importer.import_csv(str(test_csv_file))
    return collection


# ----------------------------
# Optional test logging
# ----------------------------


@pytest.fixture(autouse=True)
def log_test_name(request):
    test_name = request.node.name
    print(f"\n▶ START TEST: {test_name}")
    yield
    print(f"✓ END TEST: {test_name}")


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks slow tests")
    config.addinivalue_line("markers", "integration: marks integration tests")
