import re
import sqlite3

# right now our validator rules only allows select columns from table
# the validator needs to check if the table exists, if the columns exist, 

# define a function to get the database schema, the validator needs to know what tables exist and what columns each table has
# por ejemplo, if the db has the table people, itll return id, first name, . . .
def get_database_schema(conn):
    cursor = conn.cursor()
    # get all table names
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name;
    """)
    # extract only the table names by grabbing only the first element of each tuple
    tables = [row[0] for row in cursor.fetchall()]
    schema = {}
    for table in tables:
        # this asks sqlite what columns are in the specific table
        cursor.execute(f"PRAGMA table_info({table});")
        # extract only the column names 
        columns = [row[1] for row in cursor.fetchall()]
        # builds the mapping schema[people] = [id, firstname, . . .]
        schema[table] = columns
    return schema

# we want to reject the input we don't want. we only want to accept SELECT from already existing columns
# this will block non-select queries, multiple statements, and write operations
def basic_select_check(query):
    # this removes any extra whitespace to clean up the query
    query = query.strip()
    # check if empty
    if not query:
        return False, "Query is empty!"
    # this created a lowercased version of the query because capitalization matters, so SELECT or select should work
    lowered = query.lower()
    # if the query doesnt use select, then its automatically rejected
    if not lowered.startswith("select"):
        return False, "Only SELECT queries are allowed!"
    # multiple semicolons means that multiple query statements are being used, which we want to reject
    if ";" in query[:-1]:
        return False, "Only one SQL statement is allowed."
    # this is all of the dangerous keyworks
    forbidden = ["insert", "update", "delete", "drop", "alter", "create"]
    for word in forbidden:
        # check if word matches exacrtly, if not then detect the forbidden keyword
        if re.search(rf"\b{word}\b", lowered):
            return False, f"Forbidden keyword detected: {word}"
    return True, "Query check passed!"

# now we want to extract the table name from FROM
# por ejemplo, for SELECT first_name from people WHERE age > 20, this returns people
def extract_table_name(query):
    # all of this finds the table name after FROM
    match = re.search(r"\bfrom\s+([a-zA-Z_][a-zA-Z0-9_]*)", query, re.IGNORECASE)
    if match:
        # return the captured part
        return match.group(1)
    return None

# now we should extract whatever is between SELECT and FROM
# por ejemplo, SELECT first_name, age FROM people will return first_name and age
def extract_selected_columns(query):
    match = re.search(r"select\s+(.*?)\s+from\b", query, re.IGNORECASE)
    if not match:
        return None
    raw_columns = match.group(1).strip()
    # special case is if the in between has *
    if raw_columns == "*":
        return ["*"]
    columns = [col.strip() for col in raw_columns.split(",")]
    return columns

# and now we want to parse columns used in WHERE
# por ejemplo, SELECT first_name FROM people WHERE age > 20 will return age
def extract_where_columns(query):
    match = re.search(r"\bwhere\s+(.*?)(\blimit\b|$)", query, re.IGNORECASE)
    if not match:
        return []
    where_clause = match.group(1)
    # this looks for column_name operator
    columns = re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*(=|!=|<|>|<=|>=)", where_clause)
    return [col[0] for col in columns]

# put everything together and build the validator
def validate_select_query(conn, query):
    # this is a basic safety check that stops the validator if anything is invalid
    ok, message = basic_select_check(query)
    if not ok:
        return False, message
    schema = get_database_schema(conn)
    table_name = extract_table_name(query)
    # if missing
    if not table_name:
        return False, "Missing or invalid FROM clause!"
    # if table doesn't exist
    if table_name not in schema:
        return False, f"Unknown table: {table_name}"
    valid_columns = schema[table_name]
    # validate select columns
    selected_columns = extract_selected_columns(query)
    # if parsing fails
    if selected_columns is None:
        return False, "Could not parse selected columns."
    # if not *, check each column
    if selected_columns != ["*"]:
        for col in selected_columns:
            if col not in valid_columns:
                return False, f"Unknown column in SELECT: {col}"
    # validate where columns
    where_columns = extract_where_columns(query)
    for col in where_columns:
        if col not in valid_columns:
            return False, f"Unknown column in WHERE: {col}"
    # if everything passes
    return True, "Valid query!"