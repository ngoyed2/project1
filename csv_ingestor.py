# takes csv file and transforms it into a sql table
import pandas as pd
import sqlite3

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
def insert_data(connection, df):
    cursor = connection.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
        INSERT INTO people (first_name, last_name, age)
        VALUES (?, ?, ?)
        """, (row['first_name'], row['last_name'], row['age']))

    connection.commit()

# main
def main():
    df = load_csv("data.csv")
    connection = create_connection("database.db")

    create_table(connection)
    insert_data(connection, df)

    connection.close()

if __name__ == "__main__":
    main()