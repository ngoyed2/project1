import pandas as pd
import os
import sqlite3
import logging

# setup logging to log errors
logging.basicConfig(
    filename="error_log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# part 1 is to infer schema to inspect CSV column names and type and build CREATE TABLE dynamically
# this checks for lowercase, spaces, etc
def normalize_column_name(column_name):
    return column_name.strip().lower().replace(" ", "_")

# we need a function to map data into the sqlite type
# !! dont need float because we're only using text and age numbers
def infer_sql_type(dtype):
    dtype_str = str(dtype)
    if "int" in dtype_str:
        return "INTEGER"
    else:
        return "TEXT"

# this reads the dataframe and extracts the schema, so it returns "first_name" : "TEXT", and etc
def get_schema(df):
    schema = {}
    for column in df.columns:
        normalized_name = normalize_column_name(column)
        sql_type = infer_sql_type(df[column].dtype)
        schema[normalized_name] = sql_type
    return schema

# this dynamically builds the create table statement. so if schema is "first_name" : "TEXT", then sql will become CREATE TABLE . . .
def build_create_table_sql(table_name, schema):
    columns_sql = ["id INTEGER PRIMARY KEY AUTOINCREMENT"] 
    for column_name, sql_type in schema.items():
        columns_sql.append(f"{column_name} {sql_type}")
    columns_sql_string = ", ".join(columns_sql)
    create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql_string});"
    return create_sql

# this is a function that actually runs the SQL
def create_table(conn, table_name, schema):
    try:
        cursor = conn.cursor()
        create_sql = build_create_table_sql(table_name, schema)
        cursor.execute(create_sql)
        conn.commit()
        print(f"Table '{table_name}' created successfully.")
    except Exception as e:
        logging.error(f"Error creating table '{table_name}': {e}")
        print("Error creating table. Check error_log.txt")

# part 2 is to use PRAGMA
# pragma gives info about the columns already in the table, skip the auto-generated 'id' column in the SQL table
def get_existing_table_schema(conn, table_name):
    try:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns_info = cursor.fetchall()
        schema = {}
        for column in columns_info:
            column_name = column[1] # column name
            column_type = column[2] # data type
            if column_name.lower() != "id":
                normalized_name = normalize_column_name(column_name)
                schema[normalized_name] = column_type.upper()
        return schema
    except Exception as e:
        logging.error(f"Error reading schema for table '{table_name}': {e}")
        print("Error reading existing schema. Check error_log.txt")
        return None

# before comparing the schemas, check if the table is there
def table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name=?;
    """, (table_name,))
    
    result = cursor.fetchone()
    return result is not None

# compare the schemas 
def schemas_match(csv_schema, existing_schema):
    return csv_schema == existing_schema

# build tyhe main control function that says if table doesnt exist, then create it. if table exists and the schema matches, append the data. if the table exists and the schema doesnt match, what do we do?
def handle_schema(conn, table_name, df):
    csv_schema = get_csv_schema(df)
    if not table_exists(conn, table_name):
        print(f"Table '{table_name}' does not exist. Creating new table.")
        create_table(conn, table_name, csv_schema)
        return table_name
    existing_schema = get_existing_table_schema(conn, table_name)
    if schemas_match(csv_schema, existing_schema):
        print(f"Schema matches existing table '{table_name}'. Data can be appended.")
        return table_name
    print(f"Schema conflict detected for table '{table_name}'.")
    print("Options: overwrite / rename / skip")
    choice = input("Enter your choice: ").strip().lower()
    if choice == "overwrite":
        try:
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            conn.commit()
            create_table(conn, table_name, csv_schema)
            print(f"Table '{table_name}' was overwritten.")
            return table_name
        except Exception as e:
            logging.error(f"Error overwriting table '{table_name}': {e}")
            print("Error overwriting table. Check error_log.txt")
            return None
    elif choice == "rename":
        new_table_name = input("Enter new table name: ").strip()
        create_table(conn, new_table_name, csv_schema)
        print(f"Created new table '{new_table_name}'.")
        return new_table_name
    elif choice == "skip":
        print("Skipping table creation.")
        return None
    else:
        print("Invalid choice. Skipping by default.")
        return None