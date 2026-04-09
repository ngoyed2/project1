import os
import sys
from csv_ingestor import load_csv
from llm_adapter import translate
from query_service import list_tables, insert_data

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

# need to get access to database

# functions to handle commands other than help and exit
def load_command(csv):
    return

def ask_command(question):
    return

def sql_command(syntax):
    return

def schema_command(table):
    return

db_info = "data.csv"
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
        elif user_input.lower().strip() == "schema":
            print()
        elif user_input.lower().strip() == "ask":
            print()
        elif user_input.lower().strip() == "sql":
            print()
        elif user_input.lower().strip() == "load":
            print()
        
        elif user_input.lower().strip() == "tables":
            print()

        # handles unexpected commands
        else:
            print(user_input + " is not a command. Please enter a proper command")


if __name__ == "__main__":
    main()