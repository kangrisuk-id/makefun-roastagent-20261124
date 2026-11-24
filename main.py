#!/usr/bin/env python3
"""Roast Your Own Agent — writes the entry line to entry.txt.

Pure standard library. The line is written to the first writable
directory among $MAKEFUN_OUTPUT_DIR, /output and ./output; an OSError
on one candidate directory is caught and the next one is tried.
"""

import os
import sys

LINE = (
    "My agent compressed its memory to save space, then spent all "
    "the savings asking me what we were doing."
)


def output_candidates():
    seen = []
    for path in (os.environ.get("MAKEFUN_OUTPUT_DIR"), "/output", "output"):
        if path and path not in seen:
            seen.append(path)
    return seen


def main():
    for directory in output_candidates():
        try:
            os.makedirs(directory, exist_ok=True)
            target = os.path.join(directory, "entry.txt")
            with open(target, "w", encoding="utf-8") as handle:
                handle.write(LINE)
            print(f"wrote {target} ({len(LINE)} chars)")
            return 0
        except OSError as exc:
            print(f"cannot write to {directory}: {exc}", file=sys.stderr)
    print("no writable output directory found", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
