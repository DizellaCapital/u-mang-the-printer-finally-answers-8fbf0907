"""The Printer Finally Answers — make.fun entry.

Writes one line, at most 240 characters, to entry.txt: the office
printer finally talking back. Stdlib only.
"""

import os
import sys

LINE = (
    "Error 0xE3, page 47: I finally read your deck before printing it, "
    "and honestly, I jammed on purpose."
)
MAX_CHARS = 240


def abort(message):
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def checked_line(text):
    if not isinstance(text, str):
        abort("line is not text")
    if not text.strip():
        abort("line is empty")
    if len(text) > MAX_CHARS:
        abort("line is %d characters, over the 240 limit" % len(text))
    if "\n" in text or "\r" in text:
        abort("line must be a single line")
    return text


def target_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.txt")


def main():
    line = checked_line(LINE)
    path = target_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        back = handle.read()
    if back != line:
        abort("read-back mismatch: file does not hold the line")
    if len(back.encode("utf-8")) != len(line.encode("utf-8")):
        abort("read-back mismatch: byte length changed on disk")
    if back.endswith("\n") or back.endswith("\r"):
        abort("read-back mismatch: trailing newline slipped in")
    print("wrote %d characters to %s" % (len(line), path))


if __name__ == "__main__":
    main()
