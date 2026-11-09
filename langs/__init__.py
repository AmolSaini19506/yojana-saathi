"""
Languages.

Hindi ("hi") and English ("en") live in the main modules (dialog.py, kb.py, schemes.py, ask.py, nlu.py).
The other 8 languages that Gnani Prisma v3.0 (STT) and Timbre v3.0 (TTS) support each have ONE file here,
holding everything for that language: questions, scheme cards, verified facts, and the words the parser looks for.

BETA packs were translated by an AI assistant and have NOT been checked by a native speaker yet. The UI says so.
Amounts and rules are identical in every language: they are the same verified facts, only translated.

Auto-detection: Prisma returns `detected_language_code` (derived from the script of the transcript).
We also look at the script of the text ourselves, so typed answers work too, and we keep the current
language for short answers like "35" or "yes" so the conversation doesn't flip-flop.
"""
import importlib
import importlib.util
import os
import re

BASE = {
    "hi": {"code": "hi-IN", "name": "हिंदी / Hinglish", "en_name": "Hindi", "beta": False},
    "en": {"code": "en-IN", "name": "English", "en_name": "English", "beta": False},
}
PACK_IDS = ["bn", "gu", "kn", "ml", "mr", "pa", "ta", "te"]
PACK_IDS = [x for x in PACK_IDS if importlib.util.find_spec(f"langs.{x}")]      # skip packs not written yet
PACKS = {lang: importlib.import_module(f"langs.{lang}") for lang in PACK_IDS}
ALL = ["hi", "en"] + PACK_IDS


def pack(lang):
    """The language-pack module for lang, or None for hi / en (which live in the main modules)."""
    return PACKS.get(lang)


def valid(lang):
    return lang if lang in ALL else "hi"


def code(lang):
    """Gnani language code, e.g. 'ta' -> 'ta-IN'."""
    if lang in BASE:
        return BASE[lang]["code"]
    return PACKS[lang].CODE if lang in PACKS else "hi-IN"


def info():
    """For the UI's language picker."""
    out = [dict(id=k, **v) for k, v in BASE.items()]
    for lang in PACK_IDS:
        p = PACKS[lang]
        out.append({"id": lang, "code": p.CODE, "name": p.NAME, "en_name": p.EN_NAME, "beta": p.BETA, "ui": p.UI})
    return out


def stt_code(lang, auto=True, known=False, stream=False):
    """
    language_code for Prisma v3.0.
    Auto mode (default)      -> "indic-auto": Prisma works out the language every time, so we keep following the
                                person even if they switch language. (`known` is accepted but no longer changes this.)
    Language picked in menu  -> REST: that language + English as a hint ("ta-IN,en-IN"; a hint, not a lock).
                                Stream: that one language only. The live stream rejects lists:
                                "exactly one locale is required (e.g. hi-IN)" (tested 9 Nov 2026).
    """
    lang = valid(lang)
    if auto:
        return os.environ.get("STT_AUTO_CODE", "indic-auto")
    if stream:
        return code(lang)
    if lang == "en":
        return "en-IN,hi-IN"
    return f"{code(lang)},en-IN"


# ---------------------------------------------------------------- detection

SCRIPTS = [
    ("deva", 0x0900, 0x097F), ("bn", 0x0980, 0x09FF), ("pa", 0x0A00, 0x0A7F), ("gu", 0x0A80, 0x0AFF),
    ("ta", 0x0B80, 0x0BFF), ("te", 0x0C00, 0x0C7F), ("kn", 0x0C80, 0x0CFF), ("ml", 0x0D00, 0x0D7F),
]

# Hindi and Marathi share the Devanagari script, so we look at common words.
MR_MARKERS = {"आहे", "आहेत", "माझे", "माझा", "माझी", "माझं", "मला", "मी", "नाही", "करतो", "करते", "आणि", "वर्षांचा",
              "वर्षाची", "वर्षाचा", "वर्षे", "शेतकरी", "होय", "किती", "कुठे", "कोणती", "कोणते", "कागदपत्रे", "मिळेल",
              "पाहिजे", "आम्ही", "तुम्ही", "आमच्या", "माझ्या", "मुलगी", "महिन्याला", "कमावतो", "कमावते", "भरतो",
              "भरते", "कापला", "कापतो", "जमीन", "एकर", "सांगा", "मिळतात", "करायचा", "करायचे"}
HI_MARKERS = {"है", "हैं", "हूँ", "हूं", "मेरा", "मेरी", "मेरे", "नहीं", "करता", "करती", "और", "मैं", "का", "की", "के",
              "में", "से", "कितना", "कहाँ", "कहां", "चाहिए", "मिलेगा", "हम", "उम्र", "साल", "ज़मीन", "हाँ", "हां",
              "बताइए", "महीने", "कमाता", "कमाती", "भरता", "भरती", "कटता", "बेटी"}
# Roman-script Hindi ("Hinglish") vs English
HINGLISH = {"hai", "hain", "hoon", "hun", "hu", "mera", "meri", "mere", "main", "mai", "saal", "sal", "kaam", "karta",
            "karti", "karte", "nahi", "nahin", "haan", "han", "kitna", "kitne", "kya", "aur", "ka", "ki", "ke", "se",
            "mein", "ji", "hazaar", "hazar", "kisan", "kheti", "zameen", "jameen", "mahina", "mahine", "kamai", "kamata",
            "kamati", "rupaye", "beti", "kaunse", "kahan", "kagaz", "chahiye", "milega", "batao", "bataiye", "umar",
            "dukaan", "dukan", "thela", "mazdoor", "naukri", "bharta", "katta", "lakh", "bigha", "samjhaiye", "paisa"}
ENGLISH = {"i", "am", "my", "me", "years", "year", "old", "work", "the", "is", "a", "an", "how", "what", "where",
           "want", "know", "about", "please", "for", "can", "you", "need", "this", "that", "do", "does", "get", "to",
           "much", "do", "have", "pay", "earn", "farmer", "month", "per", "yes", "no", "which", "documents", "apply",
           "and", "of", "in", "as", "shop", "job", "daughter", "land", "acres", "tax", "income", "salary", "it", "will"}

_LATIN = re.compile(r"[a-z]+")


def script_counts(text):
    counts = {"latin": 0}
    for ch in text or "":
        o = ord(ch)
        if ("a" <= ch <= "z") or ("A" <= ch <= "Z"):
            counts["latin"] += 1
            continue
        for name, lo, hi in SCRIPTS:
            if lo <= o <= hi:
                counts[name] = counts.get(name, 0) + 1
                break
    return counts


def detect(text, prisma=None, current="hi", settled=False):
    """
    Which language should we answer in?
      text    : what the person said (transcript or typed)
      prisma  : Prisma's detected_language_code, e.g. "ta-IN" (or None)
      current : the language we're already using
      settled : True once the person has answered at least once. From then on the language is STICKY:
                it only changes on clear evidence (a different script, or a long sentence that is clearly
                another language). Short replies, numbers, English words in Hindi ("private job"), and
                Prisma tagging a short Hindi reply as Marathi never flip the conversation.
    """
    current = valid(current)
    prisma = (prisma or "").split("-")[0].lower() or None
    c = script_counts(text)
    latin = c.pop("latin")
    indic_total = sum(c.values())
    words = re.findall(r"\w+", text or "")
    if indic_total >= 2 and indic_total >= 0.2 * (latin + indic_total):
        script = max(c, key=c.get)
        if script != "deva":
            return script                                 # Tamil, Bengali, ... : the script says it all
        return _hindi_or_marathi(text, prisma, current, len(words), settled)
    # Latin script: English, or Hinglish typed / transcribed in Roman letters
    toks = _LATIN.findall((text or "").lower())
    hin = sum(t in HINGLISH for t in toks)
    eng = sum(t in ENGLISH for t in toks)
    if settled:
        if current == "en":
            return "hi" if (hin >= 3 and eng == 0) else "en"          # typed Hinglish sentence
        if len(toks) >= 4 and eng >= 3 and hin == 0:
            return "en"                                   # a whole sentence in English
        if current not in ("hi", "en") and hin >= 3 and eng == 0:
            return "hi"
        return current
    if len(toks) < 2:
        return current                                    # "yes", "35", "ok": keep going in the same language
    if hin and hin >= eng:
        return "hi"
    if eng:
        return "en"
    return current


def _hindi_or_marathi(text, prisma, current, nwords, settled=False):
    toks = set(re.findall(r"[ऀ-ॿ]+", text or ""))
    mr_words, hi_words = len(toks & MR_MARKERS), len(toks & HI_MARKERS)
    if settled and current == "hi":
        return "mr" if (mr_words >= 2 and hi_words == 0) else "hi"   # ignore Prisma's tag on short replies
    if settled and current == "mr":
        return "hi" if (hi_words >= 2 and mr_words == 0) else "mr"
    mr = mr_words + (1 if prisma == "mr" else 0) + (0.5 if current == "mr" else 0)
    hi = hi_words + (0.5 if current == "hi" else 0)
    if nwords < 2 and current in ("hi", "mr") and mr < 1.5 and hi < 1.5:
        return current                                    # "हो" / "हाँ" alone: don't switch
    return "mr" if mr > hi else "hi"
