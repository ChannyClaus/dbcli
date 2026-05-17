from dbcli.main import _detect_db_type


class TestDetectDbType:
    def test_mysql_uri(self):
        assert _detect_db_type(["mysql://root@localhost/test"]) == "mysql"

    def test_pg_uri(self):
        assert _detect_db_type(["postgres://user@localhost/db"]) == "postgres"
        assert _detect_db_type(["postgresql://user@localhost/db"]) == "postgres"

    def test_sqlite_uri(self):
        assert _detect_db_type(["sqlite:///path/to/db"]) == "sqlite"

    def test_mycli_uri(self):
        assert _detect_db_type(["mycli://root@localhost/test"]) == "mysql"

    def test_pgcli_uri(self):
        assert _detect_db_type(["pgcli://user@localhost/db"]) == "postgres"

    def test_sqlite_file_extensions(self):
        assert _detect_db_type(["/path/to/db.sqlite"]) == "sqlite"
        assert _detect_db_type(["/path/to/db.sqlite3"]) == "sqlite"
        assert _detect_db_type(["/path/to/db.db3"]) == "sqlite"
        assert _detect_db_type(["/tmp/test.db"]) == "sqlite"

    def test_mysql_port_separate(self):
        assert _detect_db_type(["-P", "3306", "test"]) == "mysql"

    def test_mysql_port_combined(self):
        assert _detect_db_type(["-P3306", "test"]) == "mysql"

    def test_mysql_long_port(self):
        assert _detect_db_type(["--port=3306", "test"]) == "mysql"
        assert _detect_db_type(["--port", "3306", "test"]) == "mysql"

    def test_pg_port_separate(self):
        assert _detect_db_type(["-p", "5432", "test"]) == "postgres"

    def test_pg_port_combined(self):
        assert _detect_db_type(["-p5432", "test"]) == "postgres"

    def test_pg_long_port(self):
        assert _detect_db_type(["--port=5432", "test"]) == "postgres"
        assert _detect_db_type(["--port", "5432", "test"]) == "postgres"

    def test_mysql_u_flag(self):
        assert _detect_db_type(["-uroot", "mydb"]) == "mysql"

    def test_pg_u_flag(self):
        assert _detect_db_type(["-Upostgres", "mydb"]) == "postgres"

    def test_no_match(self):
        assert _detect_db_type(["unknown"]) is None
        assert _detect_db_type(["-x", "foo"]) is None
        assert _detect_db_type([]) is None
