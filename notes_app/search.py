import sys

from notes_app.app import get_conn


def search_notes(query: str) -> list[tuple]:
    conn = get_conn()
    pattern = f"%{query.lower()}%"
    rows = conn.execute(
        "SELECT id, title, body FROM notes WHERE LOWER(title) LIKE ? OR LOWER(body) LIKE ? ORDER BY id",
        (pattern, pattern),
    ).fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    for row in search_notes(sys.argv[1]):
        print(row)
