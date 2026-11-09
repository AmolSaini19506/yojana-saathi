"""Run:  python -m pytest -q   (or just: python tests/test_flow.py)"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ask     # noqa: E402
import dialog  # noqa: E402
import nlu     # noqa: E402


def ids(res):
    return [s["id"] for s in res.get("eligible", [])]


# Questions added later (state, gender, business) get a neutral answer so these older scripts still work:
# "don't know" leaves the state blank (central schemes only), and "no" to starting a business.
AUTO = {"state": "pata nahi", "gender": "pata nahi", "biz": "nahi"}


def _auto(r, lang):
    while not r["done"] and r["state"].get("asked") in AUTO:
        r = dialog.turn(r["state"], AUTO[r["state"]["asked"]], lang)
    return r


def run(turns, lang="hi"):
    r = dialog.turn({}, "", lang)
    for t in turns:
        r = _auto(r, lang)
        assert not r["done"], f"finished early before: {t}"
        r = dialog.turn(r["state"], t, lang)
    return _auto(r, lang)


# ---------------------------------------------------------------- NLU

def test_hinglish_free_form():
    g = nlu.extract("Main 35 saal ka hoon, kirana ki dukaan hai, 15 hazaar mahine kamata hoon, tax nahi bharta")
    assert g == {"occupation": "shopkeeper", "age": 35, "income_month": 15000, "itax": False, "gender": "m"}  # kamata


def test_devanagari_free_form():
    g = nlu.extract("मेरी उम्र 42 साल है, मैं किसान हूँ, 3 एकड़ ज़मीन है")
    assert g["age"] == 42 and g["occupation"] == "farmer" and abs(g["land_ha"] - 1.214) < 0.01


def test_devanagari_digits_and_words():
    assert nlu.extract("उम्र ३० साल")["age"] == 30
    assert nlu.extract("पच्चीस साल")["age"] == 25
    assert nlu.extract("pachas hazaar", expecting="income_month")["income_month"] == 50000


def test_yearly_income_converted():
    assert nlu.extract("saal ke 2 lakh kama leta hoon")["income_month"] == 16667
    assert nlu.extract("2.4 lakh salana")["income_month"] == 20000


def test_bigha_and_bare_land():
    assert nlu.extract("do bigha zameen")["land_ha"] == 0.5
    assert nlu.extract("2", expecting="land_ha")["land_ha"] == 0.809
    assert nlu.extract("zameen nahi hai", expecting="land_ha")["land_ha"] == 0.0


def test_artisan_trade():
    assert nlu.detect_occupation("main darzi ka kaam karta hoon") == ("artisan", "tailor")
    assert nlu.detect_occupation("मैं बढ़ई हूँ") == ("artisan", "carpenter")


def test_street_vendor_vs_shop():
    assert nlu.detect_occupation("sabzi ka thela lagata hoon")[0] == "street_vendor"
    assert nlu.detect_occupation("meri chhoti si dukaan hai")[0] == "shopkeeper"


def test_english_do_is_not_two():
    g = nlu.extract("I do farming", expecting="land_ha")
    assert "land_ha" not in g and g["occupation"] == "farmer"


def test_yes_no():
    assert nlu.parse_yes_no("haan ji") is True
    assert nlu.parse_yes_no("nahi") is False
    assert nlu.parse_yes_no("नहीं") is False
    assert nlu.extract("PF nahi katta", expecting="epf")["epf"] is False


# ---------------------------------------------------------------- full conversations

def test_farmer_flow():
    r = run(["Main 34 saal ka kisan hoon", "do acre", "8 hazaar", "haan ek beti hai 6 saal ki"])
    assert r["done"]
    got = ids(r)
    for want in ["pm_kisan", "pm_kmy", "apy", "pmjjby", "pmsby", "sukanya"]:
        assert want in got, (want, got)


def test_shopkeeper_one_shot():
    r = run(["Main 35 saal ka hoon, kirana ki dukaan hai, 15 hazaar mahine kamata hoon", "nahi"])
    assert r["done"], r["show"]
    got = ids(r)
    assert "mudra" in got and "eshram" in got and "apy" in got and "sukanya" not in got


def test_street_vendor_flow():
    r = run(["28 saal, sabzi ka thela lagata hoon, 12000 mahina", "nahi", "nahi"])
    got = ids(r)
    assert {"pm_svanidhi", "pm_sym", "mudra", "eshram", "apy"} <= set(got), got


def test_senior_flow_english():
    r = run(["I am 72 years old and I am a homemaker", "nothing"], lang="en")
    assert r["done"]
    assert "vay_vandana" in ids(r) and "apy" not in ids(r)


def test_tax_payer_excluded():
    r = run(["40 saal, private naukri, 90 hazaar mahina", "haan tax bharta hoon", "haan PF katta hai", "nahi"])
    got = ids(r)
    assert "apy" not in got and "pm_sym" not in got and "pmjjby" in got


def test_retry_then_skip():
    r = dialog.turn({}, "", "hi")
    r = dialog.turn(r["state"], "pata nahi", "hi")      # intro: nothing understood -> asks age
    assert r["state"]["asked"] == "age"
    r = dialog.turn(r["state"], "hmm", "hi")            # can't parse -> retry once
    assert r["state"]["asked"] == "age" and "samajh" in r["show"].lower()
    r = dialog.turn(r["state"], "hmm", "hi")            # still nothing -> move on
    assert r["state"]["asked"] == "occupation"


# ---------------------------------------------------------------- follow-up chat (Samjhaiye)

def _chat(q, focus="pm_kisan", lang="hi", ids=None):
    ids = ids or ["pm_kisan", "pm_kmy", "apy", "pmjjby", "pmsby"]
    return ask.answer(q, lang, focus=focus, eligible_ids=ids, names={i: i for i in ids}, why={})


def test_ask_intents():
    assert _chat("")["intent"] == "explain"
    assert _chat("kahan apply karun?")["intent"] == "apply"
    assert _chat("कौन से कागज़ चाहिए")["intent"] == "docs"
    assert _chat("paisa kab aayega")["intent"] == "when"
    assert _chat("kitna jama karna padega", focus="apy")["intent"] == "cost"
    assert _chat("which documents do I need", lang="en")["intent"] == "docs"


def test_ask_switches_scheme_by_name():
    a = _chat("aur atal pension?")
    assert a["focus"] == "apy" and a["intent"] == "explain"


def test_ask_does_not_switch_to_unlisted_scheme():
    a = _chat("mudra loan kahan milega")          # mudra isn't on this person's list
    assert a["focus"] == "pm_kisan"


def test_ask_helpline_spoken_as_digits():
    a = _chat("helpline number")
    assert "155261" in a["show"] and "एक पाँच पाँच" in a["say"]
    assert "पक्का" in _chat("helpline", focus="apy")["say"]      # no verified number -> says so


def test_ask_unknown_never_guesses():
    a = _chat("kya main is paise se tractor khareed sakta hoon")
    assert a["intent"] == "unknown" and "अंदाज़ा" in a["say"]


def test_ask_web_spoken_not_spelled():
    a = _chat("online apply ho sakta hai?")
    assert "pmkisan.gov.in" in a["show"] and "डॉट" in a["say"]


def test_why_reasons():
    r = run(["Main 34 saal ka kisan hoon, mahine ke 8 hazaar", "do acre", "nahi"])
    why = {s["id"]: s["why"] for s in r["eligible"]}
    assert "किसान" in why["pm_kisan"] and "34" in why["pm_kmy"]


if __name__ == "__main__":
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("ok  ", name)
            except AssertionError as e:
                fails += 1
                print("FAIL", name, e)
    sys.exit(1 if fails else 0)
