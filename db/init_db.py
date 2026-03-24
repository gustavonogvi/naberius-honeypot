import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "naberius.db")


#let start the db
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            ip             TEXT NOT NULL,
            port           INTEGER NOT NULL,
            timestamp      TEXT NOT NULL,
            payload        TEXT,
            country        TEXT,
            city           TEXT,
            region         TEXT,
            asn            TEXT,
            username       TEXT,
            password       TEXT,
            client_version TEXT,
            hassh          TEXT,
            hassh_algorithms TEXT
        )
    """)

    # Safe migration: adds new columns if the database already existed
    # If the column already exists, the error is silently ignored
    for column, col_type in [
        ("username", "TEXT"),
        ("password", "TEXT"),
        ("client_version", "TEXT"),
        ("hassh", "TEXT"),
        ("hassh_algorithms", "TEXT"),
    ]:
        try:
            cursor.execute(f"ALTER TABLE events ADD COLUMN {column} {col_type}")
        except sqlite3.OperationalError:
            pass  # column already exists, that's fine

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()