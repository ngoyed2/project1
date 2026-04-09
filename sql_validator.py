import re
import sqlite3

# right now our validator rules only allows select columns from table

# define a simple api, this is the main function our query service will call, should return true/false
def validate_select_query(conn, query):
    pass

# define a function to get the database schema, the validator needs to know what tables exist and what columns each table has
# por example, if the db has the table people, itll most likely return all the columns in people
def get_database_schema(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name;
    """)
    tables = [row[0] for row in cursor.fetchall()]
    schema = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [row[1] for row in cursor.fetchall()]
        schema[table] = columns
    return schema

# we want to reject the input we don't want. we only want to accept SELECT from already existing columns
# this will block non-select queries, multiple statements, and write operations
def basic_select_check(query):
    query = query.strip()
    if not query:
        return False, "Query cannot be empty."
    lowered = query.lower()
    if not lowered.startswith("select"):
        return False, "Only SELECT queries are allowed."
    if ";" in query[:-1]:
        return False, "Only one SQL statement is allowed."
    forbidden = ["insert", "update", "delete", "drop", "alter", "create"]
    for word in forbidden:
        if re.search(rf"\b{word}\b", lowered):
            return False, f"Forbidden keyword detected: {word}"
    return True, "Passed."

# now we want to extract the table name from FROM
# por example, for SELECTR first_name from people WHERE age > 20, this returns people
def extract_table_name(query):
    match = re.search(r"\bfrom\s+([a-zA-Z_][a-zA-Z0-9_]*)", query, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

# now we should extract whatever is between SELECT and FROM
# por example, SELECT first_name, age FROM people will return first_name and age
def extract_selected_columns(query):
    match = re.search(r"select\s+(.*?)\s+from\b", query, re.IGNORECASE)
    if not match:
        return None
    raw_columns = match.group(1).strip()
    if raw_columns == "*":
        return ["*"]
    columns = [col.strip() for col in raw_columns.split(",")]
    return columns