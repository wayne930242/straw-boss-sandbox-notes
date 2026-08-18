import json
import sqlite3
import sys
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


def delete_note(note_id: int) -> bool:
    conn = get_conn()
    cur = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted


def list_notes() -> list[tuple]:
    conn = get_conn()
    rows = conn.execute("SELECT id, title, body FROM notes ORDER BY id").fetchall()
    conn.close()
    return rows


def count_notes() -> int:
    conn = get_conn()
    count = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    conn.close()
    return count


if __name__ == "__main__":
    add_note("hello", "world")
    notes = list_notes()
    if "--json" in sys.argv:
        print(json.dumps([{"id": id_, "title": title, "body": body} for id_, title, body in notes]))
    else:
        for row in notes:
            print(row)
