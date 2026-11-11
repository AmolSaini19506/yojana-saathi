"""Shared test helper: hold a whole conversation, answering each question by what was asked.

The app chooses its questions from the scheme rules (engine.py), so their order changes as schemes are added.
Tests therefore say what the person would answer to each detail, not the order of the answers.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dialog  # noqa: E402

# What a person who has nothing special to report says. "pata nahi" leaves a detail blank.
DEFAULT = {"age": "pata nahi", "occupation": "pata nahi", "state": "pata nahi", "gender": "pata nahi",
           "income_month": "pata nahi", "land_ha": "zameen nahi hai", "category": "pata nahi", "study": "pata nahi"}


def talk(first, answers=None, lang="hi", limit=40):
    """Say `first` to the opening question, then answer every follow-up from `answers` ({detail: text});
    anything not listed gets "no" (or "don't know" where yes/no makes no sense). Returns the final reply."""
    answers = answers or {}
    r = dialog.turn({}, "", lang)
    r = dialog.turn(r["state"], first, lang)
    n = 0
    while not r["done"]:
        slot = r["state"]["asked"]
        r = dialog.turn(r["state"], answers.get(slot, DEFAULT.get(slot, "nahi")), lang)
        n += 1
        assert n < limit, f"conversation did not finish: {r['state']}"
    return r


def until(slot, first, answers=None, lang="hi", limit=40):
    """Like talk(), but stop as soon as the app asks about `slot` and return that reply."""
    answers = answers or {}
    r = dialog.turn({}, "", lang)
    r = dialog.turn(r["state"], first, lang)
    n = 0
    while not r["done"] and r["state"]["asked"] != slot:
        asked = r["state"]["asked"]
        r = dialog.turn(r["state"], answers.get(asked, DEFAULT.get(asked, "nahi")), lang)
        n += 1
        assert n < limit
    assert not r["done"], f"never asked {slot}: {r['state']}"
    return r
