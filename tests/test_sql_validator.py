import sqlite3
from sql_validator import(get_database_schema,
    basic_select_check,
    extract_table_name,
    extract_selected_columns,
    extract_where_columns,
    validate_select_query,)

# used to establish sqlite connection to allow for tests
def make_connection():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE people (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            age INTEGER
        )
    """)
    conn.commit()
    return conn

class TestGetDBSchema:
    def test_table_with_no_columns(self):
        # edge case — sqlite allows tables with no columns in some versions
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE empty_table (id INTEGER)")
        schema = get_database_schema(conn)
        assert "empty_table" in schema

    def test_table_name_with_numbers(self):
        # table names can have numbers — should still be found
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE table_123 (id INTEGER)")
        schema = get_database_schema(conn)
        assert "table_123" in schema

    def test_does_not_return_sqlite_internal_tables(self):
        # sqlite_master and other internals should not appear
        conn = make_connection()
        schema = get_database_schema(conn)
        assert "sqlite_master" not in schema
        assert "sqlite_sequence" not in schema

class TestBasicSelect:
    def test_select_disguised_as_comment(self):
        # injection attempt hiding DROP inside a comment
        ok, msg = basic_select_check("SELECT * FROM people -- DROP TABLE people")
        assert ok is True  # comment is safe, documents expected behaviour

    def test_non_select_rejected(self):
        ok, msg = basic_select_check("DROP TABLE people")
        assert ok is False

    def test_multiple_statements_rejected(self):
        ok, msg = basic_select_check("SELECT * FROM people; DROP TABLE people")
        assert ok is False

class TestTableName:
    def test_extracts_table_name(self):
        assert extract_table_name("SELECT * FROM people") == "people"

    def test_no_from_returns_none(self):
        assert extract_table_name("SELECT * people") is None

    def test_with_where_clause(self):
        assert extract_table_name("SELECT * FROM people WHERE age > 20") == "people"

class TestColumns:
    def test_star(self):
        assert extract_selected_columns("SELECT * FROM people") == ["*"]

    def test_multiple_columns(self):
        result = extract_selected_columns("SELECT first_name, age FROM people")
        assert result == ["first_name", "age"]

    def test_no_from_returns_none(self):
        assert extract_selected_columns("SELECT first_name") is None

class TestExtractWhereColumns:
    def test_extracts_where_column(self):
        result = extract_where_columns("SELECT * FROM people WHERE age > 20")
        assert "age" in result

    def test_no_where_returns_empty(self):
        result = extract_where_columns("SELECT * FROM people")
        assert result == []

    def test_multiple_where_columns(self):
        result = extract_where_columns("SELECT * FROM people WHERE age > 20 AND id = 1")
        assert "age" in result
        assert "id" in result

class TestValidateSelect:
    def test_valid_query_passes(self):
        conn = make_connection()
        ok, msg = validate_select_query(conn, "SELECT * FROM people")
        assert ok is True

    def test_unknown_table_fails(self):
        conn = make_connection()
        ok, msg = validate_select_query(conn, "SELECT * FROM employees")
        assert ok is False
        assert "employees" in msg

    def test_unknown_column_fails(self):
        conn = make_connection()
        ok, msg = validate_select_query(conn, "SELECT salary FROM people")
        assert ok is False
        assert "salary" in msg

