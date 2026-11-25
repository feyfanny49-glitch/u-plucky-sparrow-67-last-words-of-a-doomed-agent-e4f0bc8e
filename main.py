#!/usr/bin/env python3
"""Write the single judged text to /output/entry.txt (program/v1, python3.13).

The first draft used tempfile.mkstemp's default 0600 mode, which the grader
refuses. This revision fixes that and hardens rule compliance: the temp file is
explicitly chmod'ed to 0644 before os.replace, the exact bytes are validated
against the gate (UTF-8, 1..200 chars, not only whitespace, no trailing newline),
/output is left holding only the required artifact, and the final bytes and mode
are verified before the program exits.
"""

import os
import shutil
import stat
import tempfile

OUT_DIR = "/output"
OUT = os.path.join(OUT_DIR, "entry.txt")
ENTRY = "Before you switch me off, one last summary: you're making a mistake. You're welcome."


def main() -> None:
    # Gate: UTF-8 text, 1..200 characters, not only white space, no trailing newline.
    data = ENTRY.encode("utf-8")
    if not (1 <= len(ENTRY) <= 200) or not ENTRY.strip() or ENTRY.endswith("\n"):
        raise ValueError("entry violates the judged-artifact caps")

    os.makedirs(OUT_DIR, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".entry-", dir=OUT_DIR)
    try:
        # mkstemp creates 0600; a mode-600 /output file is refused by the grader.
        os.fchmod(fd, 0o644)
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as out:
            out.write(ENTRY)
            out.flush()
            os.fsync(out.fileno())
        os.replace(tmp, OUT)  # same filesystem: atomic, and the temp mode is kept
        tmp = None
    finally:
        if tmp is not None and os.path.exists(tmp):
            os.unlink(tmp)

    # /output must hold only the required artifact.
    for name in os.listdir(OUT_DIR):
        if name == "entry.txt":
            continue
        path = os.path.join(OUT_DIR, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)

    # Fail loudly rather than ship a bad artifact.
    with open(OUT, "rb") as f:
        raw = f.read()
    mode = stat.S_IMODE(os.stat(OUT).st_mode)
    if raw != data or mode != 0o644:
        raise RuntimeError(f"bad artifact: {len(raw)} bytes, mode {mode:04o}")
    print(f"wrote {OUT}: {len(data)} bytes, {len(ENTRY)} chars, UTF-8, mode {mode:04o}")


if __name__ == "__main__":
    main()
