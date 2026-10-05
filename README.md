# envdiff

Zero-dependency Python CLI that compares two or more dotenv-style files. It reports keys missing from each file and keys whose values differ. Values are hidden by default, so output is safe to paste into chats and CI logs.

## Usage

    python3 envdiff.py a.env b.env
    python3 envdiff.py a.env b.env c.env --json
    python3 envdiff.py a.env b.env --keys-only      # ignore value differences
    python3 envdiff.py a.env b.env --show-values    # reveal values

Exit code is 1 if any difference exists, 0 otherwise, so it works in CI.
Handles comments, blank lines, `export ` prefixes, quoted values and trailing ` # comments`.

## Tests

    python3 -m unittest -v

MIT licensed.
