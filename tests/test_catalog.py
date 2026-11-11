"""Schemes added on 11 Nov 2026 (catalog.py, catalog_states.py), the question engine, and the new questions."""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ask      # noqa: E402
import catalog  # noqa: E402
import dialog   # noqa: E402
import engine   # noqa: E402
import kb       # noqa: E402
import langs    # noqa: E402
import nlu      # noqa: E402
import schemes  # noqa: E402
from helpers import talk, until  # noqa: E402

FIELDS = ["id", "name", "name_hi", "benefit", "benefit_hi", "speak_en", "speak_hi", "apply", "apply_hi", "docs",
          "docs_hi", "note", "note_hi", "rule"]


def match_ids(profile):
    e, m = schemes.match(profile, "hi")
    return [s["id"] for s in e], [s["id"] for s in m]


# ---------------------------------------------------------------- every entry is complete and consistent
@pytest.mark.parametrize("s", catalog.all_entries(), ids=lambda s: s["id"])
def test_entry_complete(s):
    for f in FIELDS:
        assert s.get(f), (s["id"], f)
    assert "why" in s and "tags" in s and all(t in catalog.DOCS for t in s["tags"]), s["id"]
    assert "{web}" not in s["apply_hi"] or s.get("web"), s["id"]          # a website is only named if we have one
    known = schemes._fragments({}, "hi")
    assert all(k in known for k in s["why"]), (s["id"], s["why"])
    for lang, card in s.get("local", {}).items():
        assert len(card) == 3 and all(card), (s["id"], lang)
    facts = kb.KB[s["id"]]
    assert {"explain", "apply", "docs", "who", "money"} <= set(facts["hi"]) == set(facts["en"])


def test_same_rupee_amounts_in_hindi_and_english():
    for s in catalog.all_entries():
        amount = r"₹\d+(?:,\d+)*(?:\.\d+)?"
        assert sorted(re.findall(amount, s["benefit"])) == sorted(re.findall(amount, s["benefit_hi"])), s["id"]


def test_ids_are_unique():
    all_ids = [s["id"] for s in schemes.SCHEMES + schemes.MAYBE]
    assert len(all_ids) == len(set(all_ids))
    assert len(all_ids) >= 69


# ---------------------------------------------------------------- rules
def test_widow_in_a_village_gets_pension_ration_and_work():
    p = {"age": 45, "occupation": "labourer", "gender": "f", "widow": True, "bpl": True, "rural": True, "lpg": False,
         "income_month": 6000, "itax": False, "epf": False, "state": "MH", "pucca": False}
    e, m = match_ids(p)
    assert {"widow_pension", "free_ration", "vb_g_ram_g", "ujjwala"} <= set(e), e
    assert "pmay_g" in m and "bocw" in m


def test_pregnant_woman_gets_maternity_benefits():
    p = {"age": 26, "occupation": "homemaker", "gender": "f", "maternity": True, "state": "BR", "income_month": 0}
    e, _ = match_ids(p)
    assert "pmmvy" in e and "jsy" in e                      # Bihar: Janani Suraksha for every woman
    e, _ = match_ids({**p, "state": "MH"})
    assert "pmmvy" in e and "jsy" not in e                  # elsewhere only BPL / SC / ST women
    assert "jsy" in match_ids({**p, "state": "MH", "bpl": True})[0]
    assert "pmmvy" not in match_ids({**p, "gender": "m"})[0]


def test_senior_pensions_and_state_card_replaces_general_one():
    p = {"age": 66, "occupation": "unemployed", "bpl": True, "income_month": 0, "state": "MH"}
    e, _ = match_ids(p)
    assert "old_age_pension" in e and "vayoshri" in e
    e, _ = match_ids({**p, "state": "UP"})
    assert "up_old_age" in e and "old_age_pension" not in e          # one pension, not listed twice
    e, _ = match_ids({**p, "state": "RJ"})
    assert "rj_pension" in e and "old_age_pension" not in e


def test_students():
    p = {"age": 19, "occupation": "student", "study": "college", "category": "obc", "income_month": 0}
    e, m = match_ids(p)
    assert "pm_vidyalaxmi" in e and {"csss", "pms"} <= set(m)
    e, m = match_ids({**p, "study": "school", "category": "gen", "age": 15})
    assert "nmms" in m and "pms" not in m and "pm_vidyalaxmi" not in e


def test_disability_and_house():
    e, m = match_ids({"age": 30, "occupation": "unemployed", "disabled": True, "bpl": True})
    assert "udid" in e and {"disability_pension", "adip"} <= set(m)
    assert "surya_ghar" in match_ids({"age": 40, "occupation": "shopkeeper", "pucca": True})[0]
    assert "pmay_u" in match_ids({"age": 40, "occupation": "labourer", "pucca": False, "rural": False,
                                  "income_month": 12000})[1]


WOMAN = {"age": 30, "gender": "f", "occupation": "homemaker", "income_month": 0}
FARMER = {"age": 40, "occupation": "farmer", "land_ha": 1.0, "income_month": 8000}


@pytest.mark.parametrize("state,profile,want", [
    ("DL", WOMAN, "dl_lakshmi"), ("PB", WOMAN, "pb_mawan_dheeyan"), ("OD", WOMAN, "od_subhadra"),
    ("JH", WOMAN, "jh_maiyan"), ("CG", WOMAN, "cg_mahtari"), ("HP", WOMAN, "hp_pyari_behna"),
    ("AP", FARMER, "ap_annadata"), ("AP", {**WOMAN, "school_kids": True}, "ap_thalliki"),
    ("TG", FARMER, "tg_rythu_bharosa"), ("TG", WOMAN, "tg_mahalakshmi_bus"),
    ("GJ", {"age": 15, "gender": "f", "occupation": "student", "study": "school"}, "gj_namo_lakshmi"),
])
def test_state_schemes(state, profile, want):
    e, _ = match_ids({**profile, "state": state})
    assert want in e and e[0].startswith(state.lower() + "_"), e            # state schemes come first
    assert want not in match_ids({**profile, "state": "KL"})[0]             # and only in their own state


def test_women_schemes_not_for_men_or_taxpayers():
    base = {"age": 30, "occupation": "shopkeeper", "income_month": 0, "state": "DL"}
    assert "dl_lakshmi" not in match_ids({**base, "gender": "m"})[0]
    assert "dl_lakshmi" not in match_ids({**base, "gender": "f", "itax": True})[0]
    assert "dl_lakshmi" not in match_ids({**base, "gender": "f", "income_month": 30000})[0]


def test_state_card_in_the_states_language():
    e, _ = schemes.match({**FARMER, "state": "TG"}, "te")
    card = next(s for s in e if s["id"] == "tg_rythu_bharosa")
    assert "రైతు" in card["name_local"] and "₹12,000" in card["benefit_local"]


# ---------------------------------------------------------------- the question engine
def _asked(first, answers):
    r = dialog.turn({}, "", "hi")
    r = dialog.turn(r["state"], first, "hi")
    seen = []
    while not r["done"]:
        seen.append(r["state"]["asked"])
        r = dialog.turn(r["state"], answers.get(seen[-1], "nahi"), "hi")
        assert len(seen) < 30
    return seen, r


def test_conversation_stays_short():
    for first in ["main 34 saal ka kisan hoon", "main 30 saal ki hoon, ghar sambhalti hoon", "22 saal ka student hoon",
                  "72 saal ka hoon, kuch kaam nahi karta"]:
        seen, r = _asked(first, {"state": "UP se", "gender": "pata nahi", "category": "pata nahi", "study": "college"})
        follow = [s for s in seen if s not in engine.CORE]
        assert len(follow) <= engine.MAX_FOLLOWUPS + 2, (first, seen)       # +2: a prerequisite or one re-ask


def test_never_asks_a_man_about_pregnancy_or_a_farmer_about_pf():
    seen, _ = _asked("main 34 saal ka kisan hoon, do acre zameen", {"state": "bihar", "gender": "purush"})
    assert not {"maternity", "widow", "special", "epf", "biz"} & set(seen), seen
    seen, _ = _asked("main 30 saal ka mazdoor hoon", {"state": "bihar", "gender": "purush"})
    assert not {"maternity", "widow", "special", "land_ha"} & set(seen), seen


def test_income_tax_is_only_asked_after_income():
    seen, _ = _asked("main 40 saal ka hoon, dukaan hai", {"state": "UP", "income_month": "ek lakh mahina"})
    assert "itax" in seen and seen.index("income_month") < seen.index("itax"), seen


def test_one_question_for_widow_pregnant_disabled():
    r = until("special", "main 35 saal ki hoon, ghar sambhalti hoon", {"state": "bihar", "income_month": "kuch nahi"})
    p = dialog.turn(r["state"], "main vidhwa hoon", "hi")["state"]["profile"]
    assert p["widow"] is True and p["maternity"] is False and p["disabled"] is False
    p = dialog.turn(r["state"], "nahi", "hi")["state"]["profile"]
    assert p["widow"] is False and p["maternity"] is False and p["disabled"] is False


def test_engine_reports_what_is_still_open():
    rules = dialog.rules()
    decided, open_ = engine.status(rules, {"age": 30, "occupation": "farmer", "state": "UP"})
    assert "land_ha" in open_["pm_kisan"] and decided["pm_svanidhi"] is False
    decided, open_ = engine.status(rules, {"age": 75, "occupation": "unemployed", "state": "UP"})
    assert decided["vay_vandana"] is True and decided["apy"] is False


def test_full_conversation_finds_new_schemes():
    r = talk("main 45 saal ki vidhwa hoon, gaon mein mazdoori karti hoon, 6 hazaar mahina",
             {"state": "maharashtra", "bpl": "haan", "pucca": "nahi", "lpg": "nahi", "epf": "nahi"})
    got = [s["id"] for s in r["eligible"]]
    assert {"widow_pension", "free_ration", "vb_g_ram_g"} <= set(got), got


# ---------------------------------------------------------------- understanding the new details
@pytest.mark.parametrize("text,expecting,want", [
    ("main vidhwa hoon", None, {"widow": True, "gender": "f"}),
    ("मैं गाँव में रहती हूँ", None, {"rural": True}),
    ("shehar mein", "rural", {"rural": False}),
    ("OBC", "category", {"category": "obc"}), ("हम दलित हैं", "category", {"category": "sc"}),
    ("general", "category", {"category": "gen"}),
    ("college mein", "study", {"study": "college"}), ("दसवीं कक्षा", "study", {"study": "school"}),
    ("kaccha makaan hai", "pucca", {"pucca": False}), ("haan hai", "lpg", {"lpg": True}),
    ("nahi", "bpl", {"bpl": False}), ("haan, do bachche school jaate hain", "school_kids", {"school_kids": True}),
])
def test_new_details_understood(text, expecting, want):
    got = nlu.extract(text, expecting=expecting)
    for k, v in want.items():
        assert got.get(k) == v, (text, got)


def test_skip_leaves_a_detail_blank():
    assert nlu.clarify("छोड़िए") == "dontknow" and nlu.clarify("skip") == "dontknow"


@pytest.mark.parametrize("lang", ["bn", "gu", "kn", "ml", "mr", "pa", "ta", "te"])
def test_new_questions_in_every_language(lang):
    p = langs.pack(lang)
    for key in ["rural", "bpl", "pucca", "lpg", "maternity", "widow", "disabled", "category", "study", "school_kids",
                "special"]:
        text = re.sub(r"\b(BPL|SC|ST|OBC)\b", "", p.Q[key])
        assert text and langs.script_counts(text)["latin"] == 0, (lang, key)


# ---------------------------------------------------------------- the follow-up chat knows the new schemes
def test_chat_answers_from_the_card():
    a = ask.answer("kaunse kagaz chahiye", "hi", focus="pmmvy", eligible_ids=["pmmvy"], names={"pmmvy": "x"}, why={})
    assert a["intent"] == "docs" and "आधार" in a["say"]
    a = ask.answer("kahan apply karun", "hi", focus="surya_ghar", eligible_ids=["surya_ghar"],
                   names={"surya_ghar": "x"}, why={})
    assert "pmsuryaghar.gov.in" in a["show"] and "{web}" not in a["say"]
    a = ask.answer("vidhwa pension ke baare mein batao", "hi", focus="free_ration",
                   eligible_ids=["free_ration", "widow_pension"], names={}, why={})
    assert a["focus"] == "widow_pension"
