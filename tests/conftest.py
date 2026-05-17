import os
import sys
from collections.abc import Generator

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Vendor setup
_VENDOR_BASE = os.path.join(os.path.dirname(__file__), "..", "dbcli", "vendors")
if _VENDOR_BASE not in sys.path:
    sys.path.insert(0, _VENDOR_BASE)

# Ensure PGPASSWORD is available for PostgreSQL tests
if "PGPASSWORD" not in os.environ:
    os.environ["PGPASSWORD"] = "postgres"


@pytest.fixture(scope="session")
def pg_dsn() -> str:
    return os.environ.get("PG_DSN", "postgres://postgres:postgres@127.0.0.1:5432/test")


@pytest.fixture(scope="session")
def mysql_dsn() -> str:
    return os.environ.get("MYSQL_DSN", "mysql://root:root@127.0.0.1:3306/test")


@pytest.fixture(scope="session")
def sqlite_db() -> str:
    return os.environ.get("SQLITE_DB", "/tmp/test.db")


@pytest.fixture
def pg_args() -> list[str]:
    return ["-Upostgres", "-h127.0.0.1", "-p5432", "test"]


@pytest.fixture
def mysql_args() -> list[str]:
    return ["-uroot", "-proot", "-h127.0.0.1", "-P3306", "test"]


@pytest.fixture
def sqlite_args() -> list[str]:
    return ["/tmp/test.db"]
