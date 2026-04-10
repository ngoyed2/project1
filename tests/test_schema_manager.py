import sqlite3
import pytest
import pandas as pd
from unittest.mock import patch
from schema_manager import handle_schema, get_csv_schema, table_exists, schemas_match

# helper functions to make connections/df for later testing
def make_connection():
    return sqlite3.connect(":memory:")

def make_df():
    return pd.DataFrame({
        "first_name": ["Obama", "Clinton"],
        "age": [25, 30]
    })

class TestSchemaManager:

    def test_creates_table_if_not_exists(self):
        conn = make_connection()
        result = handle_schema(conn, "people", make_df())
        assert result == "people"
        assert table_exists(conn, "people")

    def test_returns_table_name_if_schema_matches(self):
        conn = make_connection()
        handle_schema(conn, "people", make_df())
        result = handle_schema(conn, "people", make_df())
        assert result == "people"

    def test_detects_schema_mismatch(self):
        csv_schema = {"first_name": "TEXT", "age": "INTEGER"}
        db_schema  = {"first_name": "TEXT", "salary": "INTEGER"}
        assert schemas_match(csv_schema, db_schema) is False

    def test_overwrite_on_conflict(self):
        conn = make_connection()
        handle_schema(conn, "people", make_df())
        df2 = pd.DataFrame({"email": ["a@b.com"]})
        # used to handle user input aspect of code, replaces it with value we input
        with patch("builtins.input", return_value="overwrite"):
            result = handle_schema(conn, "people", df2)
        assert result == "people"

    def test_rename_on_conflict(self):
        conn = make_connection()
        handle_schema(conn, "people", make_df())
        df2 = pd.DataFrame({"email": ["a@b.com"]})
        # used to handle user input aspect of code, replaces it with value we input 
        with patch("builtins.input", side_effect=["rename", "people_v2"]):
            result = handle_schema(conn, "people", df2)
        assert result == "people_v2"

    def test_skip_returns_none(self):
        conn = make_connection()
        handle_schema(conn, "people", make_df())
        df2 = pd.DataFrame({"email": ["a@b.com"]})
        # used to handle user input aspect of code, replaces it with value we input
        with patch("builtins.input", return_value="skip"):
            result = handle_schema(conn, "people", df2)
        assert result is None

    def test_csv_schema_infers_correct_types(self):
        schema = get_csv_schema(make_df())
        assert schema["first_name"] == "TEXT"
        assert schema["age"] == "INTEGER"