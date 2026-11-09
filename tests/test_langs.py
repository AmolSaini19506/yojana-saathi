"""Checks every language pack in langs/ is complete and that the app understands a sample answer in it.

Run:  python -m pytest -q tests/test_langs.py
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ask      # noqa: E402
import dialog   # noqa: E402
import kb       # noqa: E402
import langs    # noqa: E402
import nlu      # noqa: E402
import schemes  # noqa: E402

PACKS = langs.PACK_IDS
UI_KEYS = ["tap", "answer", "think", "speak", "listen", "heard", "ask", "nothing", "eligible", "check", "where", "docs",
           "note", "why", "explain", "wa", "copy", "copied", "back", "talking", "explain_me", "rec", "share_head",
           "share_also", "share_tail", "sug", "and", "beta"]
WHY_KEYS = ["farmer", "land", "small_land", "no_tax", "age", "vendor", "artisan", "business", "unorganised", "shop",
            "income", "no_pf", "daughter", "senior"]

# One made-up person per language: (intro sentence, expected slots, yes/no answers for the follow-ups)
SAMPLES = {
    "ta": ("நான் 34 வயது விவசாயி, 2 ஏக்கர் நிலம் இருக்கிறது, மாதம் 8000 ரூபாய் சம்பாதிக்கிறேன்",
           {"age": 34, "occupation": "farmer", "income_month": 8000}, "ஆமாம்", "இல்லை"),
    "bn": ("আমার বয়স 34 বছর, আমি কৃষক, 2 একর জমি আছে, মাসে 8000 টাকা আয় করি",
           {"age": 34, "occupation": "farmer", "income_month": 8000}, "হ্যাঁ", "না"),
    "gu": ("મારી ઉંમર 34 વર્ષ છે, હું ખેડૂત છું, 2 એકર જમીન છે, મહિને 8000 રૂપિયા કમાઉં છું",
           {"age": 34, "occupation": "farmer", "income_month": 8000}, "હા", "ના"),
    "pa": ("ਮੇਰੀ ਉਮਰ 34 ਸਾਲ ਹੈ, ਮੈਂ ਕਿਸਾਨ ਹਾਂ, 2 ਏਕੜ ਜ਼ਮੀਨ ਹੈ, ਮਹੀਨੇ ਦੇ 8000 ਰੁਪਏ ਕਮਾਉਂਦਾ ਹਾਂ",
           {"age": 34, "occupation": "farmer", "income_month": 8000}, "ਹਾਂ", "ਨਹੀਂ"),
    "mr": ("माझं वय 34 वर्षे आहे, मी शेतकरी आहे, 2 एकर जमीन आहे, महिन्याला 8000 रुपये कमावतो",
           {"age": 34, "occupation": "farmer", "income_month": 8000}, "हो", "नाही"),
    "te": ("నా వయసు 34 సంవత్సరాలు, నేను రైతుని, 2 ఎకరాల భూమి ఉంది, నెలకు 8000 రూపాయలు సంపాదిస్తాను",
           {"age": 34, "occupation": "farmer", "income_month": 8000}, "అవును", "లేదు"),
    "kn": ("ನನ್ನ ವಯಸ್ಸು 34 ವರ್ಷ, ನಾನು ರೈತ, 2 ಎಕರೆ ಜಮೀನು ಇದೆ, ತಿಂಗಳಿಗೆ 8000 ರೂಪಾಯಿ ಗಳಿಸುತ್ತೇನೆ",
           {"age": 34, "occupation": "farmer", "income_month": 8000}, "ಹೌದು", "ಇಲ್ಲ"),
    "ml": ("എന്റെ പ്രായം 34 വയസ്സ്, ഞാൻ കർഷകനാണ്, 2 ഏക്കർ ഭൂമിയുണ്ട്, മാസം 8000 രൂപ സമ്പാദിക്കുന്നു",
           {"age": 34, "occupation": "farmer", "income_month": 8000}, "അതെ", "ഇല്ല"),
}


@pytest.mark.parametrize("lang", PACKS)
def test_pack_complete(lang):
    p = langs.pack(lang)
    assert set(dialog.Q["hi"]) <= set(p.Q), set(dialog.Q["hi"]) - set(p.Q)
    assert "{n}" in p.Q["found"]
    assert set(ask.LINES["hi"]) <= set(p.LINES)
    for k, field in (("helpline", "{name}"), ("helpline", "{helpline}"), ("dont_know_tail_h", "{helpline}"),
                     ("why", "{why}")):
        assert field in p.LINES[k], (k, field)
    assert set(UI_KEYS) <= set(p.UI), set(UI_KEYS) - set(p.UI)
    assert len(p.UI["sug"]) == 5
    assert set(WHY_KEYS) <= set(p.WHY) and "{age}" in p.WHY["age"] and "{inc}" in p.WHY["income"]
    for s in schemes.SCHEMES + schemes.MAYBE:
        name, benefit, speak = p.SCHEMES[s["id"]]
        assert name and benefit and speak, s["id"]


@pytest.mark.parametrize("lang", PACKS)
def test_pack_facts_match_hindi(lang):
    """Same schemes, same question types as the verified Hindi facts; placeholders only where they can be filled."""
    p = langs.pack(lang)
    assert set(p.KB) == set(kb.KB)
    for sid, entry in kb.KB.items():
        assert set(p.KB[sid]) == set(entry["hi"]), (sid, set(entry["hi"]) ^ set(p.KB[sid]))
        for intent, text in p.KB[sid].items():
            for ph in re.findall(r"\{(\w+)\}", text):
                assert ph in ("web", "helpline"), (sid, intent, ph)
                assert entry.get(ph), (sid, intent, f"{{{ph}}} used but kb.py has no {ph}")


@pytest.mark.parametrize("lang", [x for x in PACKS if x in SAMPLES])
def test_sample_person(lang):
    intro, expect, yes, no = SAMPLES[lang]
    got = nlu.extract(intro, lang=lang)
    for k, v in expect.items():
        assert got.get(k) == v, (lang, k, got)
    assert 0.7 < got.get("land_ha", 0) < 0.9, (lang, got)     # 2 acres
    assert nlu.parse_yes_no(yes, lang) is True and nlu.parse_yes_no(no, lang) is False
    assert langs.detect(intro, None, "hi") == lang

    # whole conversation in that language ends with PM-KISAN
    r = dialog.turn({}, "", lang)
    r = dialog.turn(r["state"], intro, lang)
    for _ in range(6):
        if r["done"]:
            break
        r = dialog.turn(r["state"], no, lang)
    assert r["done"] and r["lang"] == lang
    ids = [s["id"] for s in r["eligible"]]
    assert "pm_kisan" in ids and "pm_kmy" in ids, ids
    assert all(s["speak"] for s in r["eligible"]) and r["eligible"][0]["why"]


@pytest.mark.parametrize("lang", PACKS)
def test_suggestion_buttons_understood(lang):
    p = langs.pack(lang)
    wanted = ["apply", "docs", "money", "cost", "helpline"]
    got = [ask.detect_intent(q, lang) for _, q in p.UI["sug"]]
    assert got == wanted, (lang, got)
    a = ask.answer(p.UI["sug"][1][1], lang, focus="pm_kisan")
    assert a["intent"] == "docs" and a["say"] == p.KB["pm_kisan"]["docs"]


def test_detect_keeps_language_for_short_answers():
    assert langs.detect("35", "hi-IN", "ta") == "ta"
    assert langs.detect("yes", "en-IN", "hi") == "hi"
    assert langs.detect("I am 35 years old and a farmer", "en-IN", "hi") == "en"
    assert langs.detect("main 35 saal ka hoon", "en-IN", "en") == "hi"
    assert langs.detect("मैं 35 साल का हूँ, किसान हूँ", "hi-IN", "en") == "hi"


def test_helpline_spoken_as_digits_in_packs():
    if "ta" not in PACKS:
        pytest.skip("no Tamil pack")
    a = ask.answer("உதவி எண் என்ன", "ta", focus="pm_kisan")
    assert a["intent"] == "helpline" and "1 5 5 2 6 1" in a["say"] and "155261" in a["show"]


# Real Prisma v3.0 transcripts (indic-auto, format=transcribe) of Timbre reading the samples above, 9 Nov 2026.
# Prisma sometimes writes numbers as words (Tamil) and adds "8,000" commas, so we keep them as regression tests.
REAL_PRISMA = [
    ("ta", "ta-IN", "நான் முப்பத்து நான்கு வயது விவசாயி 2 ஏக்கர் நிலம் இருக்கிறது மாதம் 8,000 ரூபாய் சம்பாதிக்கிறேன்."),
    ("mr", "mr-IN", "माझं वय 34 वर्षे आहे. मी शेतकरी आहे. 2 एकर जमीन आहे. महिन्याला 8000 रुपये कमावतो."),
    ("te", "te-IN", "నా వయసు 34 సంవత్సరాలు నేను రైతుని 2 ఎకరాల భూమి ఉంది నెలకు 8,000 రూపాయలు సంపాదిస్తాను."),
    ("gu", "gu-IN", "મારી ઉંમર 34 વર્ષ છે હું ખેડૂત છું 2 એકર જમીન છે મહિને 8,000 રૂપિયા કમાઉં છું."),
    ("kn", "kn-IN", "ನನ್ನ ವಯಸ್ಸು 34 ವರ್ಷ ನಾನು ರೈತ 2 ಎಕರೆ ಜಮೀನು ಇದೆ. ತಿಂಗಳಿಗೆ 8,000 ರೂಪಾಯಿ ಗಳಿಸುತ್ತೇನೆ."),
    ("ml", "ml-IN", "എന്റെ പ്രായം 34 വയസ്സ്. ഞാൻ കർഷകനാണ്. 2 ഏക്കർ ഭൂമിയുണ്ട്. മാസം 8000 രൂപ സമ്പാദിക്കുന്നു."),
    ("en", "en-IN", "I am 34 years old. I am a farmer with 2 acres of land, and I earn 8,000 rupees a month."),
    ("hi", "hi-IN", "मैं 34 साल का हूँ, किसान हूँ, 2 एकड़ ज़मीन है, महीने के 8000 रुपये कमाता हूँ।"),
]


@pytest.mark.parametrize("lang,detected,text", REAL_PRISMA)
def test_real_prisma_transcripts(lang, detected, text):
    assert langs.detect(text, detected, "hi") == lang
    got = nlu.extract(text, lang=lang)
    assert (got.get("age"), got.get("occupation"), got.get("income_month")) == (34, "farmer", 8000), got
    assert abs(got["land_ha"] - 0.809) < 0.01


@pytest.mark.parametrize("lang,text", [("ta", "முப்பத்திநான்கு வயது"), ("ml", "മുപ്പത്തിനാല് വയസ്സ്"),
                                       ("kn", "ಮೂವತ್ತನಾಲ್ಕು ವರ್ಷ"), ("te", "ముప్పై నాలుగు సంవత్సరాలు"),
                                       ("en", "thirty four years old")])
def test_number_words_tens_plus_unit(lang, text):
    assert nlu.extract(text, lang=lang)["age"] == 34
