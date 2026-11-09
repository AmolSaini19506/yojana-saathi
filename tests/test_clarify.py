"""When the person asks back ("PF kya hota hai?") or says they don't know, instead of answering.

Bug found on the live site (9 Nov 2026): "वो क्या होता है?" in reply to the PF question was saved as "PF hai",
because "है" counted as yes.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dialog  # noqa: E402
import langs   # noqa: E402
import nlu     # noqa: E402


def at_slot(slot, lang="hi"):
    """A conversation that has just asked `slot` (a salaried 30-year-old earning 60,000, so PF and tax get asked)."""
    r = dialog.turn({}, "", lang)
    r = dialog.turn(r["state"], "main 30 saal ka hoon, company mein naukri karta hoon, 60 hazaar mahina", lang)
    for _ in range(4):
        if r["state"]["asked"] == slot:
            return r
        r = dialog.turn(r["state"], "nahi", lang)
    raise AssertionError(f"never asked {slot}: {r['state']}")


def test_screenshot_case_pf_question_is_not_yes():
    r = at_slot("epf")
    r2 = dialog.turn(r["state"], "वो क्या होता है?", "hi")
    assert "epf" not in r2["state"]["profile"]                 # not saved as "PF hai"
    assert r2["state"]["asked"] == "epf"                        # asks again...
    assert "Provident Fund" in r2["show"] and dialog.Q["hi"]["epf"]["show"] in r2["show"]   # ...after explaining
    # the explanation is given once; the real answer then counts
    r3 = dialog.turn(r2["state"], "nahi", "hi")
    assert r3["state"]["profile"]["epf"] is False


@pytest.mark.parametrize("text", ["PF kya hota hai?", "ye kya hai", "matlab?", "what is PF?", "मतलब?",
                                  "samjha nahi"])
def test_asking_back_gets_explanation(text):
    r2 = dialog.turn(at_slot("epf")["state"], text, "hi")
    assert "epf" not in r2["state"]["profile"] and "Provident Fund" in r2["show"]


def test_income_tax_explained():
    r2 = dialog.turn(at_slot("itax")["state"], "income tax kya hota hai?", "hi")
    assert "itax" not in r2["state"]["profile"] and "ITR" in r2["show"]


@pytest.mark.parametrize("text", ["pata nahi", "पता नहीं", "I don't know", "maloom nahi"])
def test_dont_know_moves_on(text):
    r = at_slot("epf")
    r2 = dialog.turn(r["state"], text, "hi")
    assert r2["state"]["profile"]["epf"] is None               # blank, not "no" and not "yes"
    assert r2["state"]["asked"] != "epf"                        # moved on
    assert r2["show"].startswith(dialog.Q["hi"]["ok_skip"]["show"]) or r2["done"]


def test_dont_know_does_not_hide_a_real_answer():
    st = dialog.turn({}, "", "hi")["state"]
    r = dialog.turn(st, "main 30 saal ka hoon, lucknow mein company mein naukri karta hoon", "hi")
    assert r["state"]["asked"] == "income_month"
    r2 = dialog.turn(r["state"], "pata nahi, shayad 12 hazaar", "hi")
    assert r2["state"]["profile"]["income_month"] == 12000


@pytest.mark.parametrize("text,expected", [
    ("haan", True), ("haan hai", True), ("हाँ, कटता है", True), ("ji haan", True), ("hai", True),
    ("nahi", False), ("नहीं", False), ("no", False),
    ("वो क्या होता है?", None), ("kya hai?", None), ("क्या है", None),
])
def test_yes_no(text, expected):
    assert nlu.parse_yes_no(text) is expected


def test_daughter_yes_still_works():
    st = dialog.turn({}, "", "hi")["state"]
    r = dialog.turn(st, "main 30 saal ka kisan hoon, zameen nahi, 8 hazaar mahina", "hi")
    while r["state"]["asked"] != "daughter_u10":
        r = dialog.turn(r["state"], "nahi", "hi")
    r = dialog.turn(r["state"], "haan beti hai", "hi")
    assert r["state"]["profile"]["daughter_u10"] is True


@pytest.mark.parametrize("lang,what,dk", [
    ("ta", "PF என்றால் என்ன?", "தெரியாது"), ("bn", "PF মানে কী?", "জানি না"), ("mr", "PF म्हणजे काय?", "माहीत नाही"),
    ("gu", "PF એટલે શું?", "ખબર નથી"), ("pa", "PF ਕੀ ਹੁੰਦਾ ਹੈ?", "ਪਤਾ ਨਹੀਂ"), ("te", "PF అంటే ఏమిటి?", "తెలియదు"),
    ("kn", "PF ಅಂದರೆ ಏನು?", "ಗೊತ್ತಿಲ್ಲ"), ("ml", "PF എന്നാൽ എന്താണ്?", "അറിയില്ല"),
])
def test_packs_explain_and_dont_know(lang, what, dk):
    assert nlu.clarify(what, lang) == "what" and nlu.clarify(dk, lang) == "dontknow"
    p = langs.pack(lang)
    st = {"profile": {"age": 30, "occupation": "salaried_private", "income_month": 60000, "itax": False},
          "asked": "epf", "retries": {}}
    r = dialog.turn(st, what, lang)
    assert r["state"]["asked"] == "epf" and r["show"].startswith(p.Q["x_epf"]) and "epf" not in r["state"]["profile"]
    r = dialog.turn(st, dk, lang)
    assert r["state"]["profile"]["epf"] is None and r["show"].startswith(p.Q["ok_skip"])


# ---------------------------------------------------------------- bug seen live: "मुझे cash मिलता है" saved as "PF hai"
@pytest.mark.parametrize("text,lang,expected", [
    ("मुझे cash मिलता है।", "hi", False),           # paid in cash -> no PF
    ("salary haath mein milti hai", "hi", False),
    ("મને રોકડ મળે છે", "gu", False),
    ("எனக்கு ரொக்கம் தான் கிடைக்கும்", "ta", False),
    ("PF कटता है", "hi", True), ("हाँ है", "hi", True), ("है", "hi", True), ("હા, PF કપાય છે", "gu", True),
    ("यह कर्मचारी की factory है।", "hi", None),     # not an answer: ask again rather than guess "yes"
    ("ਮੈਂ ਫੈਕਟਰੀ ਵਿੱਚ ਕੰਮ ਕਰਦਾ ਹਾਂ ਉੱਥੇ ਬਹੁਤ ਲੋਕ ਹੈ", "pa", None),
])
def test_pf_answer(text, lang, expected):
    assert nlu.extract(text, expecting="epf", lang=lang).get("epf") is expected


@pytest.mark.parametrize("text,lang", [("ghar mein ek beti hai", "hi"), ("हाँ, मेरी एक बेटी है", "hi"),
                                       ("வீட்டில் ஒரு மகள் இருக்கிறாள்", "ta"), ("ఉంది", "te")])
def test_daughter_yes_long_answers(text, lang):
    assert nlu.extract(text, expecting="daughter_u10", lang=lang).get("daughter_u10") is True


def test_screenshot_conversation_keeps_cash_worker_schemes():
    st = {"profile": {"age": 30, "occupation": "labourer", "income_month": 12000, "itax": False},
          "asked": "epf", "retries": {}}
    r = dialog.turn(st, "मुझे cash मिलता है।", "hi")
    assert r["state"]["profile"]["epf"] is False
    while not r["done"]:
        r = dialog.turn(r["state"], "nahi", "hi")
    ids = [s["id"] for s in r["eligible"]]
    assert "eshram" in ids and "pm_sym" in ids, ids


# ---------------------------------------------------------------- scheme cards in the conversation's language
@pytest.mark.parametrize("lang", [x for x in langs.ALL if x != "en"])
def test_card_fields_in_users_language(lang):
    import schemes
    e, _ = schemes.match({"age": 30, "occupation": "labourer", "income_month": 12000, "itax": False, "epf": False}, lang)
    for c in e:
        assert c["apply_local"] and c["docs_local"] and c["note_local"], (lang, c["id"])
        assert "{web}" not in c["apply_local"] and "{helpline}" not in c["apply_local"]
        assert langs.script_counts(c["docs_local"])["latin"] < len(c["docs_local"]) / 2      # not English
