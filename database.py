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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
                   id INTEGER PRIMARY KEY AUTOINCREAMENT,
                   title TEXT NOT NULL,
                   description TEXT,
                   due_date TEXT,
                   priority TEXT,
                   compelete INTEGER DEFAULT 0,
                   user_id INTEGER NOT NULL,
                   FOREIGN KEY (user_id) REFERENCES users(id)
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

def get_user_by_email(email):
    connection = sqlite3.connect("planner.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE email =?" , (email,))

    user = cursor.fetchone()
    connection.close
    return user

def add_task(title, description, due_date, priority, user_id):
    connection = sqlite3.connect("planner.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tasks(
                   title, description , due_date, priority, user_id)
                   VALUES (?, ?, ?)
                   """,(
                       title, description, due_date, priority, user_id))
    connection.commit()
    connection.close()


def get_tasks(user_id):
    connection = sqlite3.connect("planner.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY due_date", (user_id))
    tasks = cursor.fetchall()
    connection.close()
    return tasks


if __name__ == "__main__":
    create_database()