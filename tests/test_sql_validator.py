import sqlite3
from sql_validator import validate_select_query

conn = sqlite3.connect("database.db")

# these will be the test queries
queries = [
    "",  # Query is empty!

    "DROP TABLE people;",  # Only SELECT queries are allowed!

    "SELECT * FROM people; DROP TABLE people;",  # Only one SQL statement is allowed.

    "SELECT first_name FROM people DELETE",  # Forbidden keyword detected: delete

    "SELECT first_name",  # Missing or invalid FROM clause!

    "SELECT * FROM employees;",  # Unknown table: employees

    "SELECT salary FROM people;",  # Unknown column in SELECT: salary

    "SELECT first_name FROM people WHERE salary > 10;",  # Unknown column in WHERE: salary

    "SELECT * FROM people;",  # Valid query.

    "SELECT first_name, age FROM people;",  # Valid query.

    "SELECT first_name FROM people WHERE age > 20;"  # Valid query.
]

# test each query one by one and send a message
for q in queries:
    valid, message = validate_select_query(conn, q)
    print(q)
    print(valid, "-", message)
    print()

conn.close()