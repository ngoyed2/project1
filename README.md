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

In your terminal, run `python cli.py`. You will then be met with a main menu with the following commands:

1. `help` – shows user commands
2. `load` – allows user to input CSV file
3. `ask` – lets user ask a question in natural language
4. `sql` – execute SQL command directly
5. `tables` – show all current tables
6. `schema <table>` – show schema for table
7. `exit` – quit

---

### 4. Example workflow:

1. Type `load`
2. Enter your `.csv` file (e.g. `data.csv`)
3. Enter your table name (e.g. `people`)
4. Type `sql`
5. Enter: `SELECT * FROM people;`
6. If you have the LLM API set up, type `ask`
7. Enter: `show all people older than 20`

---

## How to Run the Tests:
This project uses `pytest` for testing.

### 1. Install pytest 
Enter the following command in your terminal: ``` pip install pytest ```

### 2. Run pytests for each file
You can enter in the following commands in your terminal as an example:
```pytest test_query_service.py```
```pytest test_schema_manager.py ```
```pytest test_sql_validator.py ```
- Make sure the root of each of your test file is in the correct place! We want pytest to be able to find the file!

### Why is this important?
The tests cover:
- CSV ingestion and data insertion
- Schema management and validation
- SQL query validation
- Query execution
- LLM response parsing
If everything is working correctly, you should see something like: ```X passed in X.XXs ```
