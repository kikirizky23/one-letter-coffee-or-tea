#!/usr/bin/env python3
"""One letter: coffee or tea.

The bounty asks for a single letter. A stands for coffee, B stands
for tea, and a judge reads two entries side by side and keeps the one
whose hidden word feels more vivid, funnier, or more true. This entry
sends A, and the word behind it is "awake".

Why A, why awake: coffee has exactly one job that everyone agrees on
-- it wakes you up. Before the first cup you are a person-shaped
pile of blankets; after it, you are a person again. "Awake" is vivid
(eyes open, lights on), it is funny in the understatement way (one
small cup against a whole night of sleep), and it is true -- nobody
drinks coffee to fall asleep. Tea has its charms, but no single word
for tea lands as hard: "brewed" fits coffee too, and "calm" is a mood,
not a reason to choose a side. A for awake is the whole argument for
coffee in one syllable, and it needs no explaining.

The program writes exactly that one letter to entry.txt inside the
output directory: one byte, no trailing newline, no extra word. It
then reads the file back and refuses to report success unless the
bytes on disk are exactly the letter it meant to write.

Only the Python standard library is used. Every run does the same
thing: the same letter, the same bytes. Nothing depends on the clock,
on randomness, on the network, or on any file outside this program.
"""

import hashlib
import os
import sys

# The entry: A for coffee. B would be tea; this entry picks coffee.
PICK = "A"

# The word the letter stands for. It never goes into entry.txt --
# the file holds the letter alone, and the word lives here and in
# the entry title so the judge can find it.
HIDDEN_WORD = "awake"

ENTRY_FILENAME = "entry.txt"


def pick_is_one_capital_letter(text):
    """Accept only a single capital letter from A to Z."""
    return (
        isinstance(text, str)
        and len(text) == 1
        and "A" <= text <= "Z"
    )


def resolve_output_dir():
    """The grader's directory when it sets one, /output otherwise."""
    given = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if given:
        return given
    return "/output"


def write_letter(directory):
    """Write the letter as one byte and return the file's path."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, ENTRY_FILENAME)
    with open(path, "wb") as handle:
        handle.write(PICK.encode("ascii"))
    return path


def read_back_matches(path):
    """True only when the bytes on disk are exactly the letter.

    Checks both the content and the length: one byte, no trailing
    newline, no hidden extra character. Returns the sha256 of the
    bytes on disk when they match, so the run can prove the file it
    wrote is the file it verified, byte for byte.
    """
    with open(path, "rb") as handle:
        on_disk = handle.read()
    if len(on_disk) != 1:
        print("entry.txt must hold exactly one byte", file=sys.stderr)
        return None
    if on_disk != PICK.encode("ascii"):
        print("entry.txt does not hold the letter %r" % PICK, file=sys.stderr)
        return None
    return hashlib.sha256(on_disk).hexdigest()


def main():
    if not pick_is_one_capital_letter(PICK):
        print("entry must be one capital letter, A to Z", file=sys.stderr)
        return 1
    path = write_letter(resolve_output_dir())
    digest = read_back_matches(path)
    if digest is None:
        return 1
    print("wrote %s: %r (%s) sha256 %s" % (path, PICK, HIDDEN_WORD, digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
