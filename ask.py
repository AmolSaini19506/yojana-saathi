"""
Follow-up chat about one scheme ("Samjhaiye" button).

1. Detect which scheme the person means (keeps the current one if they don't name another).
2. Detect what they're asking (where to apply, documents, how much, ...).
3. Answer from kb.py. If the question is outside the known facts:
     - with LLM_API_KEY set: an LLM answers, but ONLY from that scheme's facts (else says it doesn't know)
     - without: says it doesn't know and points to the helpline / CSC.
Nothing is ever invented.
"""
import json
import os
import re
import unicodedata

from functools import lru_cache

import requests

import langs
from kb import INTENTS, KB, SCHEME_NAMES
from nlu import find_kw, kw, normalize

HI_DIGITS = ["शून्य", "एक", "दो", "तीन", "चार", "पाँच", "छह", "सात", "आठ", "नौ"]
EN_DIGITS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def _n(s):
    return unicodedata.normalize("NFC", (s or "")).lower()


def _has(text, keys):
    t = f" {_n(text)} "
    for k in keys:
        k = _n(k)
        if re.search(rf"(?<![a-zऀ-ॿ]){re.escape(k)}(?:s|es)?(?![a-zऀ-ॿ])", t) or (" " in k and k in t):
            return True
    return False


def _has_pack(text, keys):
    """Language-pack keywords are stems: match at the start of a word."""
    t = normalize(text)
    return any(find_kw(t, kw(k)) for k in keys)


@lru_cache(maxsize=None)
def _pack_tables(lang):
    p = langs.pack(lang)
    names = getattr(p, "SCHEME_NAMES", {}) if p else {}
    intents = getattr(p, "INTENTS", {}) if p else {}
    return names, intents


def detect_scheme(text, allowed=None, lang="hi"):
    names, _ = _pack_tables(lang)
    for sid, keys in SCHEME_NAMES:
        if allowed and sid not in allowed:
            continue
        if _has(text, keys) or (names.get(sid) and _has_pack(text, names[sid])):
            return sid
    return None


def detect_intent(text, lang="hi"):
    _, intents = _pack_tables(lang)
    for intent, keys in INTENTS:
        if _has(text, keys) or (intents.get(intent) and _has_pack(text, intents[intent])):
            return intent
    return None


def _spell(num, lang):
    if lang not in ("hi", "en"):
        return " ".join(d for d in num if d.isdigit())     # Timbre reads each digit in that language
    words = HI_DIGITS if lang == "hi" else EN_DIGITS
    return " ".join(words[int(d)] for d in num if d.isdigit())


def _facts(sid, lang):
    p = langs.pack(lang)
    return p.KB[sid] if p else KB[sid][lang]


def _lines(lang):
    p = langs.pack(lang)
    return p.LINES if p else LINES[lang]


def _fill(template, sid, lang):
    """Return (show, say) with {web} / {helpline} filled in differently for screen and voice."""
    k = KB[sid]
    web = k.get("web") or ""
    spoken_web = k.get(f"web_{lang}") or web               # packs: Timbre reads web addresses in English
    show = template.replace("{web}", web).replace("{helpline}", k.get("helpline", ""))
    say = template.replace("{web}", spoken_web).replace("{helpline}", _spell(k.get("helpline", ""), lang))
    return show, say


LINES = {
    "hi": {
        "helpline": "{name} की हेल्पलाइन है {helpline}।",
        "no_helpline": "इस योजना का पक्का हेल्पलाइन नंबर मेरे पास नहीं है। नज़दीकी सीएससी केंद्र या बैंक पर पूछिए।",
        "dont_know": "इस सवाल का पक्का जवाब मेरे पास नहीं है, और मैं अंदाज़ा नहीं लगाऊँगा। ",
        "dont_know_tail_h": "हेल्पलाइन {helpline} पर या नज़दीकी सीएससी केंद्र पर पूछिए।",
        "dont_know_tail": "नज़दीकी सीएससी केंद्र या बैंक पर पूछिए।",
        "follow": " आप पूछ सकते हैं: कहाँ आवेदन करें, कौन से कागज़ चाहिए, या कितना पैसा मिलेगा।",
        "why": "आप इसलिए योग्य लग रहे हैं क्योंकि {why}।",
        "which": "किस योजना के बारे में जानना है? उसका नाम बोलिए, या कार्ड पर समझाइए बटन दबाइए।",
        "back": "ठीक है। बाकी योजनाएँ स्क्रीन पर हैं। किसी और के बारे में जानना हो तो उसका नाम बोलिए।",
    },
    "en": {
        "helpline": "The {name} helpline is {helpline}.",
        "no_helpline": "I don't have a confirmed helpline number for this scheme. Please ask at your nearest CSC or bank.",
        "dont_know": "I don't have a confirmed answer to that, and I won't guess. ",
        "dont_know_tail_h": "Please ask the helpline on {helpline} or at your nearest CSC.",
        "dont_know_tail": "Please ask at your nearest CSC or bank.",
        "follow": " You can ask where to apply, which documents you need, or how much you'll get.",
        "why": "You look eligible because {why}.",
        "which": "Which scheme do you want to know about? Say its name, or tap Explain on a card.",
        "back": "Okay. The other schemes are on the screen. Say a scheme's name to ask about it.",
    },
}


CAN_I = ["sakta", "sakti", "sakte", "skta", "सकता", "सकती", "सकते", "can i", "can we", "allowed", "chalega", "चलेगा"]


def _dont_know(sid, lang):
    L, k = _lines(lang), KB[sid]
    if k.get("helpline"):
        tail_show = L["dont_know_tail_h"].replace("{helpline}", k["helpline"])
        tail_say = L["dont_know_tail_h"].replace("{helpline}", _spell(k["helpline"], lang))
    else:
        tail_show = tail_say = L["dont_know_tail"]
    return L["dont_know"] + tail_show, L["dont_know"] + tail_say


# ---------------------------------------------------------------- optional grounded LLM

def llm_config():
    """Read at call time, so values from .env (loaded by app.py) are picked up."""
    return (os.environ.get("LLM_BASE_URL", "").rstrip("/"), os.environ.get("LLM_API_KEY", ""),
            os.environ.get("LLM_MODEL", ""))


def _llm(sid, question, lang, scheme_name):
    LLM_BASE, LLM_KEY, LLM_MODEL = llm_config()
    if not (LLM_BASE and LLM_KEY and LLM_MODEL):
        return None
    facts = dict(_facts(sid, lang))
    facts["website"] = KB[sid].get("web")
    facts["helpline"] = KB[sid].get("helpline")
    sys_prompt = (
        "You answer questions about ONE Indian government scheme for people who may have little schooling. "
        "Use ONLY the FACTS given. If the facts don't answer the question, reply exactly: UNKNOWN. "
        "Never invent amounts, dates, rules, numbers or websites. "
        + ("Reply in simple Hindi in Devanagari script, written to be spoken aloud: numbers as Hindi words. "
           if lang == "hi" else "Reply in simple English written to be spoken aloud. " if lang == "en" else
           f"Reply in simple {langs.pack(lang).EN_NAME} in its own script, written to be spoken aloud. ")
        + "Maximum 2 short sentences."
    )
    try:
        r = requests.post(
            f"{LLM_BASE}/chat/completions",
            headers={"Authorization": f"Bearer {LLM_KEY}", "Content-Type": "application/json"},
            json={"model": LLM_MODEL, "temperature": 0, "max_tokens": 200,
                  "messages": [{"role": "system", "content": sys_prompt},
                               {"role": "user", "content": f"SCHEME: {scheme_name}\nFACTS: "
                                f"{json.dumps(facts, ensure_ascii=False)}\nQUESTION: {question}"}]},
            timeout=20,
        )
        text = r.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        return None
    if not text or "UNKNOWN" in text.upper():
        return None
    return text


# ---------------------------------------------------------------- main entry

def answer(text, lang="hi", focus=None, eligible_ids=None, names=None, why=None):
    """
    text: what the person said ("" = just pressed Explain)
    focus: scheme currently being discussed (or None)
    eligible_ids: schemes shown on screen (only these can be switched to by name)
    names: {scheme_id: display name}; why: {scheme_id: reason text in `lang`}
    Returns dict(show, say, focus, intent).
    """
    lang = langs.valid(lang)
    L = _lines(lang)
    names, why = names or {}, why or {}
    allowed = set(eligible_ids or KB.keys())

    intent = detect_intent(text, lang) if text else "explain"
    named = detect_scheme(text, allowed, lang) if text else None
    sid = named or focus

    if intent == "back" and not named:
        return {"show": L["back"], "say": L["back"], "focus": None, "intent": "back"}
    if not sid or sid not in KB:
        return {"show": L["which"], "say": L["which"], "focus": None, "intent": intent}
    if named and named != focus and intent is None:
        intent = "explain"                       # "aur Atal Pension?" -> explain the new scheme
    if intent is None:
        intent = "unknown"
    # "kya main X kar sakta hoon?" is a specific yes/no question; a keyword like "paise" in it
    # shouldn't trigger the generic money answer. Let the LLM (if any) or "don't know" handle it.
    can_i = getattr(langs.pack(lang), "CAN_I", [])
    if intent in ("money", "explain") and text and (_has(text, CAN_I) or any(kw(c) in normalize(text) for c in can_i)):
        intent = "unknown"

    facts = _facts(sid, lang)
    name = names.get(sid, sid)

    if intent == "explain":
        show, say = _fill(facts["explain"], sid, lang)
        if why.get(sid):
            w = L["why"].format(why=why[sid])
            show, say = f"{show}\n\n{w}", f"{say} {w}"
        show += "\n\n" + L["follow"].strip()
        say += L["follow"]
        return {"show": show, "say": say, "focus": sid, "intent": intent}

    if intent == "helpline":
        hl = KB[sid].get("helpline")
        if hl:
            return {"show": L["helpline"].format(name=name, helpline=hl),
                    "say": L["helpline"].format(name=name, helpline=_spell(hl, lang)), "focus": sid, "intent": intent}
        return {"show": L["no_helpline"], "say": L["no_helpline"], "focus": sid, "intent": intent}

    template = facts.get(intent)
    if template is None and intent == "online":
        template = facts.get("apply")
    if template:
        show, say = _fill(template, sid, lang)
        return {"show": show, "say": say, "focus": sid, "intent": intent}

    llm = _llm(sid, text, lang, name)
    if llm:
        return {"show": llm, "say": llm, "focus": sid, "intent": "llm"}
    show, say = _dont_know(sid, lang)
    return {"show": show, "say": say, "focus": sid, "intent": "unknown"}
