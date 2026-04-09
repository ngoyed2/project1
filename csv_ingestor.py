# takes csv file and transforms it into a sql table
import pandas as pd
import sqlite3
from schema_manager import handle_schema

# step 1 is to load the csv
def load_csv(file_path):
    # instructions said to use pandas.read_csv() to load data
    df = pd.read_csv(file_path)
    print(df.head())
    return df

# step 2 is to connect with sqlite
def create_connection(db_name):
    connection = sqlite3.connect(db_name)
    return connection

# step 3 is to create our table. it is based on our basic csv file
def create_table(connection):
    # cursor sends sql commands to sqlite
    cursor = connection.cursor()
    # create our table with the data columns and the correct data type
    # slides say to add integer primary key column
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        age INTEGER
    )
    """)
    connection.commit()

# step 4 is to insert the data into sqlite
def insert_data(connection, table_name, df):
    cursor = connection.cursor()
    # create the placeholders for sql insertion for parameterized queries
    placeholders = ", ".join(["?"] * len(df.columns))
    # create a comma-separated list of the column names
    columns_sql = ", ".join(df.columns)
    # this helps to work with multiple tables without needing to hardcode the column names every single time
    insert_sql = f"INSERT INTO {table_name} ({columns_sql}) VALUES ({placeholders})"
    # pandas returns the row index and contents for each row to insert them into the sql table
    for _, row in df.iterrows():
        cursor.execute(insert_sql, tuple(row))
    connection.commit()
    print("Data inserted!")

# main
def main():
    df = load_csv("data.csv")
    connection = create_connection("database.db")
    # for this project we'll name our table "people"
    table_name = "people"
    # this sends our connection, table name and dataframe to the schema manager
    final_table_name = handle_schema(connection, table_name, df)
    # if the schema manager changed the table in any way, we want to insert the new table name
    insert_data(connection, final_table_name, df)
    connection.close()

if __name__ == "__main__":
    main()