"""dbcli - Unified CLI for MySQL, PostgreSQL, and SQLite databases."""

import os
import shutil
import subprocess
import sys
from typing import NoReturn

_SQLITE_EXTENSIONS = {'.db', '.sqlite', '.sqlite3', '.db3'}


def main() -> None:
    args = sys.argv[1:]

    detected = _detect_db_type(args)
    if detected == 'mysql':
        _run_tool('mycli', 'mycli', args)
    elif detected == 'postgres':
        _run_tool('pgcli', 'pgcli', args)
    elif detected == 'sqlite':
        _run_tool('litecli', 'litecli', args)

    _show_usage()


def _detect_db_type(args: list[str]) -> str | None:
    for a in args:
        if '://' in a:
            scheme = a.split('://')[0].lower()
            if scheme in ('mysql', 'mycli'):
                return 'mysql'
            if scheme in ('postgres', 'postgresql', 'pgcli'):
                return 'postgres'
            if scheme in ('sqlite', 'sqlite3'):
                return 'sqlite'

    for i, a in enumerate(args):
        if a in ('-p', '--port', '-P') and i + 1 < len(args):
            port = args[i + 1]
            if port == '3306':
                return 'mysql'
            if port == '5432':
                return 'postgres'

    for a in args:
        if not a.startswith('-'):
            _, ext = os.path.splitext(a)
            if ext.lower() in _SQLITE_EXTENSIONS:
                return 'sqlite'

    return None


def _run_tool(name: str, cmd: str, args: list[str]) -> NoReturn:
    bin_path = shutil.which(cmd)
    if not bin_path:
        print(
            f"dbcli: {name} is not installed.\n"
            f"  Install it with:  pip install {name}\n"
            f"  Or via brew:      brew install {name}\n"
            f"  Or via uv:        uv tool install {name}",
            file=sys.stderr,
        )
        sys.exit(1)
    sys.exit(subprocess.run([bin_path, *args]).returncode)


def _show_usage() -> NoReturn:
    print("Usage: dbcli [OPTIONS] [DBNAME]")
    print()
    print("  A unified CLI for MySQL, PostgreSQL, and SQLite databases.")
    print()
    print("  Database type is auto-detected from the connection URI or file extension:")
    print("    mysql://user@host:3306/db     -> MySQL (mycli)")
    print("    postgres://user@host:5432/db  -> PostgreSQL (pgcli)")
    print("    path/to/db.sqlite             -> SQLite (litecli)")
    print()
    print("  Port-based detection is also supported (-p/-P/--port 3306 or 5432).")
    sys.exit(1)


if __name__ == "__main__":
    main()
