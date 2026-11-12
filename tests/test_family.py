"""The "about ₹X a year" line, the one combined list of papers, and checking for more than one family member."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import catalog  # noqa: E402
import dialog   # noqa: E402
import langs    # noqa: E402
from helpers import talk  # noqa: E402


def finish(r, answers=None, lang="hi"):
    answers = answers or {}
    n = 0
    while not r["done"]:
        slot = r["state"]["asked"]
        r = dialog.turn(r["state"], answers.get(slot, {"state": "pata nahi", "gender": "pata nahi"}.get(slot, "nahi")), lang)
        n += 1
        assert n < 40
    return r


# ---------------------------------------------------------------- yearly money: only what is fixed and yearly
def test_yearly_cash_counts_only_fixed_yearly_money():
    assert catalog.yearly_cash(["pm_kisan", "mh_namo_shetkari"]) == 12000
    assert catalog.yearly_cash(["mudra", "pmjjby", "kcc", "surya_ghar", "pmmvy"]) == 0      # loans, cover, one-time
    assert catalog.yearly_cash(["dl_lakshmi"]) == 30000 and catalog.yearly_cash(["jh_maiyan"]) == 30000


def test_farmer_is_told_the_yearly_amount():
    r = talk("Main 34 saal ka kisan hoon, Pune se", {"land_ha": "do acre", "income_month": "8 hazaar"})
    assert r["cash_year"] == 12000                         # PM-KISAN + Namo Shetkari
    assert "₹12,000" in r["summary"] and "12000" in r["say"]
    assert "₹12,000" not in r["show"]                      # the page shows the amount in its own summary card


def test_no_amount_line_when_nothing_is_fixed():
    r = talk("40 saal, private naukri, 90 hazaar mahina", {"itax": "haan tax bharta hoon"})
    assert r["cash_year"] == 0 and "₹0" not in r["show"]


# ---------------------------------------------------------------- one list of papers
def test_papers_are_combined_and_ordered():
    tags, labels = catalog.papers(["pm_kisan", "kcc", "pmjjby"], "hi")
    assert tags == ["aadhaar", "bank", "photo", "land"]
    assert labels[0] == "आधार कार्ड" and len(labels) == len(set(labels))
    assert catalog.papers(["pm_kisan"], "en")[1] == ["Aadhaar card", "bank passbook", "land records"]


def test_results_show_the_combined_list():
    r = talk("Main 34 saal ka kisan hoon", {"land_ha": "do acre", "income_month": "8 hazaar"})
    assert r["docs_all"][:2] == ["आधार कार्ड", "बैंक पासबुक"] and "ज़मीन के कागज़" in r["docs_all"]
    assert "आधार कार्ड, बैंक पासबुक" in r["summary"]


@pytest.mark.parametrize("lang", ["bn", "gu", "kn", "ml", "mr", "pa", "ta", "te"])
def test_papers_in_every_language(lang):
    _, labels = catalog.papers(["pm_kisan", "eshram", "mh_ladki_bahin"], lang)
    assert labels and all(langs.script_counts(x)["latin"] == 0 for x in labels), (lang, labels)
    p = langs.pack(lang)
    assert "{amt}" in p.Q["saved"] and "{docs}" in p.Q["docs_all"] and p.Q["member_intro"]


# ---------------------------------------------------------------- family: same home, next person
def test_next_member_keeps_the_home_and_forgets_the_person():
    r = talk("Main 34 saal ka kisan hoon, Lucknow se", {"land_ha": "do acre", "income_month": "8 hazaar", "bpl": "haan",
                                                        "pucca": "nahi"})
    first = r["state"]["profile"]
    assert first["state"] == "UP" and first["bpl"] is True
    m = dialog.next_member(r["state"], "hi")
    p = m["state"]["profile"]
    assert m["member"] == 2 and not m["done"] and "परिवार" in m["show"]
    assert p == {k: first[k] for k in dialog.SHARED if k in first}        # state, village, ration card, house, gas
    assert "age" not in p and "occupation" not in p and "land_ha" not in p


def test_mother_gets_her_own_list():
    r = talk("Main 34 saal ka kisan hoon, Lucknow se", {"land_ha": "do acre", "income_month": "8 hazaar", "bpl": "haan"})
    m = dialog.next_member(r["state"], "hi")
    r2 = dialog.turn(m["state"], "meri maa 66 saal ki hain, ghar par rehti hain", "hi")
    r2 = finish(r2, {"income_month": "kuch nahi"})
    ids = [s["id"] for s in r2["eligible"]]
    assert "up_old_age" in ids and "pm_kisan" not in ids                  # her list, not her son's
    assert r2["member"] == 2 and r2["cash_year"] >= 12000
    asked_again = [k for k in ("state", "bpl") if r2["state"]["profile"].get(k) is None]
    assert not asked_again                                                # the home's details were not asked again


def test_relative_named_in_the_first_sentence():
    import nlu
    assert nlu.relation_gender("meri maa 66 saal ki hain") == "f" and nlu.relation_gender("मेरे पिताजी किसान हैं") is None
    assert nlu.relation_gender("mere pita ji kisan hain") == "m" and nlu.relation_gender("main 30 saal ka hoon") is None
    assert nlu.detect_occupation("meri maa ghar par rehti hain")[0] == "homemaker"
    assert nlu.detect_occupation("pitaji retired hain")[0] == "unemployed"
    r = talk("Main 34 saal ka kisan hoon, Lucknow se", {"land_ha": "do acre", "income_month": "8 hazaar"})
    m = dialog.next_member(r["state"], "hi")
    r2 = dialog.turn(m["state"], "meri maa 66 saal ki hain, ghar par rehti hain", "hi")
    p = r2["state"]["profile"]
    assert p["gender"] == "f" and p["occupation"] == "homemaker" and p["age"] == 66
    assert r2["state"]["asked"] not in ("gender", "occupation", "age", "state")
