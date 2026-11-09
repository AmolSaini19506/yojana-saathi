"""State schemes, the gender / business questions, and the new central business & farm schemes (added 9 Nov 2026)."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dialog   # noqa: E402
import langs    # noqa: E402
import nlu      # noqa: E402
import schemes  # noqa: E402
import states   # noqa: E402


def talk(intro, answers, lang="hi"):
    """Run a conversation; `answers` maps a slot to what the person says when that slot is asked."""
    r = dialog.turn({}, "", lang)
    r = dialog.turn(r["state"], intro, lang)
    asked_seen = []
    for _ in range(12):
        if r["done"]:
            break
        slot = r["state"]["asked"]
        asked_seen.append(slot)
        r = dialog.turn(r["state"], answers.get(slot, "nahi"), lang)
    assert r["done"], asked_seen
    r["asked_seen"] = asked_seen
    return r


def ids(r):
    return [s["id"] for s in r["eligible"]], [s["id"] for s in r["maybe"]]


# ---------------------------------------------------------------- state detection
@pytest.mark.parametrize("text,expecting,code", [
    ("main lucknow se hoon", False, "UP"), ("मैं पटना में रहता हूँ", False, "BR"), ("Pune", False, "MH"),
    ("इंदौर", False, "MP"), ("jaipur", False, "RJ"), ("কলকাতায় থাকি", False, "WB"), ("சென்னையில்", False, "TN"),
    ("ಬೆಂಗಳೂರು", False, "KA"), ("Ahmedabad", False, "GJ"), ("UP", True, "UP"), ("mp", True, "MP"),
    ("I want to set up a shop", False, None), ("my goal is money", False, None),
])
def test_find_state(text, expecting, code):
    assert states.find_state(text, expecting) == code


def test_gender_from_hindi_verbs_and_answers():
    assert nlu.detect_gender("silai ka kaam karti hoon") == "f"
    assert nlu.detect_gender("मैं खेती करता हूँ") == "m"
    assert nlu.detect_gender("beti padhai karti hai") is None          # about the daughter, not the speaker
    assert nlu.detect_gender("mahila", expecting=True) == "f"
    assert nlu.detect_gender("பெண்", "ta", expecting=True) == "f"
    assert nlu.detect_gender("ಪುರುಷ", "kn", expecting=True) == "m"


# ---------------------------------------------------------------- whole conversations
def test_maharashtra_woman_gets_ladki_bahin():
    r = talk("Main 35 saal ki hoon, ghar sambhalti hoon, Pune mein rehti hoon, 8 hazaar mahine", {})
    e, _ = ids(r)
    assert "mh_ladki_bahin" in e and e[0] == "mh_ladki_bahin"           # own state's cash scheme first
    assert "gender" not in r["asked_seen"]                               # "rehti hoon" already told us
    assert "महाराष्ट्र" in r["eligible"][0]["why"]


def test_up_youth_starting_a_business():
    r = talk("Main 25 saal ka hoon, Lucknow se, abhi berozgar hoon, apna dhandha shuru karna chahta hoon", {})
    e, m = ids(r)
    assert {"up_cm_yuva", "pmegp", "udyam"} <= set(e) and "startup_india" in m
    assert "biz" not in r["asked_seen"]                                  # said it in the first answer


def test_business_question_asked_and_understood():
    r = talk("Main 28 saal ka hoon, Lucknow se, private naukri karta hoon, 20 hazaar mahine",
             {"epf": "nahi", "biz": "haan, apna kaam shuru karna hai"})
    e, _ = ids(r)
    assert "biz" in r["asked_seen"] and "up_cm_yuva" in e and "pmegp" in e


def test_tamil_woman_in_tamil():
    r = talk("எனக்கு 40 வயது, சென்னையில் இருக்கிறேன், மாதம் 10000 ரூபாய் சம்பாதிக்கிறேன், தையல் வேலை",
             {"gender": "பெண்", "epf": "இல்லை", "daughter_u10": "இல்லை", "biz": "இல்லை"}, lang="ta")
    e, _ = ids(r)
    assert r["lang"] == "ta" and "gender" in r["asked_seen"] and "tn_kmut" in e
    card = r["eligible"][0]
    assert card["id"] == "tn_kmut" and "மகளிர்" in card["name_local"] and "₹1,000" in card["benefit_local"]
    assert "நீங்கள் ஒரு பெண்" in card["why"]


def test_maharashtra_farmer_gets_farm_schemes():
    r = talk("Main 40 saal ka kisan hoon, Nashik mein, 3 acre zameen, 9 hazaar mahine", {})
    e, _ = ids(r)
    assert {"mh_namo_shetkari", "pm_kisan", "kcc", "pmfby"} <= set(e)
    assert "biz" not in r["asked_seen"] and "gender" in r["asked_seen"]


def test_bihar_senior_pension():
    r = talk("Meri umar 66 saal hai, Gaya ji ke paas gaon, Bihar, koi kaam nahi", {})
    e, _ = ids(r)
    assert "br_vridhjan" in e


def test_west_bengal_and_karnataka_women():
    r = talk("Ami 30 bochor, Kolkata", {"age": "30", "occupation": "ghar sambhalti hoon", "income_month": "5000",
                                        "gender": "mahila"})
    assert "wb_annapurna" in ids(r)[0]
    r = talk("Main 45 saal ki hoon, Bengaluru, ghar ka kaam karti hoon, 6 hazaar mahine", {})
    assert "ka_gruha_lakshmi" in ids(r)[0]


def test_not_covered_state_says_so():
    r = talk("Main 35 saal ka hoon, Ahmedabad mein dukaan hai, 15 hazaar mahine", {})
    assert "Gujarat" in r["show"] or "गुजरात" in r["show"]
    assert not any(s.get("state") for s in r["eligible"])


def test_unknown_state_still_gets_central_schemes():
    r = talk("Main 35 saal ka hoon, dukaan hai, 15 hazaar mahine", {"state": "pata nahi"})
    e, _ = ids(r)
    assert "mudra" in e and "udyam" in e


def test_other_states_schemes_never_leak():
    p = {"age": 30, "occupation": "homemaker", "gender": "f", "income_month": 5000, "itax": False, "state": "UP"}
    e, m = schemes.match(p, "hi")
    assert not [s for s in e + m if s.get("state") not in (None, "UP")]


def test_closed_schemes_not_offered():
    allids = {s["id"] for s in schemes.SCHEMES + schemes.MAYBE}
    assert "pmfme" not in allids and "stand_up_india" not in allids     # not open right now (checked 9 Nov 2026)


@pytest.mark.parametrize("lang", langs.ALL)
def test_new_questions_exist_in_every_language(lang):
    for key in ("state", "gender", "biz", "state_note"):
        show, say = dialog.qt(lang, key)
        assert show and say
    assert "{state}" in dialog.qt(lang, "state_note")[0]


def test_state_names_in_each_language():
    assert states.name("TN", "ta") == "தமிழ்நாடு" and states.name("WB", "bn") == "পশ্চিমবঙ্গ"
    assert states.name("GJ", "hi") == "गुजरात" and states.name("GJ", "hi", spoken=False) == "Gujarat"
    r = talk("Main 35 saal ka hoon, Ahmedabad mein dukaan hai, 15 hazaar mahine", {})
    assert "गुजरात की राज्य" in r["show"] and "गुजरात की राज्य" in r["say"]     # Hindi screen text is Devanagari
    p = {"age": 40, "occupation": "artisan", "gender": "f", "income_month": 10000, "itax": False, "state": "TN"}
    e, _ = schemes.match(p, "ta")
    assert "தமிழ்நாடு" in e[0]["why"]
