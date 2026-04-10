import os
import pytest
import sqlite3
import pandas as pd
from src.csv_ingestor import load_csv, create_connection, create_table, insert_data

# sends sample_df to a real csv file and returns the path
@pytest.fixture
def csv_file(tmp_path, sample_df):
    path = tmp_path / "people.csv"
    sample_df.to_csv(path, index=False)
    return str(path)

class TestLoadCSV:

    # test to make sure it returns correctly
    def test_returns_df(self):
        df = load_csv("data.csv")
        assert isinstance(df, pd.DataFrame)

    # testing missing files
    def test_raises_on_missing_file(self):
        with pytest.raises(FileNotFoundError):
            load_csv("doesnotexist.csv")

    # checks that file is a csv
    def test_rejects_non_csv_extension(self):
        with pytest.raises(ValueError):
            load_csv("invalid.txt")

class TestCreateConnection:

    # tests establishing connection
    def test_returns_sqlite_connection(self):
        conn = create_connection(":memory:")
        assert isinstance(conn, sqlite3.Connection)
        conn.close

    # tests for path that doesn't exist
    def test_invalid_path_raises(self):
        with pytest.raises(Exception):
            create_connection("/fake/path/data.db")
    
    # checks for empty inputs
    def test_empty_string_raises(self):
        with pytest.raises(Exception):
            create_connection("")

class TestCreateTable:

    def test_table_exists(self):
        conn = create_connection(":memory:")
        create_table(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='people'")
        assert cursor.fetchone() is not None
        conn.close()

    def test_accurate_columns(self):
        conn = create_connection(":memory:")
        create_table(conn)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info('people')")
        columns = [row[1] for row in cursor.fetchall()]
        assert "id"         in columns
        assert "first_name" in columns
        assert "last_name"  in columns
        assert "age"        in columns
        conn.close()

    def test_raises_on_closed_connection(self):
        conn = create_connection(":memory:")
        conn.close()
        with pytest.raises(Exception):
            create_table(conn)

class TestInsertData:
    def test_insert_into_nonexistent_table_raises(self):
        conn = create_connection(":memory:")
        df = pd.DataFrame({
            "first_name": ["Jane"],
            "last_name":  ["Doe"],
            "age":        [25]
        })
        with pytest.raises(Exception):
            insert_data(conn, "nonexistent", df)
        conn.close()