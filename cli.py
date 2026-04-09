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

db_info = "data.csv"
def main():
    # main function that contains operative aspect of system
    print("HELLO! WELCOME TO OUR LLM ASSISTED DATA SYSTEM!\n")
    print(commands) # displays options for user
    print("\n")
    while True:
        user_input = input("Please enter a command: ")
        if user_input.lower().strip() == "exit":
            print("GOODBYE!")
            break
        elif user_input.lower().strip() == "help":
            print(commands)
        else:
            print("you said: " + user_input)

if __name__ == "__main__":
    main()