#!/usr/bin/env python3
"""envdiff: compare dotenv-style files. Values hidden unless --show-values."""
import argparse, json, sys


def parse(text):
    out = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
            v = v[1:-1]
        elif " #" in v:
            v = v.split(" #", 1)[0].rstrip()
        out[k] = v
    return out


def compare(files, keys_only=False):
    """files: {name: dict}. Returns {'missing': {name:[keys]}, 'differs': {key:{name:val}}}."""
    allkeys = set().union(*files.values()) if files else set()
    missing = {n: sorted(allkeys - set(d)) for n, d in files.items()}
    missing = {n: k for n, k in missing.items() if k}
    differs = {}
    if not keys_only:
        for k in sorted(allkeys):
            vals = {n: d[k] for n, d in files.items() if k in d}
            if len(set(vals.values())) > 1:
                differs[k] = vals
    return {"missing": missing, "differs": differs}


def main(argv=None):
    p = argparse.ArgumentParser(description="Compare dotenv-style files")
    p.add_argument("files", nargs="+")
    p.add_argument("--show-values", action="store_true")
    p.add_argument("--keys-only", action="store_true")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    if len(a.files) < 2:
        p.error("need at least two files")
    data = {}
    for f in a.files:
        with open(f) as fh:
            data[f] = parse(fh.read())
    r = compare(data, a.keys_only)
    if not a.show_values:
        r["differs"] = {k: {n: "<differs>" for n in v} for k, v in r["differs"].items()}
    bad = bool(r["missing"] or r["differs"])
    if a.json:
        print(json.dumps(r, indent=2))
    else:
        for n, ks in r["missing"].items():
            print(f"{n}: missing {', '.join(ks)}")
        for k, v in r["differs"].items():
            print(f"{k}: " + "; ".join(f"{n}={x}" for n, x in v.items()))
        if not bad:
            print("no differences")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
