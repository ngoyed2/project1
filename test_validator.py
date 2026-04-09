import sqlite3
from sql_validator import validate_select_query

conn = sqlite3.connect("database.db")

# these will be the test queries
queries = [
    "SELECT * FROM people;", # should work
    "SELECT salary FROM people;", # shouldnt work
    "SELECT first_name, age FROM people;", # should work
    "SELECT * FROM employees;", # shouldnt work
    "SELECT first_name FROM people WHERE age > 20;", # should work
    "DROP TABLE people;" # shouldnt work
]

# test each query one by one and send a message
for q in queries:
    valid, message = validate_select_query(conn, q)
    print(q)
    print(valid, "-", message)
    print()

conn.close()