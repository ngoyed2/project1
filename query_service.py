import sqlite3
import pandas as pd
from schema_manager import handle_schema
from sql_validator import validate_select_query

# query service should let the user load a csv, list tables, type a sql query, validate the sql query, then execute

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
    # get all the tables in the db
    tables = cursor.fetchall()
    # checks if the list is empty
    if not tables:
        print("No tables found!")
        return
    print("\nTables:")
    # this loops through each typle and prints the table name
    for table in tables:
        print(f"- {table[0]}")

# now create an insert_data function to load the csv
def insert_data(conn, table_name, df):
    cursor = conn.cursor()
    # normalize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    # create the placeholders
    placeholders = ", ".join(["?"] * len(df.columns))
    columns_sql = ", ".join(df.columns)
    # this is a parameterized query (and prevents sql injections-- shout out ec521 cybersecurity! :D)
    insert_sql = f"INSERT INTO {table_name} ({columns_sql}) VALUES ({placeholders})"
    # loops through each row of the df then runs the insert_sql with actual values
    for _, row in df.iterrows():
        cursor.execute(insert_sql, tuple(row))
    conn.commit()
    print("Data inserted!")

# ask the user for a csv file, preview it, let the schema manager decide what to do and then insert the data if it can
def load_csv_flow(conn):
    file_path = input("Enter CSV file path: ").strip()
    table_name = input("Enter table name: ").strip()
    try:
        df = pd.read_csv(file_path)
        print("\nCSV Preview:")
        print(df.head())
        # let schema manager decide whether to create, append, rename, or skip
        final_table_name = handle_schema(conn, table_name, df)
        # only insert if schema handling returned a valid table name
        if final_table_name:
            insert_data(conn, final_table_name, df)
    except Exception as e:
        print(f"Error loading CSV: {e}")

# execute a validated SQL query and print the results
def execute_query(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            print("\nResults:")
            for row in results:
                print(row)
        else:
            print("Query ran but returned no rows!")
    except Exception as e:
        print(f"Execution error: {e}")

# handle the workflow for accepting, validating, and running sql
def run_sql_flow(conn):
    query = input("Enter your SQL query: ").strip()
    # check to make sure that the query is valid 
    is_valid, message = validate_select_query(conn, query)
    print(message)
    if is_valid:
        execute_query(conn, query)

# the menu loop for the query service
def main():
    conn = connect_db()
    while True:
        print("\n--- Query Service ---")
        print("1. Load CSV")
        print("2. List tables")
        print("3. Run SQL query")
        print("4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            load_csv_flow(conn)
        elif choice == "2":
            list_tables(conn)
        elif choice == "3":
            run_sql_flow(conn)
        elif choice == "4":
            print("Byebye!")
            break
        else:
            print("Invalid choice, please enter 1, 2, 3, or 4!")
    conn.close()

if __name__ == "__main__":
    main()