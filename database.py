import pymysql
import pymysql.cursors
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

def get_mysql_raw_connection():
    """Connects to MySQL server without selecting a specific database."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )

def get_mysql_connection():
    """Connects to the specified MySQL database."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )

class DatabaseManager:
    """Pure MySQL Database Manager for SecureDoc AI."""

    def __init__(self):
        self.connected = False
        self.connection_error = None
        self.init_db()

    def init_db(self):
        """Initializes database and tables strictly in MySQL."""
        try:
            # Step 1: Ensure MySQL database exists
            raw_conn = get_mysql_raw_connection()
            with raw_conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` DEFAULT CHARACTER SET utf8mb4;")
            raw_conn.close()

            # Step 2: Initialize tables in MySQL
            conn = get_mysql_connection()
            with conn.cursor() as cursor:
                # Users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(150) NOT NULL UNIQUE,
                        password_hash VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)

                # File metadata table (No PDF contents or sensitive text stored!)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS file_metadata (
                        file_id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        original_filename VARCHAR(255) NOT NULL,
                        risk_level VARCHAR(20) NOT NULL,
                        detected_count INT NOT NULL DEFAULT 0,
                        selected_action VARCHAR(50) DEFAULT 'Scanned',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)

                # Activity logs table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS activity_logs (
                        log_id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        action VARCHAR(255) NOT NULL,
                        filename VARCHAR(255) DEFAULT '',
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)
            conn.close()
            self.connected = True
            self.connection_error = None
            print(f"[MySQL] Successfully connected to MySQL at {DB_HOST}:{DB_PORT} and verified database '{DB_NAME}'.")
        except Exception as e:
            self.connected = False
            self.connection_error = f"Unable to connect to MySQL database at {DB_HOST}:{DB_PORT}. Error: {e}"
            print(f"[MySQL Connection Error] {self.connection_error}")

    def execute_query(self, query, params=()):
        """Executes a write query (INSERT, UPDATE, DELETE) on MySQL."""
        if not self.connected:
            raise RuntimeError(self.connection_error)
        conn = get_mysql_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                last_id = cursor.lastrowid
            return last_id
        finally:
            conn.close()

    def fetch_one(self, query, params=()):
        """Executes a read query returning a single row dict from MySQL."""
        if not self.connected:
            raise RuntimeError(self.connection_error)
        conn = get_mysql_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        finally:
            conn.close()

    def fetch_all(self, query, params=()):
        """Executes a read query returning all matching rows as dicts from MySQL."""
        if not self.connected:
            raise RuntimeError(self.connection_error)
        conn = get_mysql_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        finally:
            conn.close()

# Singleton instance
db = DatabaseManager()
