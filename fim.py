import os
import hashlib
import sqlite3
from datetime import datetime

# Creates SQLite3 database and table for storing file metadata
def create_db():
    
    # Connect to database
    db_connection = sqlite3.connect("files.db")
    cursor = db_connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS tblFileIntegrity (
        file_id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT UNIQUE NOT NULL,
        hash TEXT NOT NULL,
        size INTEGER,
        last_modified TIMESTAMP
    );
    """

    # Create the table
    cursor.execute(create_table_query)

    # Commit changes and close connection
    db_connection.commit()
    db_connection.close()

# Calculates the Blake2 hash of a file
def blake2_hash(filepath):
    hasher = hashlib.blake2b()
    with open(filepath, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

# Traverse filesystem, hash each file, and store metadata in database
def traverse_filesystem():
    
    with sqlite3.connect("files.db") as db_connection:
        cursor = db_connection.cursor()
    
        for dirpath, dirnames, filenames in os.walk("/"):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    file_hash = blake2_hash(filepath)
                    file_size = os.path.getsize(filepath)
                    file_timestamp = os.path.getmtime(filepath)
                    file_last_modified = datetime.fromtimestamp(file_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                    
                    insert_query = """
                    INSERT INTO tblFileIntegrity (path, hash, size, last_modified) VALUES (?, ?, ?, ?);
                    """
                    try:
                        cursor.execute(insert_query, (filepath, file_hash, file_size, file_last_modified))
                    except sqlite3.IntegrityError:
                        # Handle duplicate entries without overwriting
                        print(f"Entry already exists for {filepath}, skipping.")

                except (PermissionError, FileNotFoundError, OSError) as e:
                    # Handle cases where the file can't be accessed
                    print(f"Skipping {filepath}: {e}")
        db_connection.commit()

def main():
    create_db()
    traverse_filesystem()

if __name__ == "__main__":
    main()