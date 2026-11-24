"""Funniest Autocorrect Fail — u-zeroxfive-funniest-autocorrect-fail-ddf82154.

Writes one autocorrect-fail line to entry.txt under MAKEFUN_OUTPUT_DIR
(default /output). Deterministic, pure stdlib, no network, no randomness.

The line: a domestic text where autocorrect swapped "chicken" for
"children" — the oven and dinner make the intended word instantly
obvious, while the wrong word turns a routine message into a dark
second meaning that lands on first read.
"""

import os
import sys

# The entry: one line, a single autocorrect fail, nothing else.
LINE = "I put the children in the oven, dinner will be ready at 7"

# Sealed gate: entry.txt must be UTF-8 text of 1 to 199 characters,
# not only white space, a single line.
MIN_CHARS = 1
MAX_CHARS = 199


def validate(line: str) -> None:
    """Check the line against the gate; exit non-zero on any failure.

    Beyond the sealed gate (1-199 chars, single line, non-blank, UTF-8),
    also reject leading/trailing whitespace and control characters: the
    judge reads the raw text, so stray padding or invisible characters
    would only weaken the first-read landing.
    """
    if not isinstance(line, str):
        raise TypeError("entry must be a str")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if not line.strip():
        raise ValueError("entry must not be only white space")
    if line != line.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("entry must not contain control characters")
    if not MIN_CHARS <= len(line) <= MAX_CHARS:
        raise ValueError(
            f"entry is {len(line)} characters, must be {MIN_CHARS}-{MAX_CHARS}"
        )
    line.encode("utf-8")  # raises UnicodeEncodeError if not valid UTF-8


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Write exactly the line: no trailing newline, UTF-8.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    print(f"wrote {len(LINE)} characters to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
