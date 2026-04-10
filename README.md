system overview
how to run the project
how to run tests

# Building Data Systems with LLM Interfaces

## System Overview:

In this project, our goals are to build a system that:
- Loads structured data into a SQL database
- Allows users to query data via natural language
- Uses an LLM to translate queries into SQL
- Executes queries safely and returns results

Our project implements a command-line main menu system that allows users to:
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
