import sqlite3

def create_database():
    print("Starting database creation...")

    connection = sqlite3.connect("planner.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

    print("Database created successfully!")

def add_user(username, email, password):
    connection = sqlite3.connect("planner.db")
    cursor = connection.cursor()

    cursor.execute("""
            INSERT INTO users(username, email, password) VALUES (?, ?, ?)      
    """,(username, email, password))

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_database()