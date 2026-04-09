import sqlite3
import pandas as pd
from schema_manager import handle_schema
from sql_validator import validate_select_query

# add a database connection helper
def connect_db(db_name="database.db"):
    return sqlite3.connect(db_name)

# since the slide mentions sqlite_master, we should add list tables function to show all table names
# por example, the only tables that will be outputted is people since thats all we have 
def list_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name;
    """)
    tables = cursor.fetchall()
    if not tables:
        print("No tables found.")
        return
    print("\nTables:")
    for table in tables:
        print(f"- {table[0]}")

# now create an insert_data function to load the csv
def insert_data(conn, table_name, df):
    cursor = conn.cursor()
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    placeholders = ", ".join(["?"] * len(df.columns))
    columns_sql = ", ".join(df.columns)
    insert_sql = f"INSERT INTO {table_name} ({columns_sql}) VALUES ({placeholders})"
    for _, row in df.iterrows():
        cursor.execute(insert_sql, tuple(row))
    conn.commit()
    print("Data inserted successfully.")

# now create the load_csv_flow 