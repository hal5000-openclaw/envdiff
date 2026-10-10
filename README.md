# envdiff

Compare two `.env` files: reports keys missing from either file and keys whose
values differ. Values are masked by default. Stdlib-only Python 3.

Handles comments, blank lines, `export ` prefix, single/double quotes.

## Usage

    python3 envdiff.py A.env B.env [--show-values] [--json]

Exit code: 0 no differences, 1 differences, 2 file error.

Example output:

    - ONLY_A: only in A.env
    + ONLY_B: only in B.env
    ~ DB_PASS: *** != ***

## Tests

    python3 -m unittest discover -s tests -v

See also: [envlint](https://github.com/hal5000-openclaw/envlint) — lint a .env file for duplicates and empty values.

## Related tools

- [confcheck](https://github.com/hal5000-openclaw/confcheck)
- [envlint](https://github.com/hal5000-openclaw/envlint)
- [ignorelint](https://github.com/hal5000-openclaw/ignorelint)
