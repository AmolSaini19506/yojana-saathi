"""
Rule-based understanding for Hinglish / Hindi (Devanagari) / English answers,
plus the 8 other languages in langs/ (their words come from each language pack).

No LLM needed: Prisma gives us the transcript, and these rules pull out
age, occupation, land, income, tax status, PF status and yes/no answers.

Hindi/English keywords match whole words. Language-pack keywords are STEMS: a word matches if it starts
with the stem, because Tamil, Telugu, Kannada, Malayalam (and others) glue endings onto words
("ஏக்கர்" -> "ஏக்கரில்"). Prisma's `transcribe` format writes numbers as digits in every language,
so packs only need a few number words as a backup.
"""
import re
import unicodedata
from functools import lru_cache

import langs
import states

# ---------------------------------------------------------------- helpers

# native digits of every Indian script -> 0-9 (Devanagari, Bengali, Gurmukhi, Gujarati, Odia, Tamil, Telugu,
# Kannada, Malayalam)
DIGITS = str.maketrans({chr(base + i): str(i) for base in (0x0966, 0x09E6, 0x0A66, 0x0AE6, 0x0B66, 0x0BE6, 0x0C66,
                                                            0x0CE6, 0x0D66) for i in range(10)})
L = "a-z\u0900-\u0D7F"           # letters: Latin + all Indian scripts from Devanagari to Malayalam


# Malayalam "chillu" letters (\u0d7b \u0d7c \u0d7d \u0d7e \u0d7a \u0d7f) are also written the old way as letter + virama (+ ZWJ).
# Map both to letter + virama so keywords match whichever form Prisma returns.
CHILLU = str.maketrans({"\u0d7a": "\u0d23\u0d4d", "\u0d7b": "\u0d28\u0d4d", "\u0d7c": "\u0d30\u0d4d",
                        "\u0d7d": "\u0d32\u0d4d", "\u0d7e": "\u0d33\u0d4d", "\u0d7f": "\u0d15\u0d4d"})


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s).replace("\u200c", "").replace("\u200d", "").translate(CHILLU)


def kw(s: str) -> str:
    """Normalise a keyword the same way as the text."""
    return _nfc(s).lower()


def normalize(text: str) -> str:
    t = _nfc(text or "").translate(DIGITS).lower()
    t = re.sub(r"(?<=\d),(?=\d)", "", t)          # 15,000 -> 15000
    t = t.replace("₹", " rupaye ")
    t = re.sub(r"[?!।॥|\"“”]", " ", t)
    t = re.sub(rf"(\d)([{L}])", r"\1 \2", t)     # 35saal -> 35 saal
    t = re.sub(rf"([{L}])(\d)", r"\1 \2", t)     # words glued before digits
    return re.sub(r"\s+", " ", t).strip()


def tokens(text: str):
    return re.findall(rf"[0-9]+(?:\.[0-9]+)?|[{L}]+", text)


def find_kw(text_norm: str, key: str) -> bool:
    """key appears in the (normalised) text at the start of a word (prefix match, works for phrases too)."""
    return re.search(rf"(?<![{L}]){re.escape(key)}", text_norm) is not None


# ---------------------------------------------------------------- number words

NUM_WORDS = {
    # roman Hindi
    "ek": 1, "do": 2, "teen": 3, "tin": 3, "char": 4, "chaar": 4, "paanch": 5, "panch": 5,
    "chhe": 6, "chhah": 6, "chah": 6, "che": 6, "saat": 7, "aath": 8, "nau": 9, "das": 10,
    "gyarah": 11, "barah": 12, "baarah": 12, "terah": 13, "chaudah": 14, "pandrah": 15,
    "solah": 16, "satrah": 17, "atharah": 18, "unnis": 19, "bees": 20, "bis": 20,
    "pachchis": 25, "pachees": 25, "pachis": 25, "tees": 30, "tis": 30, "paintis": 35,
    "chalis": 40, "chaalis": 40, "paintalis": 45, "pachas": 50, "pachaas": 50, "pachpan": 55,
    "painsath": 65, "sattar": 70, "pachattar": 75, "assi": 80, "nabbe": 90, "sau": 100,
    "dedh": 1.5, "dhai": 2.5, "dhaai": 2.5, "aadha": 0.5,
    # English
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
    "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "fifteen": 15, "twenty": 20,
    "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80,
    "half": 0.5,
    # Devanagari
    "एक": 1, "दो": 2, "तीन": 3, "चार": 4, "पांच": 5, "पाँच": 5, "छह": 6, "छः": 6, "छे": 6,
    "सात": 7, "आठ": 8, "नौ": 9, "दस": 10, "ग्यारह": 11, "बारह": 12, "तेरह": 13, "चौदह": 14,
    "पंद्रह": 15, "पन्द्रह": 15, "सोलह": 16, "सत्रह": 17, "अठारह": 18, "उन्नीस": 19, "बीस": 20,
    "पच्चीस": 25, "तीस": 30, "पैंतीस": 35, "चालीस": 40, "पैंतालीस": 45, "पचास": 50,
    "पचपन": 55, "साठ": 60, "पैंसठ": 65, "सत्तर": 70, "पचहत्तर": 75, "अस्सी": 80, "नब्बे": 90,
    "सौ": 100, "डेढ़": 1.5, "ढाई": 2.5, "आधा": 0.5,
}

MULTIPLIERS = {
    "hazaar": 1000, "hazar": 1000, "hajar": 1000, "hazzar": 1000, "thousand": 1000, "k": 1000,
    "हज़ार": 1000, "हजार": 1000,
    "lakh": 100000, "lac": 100000, "lakhs": 100000, "लाख": 100000,
}

AGE_WORDS = {"saal", "sal", "varsh", "years", "year", "yrs", "umar", "umra", "age", "old",
             "साल", "वर्ष", "उम्र", "उमर", "बरस", "baras"}
MONTH_WORDS = {"mahina", "mahine", "mahinе", "month", "monthly", "mahinay", "per", "महीना",
               "महीने", "मासिक", "maheena", "mahine"}
YEAR_MONEY_WORDS = {"saalana", "salana", "annual", "yearly", "सालाना", "वार्षिक"}
MONEY_WORDS = {"rupaye", "rupay", "rupees", "rupee", "rs", "rupiya", "रुपये", "रुपए", "रूपये",
               "kamai", "kamata", "kamati", "income", "salary", "tankhwah", "कमाई", "कमाता",
               "कमाती", "आमदनी", "aamdani", "तनख्वाह"}
LAND_UNITS = {
    "acre": 0.4047, "acres": 0.4047, "ekad": 0.4047, "ekar": 0.4047, "एकड़": 0.4047, "एकर": 0.4047,
    "hectare": 1.0, "hectares": 1.0, "hektare": 1.0, "हेक्टेयर": 1.0,
    "bigha": 0.25, "bighe": 0.25, "बीघा": 0.25, "बीघे": 0.25,          # bigha varies by state; ~0.25 ha
    "killa": 0.4047, "kille": 0.4047, "किल्ला": 0.4047,
    "guntha": 0.0101, "gunthe": 0.0101, "गुंठा": 0.0101,
    "kanal": 0.0506, "कनाल": 0.0506,
}
LAND_WORDS = {"zameen", "jameen", "zamin", "jamin", "land", "khet", "ज़मीन", "जमीन", "खेत"}
RANGE_WORDS = {"se", "to", "ya", "or", "से", "या"}
AGE_LEADERS = {"am", "im", "aged", "age", "umar", "umra", "उम्र", "उमर"}
AGE_TRAILERS = {"hoon", "hun", "hu", "hai", "हूं", "हूँ", "हैं", "है"}
# words that are also common English/Hinglish words: only count them as numbers next to a unit
AMBIGUOUS_NUM = {"do", "tin", "bis", "tis", "che", "na", "das", "one"}

# make every Devanagari keyword use the same Unicode form as normalize()
NUM_WORDS = {_nfc(k): v for k, v in NUM_WORDS.items()}
MULTIPLIERS = {_nfc(k): v for k, v in MULTIPLIERS.items()}
LAND_UNITS = {_nfc(k): v for k, v in LAND_UNITS.items()}
AGE_WORDS, MONTH_WORDS, YEAR_MONEY_WORDS, MONEY_WORDS, LAND_WORDS, RANGE_WORDS, AGE_LEADERS, AGE_TRAILERS = (
    {_nfc(w) for w in S} for S in (AGE_WORDS, MONTH_WORDS, YEAR_MONEY_WORDS, MONEY_WORDS, LAND_WORDS,
                                   RANGE_WORDS, AGE_LEADERS, AGE_TRAILERS))
YEAR_WORDS = {_nfc(w) for w in ("saal", "year", "साल")}


@lru_cache(maxsize=None)
def vocab(lang: str):
    """Hindi/English word sets (exact) + this language's stems (prefix) for each category."""
    W = getattr(langs.pack(lang), "WORDS", {}) if lang else {}

    def stems(key):
        return tuple(sorted({kw(x) for x in W.get(key, ())}, key=len, reverse=True))

    def stem_map(key):
        return tuple(sorted(((kw(k), v) for k, v in W.get(key, {}).items()), key=lambda kv: -len(kv[0])))

    return {
        "age": (AGE_WORDS, stems("age")), "month": (MONTH_WORDS, stems("month")),
        "year_money": (YEAR_MONEY_WORDS, stems("year_money")), "money": (MONEY_WORDS, stems("money")),
        "range": (RANGE_WORDS, stems("range")), "year": (YEAR_WORDS, stems("year_money") + stems("year")),
        "land_units": (LAND_UNITS, stem_map("land_units")), "multipliers": (MULTIPLIERS, stem_map("multipliers")),
        "numbers": {kw(k): v for k, v in W.get("numbers", {}).items()},
        "tens": ({}, stem_map("tens")),
        "yes": {kw(x) for x in W.get("yes", ())}, "no": {kw(x) for x in W.get("no", ())},
        "no_sub": stems("no_sub"), "and": stems("and"),
        "tax": stems("tax"), "pf": stems("pf"), "no_land": stems("no_land"), "zero_income": stems("zero_income"),
        "what": stems("what"), "dontknow": stems("dontknow"),
    }


def _in(tok, cat):
    exact, st = cat
    return tok in exact or any(tok.startswith(s) for s in st)


def _val(tok, cat):
    """Value for tok from a {word: value} category (exact first, then the longest matching stem)."""
    exact, st = cat
    if tok in exact:
        return exact[tok]
    for s, v in st:
        if tok.startswith(s):
            return v
    return None


def _num_word(tok, V):
    if tok in NUM_WORDS:
        return NUM_WORDS[tok]
    if tok in V["numbers"]:
        return V["numbers"][tok]
    # Dravidian tens glued to a unit: "മുപ്പത്തിനാല്" = മുപ്പത്തി (30) + നാല് (4)
    for stem, tens in V["tens"][1]:
        if tok.startswith(stem):
            u = V["numbers"].get(tok[len(stem):])
            if u is not None and 1 <= u <= 9:
                return tens + u
    return None


def find_numbers(text: str, lang: str = "hi"):
    """Return list of dicts: value, index (token position), unit (age/land/money/None), land_ha."""
    V = vocab(lang)
    t = normalize(text)
    toks = tokens(t)
    found = []
    i = 0
    while i < len(toks):
        tok = toks[i]
        val = None
        if re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", tok):
            val = float(tok)
        elif _num_word(tok, V) is not None:
            nxt = toks[i + 1] if i + 1 < len(toks) else ""
            if tok in AMBIGUOUS_NUM and not (_val(nxt, V["multipliers"]) or _in(nxt, V["age"])
                                             or _val(nxt, V["land_units"]) or _in(nxt, V["money"]) or len(toks) == 1):
                i += 1
                continue
            val = float(_num_word(tok, V))
        elif tok == "saath" and i + 1 < len(toks) and toks[i + 1] in AGE_WORDS:
            val = 60.0  # "saath saal" = 60 years (bare "saath" usually means "with")
        if val is None:
            i += 1
            continue
        # "thirty four" / "முப்பத்து நான்கு": a tens word followed by a unit word is one number
        end = i
        if 20 <= val <= 90 and val % 10 == 0 and i + 1 < len(toks):
            u = _num_word(toks[i + 1], V)
            if u is not None and 1 <= u <= 9 and u == int(u):
                val += u
                end = i + 1
        # ranges like "10-12 hazaar" / "10 se 12 hazaar": keep the upper number (conservative for income limits)
        k = end + 1
        if k < len(toks) and _in(toks[k], V["range"]):
            k += 1
        if k < len(toks) and (re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", toks[k]) or _num_word(toks[k], V) is not None) \
                and k + 1 < len(toks) and _val(toks[k + 1], V["multipliers"]):
            i = k
            continue
        # compound like "pachas hazaar" / "1.5 lakh" / "do lakh pachas hazaar"
        j = end + 1
        if j < len(toks) and _val(toks[j], V["multipliers"]):
            val *= _val(toks[j], V["multipliers"])
            j += 1
        # unit detection: look at a small window after (and a bit before)
        after = toks[j:j + 4]
        before = toks[max(0, i - 3):i]
        unit, land_ha = None, None
        for w in after:
            if re.fullmatch(r"[0-9.]+", w) or _num_word(w, V) is not None:
                break                      # a unit belongs to the nearest number: "34 வயது, 2 ஏக்கர்"
            if _val(w, V["land_units"]):
                unit, land_ha = "land", val * _val(w, V["land_units"])
                break
        if unit is None:
            window = set(after[:3]) | set(before)
            if any(_in(w, V["age"]) for w in window) and val < 120:
                unit = "age"
            elif 14 <= val <= 110 and (set(before[-2:]) & AGE_LEADERS or
                                       (set(after[:1]) & {"ka", "ki", "का", "की"} and set(after[1:3]) & AGE_TRAILERS)):
                unit = "age"     # "I am 38", "aged 40", "35 ka hoon"
            elif any(_in(w, V["money"]) or _in(w, V["month"]) or _in(w, V["year_money"]) for w in window) \
                    or val >= 1000:
                unit = "money"
        period = None
        if unit == "money":
            ctx = set(toks[max(0, i - 4):j + 4])
            if any(_in(w, V["year_money"]) for w in ctx) or any(_in(w, V["year"]) for w in after[:3]):
                period = "year"
            elif any(_in(w, V["month"]) for w in ctx):
                period = "month"
        found.append({"value": val, "index": i, "unit": unit, "land_ha": land_ha, "period": period})
        i = j
    return found


def money_to_monthly(n):
    v = n["value"]
    if n["period"] == "year":
        return v / 12
    if n["period"] is None and v >= 100000:   # "2 lakh" with no period -> most people mean yearly
        return v / 12
    return v


# ---------------------------------------------------------------- yes / no

NEG = {"nahi", "nahin", "nahiin", "nai", "na", "no", "nope", "not", "never", "kabhi",
       "नहीं", "नही", "ना", "न", "मत"}
POS = {"haan", "han", "ha", "haa", "hanji", "ji", "yes", "yeah", "yep", "bilkul", "sure", "zaroor",
       "hai", "हाँ", "हां", "हा", "जी", "बिल्कुल", "ज़रूर", "जरूर", "है", "bharta", "bharti",
       "bharte", "katta", "kat", "भरता", "भरती", "कटता"}


NEG, POS = {_nfc(w) for w in NEG}, {_nfc(w) for w in POS}


# "है" / "hai" / "ji" also appear in questions ("वो क्या होता है?"), so on their own they only count as "yes"
# when the person isn't asking something.
WEAK_POS = {_nfc(w) for w in (
    "hai", "है", "ji", "जी",
    # "is / has / there is" in the other languages: also present in answers that are NOT a yes
    # ("મને રોકડ મળે છે" = "I get cash"), so on their own they only count in short answers or with the topic word
    "છે", "ਹੈ", "ਹੈਗਾ", "ਹੈਗੀ", "आहे", "ಇದೆ", "ಇದ್ದಾರೆ", "ಇದ್ದಾಳೆ", "ఉంది", "ఉన్నారు", "ఉన్నాడు", "ആണ്", "ഉണ്ട്",
    "আছে", "இருக்கு", "இருக்கிறது", "இருக்கிறாள்", "இருக்கா")}
QUESTION_WORDS = {_nfc(w) for w in ("kya", "kyaa", "क्या", "what", "whats", "kaun", "kaunsa", "कौन", "कौनसा", "kaise",
                                    "कैसे", "kyun", "kyon", "क्यों", "why", "how", "which", "matlab", "मतलब")}


# words that show the answer is about the question asked (so "PF कटता है" / "बेटी है" count as yes)
DAUGHTER_KEYS = [_nfc(k) for k in ["beti", "bitiya", "ladki", "daughter", "girl", "बेटी", "बिटिया", "लड़की", "लडकी",
                                   "மகள்", "মেয়ে", "मुलगी", "દીકરી", "ਧੀ", "ਬੇਟੀ", "కూతురు", "ಮಗಳು", "മകൾ"]]
# paid in cash -> no PF / ESIC
CASH_KEYS = [_nfc(k) for k in ["cash", "kaish", "nakad", "naqad", "haath mein", "hath mein", "कैश", "नकद", "नक़द",
                               "हाथ में", "ரொக்கம்", "கேஷ்", "নগদ", "ক্যাশ", "रोख", "कॅश", "રોકડ", "કેશ", "ਨਕਦ", "ਕੈਸ਼",
                               "నగదు", "క్యాష్", "ನಗದು", "ಕ್ಯಾಶ್", "പണമായി", "ക്യാഷ്"]]


# Words that mean "yes" only at the start of an answer. Punjabi "ਹਾਂ" is "yes" but also "am"
# ("ਕੰਮ ਕਰਦਾ ਹਾਂ" = "I work"), so "ਹਾਂ, PF ਕੱਟਦਾ ਹੈ" is a yes but "... ਕਰਦਾ ਹਾਂ" is not.
FIRST_ONLY_YES = {_nfc(w) for w in ("ਹਾਂ", "ਹਾਂਜੀ")}


# ---------------------------------------------------------------- gender (asked only when a women's scheme could apply)
# Always clear, even inside a longer answer:
FEMALE_SURE = [_nfc(k) for k in ["mahila", "aurat", "woman", "female", "lady", "housewife", "homemaker", "widow",
                                 "vidhwa", "grihini", "karti hoon", "karti hu", "karti hun", "kamati hoon", "kamati hu",
                                 "rehti hoon", "rehti hu", "महिला", "औरत", "विधवा", "गृहिणी", "करती हूँ", "करती हूं",
                                 "कमाती हूँ", "कमाती हूं", "रहती हूँ", "रहती हूं", "कमावते", "இல்லத்தரசி",
                                 "গৃহবধূ", "গৃহিণী"]]
MALE_SURE = [_nfc(k) for k in ["karta hoon", "karta hu", "karta hun", "kamata hoon", "kamata hu", "rehta hoon",
                               "rehta hu", "करता हूँ", "करता हूं", "कमाता हूँ", "कमाता हूं", "रहता हूँ", "रहता हूं",
                               "कमावतो"]]
# Only as an answer to "are you a woman or a man?" (some also mean "daughter" / "is"):
FEMALE_ANSWER = [_nfc(k) for k in ["stree", "ladki", "aurat", "female", "woman", "f", "स्त्री", "लड़की", "बाई",
                                   "பெண்", "মহিলা", "নারী", "মেয়ে", "স্ত্রী", "स्त्री", "સ્ત્રી", "મહિલા", "બહેન", "ਔਰਤ",
                                   "ਇਸਤਰੀ", "ਮਹਿਲਾ", "ਜ਼ਨਾਨੀ", "స్త్రీ", "మహిళ", "ఆడ", "ಮಹಿಳೆ", "ಹೆಣ್ಣು", "ಸ್ತ್ರೀ",
                                   "സ്ത്രീ", "വനിത", "പെണ്ണ്"]]
MALE_ANSWER = [_nfc(k) for k in ["purush", "aadmi", "mard", "male", "man", "m", "ladka", "पुरुष", "आदमी", "मर्द",
                                 "लड़का", "ஆண்", "পুরুষ", "ছেলে", "पुरुष", "પુરુષ", "ભાઈ", "ਆਦਮੀ", "ਮਰਦ", "ਪੁਰਸ਼",
                                 "పురుష", "మగ", "ಪುರುಷ", "ಗಂಡು", "പുരുഷ"]]


def detect_gender(text, lang="hi", expecting=False):
    t = normalize(text)
    if any(find_kw(t, k) for k in FEMALE_SURE):
        return "f"
    if any(find_kw(t, k) for k in MALE_SURE):
        return "m"
    if expecting:
        toks = tokens(t)
        if any(tok.startswith(k) for tok in toks for k in FEMALE_ANSWER if len(k) > 1) or set(toks) & {"f"}:
            return "f"
        if any(tok.startswith(k) for tok in toks for k in MALE_ANSWER if len(k) > 1) or set(toks) & {"m"}:
            return "m"
    return None


# ---------------------------------------------------------------- wants to start / grow a business
BIZ_KEYS = [_nfc(k) for k in ["business", "dhandha", "dhanda", "kaam", "kaarobar", "karobar", "dukaan", "dukan",
                              "udyog", "startup", "start up", "shuru", "kholna", "kholni", "factory", "unit",
                              "धंधा", "काम", "कारोबार", "व्यापार", "व्यवसाय", "दुकान", "उद्योग", "शुरू", "खोलना", "खोलनी"]]
BIZ_INTRO = [_nfc(k) for k in ["shuru karna chahta", "shuru karna chahti", "shuru karni hai", "shuru karna hai",
                               "kholna chahta", "kholna chahti", "kholni hai", "kholna hai", "start a business",
                               "start my own", "start my business", "open a shop", "naya kaam", "naya dhandha",
                               "naya business", "apna business", "apna kaam shuru", "apna dhandha", "शुरू करना चाहता",
                               "शुरू करना चाहती", "शुरू करना है", "खोलना चाहता", "खोलना चाहती", "खोलना है",
                               "नया काम", "नया धंधा", "अपना काम शुरू", "अपना धंधा"]]


def _topic_keys(slot, lang):
    V = vocab(lang)
    if slot == "biz":
        return BIZ_KEYS
    if slot == "epf":
        return PF_KEYS + list(V["pf"])
    if slot == "itax":
        return TAX_KEYS + list(V["tax"])
    if slot == "daughter_u10":
        return DAUGHTER_KEYS
    return []


def parse_yes_no(text: str, lang: str = "hi", slot: str | None = None):
    """True / False / None. `slot` = the yes/no question just asked: then a weak word like "है" only counts
    in a short answer ("हाँ है", "beti hai") or when the answer mentions the topic ("PF कटता है")."""
    V = vocab(lang)
    t = normalize(text)
    seq = tokens(t)
    toks = set(seq)
    if toks & NEG or toks & V["no"] or any(s in t for s in V["no_sub"]):
        return False
    yes_words = V["yes"] - WEAK_POS - (FIRST_ONLY_YES if not seq or seq[0] not in FIRST_ONLY_YES else set())
    strong = (toks & (POS - WEAK_POS)) or (toks & yes_words)
    if strong:
        return True
    if toks & (WEAK_POS | V["yes"]) and not (toks & QUESTION_WORDS or "?" in (text or "")):
        if slot is None or len(tokens(t)) <= 3 or any(k in t for k in _topic_keys(slot, lang)):
            return True
    return None


# The person didn't answer, they asked back ("PF kya hota hai?") or said they don't know ("pata nahi").
WHAT_KEYS = [_nfc(k) for k in ["kya hota", "kya hoti", "kya hai ye", "kya hai yeh", "ye kya", "yeh kya", "kya matlab",
                               "matlab", "samjha nahi", "samjhi nahi", "samajh nahi", "samjha nahin", "what is",
                               "what's", "what does", "what do you mean", "meaning", "didn't understand", "dont understand",
                               "don't understand", "क्या होता", "क्या होती", "क्या है ये", "क्या है यह", "ये क्या", "यह क्या",
                               "मतलब", "समझ नहीं", "समझा नहीं", "समझी नहीं"]]
DONTKNOW_KEYS = [_nfc(k) for k in ["skip", "chhodiye", "chhodo", "chodiye", "rehne do", "nahi batana", "छोड़िए", "छोड़ो",
                                   "रहने दो", "नहीं बताना", "pata nahi", "pata nahin", "pata nai", "nahi pata", "nahin pata", "maloom nahi",
                                   "malum nahi", "don't know", "dont know", "do not know", "not sure", "no idea",
                                   "पता नहीं", "नहीं पता", "मालूम नहीं", "नहीं मालूम", "पता नही"]]


def clarify(text: str, lang: str = "hi"):
    """'what' if the person asked what something means, 'dontknow' if they said they don't know, else None."""
    V = vocab(lang)
    t = normalize(text)
    if any(k in t for k in DONTKNOW_KEYS) or any(k in t for k in V["dontknow"]):
        return "dontknow"
    if any(k in t for k in WHAT_KEYS) or any(k in t for k in V["what"]):
        return "what"
    toks = set(tokens(t))
    if ("?" in (text or "") or toks & QUESTION_WORDS) and not ((toks & (POS - WEAK_POS)) or (toks & (V["yes"] - WEAK_POS))
                                                              or toks & NEG or toks & V["no"]):
        return "what"             # a question with no yes/no in it
    return None


def _clause_with(text: str, keys, lang: str = "hi"):
    """Return the clause (split on commas / aur / and) that mentions any key."""
    t = normalize(text)
    joiners = "".join(f"| {re.escape(a)} " for a in vocab(lang)["and"])
    for clause in re.split(r",|\.| aur | and | और |;" + joiners, t):
        if any(k in clause for k in keys):
            return clause
    return None


TAX_KEYS = [_nfc(k) for k in ["tax", "टैक्स", "itr", "आयकर", "income tax"]]
PF_KEYS = [_nfc(k) for k in ["pf", "epf", "esic", "nps", "पीएफ", "provident", "ईएसआईसी"]]


def detect_tax(text, lang="hi"):
    clause = _clause_with(text, TAX_KEYS + list(vocab(lang)["tax"]), lang)
    return None if clause is None else parse_yes_no(clause, lang)


def detect_pf(text, lang="hi"):
    clause = _clause_with(text, PF_KEYS + list(vocab(lang)["pf"]), lang)
    if clause is None:
        return None
    yn = parse_yes_no(clause, lang)
    return True if yn is None else yn   # "mera PF katta hai" -> True


# ---------------------------------------------------------------- occupation

ARTISAN_TRADES = {
    "carpenter": ["barhai", "badhai", "suthar", "carpenter", "बढ़ई", "बढई", "सुथार", "furniture"],
    "blacksmith": ["lohar", "blacksmith", "लोहार"],
    "goldsmith": ["sunar", "sonar", "goldsmith", "सुनार"],
    "potter": ["kumhar", "potter", "kumbhar", "कुम्हार", "matke"],
    "cobbler": ["mochi", "cobbler", "joote banata", "joota", "मोची", "चर्मकार"],
    "mason": ["rajmistri", "raj mistri", "mason", "राजमिस्त्री", "राज मिस्त्री"],
    "tailor": ["darzi", "darji", "tailor", "silai", "दर्जी", "सिलाई"],
    "barber": ["naai", "hajjam", "barber", "नाई", "हज्जाम"],
    "washerman": ["dhobi", "washerman", "धोबी"],
    "garland_maker": ["mali", "maali", "maala", "garland", "माली", "माला"],
    "locksmith": ["locksmith", "taala", "chabi", "ताला", "चाबी"],
    "sculptor": ["moortikar", "murtikar", "sculptor", "sangtarash", "मूर्तिकार", "पत्थर"],
    "basket_maker": ["tokri", "chatai", "jhadu", "basket", "टोकरी", "चटाई", "झाड़ू"],
    "toy_maker": ["khilona", "toy", "खिलौना", "खिलौने"],
    "fishing_net_maker": ["jaal", "fishing net", "जाल"],
    "boat_maker": ["naav", "boat", "नाव"],
    "armourer": ["armourer", "hathiyar", "हथियार"],
    "tool_maker": ["hathoda", "auzar", "औज़ार", "औजार", "tool kit"],
}

OCCUPATIONS = [
    # order matters: more specific first
    ("govt_employee", ["sarkari naukri", "sarkari job", "government job", "govt job", "government employee",
                       "सरकारी नौकरी", "सरकारी कर्मचारी", "sarkari karmchari"]),
    ("street_vendor", ["thela", "thele", "rehdi", "rehri", "redi", "patri", "pheri", "footpath",
                       "street vendor", "hawker", "ठेला", "ठेले", "रेहड़ी", "रेहडी", "फेरी", "पटरी", "khomcha"]),
    ("farmer", ["kisan", "kisaan", "kheti", "kheti baadi", "farmer", "farming", "agriculture",
                "किसान", "खेती", "कृषि", "kashtkar"]),
    ("shopkeeper", ["dukaan", "dukan", "kirana", "shop", "store", "vyapar", "vyapari", "trader",
                    "business", "dhandha", "दुकान", "किराना", "व्यापार", "व्यापारी", "धंधा", "बिज़नेस", "बिजनेस"]),
    ("labourer", ["mazdoor", "majdoor", "mazdoori", "majdoori", "labour", "labor", "dihadi", "daily wage",
                  "construction", "मज़दूर", "मजदूर", "मज़दूरी", "मजदूरी", "दिहाड़ी", "driver", "ड्राइवर",
                  "rickshaw", "रिक्शा", "auto chala", "drive an auto", "auto driver", "taxi", "cab", "e-rickshaw",
                  "delivery", "डिलीवरी", "ऑटो", "domestic", "maid", "kaamwali", "घरेलू कामगार", "safai"]),
    ("salaried_private", ["private job", "private naukri", "company", "naukri", "job karta", "job karti",
                          "salary", "office", "नौकरी", "कंपनी", "प्राइवेट"]),
    ("homemaker", ["housewife", "homemaker", "grihini", "gharelu", "ghar sambhal", "गृहिणी", "हाउसवाइफ"]),
    ("student", ["student", "padhai", "padhta", "padhti", "college", "छात्र", "पढ़ाई", "पढाई", "विद्यार्थी"]),
    ("unemployed", ["berozgar", "unemployed", "koi kaam nahi", "kaam nahi", "बेरोज़गार", "बेरोजगार",
                    "कोई काम नहीं"]),
]


ARTISAN_TRADES = {k: [_nfc(x) for x in v] for k, v in ARTISAN_TRADES.items()}
OCCUPATIONS = [(o, [_nfc(x) for x in v]) for o, v in OCCUPATIONS]


@lru_cache(maxsize=None)
def _occ_keys(lang):
    p = langs.pack(lang)
    trades = {k: list(v) for k, v in ARTISAN_TRADES.items()}
    occs = [(o, list(v)) for o, v in OCCUPATIONS]
    if p:
        for trade, keys in getattr(p, "TRADES", {}).items():
            trades.setdefault(trade, [])[:0] = [kw(k) for k in keys]
        extra = getattr(p, "OCCUPATIONS", {})
        occs = [(o, [kw(k) for k in extra.get(o, ())] + v) for o, v in occs]
    return trades, occs


def detect_occupation(text: str, lang: str = "hi"):
    """Return (occupation, trade) or (None, None)."""
    t = normalize(text)
    trades, occs = _occ_keys(lang)
    for trade, keys in trades.items():
        if any(find_kw(t, k) for k in keys):
            return "artisan", trade
    for occ, keys in occs:
        if any(find_kw(t, k) for k in keys):
            return occ, None
    return None, None


NO_LAND = [_nfc(x) for x in ["zameen nahi", "jameen nahi", "khet nahi", "no land", "ज़मीन नहीं", "जमीन नहीं",
           "zameen nahin", "bina zameen", "batai", "बटाई", "kiraye ki zameen"]]


# ---------------------------------------------------------------- details added 11 Nov 2026 (wider scheme list)
YES_NO_EXTRA = ("bpl", "pucca", "lpg", "maternity", "widow", "disabled")
WIDOW_KEYS = [_nfc(k) for k in ["vidhwa", "vidhva", "widow", "विधवा", "pati nahi rahe", "pati guzar", "husband died",
                                "husband passed", "पति नहीं रहे", "पति गुज़र", "पति गुजर", "বিধবা", "વિધવા", "ವಿಧವೆ", "വിധവ",
                                "ਵਿਧਵਾ", "விதவை", "కైம்பெண்", "వితంతువు"]]
DISABLED_KEYS = [_nfc(k) for k in ["viklang", "divyang", "handicap", "disabled", "disability", "apahij", "विकलांग",
                                   "दिव्यांग", "अपाहिज", "প্রতিবন্ধী", "દિવ્યાંગ", "ಅಂಗವಿಕಲ", "ഭിന്നശേഷി", "ਦਿਵਿਆਂਗ", "ਅਪਾਹਜ",
                                   "மாற்றுத்திறனாளி", "దివ్యాంగ", "వికలాంగ"]]
PREGNANT_KEYS = [_nfc(k) for k in ["pregnant", "garbhvati", "garbhwati", "pet se", "expecting a baby", "गर्भवती", "पेट से",
                                   "অন্তঃসত্ত্বা", "ગર્ભવતી", "ಗರ್ಭಿಣಿ", "ഗർഭിണി", "गरोदर", "ਗਰਭਵਤੀ", "கர்ப்ப",
                                   "గర్భవతి", "గర్భిణి"]]
VILLAGE_KEYS = [_nfc(k) for k in ["gaon", "gaanv", "gaav", "village", "dehat", "gram panchayat", "गाँव", "गांव", "देहात",
                                  "ग्राम"]]
TOWN_KEYS = [_nfc(k) for k in ["shehar", "shahar", "sheher", "city", "town", "kasba", "kasbe", "nagar", "metro", "शहर",
                               "कस्बा", "कस्बे", "नगर"]]
KACCHA_KEYS = [_nfc(k) for k in ["kaccha", "kachcha", "kacha", "jhopdi", "jhuggi", "kiraye", "kiraya", "rent", "rented",
                                 "कच्चा", "कच्चे", "झोपड़ी", "झुग्गी", "किराए", "किराये"]]
NO_LPG_KEYS = [_nfc(k) for k in ["chulha", "chulhe", "lakdi", "चूल्हा", "चूल्हे", "लकड़ी"]]
CATEGORY_KEYS = {
    "sc": ["anusuchit jati", "scheduled caste", "dalit", "harijan", "अनुसूचित जाति", "दलित", "एससी"],
    "st": ["anusuchit janjati", "scheduled tribe", "adivasi", "tribal", "अनुसूचित जनजाति", "आदिवासी", "एसटी"],
    "obc": ["pichhda", "pichda", "pichhra", "backward", "पिछड़ा", "पिछड़े", "पिछड़ी", "ओबीसी"],
    "gen": ["general", "samanya", "unreserved", "सामान्य", "जनरल"],
}
CATEGORY_KEYS = {c: [_nfc(k) for k in v] for c, v in CATEGORY_KEYS.items()}
CATEGORY_TOKENS = {"sc": "sc", "s.c": "sc", "st": "st", "s.t": "st", "obc": "obc", "o.b.c": "obc", "ebc": "obc",
                   "bc": "obc", "gen": "gen", "open": "gen"}       # only as an answer to the category question
SCHOOL_KEYS = [_nfc(k) for k in ["school", "class", "kaksha", "dasvi", "barahvi", "10th", "11th", "12th", "9th", "स्कूल",
                                 "कक्षा", "दसवीं", "बारहवीं"]]
COLLEGE_KEYS = [_nfc(k) for k in ["college", "degree", "graduation", "graduate", "b.a", "bsc", "b.sc", "bcom", "b.com",
                                  "btech", "b.tech", "iti", "diploma", "polytechnic", "university", "masters", "कॉलेज",
                                  "डिग्री", "यूनिवर्सिटी", "आईटीआई", "डिप्लोमा", "ग्रेजुएशन"]]


def _extra_words(kind):
    """Words for the new questions in the 8 pack languages (langs/more_q.py), valid whatever the conversation's language."""
    from langs import more_q
    return [_nfc(w) for w in more_q.WORDS[kind]]


def detect_extra(text: str, expecting: str | None = None, lang: str = "hi") -> dict:
    """The details added for the wider scheme list: village/town, house, gas, maternity, widow, disability, category,
    school/college. Clear statements count anywhere ("main vidhwa hoon"); bare yes/no only for the question asked."""
    out = {}
    t = normalize(text)

    def has(keys):
        return any(find_kw(t, k) for k in keys)

    if has(WIDOW_KEYS) and expecting != "widow":
        out["widow"], out["gender"] = True, "f"
    if has(DISABLED_KEYS) and expecting != "disabled":
        out["disabled"] = True
    if has(PREGNANT_KEYS) and expecting != "maternity":
        out["maternity"], out["gender"] = True, "f"
    if has(VILLAGE_KEYS) or (expecting == "rural" and has(_extra_words("village"))):
        out["rural"] = True
    elif expecting == "rural" and (has(TOWN_KEYS) or has(_extra_words("town"))):
        out["rural"] = False
    for cat, keys in CATEGORY_KEYS.items():
        if has(keys) and (expecting == "category" or cat != "gen"):
            out["category"] = cat
    if expecting == "category" and "category" not in out:
        for tok in tokens(t):
            if tok in CATEGORY_TOKENS:
                out["category"] = CATEGORY_TOKENS[tok]
                break
        else:
            if has(_extra_words("general")):
                out["category"] = "gen"
    if expecting == "study":
        if has(COLLEGE_KEYS) or has(_extra_words("college")):
            out["study"] = "college"
        elif has(SCHOOL_KEYS) or has(_extra_words("school")):
            out["study"] = "school"
    if expecting == "pucca" and has(KACCHA_KEYS):
        out["pucca"] = False
    if expecting == "lpg" and has(NO_LPG_KEYS):
        out["lpg"] = False
    if expecting in YES_NO_EXTRA and expecting not in out:
        yn = parse_yes_no(text, lang, slot=expecting)
        if yn is not None:
            out[expecting] = yn
    return out


# ---------------------------------------------------------------- main entry

def extract(text: str, expecting: str | None = None, lang: str = "hi") -> dict:
    """
    Pull every slot we can find out of one utterance.
    `expecting` is the slot we just asked about; it lets bare answers like "35" or "nahi" count.
    """
    out = {}
    V = vocab(lang)
    t = normalize(text)
    nums = find_numbers(text, lang)

    occ, trade = detect_occupation(text, lang)
    if occ:
        out["occupation"] = occ
        if trade:
            out["trade"] = trade
    st = states.find_state(text, expecting == "state")
    if st:
        out["state"] = st
    g = detect_gender(text, lang, expecting == "gender")
    if g:
        out["gender"] = g
    if occ == "homemaker" and "gender" not in out:
        out["gender"] = "f"
    if any(k in t for k in BIZ_INTRO):
        out["biz"] = True

    for n in nums:
        if n["unit"] == "age" and 14 <= n["value"] <= 110 and "age" not in out:
            out["age"] = int(n["value"])
        elif n["unit"] == "land" and "land_ha" not in out:
            out["land_ha"] = round(n["land_ha"], 3)
        elif n["unit"] == "money" and "income_month" not in out:
            out["income_month"] = int(round(money_to_monthly(n)))

    if any(p in t for p in NO_LAND) or any(p in t for p in V["no_land"]):
        out["land_ha"] = 0.0

    tax = detect_tax(text, lang)
    if tax is not None:
        out["itax"] = tax
    pf = detect_pf(text, lang)
    if pf is not None:
        out["epf"] = pf

    # bare answers to the question we just asked
    bare = [n for n in nums if n["unit"] is None or n["unit"] == expecting]
    if expecting == "age" and "age" not in out:
        for n in nums:
            if 14 <= n["value"] <= 110 and n["unit"] in (None, "age"):
                out["age"] = int(n["value"])
                break
    elif expecting == "land_ha" and "land_ha" not in out:
        yn = parse_yes_no(text, lang)
        if bare:
            out["land_ha"] = round(bare[0]["value"] * 0.4047, 3)   # bare number -> assume acres
            out["_assumed_acres"] = True
        elif yn is False:
            out["land_ha"] = 0.0
    elif expecting == "income_month" and "income_month" not in out:
        money = [n for n in nums if n["unit"] in (None, "money")]
        if money:
            out["income_month"] = int(round(money_to_monthly(money[0])))
        elif re.search(r"kuch nahi|kamai nahi|nahi kama|zero|nothing|none|no income|not earning|don't earn|"
                       r"शून्य|कुछ नहीं|कमाई नहीं", t) or any(z in t for z in V["zero_income"]) \
                or parse_yes_no(text, lang) is False:
            out["income_month"] = 0
    elif expecting in ("itax", "epf", "daughter_u10", "biz") and expecting not in out:
        if expecting == "epf" and any(k in t for k in CASH_KEYS):
            out["epf"] = False                       # "मुझे cash मिलता है": paid in cash, so no PF / ESIC
        else:
            yn = parse_yes_no(text, lang, slot=expecting)
            if yn is not None:
                out[expecting] = yn
    for k, v in detect_extra(text, expecting, lang).items():
        out.setdefault(k, v)
    return out
