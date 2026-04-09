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
def normalize_column_name(column_name):
    return column_name.strip().lower().replace(" ", "_")

def infer_sql_type(dtype):
    dtype_str = str(dtype)

    if "int" in dtype_str:
        return "INTEGER"
    elif "float" in dtype_str:
        return "REAL"
    else:
        return "TEXT"

def normalize_column_name(column_name):
    return column_name.strip().lower().replace(" ", "_")
 
def get_csv_schema(df):
    schema = {}

    for column in df.columns:
        normalized_name = normalize_column_name(column)
        sql_type = infer_sql_type(df[column].dtype)
        schema[normalized_name] = sql_type

    return schema

def build_create_table_sql(table_name, schema):
    columns_sql = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]

    for column_name, sql_type in schema.items():
        columns_sql.append(f"{column_name} {sql_type}")

    columns_sql_string = ", ".join(columns_sql)

    create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql_string});"
    return create_sql

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