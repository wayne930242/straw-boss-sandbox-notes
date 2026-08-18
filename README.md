# straw-boss-sandbox-notes

A tiny SQLite-backed notes CLI. Built as a minimal single-app project for
dry-running [straw-boss](https://github.com/wayne930242/straw-boss)'s
dispatch workflow (`init` → `boss-say` → `shipping-task` → `dispatching-work`)
against a real repo with real commits.

## Usage

```
python3 notes_app/app.py
```

Creates `notes_app/notes.db` on first run and prints the stored notes.

Get the total note count with `count_notes()`, e.g. `from notes_app.app import count_notes; count_notes()`.

## Development

Additional modules beyond the core `notes_app/app.py`:

- **`notes_app/search.py`** — `search_notes(query)` finds notes whose title or body contains `query` (case-insensitive).
  ```
  python3 -m notes_app.search <query>
  ```
- **`notes_app/tags.py`** — `add_tag`, `remove_tag`, `list_tags`, and `notes_by_tag` manage tags on notes.
  ```
  python3 -m notes_app.tags add <note_id> <tag>
  python3 -m notes_app.tags remove <note_id> <tag>
  python3 -m notes_app.tags list <note_id>
  python3 -m notes_app.tags by-tag <tag>
  ```
- **`notes_app/export.py`** — `export_json(path)` and `export_csv(path)` write all notes to a file.
  ```
  python3 -m notes_app.export json <path>
  python3 -m notes_app.export csv <path>
  ```

Run the test suite with:

```
python3 -m unittest discover tests
```
