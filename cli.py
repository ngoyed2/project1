import os
import sys
import sqlite3
from csv_ingestor import csv_to_sql
from query_service import list_tables, insert_data # can only access csv and query modules directly

commands = """
Commands:

help -> shows user commands
load <csv> -> allows user to input CSV file
ask <question> -> lets user ask question in natural language
sql <command> -> execute sql command directly
tables -> show all current tables
schema <table> -> show schema for table
exit -> quit

"""

db = "database.db"

# need to get access to database

# functions to handle commands other than help and exit
def load_command(args: str, csv:str):
    try:
        loaded_csv = csv_to_sql(csv,db)
        table_name = loaded_csv["final_table_name"]
        print("Your table named " + " has been successfully loaded!")
    except FileNotFoundError as e:
        print("Error: " + e)

# function utilizing LLM for user to ask natural language question    
def ask_command(question):
    # once llm function is imported to query service, input here along with schema to fun
    return

def sql_command(syntax):
    return

def schema_command(table):
    return

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
            print()
        elif user_input.lower().strip().startswith("ask"):
            print("test")
        elif user_input.lower().strip().startswith("sql"):
            print()
        elif user_input.lower().strip().startswith("load"):
            command, csv = user_input.split(" ")
            print("\n")
            print(load_command(command, csv))
        elif user_input.lower().strip().startswith("tables"):
            print()

        # handles unexpected commands
        else:
            print(user_input + " is not a command. Please enter a proper command")


if __name__ == "__main__":
    main()