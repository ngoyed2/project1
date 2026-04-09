# takes csv file and transforms it into a sql table
import pandas as pd
import sqlite3
from schema_manager import handle_schema

# step 1 is to load the csv
def load_csv(file_path):
    df = pd.read_csv(file_path)
    print(df.head())
    return df

# step 2 is to create a sqlite connection
def create_connection(db_name):
    connection = sqlite3.connect(db_name)
    return connection

# step 3 is to create the table
def create_table(connection):
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        age INTEGER
    )
    """)

    connection.commit()

# step 4 is to insert the data manually using the code
def insert_data(connection, table_name, df):
    cursor = connection.cursor()
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    placeholders = ", ".join(["?"] * len(df.columns))
    columns_sql = ", ".join(df.columns)
    insert_sql = f"INSERT INTO {table_name} ({columns_sql}) VALUES ({placeholders})"
    for _, row in df.iterrows():
        cursor.execute(insert_sql, tuple(row))
    connection.commit()
    print("Data inserted successfully.")

# main
def main():
    df = load_csv("data.csv")
    connection = create_connection("database.db")

    table_name = "people"

    final_table_name = handle_schema(connection, table_name, df)

    create_table(connection)
    insert_data(connection, final_table_name, df)

    connection.close()

if __name__ == "__main__":
    main()