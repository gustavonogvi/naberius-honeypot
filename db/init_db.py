import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "honeypot.db")


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
            client_version TEXT
        )
    """)

    # Migração segura: adiciona as colunas novas se o banco já existia
    # Se a coluna já existe, o erro é ignorado silenciosamente
    for column, col_type in [
        ("username", "TEXT"),
        ("password", "TEXT"),
        ("client_version", "TEXT"),
    ]:
        try:
            cursor.execute(f"ALTER TABLE events ADD COLUMN {column} {col_type}")
        except sqlite3.OperationalError:
            pass  # coluna já existe, tudo certo

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()