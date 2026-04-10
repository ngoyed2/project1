from query_service import list_tables

def main():
    db_file = "database.db"
    list_tables(db_file)

if __name__ == "__main__":
    main()