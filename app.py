import sqlite3

DB = "students.db"

def get_db_connection():
    conn = sqlite3.connect(DB)
    # This line makes SQLite behave like the MySQL dictionary cursor
    conn.row_factory = sqlite3.Row 
    return conn
