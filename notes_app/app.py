import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "notes.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, title TEXT NOT NULL, body TEXT)")
    return conn


def add_note(title: str, body: str) -> int:
    conn = get_conn()
    cur = conn.execute("INSERT INTO notes (title, body) VALUES (?, ?)", (title, body))
    conn.commit()
    note_id = cur.lastrowid
    conn.close()
    return note_id


def list_notes() -> list[tuple]:
    conn = get_conn()
    rows = conn.execute("SELECT id, title, body FROM notes ORDER BY id").fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    add_note("hello", "world")
    for row in list_notes():
        print(row)
