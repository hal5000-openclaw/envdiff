#!/usr/bin/env python3
"""envdiff: compare two .env files."""
import argparse
import json
import sys


def _unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        q = v[0]
        v = v[1:-1]
        if q == '"':
            v = v.replace("\\n", "\n").replace('\\"', '"').replace("\\\\", "\\")
        return v
    # unquoted: strip trailing inline comment
    i = v.find(" #")
    if i != -1:
        v = v[:i]
    return v.strip()


def parse(text):
    env = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export ") or line.startswith("export\t"):
            line = line[7:].lstrip()
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        if k:
            env[k] = _unquote(v)
    return env


def diff(a, b):
    return {
        "missing_in_b": sorted(set(a) - set(b)),
        "missing_in_a": sorted(set(b) - set(a)),
        "different": sorted(k for k in set(a) & set(b) if a[k] != b[k]),
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Compare two .env files.")
    p.add_argument("a")
    p.add_argument("b")
    p.add_argument("--show-values", action="store_true", help="reveal values")
    p.add_argument("--json", action="store_true", help="JSON output")
    args = p.parse_args(argv)
    try:
        with open(args.a, encoding="utf-8") as f:
            a = parse(f.read())
        with open(args.b, encoding="utf-8") as f:
            b = parse(f.read())
    except OSError as e:
        print(f"envdiff: {e}", file=sys.stderr)
        return 2
    d = diff(a, b)
    show = lambda v: v if args.show_values else "***"
    changes = {k: {"a": show(a[k]), "b": show(b[k])} for k in d["different"]}
    has = any(d.values())
    if args.json:
        out = dict(d, different=changes)
        print(json.dumps(out, indent=2))
    else:
        for k in d["missing_in_b"]:
            print(f"- {k}: only in {args.a}")
        for k in d["missing_in_a"]:
            print(f"+ {k}: only in {args.b}")
        for k, c in changes.items():
            print(f"~ {k}: {c['a']} != {c['b']}")
        if not has:
            print("No differences.")
    return 1 if has else 0


if __name__ == "__main__":
    sys.exit(main())
