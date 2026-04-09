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

# this converts ourcsv into a schema dictionary, so the schema is column names + sql types, for example it returns "first_name" : "TEXT", and etc
def get_csv_schema(df):
    # make an empty dictionary first and then we will fill it
    schema = {}
    for column in df.columns:
        # not necessary for our specific data, but this will clean up the column name
        normalized_name = normalize_column_name(column)
        # this will find the sql type for the specific column
        sql_type = infer_sql_type(df[column].dtype)
        # this adds an entry to the dictionary, for example schema[age] = integer
        schema[normalized_name] = sql_type
    return schema

# this dynamically builds the create table statement. so if schema is "first_name" : "TEXT", then sql will become CREATE TABLE . . .
def build_create_table_sql(table_name, schema):
    columns_sql = ["id INTEGER PRIMARY KEY AUTOINCREMENT"] 
    # this loops through the schema dictionary and adds each column to the list
    for column_name, sql_type in schema.items():
        columns_sql.append(f"{column_name} {sql_type}")
    # this turns the list into a single string seperated by commas because sql expects col1 type, col2 type, . . .
    columns_sql_string = ", ".join(columns_sql)
    # this builds the full sql statement, the IF NOT EXISTS is not there to prevent errors if the table already exists
    create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql_string});"
    return create_sql

# this is a function that actually runs the SQL
def create_table(conn, table_name, schema):
    # we are using try and except because database operations can fail
    try:
        cursor = conn.cursor()
        # we will build the sql string using our previous function
        create_sql = build_create_table_sql(table_name, schema)
        cursor.execute(create_sql)
        conn.commit()
        print(f"Table '{table_name}' is created!")
    # we wanna catch any errors that may occur in the try block
    except Exception as e:
        logging.error(f"Error creating table '{table_name}': {e}")
        print("Error occured, check log file!")

# part 2 is to use PRAGMA
# pragma gives info about the columns already in the table, skip the auto-generated 'id' column in the SQL table
def get_existing_table_schema(conn, table_name):
    try:
        cursor = conn.cursor()
        # this asks sqlite to give information about all columns in table, then pragma returns cid, name, type, . . .
        cursor.execute(f"PRAGMA table_info({table_name});")
        # this stores all column metadata into a list 
        columns_info = cursor.fetchall()
        schema = {}
        # loop through each column returns by sqlite
        for column in columns_info:
            # extract the column name
            column_name = column[1]
            # extract the sql type
            column_type = column[2]
            # we want to skip the id column because the sql table includes id but our csv doesn't, so we gotta ignore it
            if column_name.lower() != "id":
                normalized_name = normalize_column_name(column_name)
                schema[normalized_name] = column_type.upper()
        return schema
    except Exception as e:
        logging.error(f"Error reading schema for table '{table_name}': {e}")
        print("Error occured, check log file!")
        return None

# before comparing the schemas, check if the table is there
def table_exists(conn, table_name):
    cursor = conn.cursor()
    # this asks sqlite to find a table with this exact name
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name=?;
    """, (table_name,))
    # gets the result whether the table exist, or none if the table doesn't exist
    result = cursor.fetchone()
    # returns true is table exist 
    return result is not None

# does the csv schema exactly match the existing table schema?
def schemas_match(csv_schema, existing_schema):
    return csv_schema == existing_schema

# build tyhe main control function that says if table doesnt exist, then create it. if table exists and the schema matches, append the data. if the table exists and the schema doesnt match, what do we do?
def handle_schema(conn, table_name, df):
    # build the schema dictionary for the incoming csv
    csv_schema = get_csv_schema(df)
    # this checks whether the target table already exists. if the table doesnt, create it. if it does, compare schemas
    if not table_exists(conn, table_name):
        print(f"Table '{table_name}' does not exist! Creating new table!")
        create_table(conn, table_name, csv_schema)
        return table_name
    existing_schema = get_existing_table_schema(conn, table_name)
    if schemas_match(csv_schema, existing_schema):
        print(f"Schema matches existing table '{table_name}'! Data can be appended!")
        return table_name
    # table exists but schemas don't match
    print(f"Schema conflict detected for table '{table_name}'.")
    print("Options: overwrite / rename / skip")
    # ask the user what they want to do 
    choice = input("Enter your choice: ").strip().lower()
    if choice == "overwrite":
        # this will replace the old table
        try:
            cursor = conn.cursor()
            # delete the old table from the database
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            conn.commit()
            # recreate the table with the new csv schema
            create_table(conn, table_name, csv_schema)
            print(f"Table '{table_name}' was overwritten!")
            return table_name
        except Exception as e:
            logging.error(f"Error overwriting table '{table_name}': {e}")
            print("Error occured, check log file!")
            return None
    # if the user chooses rename, create a new table with a different name 
    elif choice == "rename":
        new_table_name = input("Enter new table name: ").strip()
        create_table(conn, new_table_name, csv_schema)
        print(f"Created new table '{new_table_name}'.")
        return new_table_name
    # dont create or change any table if user chooses skip
    elif choice == "skip":
        print("Skipping table creation!")
        return None
    # they type anything else
    else:
        print("Invalid choice, skipping by default!")
        return None
    
# as of 4/8, the rows get duplicated