import sqlite3

def initializeDb(dbname):
    try:
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                book_name TEXT NOT NULL,
                author TEXT NOT NULL
            )
        ''')

        conn.commit()
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

def PopuDb(NameAuthorAndBook, dbname):
    try:
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()

        for book_info in NameAuthorAndBook:
            book_name, author_name = book_info
            cursor.execute('''
                INSERT INTO books (book_name, author) VALUES (?, ?)
            ''', (book_name, author_name))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Error populating database: {e}")
    finally:
        if conn:
            conn.close()

def ReadDb(dbname):
    try:
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()  # Fetch all rows from the query result

        for row in rows:
            print(row)  # Print each row

    except sqlite3.Error as e:
        print(f"Error reading database: {e}")

    finally:
        if conn:
            conn.close()

def cleardb(dbname, table_name):
    try:
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()

        # Execute DELETE statement to clear all rows from the table
        cursor.execute(f"DELETE FROM {table_name}")

        conn.commit()
        print(f"All data cleared from {table_name} in {dbname}")

    except sqlite3.Error as e:
        print(f"Error clearing database: {e}")

    finally:
        if conn:
            conn.close()

def main(NameAuthorAndBook, dbname,Table):
    initializeDb(dbname)
    while True:
        print("\nList of actions:\nClearDb\nPopulateDb\nReadDb\nExit")
        action = input("What action would you like to execute: ").strip().upper()

        if action == "EXIT":
            print("Exiting program...")
            break
        elif action == "CLEARDB":
            cleardb(dbname, Table)
        elif action == "POPULATEDB":
            PopuDb(NameAuthorAndBook, dbname)
        elif action == "READDB":
            ReadDb(dbname)
        else:
            print("Invalid action. Please choose from the provided options.")


if __name__ == "__main__":
    NameAuthorAndBook = [
        ('Moonwalking With Einstein', 'Author1'),
        ('Adventures In Numberland', 'Author2'),
        ('MegaMemory', 'Author3')
    ]
    dbname = "bookstore.db"
    Table = "books"
    main(NameAuthorAndBook, dbname,Table)
