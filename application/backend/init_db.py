from mysql.connector import Error

from config import Config
from database import get_connection


def initialize_database():
    connection = get_connection(Config.DB_NAME)
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INT NOT NULL AUTO_INCREMENT,
            title VARCHAR(255) NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id)
        )
        """
    )
    connection.commit()
    cursor.close()
    connection.close()
    print("Database and tasks table are ready.")


if __name__ == "__main__":
    try:
        initialize_database()
    except Error as error:
        print("Table initialization failed: {}".format(error))
        raise SystemExit(1)
