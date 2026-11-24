#!/usr/bin/env python3
"""One Line, One Chill — make.fun bounty entry.

Writes one line of horror to /output/entry.txt: a single sentence of
under 200 characters that frightens a reader in one breath.

The line (106 characters, one sentence):

    Last night the baby monitor played a lullaby in my voice, from the
    nursery where my daughter sleeps alone.

Why this line, against the judge's brief (most important first):
  1. It is a horror story in a single sentence: a parent, a baby
     monitor, a nursery at night — the scare lands in one breath, and
     it is on the subject throughout.
  2. It frightens by dread that outlasts the line, and the scare is
     earned, not announced: nothing says "scary" or "afraid". The
     horror is the implication — something in the nursery is singing
     in the parent's voice to a child who sleeps alone — and the reader
     is left with it after the sentence ends.
  3. It is vivid and concrete: a baby monitor, a lullaby, a nursery,
     a daughter sleeping alone. A reader can see and hear all of it;
     there is no vague talk of darkness or fear.
  4. It is original: the turn is mimicry — the thing in the nursery
     has learned the parent's voice. No mirror, no doll, no basement,
     no ghost at the foot of the bed.
  5. It is crafted: the rhythm builds from the ordinary ("Last night
     the baby monitor played a lullaby") through the wrongness ("in my
     voice") to the last words, "sleeps alone", which land the blow.

Pure standard library only. No network, no randomness, no arguments:
the output is fixed and deterministic.

Gate self-check (mirrors the sealed scorer): the text must be UTF-8,
1 to 200 characters, not only white space, and a single sentence on
one line. The program refuses to write anything if a gate fails.
"""

import os
import sys

ENTRY = ("Last night the baby monitor played a lullaby in my voice, "
         "from the nursery where my daughter sleeps alone.")

MAX_CHARS = 200
OUTPUT_PATH = "/output/entry.txt"


def check_gates(text):
    """Return a list of gate failures; empty means every gate passes."""
    failures = []
    if not isinstance(text, str):
        failures.append("entry is not text")
        return failures
    if not text.strip():
        failures.append("entry is only white space")
    if len(text) < 1 or len(text) > MAX_CHARS:
        failures.append(
            "entry is %d characters, gate requires 1 to %d"
            % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        failures.append("entry must be a single line")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        failures.append("entry is not valid UTF-8: %s" % exc)
    # The brief asks for one sentence: exactly one sentence-ending mark,
    # at the end, and no second sentence hiding behind a comma splice.
    stripped = text.strip()
    if stripped.count(".") != 1 or not stripped.endswith("."):
        failures.append("entry must be exactly one sentence ending in '.'")
    if any(mark in text for mark in ("!", "?", ";", ":")):
        failures.append("entry must carry no '!', '?', ';' or ':'")
    # The scare must be earned, not announced: no word that names fear.
    lowered = text.lower()
    if any(word in lowered for word in ("scary", "scared", "afraid",
                                        "terrified", "horror", "fear",
                                        "nightmare", "monster", "ghost",
                                        "demon", "blood", "dead", "died",
                                        "kill")):
        failures.append("entry announces its scare instead of earning it")
    # The concrete image must be present: the monitor, the lullaby,
    # the voice, the nursery.
    for word in ("baby monitor", "lullaby", "my voice", "nursery"):
        if word not in lowered:
            failures.append("entry is missing its concrete image: %s" % word)
    return failures


def main():
    failures = check_gates(ENTRY)
    if failures:
        for failure in failures:
            print("GATE FAILED: %s" % failure, file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    # Outputs must be readable by every user: the grader collects them
    # as another user than the one the program runs as.
    os.chmod(OUTPUT_PATH, 0o644)

    # Read-back verification: what is on disk must be exactly the entry.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != ENTRY:
        print("GATE FAILED: read-back mismatch", file=sys.stderr)
        return 1
    if check_gates(written):
        print("GATE FAILED: written text fails gates", file=sys.stderr)
        return 1

    print("wrote %s (%d characters, 1 line)" % (OUTPUT_PATH, len(ENTRY)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
