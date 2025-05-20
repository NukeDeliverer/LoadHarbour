import threading

db_lock = threading.Lock()

def save_file_to_db(filename, content, db):
    # content should be bytes
    with db_lock:
        cursor = db.cursor()
        cursor.execute("INSERT INTO files (filename, content) VALUES (?, ?)", (filename, content))
        db.commit()

def get_all_files(db):
    with db_lock:
        cursor = db.cursor()
        cursor.execute("SELECT filename FROM files")
        return [row[0] for row in cursor.fetchall()]  # Return only filenames as list of strings

def get_file_by_name(filename, db):
    with db_lock:
        cursor = db.cursor()
        cursor.execute("SELECT filename, content FROM files WHERE filename = ?", (filename,))
        result = cursor.fetchone()
        if result:
            name, content = result
            return name, content  # Return raw bytes for file content
        return None
def delete_file_by_name(filename, db):
    with db_lock:
        cursor = db.cursor()
        cursor.execute("DELETE FROM files WHERE filename = ?", (filename,))
        db.commit()
        return cursor.rowcount  # returns number of deleted rows (0 if not found)
