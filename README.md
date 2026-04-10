how to run tests

# Building Data Systems with LLM Interfaces: Project 1

## System Overview:

In this project, our goals are to build a system that:
- Loads structured data into a SQL database
- Allows users to query data via natural language
- Uses an LLM to translate queries into SQL
- Executes queries safely and returns results

Our project implements a command-line interface system that allows users to:
1. Load CSV files into a SQLite database
2. List all the tables in the database
3. Run SQL queries safely using a validator
4. Ask questions in natural language, which are converted to SQL using an LLM
5. Safetly exit the system

In this project, we want to file this specific flow of responsibility:
Flow of Responsibility: CLI → Query Service → LLM Adapter → Validator → DB
Two independent flows: data ingestion and query processing

Based on the system architecture shown above, our essential project files includes:
- **CSV Ingestor**: Loads CSV files and converts them into database tables
- **Schema Manager**: Handles schema creation, validation, and conflicts
- **Query Service (CLI)**: Main interface for user interaction
- **SQL Validator**: Ensures only safe and valid SQL queries are executed
- **LLM Adapter**: Converts natural language into SQL queries
---
## How to Run the Project:

### 1. Install all dependencies
- Make sure you have Python installed!
- Run the following in your terminal:
``` bash
pip install pandas python-dotenv
```
---
### 2. Set up LLM API key:
⚠️ This part is optional-- you can use a mock LLM instead!
If you want to use the natural language feature with an actual LLM, you must set up an API key.
To do so, do the following:
1. Create a file in the project root called ".env".
2. Add your API key in the file: OPENAI_API_KEY=add_your_api_key_here
---
### 3. Run the program:

In your terminal, run the following: ``` python cli.py ```. You will then be met with our main menu system that prompts the following commands:
1. help -> shows user commands
2. load -> allows user to input CSV file
3. ask -> lets user ask question in natural language
4. sql -> execute sql command directly
5. tables -> show all current tables
6. schema <table> -> show schema for table
7. exit -> quit
---
### 4. Example workflow:
1. Type in `load`
2. Enter in your .csv file (in our case, data.csv)
3. Enter your table name (in our case, people)
4. Type in `sql`
5. Enter in the following sql query (all data from the table should be displayed): ``` sql SELECT * FROM people; ```
6. If you have LLM API set up, type in `ask`
7. Enter in the following sql query (this will display all the people older than 20): ``` sql show all people older than 20 ```
---
## How to Run the Tests:
