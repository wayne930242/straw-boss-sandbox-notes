import csv
import json
import sys

from notes_app.app import list_notes


def export_json(path: str) -> None:
    notes = list_notes()
    with open(path, "w") as f:
        json.dump([{"id": id_, "title": title, "body": body} for id_, title, body in notes], f)


def export_csv(path: str) -> None:
    notes = list_notes()
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "title", "body"])
        writer.writerows(notes)


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] not in ("json", "csv"):
        print("usage: python3 -m notes_app.export [json|csv] <path>", file=sys.stderr)
        sys.exit(1)
    fmt, path = sys.argv[1], sys.argv[2]
    if fmt == "json":
        export_json(path)
    else:
        export_csv(path)


if __name__ == "__main__":
    main()
