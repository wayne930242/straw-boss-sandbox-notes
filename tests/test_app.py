import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from notes_app import app


class NotesAppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        self.db_path = Path(path)
        self.patcher = patch.object(app, "DB_PATH", self.db_path)
        self.patcher.start()

    def tearDown(self) -> None:
        self.patcher.stop()
        self.db_path.unlink(missing_ok=True)

    def test_add_note_returns_id(self) -> None:
        note_id = app.add_note("title", "body")
        self.assertEqual(note_id, 1)

        second_id = app.add_note("another", "body2")
        self.assertEqual(second_id, 2)

    def test_list_notes_returns_added_notes_in_order(self) -> None:
        app.add_note("first", "body1")
        app.add_note("second", "body2")

        notes = app.list_notes()

        self.assertEqual(notes, [(1, "first", "body1"), (2, "second", "body2")])

    def test_list_notes_empty(self) -> None:
        self.assertEqual(app.list_notes(), [])

    def test_delete_note_removes_existing_note(self) -> None:
        note_id = app.add_note("title", "body")

        deleted = app.delete_note(note_id)

        self.assertTrue(deleted)
        self.assertEqual(app.list_notes(), [])

    def test_delete_note_returns_false_for_missing_note(self) -> None:
        deleted = app.delete_note(999)

        self.assertFalse(deleted)

    def test_count_notes(self) -> None:
        self.assertEqual(app.count_notes(), 0)

        app.add_note("title1", "body1")
        app.add_note("title2", "body2")

        self.assertEqual(app.count_notes(), 2)

        app.delete_note(1)

        self.assertEqual(app.count_notes(), 1)


if __name__ == "__main__":
    unittest.main()
