"""Only relevant questions, few of them, and no question whose answer the person already gave."""
import pytest

from yojana import engine, nlu
from helpers import talk


def asked(first, answers=None, lang="hi"):
    """The follow-up questions (after age / work / state) the app asks, and the final reply."""
    from yojana import dialog
    answers = answers or {}
    r = dialog.turn({}, "", lang)
    r = dialog.turn(r["state"], first, lang)
    seen, shown = [], {}
    while not r["done"]:
        slot = r["state"]["asked"]
        seen.append(slot)
        shown[slot] = r["show"]
        r = dialog.turn(r["state"], answers.get(slot, "pata nahi" if slot in ("income_month", "study", "category",
                                                                              "gender", "rural", "land_ha") else "nahi"),
                        lang)
    return [s for s in seen if s not in engine.CORE], shown, r


# ---------------------------------------------------------------- unrelated questions
def test_young_student_is_not_asked_about_daughters_business_or_salary():
    qs, shown, _ = asked("main 20 saal ka hoon, college mein padhta hoon, UP se")
    assert "daughter_u10" not in qs and "biz" not in qs and "school_kids" not in qs and "gender" not in qs, qs
    if "income_month" in qs:                                    # asked about the household, not "your salary"
        assert "घर" in shown["income_month"], shown["income_month"]


def test_homemaker_and_elderly_are_asked_household_income():
    _, shown, _ = asked("main 38 saal ki hoon, ghar sambhalti hoon, Rajasthan")
    assert "घर" in shown.get("income_month", "घर")
    _, shown, _ = asked("I am 68, I don't work, I live in Punjab", lang="en")
    assert "household" in shown.get("income_month", "household")


# ---------------------------------------------------------------- not too many questions
@pytest.mark.parametrize("first", [
    "main 20 saal ka hoon, student hoon, UP se",
    "मैं 20 साल की हूँ, कॉलेज में पढ़ती हूँ, बिहार से",
    "main 45 saal ka kisan hoon, 2 acre zameen, Maharashtra",
    "32 saal, sabzi bechta hoon, Delhi",
    "38 saal ki hoon, gharelu mahila, Rajasthan",
    "I am 27, I work in a private company in Karnataka",
    "29 saal ki hoon, silai karti hoon, Madhya Pradesh",
])
def test_at_most_five_follow_up_questions(first):
    qs, _, r = asked(first)
    assert len(set(qs)) <= engine.MAX_FOLLOWUPS, qs
    assert r["eligible"] or r["maybe"]


# ---------------------------------------------------------------- gender from how people talk
@pytest.mark.parametrize("text,lang,want", [
    ("main 20 saal ka hoon", "hi", "m"),
    ("main 45 saal ka kisan hoon", "hi", "m"),
    ("sabzi bechti hoon", "hi", "f"),
    ("मैं 20 साल की हूँ, कॉलेज में पढ़ती हूँ", "hi", "f"),
    ("मैं खेती करता हूँ", "hi", "m"),
    ("main padh rahi hoon", "hi", "f"),
    ("main ek kisan ki beti hoon", "hi", "f"),
    ("ਮੈਂ ਖੇਤੀ ਕਰਦੀ ਹਾਂ", "pa", "f"),
    ("ਮੈਂ 40 ਸਾਲ ਦਾ ਹਾਂ", "pa", "m"),
    ("मी शेती करतो", "mr", "m"),
    ("मी ३५ वर्षांची आहे", "mr", "f"),
    ("I am a woman, 30 years old", "en", "f"),
    # says nothing about the speaker
    ("meri beti 8 saal ki hai", "hi", None),
    ("main kota se hoon", "hi", None),
    ("I am a manager in a company", "en", None),
    ("main 30 saal ka hoon aur meri patni silai karti hai", "hi", "m"),
])
def test_gender_from_wording(text, lang, want):
    assert nlu.detect_gender(text, lang) == want


def test_gender_question_skipped_when_wording_says_it():
    qs, _, r = asked("main 29 saal ki hoon, silai karti hoon, Delhi", {"income_month": "8000"})
    assert "gender" not in qs and r["profile"]["gender"] == "f"
    qs, _, r = asked("मैं 34 साल का हूँ, ठेला लगाता हूँ, दिल्ली", {"income_month": "12000"})
    assert "gender" not in qs and r["profile"]["gender"] == "m"


# ---------------------------------------------------------------- work people describe in their own words
@pytest.mark.parametrize("text,want", [
    ("sabzi bechta hoon", "street_vendor"),
    ("मैं सब्ज़ी बेचती हूँ", "street_vendor"),
    ("कॉलेज में पढ़ती हूँ", "student"),
    ("main school mein teacher hoon", "salaried_private"),
    ("kapde bechta hoon", "shopkeeper"),
])
def test_occupation_in_own_words(text, want):
    assert nlu.detect_occupation(text)[0] == want


# ---------------------------------------------------------------- Uttar Pradesh, written out
@pytest.mark.parametrize("text", ["main UP ka hoon", "I live in UP", "from UP", "Uttar Pradesh", "uttarpradesh",
                                  "उत्तर प्रदेश से", "उत्तरप्रदेश", "यूपी से हूँ", "lucknow mein rehta hoon"])
def test_uttar_pradesh_from_short_and_full_name(text):
    from yojana import states
    assert states.find_state(text) == "UP"


def test_uttar_pradesh_is_written_out_for_people():
    from yojana import dialog, states
    assert states.name("UP", "en") == "Uttar Pradesh" and states.name("UP", "hi") == "उत्तर प्रदेश"
    assert "उत्तर प्रदेश" in dialog.qt("hi", "state")[0] and "UP" not in dialog.qt("hi", "state")[0]
    assert "Uttar Pradesh" in dialog.qt("en", "state")[0]


# ---------------------------------------------------------------- "what is BPL?"
@pytest.mark.parametrize("lang,first,question,yes", [
    ("hi", "38 saal ki hoon, gharelu mahila, Rajasthan", "BPL kya hota hai?", "haan"),
    ("hi", "38 saal ki hoon, gharelu mahila, Rajasthan", "ये क्या होता है?", "हाँ"),
    ("en", "I am a 38 year old housewife in Rajasthan", "what is BPL?", "yes"),
    ("mr", "मी ३८ वर्षांची गृहिणी आहे, राजस्थान", "BPL म्हणजे काय?", "हो"),
])
def test_bpl_is_explained_then_asked_again(lang, first, question, yes):
    from yojana import dialog
    from helpers import until
    r = until("bpl", first, {"income_month": "8000", "rural": "gaon"}, lang=lang)
    r = dialog.turn(r["state"], question, lang)
    assert r["state"]["asked"] == "bpl" and "BPL" in r["show"] and len(r["show"]) > 120
    r = dialog.turn(r["state"], yes, lang)
    assert r["state"]["profile"]["bpl"] is True


def test_farmer_with_young_daughter_still_hears_about_sukanya():
    r = talk("Main 34 saal ka kisan hoon", {"land_ha": "do acre", "income_month": "8 hazaar",
                                            "daughter_u10": "haan ek beti hai 6 saal ki"})
    assert "sukanya" in [s["id"] for s in r["eligible"]]
