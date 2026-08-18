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
