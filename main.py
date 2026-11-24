import argparse
import csv
import json

def load(filename, key):
    with open(filename, encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames or []
        if key not in fields or len(fields) != len(set(fields)) or "" in fields:
            raise ValueError(f"{filename}: invalid header or missing key {key}")
        rows = {}
        for row in reader:
            if None in row or None in row.values():
                raise ValueError(f"{filename}: malformed row near line {reader.line_num}")
            identity = row[key]
            if not identity.strip() or identity in rows:
                raise ValueError(f"{filename}: blank or repeated key near line {reader.line_num}")
            rows[identity] = row
        return fields, rows

parser = argparse.ArgumentParser(description="Compare two keyed CSV snapshots")
parser.add_argument("before")
parser.add_argument("after")
parser.add_argument("key")
args = parser.parse_args()
try:
    columns, old = load(args.before, args.key)
    new_columns, new = load(args.after, args.key)
    if set(columns) != set(new_columns):
        raise ValueError("Column sets differ. Align the headers before comparing.")
    changes = []
    for key in sorted(old.keys() & new.keys()):
        for column in columns:
            if old[key][column] != new[key][column]:
                changes.append(dict(key=key, column=column,
                                    before=old[key][column], after=new[key][column]))
    report = dict(added=[new[k] for k in sorted(new.keys() - old.keys())],
                  removed=[old[k] for k in sorted(old.keys() - new.keys())],
                  changed=changes)
    print(json.dumps(report, ensure_ascii=False, indent=2))
except (OSError, ValueError, csv.Error) as error:
    parser.exit(1, f"{error}\n")
