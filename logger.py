from database import db

def log_activity(user_id: int, action: str, filename: str = ""):
    """Logs user actions into the activity_logs database table."""
    try:
        db.execute_query(
            "INSERT INTO activity_logs (user_id, action, filename) VALUES (%s, %s, %s)",
            (user_id, action, filename)
        )
    except Exception as e:
        print(f"[Error] Failed to log activity: {e}")

def get_user_activity_logs(user_id: int, limit: int = 50):
    """Retrieves recent activity logs for a specific user."""
    try:
        return db.fetch_all(
            "SELECT * FROM activity_logs WHERE user_id = %s ORDER BY timestamp DESC LIMIT %s",
            (user_id, limit)
        )
    except Exception as e:
        print(f"[Error] Failed to fetch activity logs: {e}")
        return []

def log_file_metadata(user_id: int, filename: str, risk_level: str, detected_count: int, action: str = "Scanned"):
    """Saves file scan metadata into the database."""
    try:
        file_id = db.execute_query(
            "INSERT INTO file_metadata (user_id, original_filename, risk_level, detected_count, selected_action) "
            "VALUES (%s, %s, %s, %s, %s)",
            (user_id, filename, risk_level, detected_count, action)
        )
        return file_id
    except Exception as e:
        print(f"[Error] Failed to save file metadata: {e}")
        return None

def update_file_action(file_id: int, action: str):
    """Updates the action performed on a processed file."""
    try:
        db.execute_query(
            "UPDATE file_metadata SET selected_action = %s WHERE file_id = %s",
            (action, file_id)
        )
    except Exception as e:
        print(f"[Error] Failed to update file action: {e}")

def get_user_file_history(user_id: int):
    """Retrieves processed file history metadata for a specific user."""
    try:
        return db.fetch_all(
            "SELECT * FROM file_metadata WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,)
        )
    except Exception as e:
        print(f"[Error] Failed to fetch file history: {e}")
        return []
