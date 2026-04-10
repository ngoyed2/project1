# takes csv file and transforms it into a sql table
import os
import pandas as pd
import sqlite3
from src.schema_manager import handle_schema

# step 1 is to load the csv
def load_csv(file_path):
    if not file_path:
        raise ValueError("File path cannot be empty")
    if not file_path.endswith(".csv"):
        raise ValueError("Invalid file type, must be .csv file")
    if not os.path.exists(file_path):
        raise FileNotFoundError("File not found")
    # instructions said to use pandas.read_csv() to load data
    df = pd.read_csv(file_path)
    print(df.head())
    return df

# step 2 is to connect with sqlite
def create_connection(db_name):
    if not db_name:
        raise ValueError("Database path cannot be empty")
    connection = sqlite3.connect(db_name)
    return connection

# step 3 is to create our table. it is based on our basic csv file
# we do not need this function anymore since we have handle_schema!!!
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

# def csv_to_sql(csv:str, database:str):
#     df = load_csv(csv)
#     connection = create_connection(database)
#     # determines name for the table based on csv name
#     table_name = csv.split(".")[0].replace(" ","_")
#     # this sends our connection, table name and dataframe to the schema manager
#     final_table_name = handle_schema(connection, table_name, d
# f)
#     # if the schema manager changed the table in any way, we want to insert the new table name
#     insert_data(connection, final_table_name, df)
#     connection.close()

#     return {
#         "connection": connection,
#         "final_table_name": final_table_name,
#         "dataframe": df
#     }

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