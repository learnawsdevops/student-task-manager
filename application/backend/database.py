import mysql.connector
from mysql.connector import Error
from config import Config


def get_connection(db_name=None):
    from config import Config

    settings = {
        "host": Config.DB_HOST,
        "port": Config.DB_PORT,
        "user": Config.DB_USER,
        "password": Config.DB_PASSWORD,
        "connection_timeout": 5,
    }
    if db_name:
        settings["database"] = db_name
    return mysql.connector.connect(**settings)


def database_health():
    connection = None
    cursor = None
    try:
        connection = get_connection(Config.DB_NAME)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, title, completed, created_at FROM tasks LIMIT 0"
        )
        return True
    except Error:
        return False
    finally:
        try:
            if cursor is not None:
                cursor.close()
        finally:
            if connection is not None:
                connection.close()


def fetch_tasks():
    connection = get_connection(Config.DB_NAME)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, title, completed, created_at "
        "FROM tasks ORDER BY id ASC"
    )
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()
    return tasks


def create_task(title):
    connection = get_connection(Config.DB_NAME)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO tasks (title, completed) VALUES (%s, FALSE)",
        (title,),
    )
    task_id = cursor.lastrowid
    connection.commit()
    cursor.execute(
        "SELECT id, title, completed, created_at "
        "FROM tasks WHERE id = %s",
        (task_id,),
    )
    task = cursor.fetchone()
    cursor.close()
    connection.close()
    return task


def update_task(task_id, completed):
    connection = get_connection(Config.DB_NAME)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "UPDATE tasks SET completed = %s WHERE id = %s",
        (completed, task_id),
    )
    connection.commit()
    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        return None
    cursor.execute(
        "SELECT id, title, completed, created_at "
        "FROM tasks WHERE id = %s",
        (task_id,),
    )
    task = cursor.fetchone()
    cursor.close()
    connection.close()
    return task


def delete_task(task_id):
    connection = get_connection(Config.DB_NAME)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    connection.commit()
    deleted = cursor.rowcount > 0
    cursor.close()
    connection.close()
    return deleted
