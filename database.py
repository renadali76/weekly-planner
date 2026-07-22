import sqlite3

def create_database():
    connection = sqlite3.connect("planner.db")
    cursor = connection.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    # Create tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            priority TEXT,
            status TEXT DEFAULT 'Not Started',
            created_at TEXT,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
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
                   VALUES (?, ?, ?, ?, ?)
                   """,(
                       title, description, due_date, priority, user_id))
    connection.commit()
    connection.close()


def get_tasks(user_id, search="", status="", priority="", sort="due_date"):
    connection = sqlite3.connect("planner.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query = """
        SELECT *
        FROM tasks
        WHERE user_id = ?
    """

    parameters = [user_id]

    if search:
        query += """
            AND (
                title LIKE ?
                OR description LIKE ?
            )
        """
        parameters.append(f"%{search}%")
        parameters.append(f"%{search}%")

    if status:
        query += " AND status = ?"
        parameters.append(status)

    if priority:
        query += " AND priority = ?"
        parameters.append(priority)

    if sort == "priority_high":
        query += """
        ORDER BY
            CASE priority
                WHEN 'High' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'Low' THEN 3
            END
        """

    elif sort == "priority_low":
        query += """
        ORDER BY
            CASE priority
                WHEN 'Low' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'High' THEN 3
            END
        """

    elif sort == "title":
        query += " ORDER BY title ASC"

    elif sort == "title_desc":
        query += " ORDER BY title DESC"

    else:
        query += " ORDER BY due_date ASC"

        cursor.execute(query, parameters)

        tasks = cursor.fetchall()
        connection.close()
        return tasks


def delete_task(task_id, user_id):
    connection = sqlite3.connect("planner.db")
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM tasks
        WHERE id = ? AND user_id = ?
    """, (task_id, user_id))

    connection.commit()
    connection.close()

def get_task_by_id(task_id, user_id):
    connection = sqlite3.connect("planner.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id =? AND user_id = ?", (task_id, user_id))

    task = cursor.fetchone()
    connection.close()

    return task

def update_task(task_id, title, description, due_date, priority, user_id):
    connection = sqlite3.connect("planner.db")
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE tasks
        SET title = ?,
            description = ?,
            due_date = ?,
            priority = ?
        WHERE id = ? AND user_id = ?
    """, (
        title,
        description,
        due_date,
        priority,
        task_id,
        user_id
    ))

    connection.commit()
    connection.close()

def complete_task(task_id, user_id):
    connection = sqlite3.connect("planner.db")
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE tasks
        SET status = 'Completed'
        WHERE id = ? AND user_id = ?
    """, (task_id, user_id))
    connection.commit()
    connection.close()

def get_total_tasks(user_id):
    connection = sqlite3.connect("planner.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE user_id = ?
    """, (user_id,))

    total = cursor.fetchone()[0]

    connection.close()

    return total

def get_completed_tasks(user_id):
    connection = sqlite3.connect("planner.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE user_id = ?
        AND status = 'Completed'
    """, (user_id,))

    completed = cursor.fetchone()[0]

    connection.close()

    return completed

if __name__ == "__main__":
    create_database()
