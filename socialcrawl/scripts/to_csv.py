#!/usr/bin/env python3
"""Flatten canonical rows to CSV with stable columns. Reads JSONL or one JSON document.

usage: to_csv.py [--archetype Comment] [--in rows.jsonl] [--out rows.csv] [--columns a,b.c] [--extra] [--all-ext]

  python3 scripts/paginate.py tiktok/post/comments --items 200 url=... | python3 scripts/to_csv.py --archetype Comment > comments.csv

Input is JSONL (what paginate.py and batch.py print), a JSON array of rows, or a whole API
response (its data.items rows are used). With --archetype the columns are the canonical
schema's core columns, in its order, from assets/endpoints.json, so the header never depends on which rows
arrived; wrapped rows (`{"comment": {...}}`) are unwrapped. Without it the columns are the sorted
union of every row's dotted leaf paths. The schema's platform-specific `ext.*` columns are left
out unless --all-ext. --columns overrides the list; --extra appends any leaf
the schema does not declare (sorted). Lists and objects below a column are written as JSON.
Strings that start with = + - @ are prefixed with ' so a spreadsheet does not run them.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys

import sclib

DANGEROUS = ("=", "+", "-", "@", "\t", "\r")


def load_rows(text: str) -> list:
    text = text.strip()
    if not text:
        return []
    try:
        doc = json.loads(text)
    except ValueError:
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    if isinstance(doc, list):
        return doc
    if isinstance(doc, dict) and isinstance(doc.get("data"), dict):
        rows = sclib.rows_of(doc)
        if rows:
            return rows
    return [doc]


def leaves(value, prefix: str = "") -> dict:
    out: dict = {}
    if isinstance(value, dict) and value:
        for k, v in value.items():
            out.update(leaves(v, f"{prefix}.{k}" if prefix else k))
    else:
        out[prefix] = value
    return out


def get_path(row, path: str):
    cur = row
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def is_ext(path: str) -> bool:
    return path == "ext" or path.startswith("ext.")


def cell(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return json.dumps(value)
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    s = str(value)
    return "'" + s if s.startswith(DANGEROUS) else s


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--archetype", help="canonical row type, e.g. Comment, Post, Author")
    ap.add_argument("--in", dest="src", help="input file (default stdin)")
    ap.add_argument("--out", help="output file (default stdout)")
    ap.add_argument("--columns", help="comma-separated dotted column paths (overrides the schema's)")
    ap.add_argument("--all-ext", action="store_true", help="include the schema's platform-specific ext.* columns")
    ap.add_argument("--extra", action="store_true", help="append leaves the column list does not cover")
    args = ap.parse_args(argv)

    columns: list[str] | None = None
    row_key = None
    if args.archetype:
        arch = ((sclib.load_catalogue() or {}).get("archetypes") or {})
        spec = arch.get(args.archetype) or arch.get(args.archetype.removesuffix("List"))
        if spec is None:
            print(f"unknown archetype {args.archetype!r}; known: {', '.join(sorted(arch)) or '(catalogue missing)'}", file=sys.stderr)
            return 1
        columns, row_key = list(spec["columns"]), spec.get("row_key")
        if not args.all_ext:
            columns = [c for c in columns if not is_ext(c)]
    if args.columns:
        columns = [c.strip() for c in args.columns.split(",") if c.strip()]

    text = open(args.src, encoding="utf-8").read() if args.src else sys.stdin.read()
    rows = []
    for r in load_rows(text):
        if row_key and isinstance(r, dict) and isinstance(r.get(row_key), dict):
            r = r[row_key]
        rows.append(r)

    if columns is None:
        union: set[str] = set()
        for r in rows:
            union.update(leaves(r))
        columns = sorted(union)
    elif args.extra:
        known = set(columns)
        extra: set[str] = set()
        for r in rows:
            for path in leaves(r):
                if not args.all_ext and is_ext(path):
                    continue
                if not any(path == c or path.startswith(c + ".") or c.startswith(path + ".") for c in known):
                    extra.add(path)
        columns = columns + sorted(extra)

    out = open(args.out, "w", encoding="utf-8", newline="") if args.out else sys.stdout
    try:
        w = csv.writer(out, lineterminator="\n")
        w.writerow(columns)
        for r in rows:
            w.writerow([cell(get_path(r, c)) for c in columns])
    finally:
        if args.out:
            out.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
