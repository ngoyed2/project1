import sqlite3
import pytest
import os
import pandas as pd
from query_service import list_tables, insert_data, execute_query

test_db = "test_database.db"

# create a temporary in-memory database for clean and fast data
def setup_test_db():
    if os.path.exists(test_db):
        os.remove(test_db)
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            age INTEGER
        );
    """)
    conn.commit()
    conn.close()

# remove test db after each test
def teardown_test_db():
    if os.path.exists(test_db):
        os.remove(test_db)

# test listing tables first
def test_list_tables(capsys):
    setup_test_db()
    list_tables(test_db)
    captured = capsys.readouterr()
    # looks for "people" in output
    assert "people" in captured.out
    teardown_test_db()

# test inserting data next
def test_insert_data(capsys):
    conn = setup_test_db()
    df = pd.DataFrame({
        "first_name": ["Alice", "Bob"],
        "age": [25, 30]
    })
    insert_data(test_db, "people", df)
    # verify data was inserted
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people;")
    results = cursor.fetchall()
    assert len(results) == 2
    captured = capsys.readouterr()
    assert "Data inserted!" in captured.out
    conn.close()
    teardown_test_db()

# test executing a valid query
def test_execute_query_valid(capsys):
    setup_test_db()
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO people (first_name, age) VALUES ('Alice', 25);")
    conn.commit()
    execute_query(conn, "SELECT * FROM people;")
    captured = capsys.readouterr()
    assert "Alice" in captured.out
    conn.close()
    teardown_test_db()

# test executing query with no results
def test_execute_query_no_results(capsys):
    setup_test_db()
    conn = sqlite3.connect(test_db)
    execute_query(conn, "SELECT * FROM people WHERE age > 100;")
    captured = capsys.readouterr()
    assert "returned no rows" in captured.out
    conn.close()
    teardown_test_db()

# test executing invalid query
def test_execute_query_invalid(capsys):
    setup_test_db()
    conn = sqlite3.connect(test_db)
    execute_query(conn, "SELECT * FROM unknown_table;")
    captured = capsys.readouterr()
    assert "Execution error" in captured.out
    conn.close()
    teardown_test_db()