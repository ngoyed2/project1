import os
import sys
import sqlite3
from query_service import list_tables, load_csv_flow, run_sql_flow, run_nl_flow, get_schema # can only access csv and query modules directly

commands = """
Commands:

help -> shows user commands
load -> allows user to input CSV file
ask -> lets user ask question in natural language
sql -> execute sql command directly
tables -> show all current tables
schema <table> -> show schema for table
exit -> quit

"""

db = "database.db"

conn = sqlite3.connect(db)

def main():
    # main function that contains operative aspect of system
    print("\nHELLO! WELCOME TO OUR LLM ASSISTED DATA SYSTEM!")
    print(commands) # displays options for user
    while True:
        user_input = input("Please enter a command: ")
        if user_input.lower().strip() == "exit":
            print("GOODBYE!")
            break

        # connect these inputs to functions probably, instead of putting all code in one place
        elif user_input.lower().strip() == "help":
            print(commands)
        elif user_input.lower().strip().startswith("schema"):
            result = get_schema(conn)
            print(result)
        elif user_input.lower().strip().startswith("ask"):
            result = run_nl_flow(conn)
            print(result)
        elif user_input.lower().strip().startswith("sql"):
            result = run_sql_flow(conn)
            print(result)
        elif user_input.lower().strip().startswith("load"):
            result = load_csv_flow(conn)
            print(result)
        elif user_input.lower().strip().startswith("tables"):
            result = list_tables(conn)
            print(result)

        # handles unexpected commands
        else:
            print(user_input + " is not a command. Please enter a proper command")


if __name__ == "__main__":
    main()