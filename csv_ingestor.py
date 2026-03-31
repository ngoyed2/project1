# takes csv file and transforms it into a sql table
import pandas as pd
import sqlite3

# Step 1: Load CSV
def load_csv(file_path):
    df = pd.read_csv(file_path)
    print(df.head())  # inspect data
    return df

# Step 2: Create SQLite connection
def create_connection(db_name):
    conn = sqlite3.connect(db_name)
    return conn

# Step 3: Create table manually
def create_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        age INTEGER
    )
    """)

    conn.commit()

# Step 4: Insert data manually
def insert_data(conn, df):
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
        INSERT INTO people (first_name, last_name, age)
        VALUES (?, ?, ?)
        """, (row['first_name'], row['last_name'], row['age']))

    conn.commit()

# Main execution
def main():
    df = load_csv("data.csv")
    conn = create_connection("database.db")

    create_table(conn)
    insert_data(conn, df)

    conn.close()

if __name__ == "__main__":
    main()