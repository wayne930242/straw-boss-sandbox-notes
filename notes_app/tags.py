import sqlite3
import sys

from notes_app.app import get_conn


def _init_tag_tables(conn: sqlite3.Connection) -> None:
    conn.execute("CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS note_tags ("
        "note_id INTEGER, tag_id INTEGER, "
        "PRIMARY KEY(note_id, tag_id), "
        "FOREIGN KEY(note_id) REFERENCES notes(id), "
        "FOREIGN KEY(tag_id) REFERENCES tags(id))"
    )


def add_tag(note_id: int, tag_name: str) -> int:
    conn = get_conn()
    _init_tag_tables(conn)
    conn.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag_name,))
    tag_id = conn.execute("SELECT id FROM tags WHERE name = ?", (tag_name,)).fetchone()[0]
    conn.execute("INSERT OR IGNORE INTO note_tags (note_id, tag_id) VALUES (?, ?)", (note_id, tag_id))
    conn.commit()
    conn.close()
    return tag_id


def remove_tag(note_id: int, tag_name: str) -> bool:
    conn = get_conn()
    _init_tag_tables(conn)
    row = conn.execute("SELECT id FROM tags WHERE name = ?", (tag_name,)).fetchone()
    if row is None:
        conn.close()
        return False
    tag_id = row[0]
    cur = conn.execute("DELETE FROM note_tags WHERE note_id = ? AND tag_id = ?", (note_id, tag_id))
    conn.commit()
    removed = cur.rowcount > 0
    conn.close()
    return removed


def list_tags(note_id: int) -> list[str]:
    conn = get_conn()
    _init_tag_tables(conn)
    rows = conn.execute(
        "SELECT tags.name FROM tags "
        "JOIN note_tags ON tags.id = note_tags.tag_id "
        "WHERE note_tags.note_id = ? ORDER BY tags.name",
        (note_id,),
    ).fetchall()
    conn.close()
    return [name for (name,) in rows]


def notes_by_tag(tag_name: str) -> list[tuple]:
    conn = get_conn()
    _init_tag_tables(conn)
    rows = conn.execute(
        "SELECT notes.id, notes.title, notes.body FROM notes "
        "JOIN note_tags ON notes.id = note_tags.note_id "
        "JOIN tags ON tags.id = note_tags.tag_id "
        "WHERE tags.name = ? ORDER BY notes.id",
        (tag_name,),
    ).fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "add":
        note_id, tag = int(sys.argv[2]), sys.argv[3]
        print(add_tag(note_id, tag))
    elif command == "remove":
        note_id, tag = int(sys.argv[2]), sys.argv[3]
        print(remove_tag(note_id, tag))
    elif command == "list":
        note_id = int(sys.argv[2])
        for tag in list_tags(note_id):
            print(tag)
    elif command == "by-tag":
        tag = sys.argv[2]
        for row in notes_by_tag(tag):
            print(row)
    else:
        raise ValueError(f"unknown command: {command}")
