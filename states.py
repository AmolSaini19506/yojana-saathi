"""
Indian states: names (for the question "which state?") and which ones have state schemes in the app.

COVERED states have 1–2 flagship state schemes in schemes.py (checked 9 Nov 2026). For every other state the app
still checks central schemes and says honestly that its state schemes aren't in the app yet.
"""
import re
import unicodedata

# code: (English name, Hindi name, keywords). Keywords are matched at the start of a word in the normalised text.
# Bare "up" / "mp" are ambiguous ("set up"), so they only count as an answer to the state question.
STATES = {
    "UP": ("Uttar Pradesh", "उत्तर प्रदेश",
           ["uttar pradesh", "u.p.", "up se", "up mein", "up me", "उत्तर प्रदेश", "यूपी", "यू.पी", "lucknow", "लखनऊ",
            "kanpur", "कानपुर", "varanasi", "banaras", "वाराणसी", "बनारस", "prayagraj", "allahabad", "प्रयागराज",
            "agra", "आगरा", "meerut", "मेरठ", "gorakhpur", "गोरखपुर", "ghaziabad", "गाज़ियाबाद", "गाजियाबाद",
            "noida", "नोएडा", "bareilly", "बरेली", "aligarh", "अलीगढ़", "moradabad", "मुरादाबाद", "ayodhya", "अयोध्या",
            "jhansi", "झांसी", "mathura", "मथुरा", "உத்தர பிரதேசம்", "উত্তরপ্রদেশ", "ఉత్తరప్రదేశ్", "ಉತ್ತರ ಪ್ರದೇಶ"]),
    "BR": ("Bihar", "बिहार", ["bihar", "बिहार", "patna", "पटना", "gaya", "गया जी", "muzaffarpur", "मुजफ्फरपुर",
                            "bhagalpur", "भागलपुर", "darbhanga", "दरभंगा", "purnia", "पूर्णिया", "বিহার", "பீகார்"]),
    "MH": ("Maharashtra", "महाराष्ट्र",
           ["maharashtra", "maharastra", "महाराष्ट्र", "mumbai", "bombay", "मुंबई", "pune", "पुणे", "nagpur", "नागपुर",
            "नागपूर", "nashik", "नाशिक", "aurangabad", "औरंगाबाद", "sambhajinagar", "संभाजीनगर", "kolhapur", "कोल्हापूर",
            "solapur", "सोलापूर", "thane", "ठाणे", "மகாராஷ்டிரா", "ಮಹಾರಾಷ್ಟ್ರ", "মহারাষ্ট্র"]),
    "MP": ("Madhya Pradesh", "मध्य प्रदेश",
           ["madhya pradesh", "m.p.", "mp se", "mp mein", "mp me", "मध्य प्रदेश", "मध्यप्रदेश", "एमपी", "bhopal", "भोपाल",
            "indore", "इंदौर", "jabalpur", "जबलपुर", "gwalior", "ग्वालियर", "ujjain", "उज्जैन", "rewa",
            "रीवा", "satna", "सतना"]),
    "RJ": ("Rajasthan", "राजस्थान", ["rajasthan", "राजस्थान", "jaipur", "जयपुर", "jodhpur", "जोधपुर", "udaipur",
                                   "उदयपुर", "kota", "कोटा", "bikaner", "बीकानेर", "ajmer", "अजमेर", "alwar", "अलवर"]),
    "WB": ("West Bengal", "पश्चिम बंगाल",
           ["west bengal", "bengal", "bangal", "paschim banga", "पश्चिम बंगाल", "बंगाल", "kolkata", "calcutta", "कोलकाता",
            "howrah", "हावड़ा", "siliguri", "पश्चिमबंगाल", "পশ্চিমবঙ্গ", "পশ্চিম বঙ্গ", "বাংলা থেকে", "কলকাতা", "হাওড়া",
            "শিলিগুড়ি", "মেদিনীপুর", "বর্ধমান", "মুর্শিদাবাদ", "নদিয়া"]),
    "TN": ("Tamil Nadu", "तमिलनाडु",
           ["tamil nadu", "tamilnadu", "तमिलनाडु", "तमिल नाडु", "chennai", "madras", "चेन्नई", "madurai", "मदुरै",
            "coimbatore", "कोयंबटूर", "trichy", "salem", "தமிழ்நாடு", "தமிழ் நாடு", "தமிழகம்", "சென்னை", "மதுரை",
            "கோயம்புத்தூர்", "கோவை", "திருச்சி", "சேலம்", "திருநெல்வேலி"]),
    "KA": ("Karnataka", "कर्नाटक",
           ["karnataka", "कर्नाटक", "bengaluru", "bangalore", "बेंगलुरु", "बैंगलोर", "mysuru", "mysore", "मैसूर",
            "hubli", "hubballi", "mangaluru", "mangalore", "belagavi", "belgaum", "ಕರ್ನಾಟಕ", "ಬೆಂಗಳೂರು", "ಮೈಸೂರು",
            "ಹುಬ್ಬಳ್ಳಿ", "ಮಂಗಳೂರು", "ಬೆಳಗಾವಿ", "ಕಲಬುರಗಿ", "ಕರ್ನಾಟಕದ"]),
    # not covered yet (central schemes only)
    "GJ": ("Gujarat", "गुजरात", ["gujarat", "गुजरात", "ahmedabad", "अहमदाबाद", "surat", "सूरत", "vadodara", "baroda",
                              "rajkot", "ગુજરાત", "અમદાવાદ", "સુરત", "વડોદરા", "રાજકોટ"]),
    "PB": ("Punjab", "पंजाब", ["punjab", "पंजाब", "ludhiana", "लुधियाना", "amritsar", "अमृतसर", "jalandhar", "ਪੰਜਾਬ",
                             "ਲੁਧਿਆਣਾ", "ਅੰਮ੍ਰਿਤਸਰ", "ਜਲੰਧਰ", "ਪਟਿਆਲਾ"]),
    "HR": ("Haryana", "हरियाणा", ["haryana", "हरियाणा", "gurgaon", "gurugram", "गुरुग्राम", "faridabad", "फरीदाबाद",
                                "rohtak", "रोहतक", "panipat", "पानीपत", "hisar", "हिसार", "ਹਰਿਆਣਾ"]),
    "DL": ("Delhi", "दिल्ली", ["delhi", "dilli", "दिल्ली", "ਦਿੱਲੀ", "দিল্লি", "டெல்லி", "ದೆಹಲಿ", "ఢిల్లీ", "ഡൽഹി"]),
    "KL": ("Kerala", "केरल", ["kerala", "केरल", "kochi", "cochin", "trivandrum", "thiruvananthapuram", "kozhikode",
                            "thrissur", "കേരളം", "കേരള", "കൊച്ചി", "തിരുവനന്തപുരം", "കോഴിക്കോട്", "തൃശ്ശൂർ"]),
    "AP": ("Andhra Pradesh", "आंध्र प्रदेश", ["andhra", "आंध्र", "vijayawada", "visakhapatnam", "vizag", "guntur",
                                            "tirupati", "ఆంధ్ర", "విజయవాడ", "విశాఖ", "గుంటూరు", "తిరుపతి"]),
    "TG": ("Telangana", "तेलंगाना", ["telangana", "तेलंगाना", "hyderabad", "हैदराबाद", "warangal", "తెలంగాణ",
                                   "హైదరాబాద్", "వరంగల్"]),
    "OD": ("Odisha", "ओडिशा", ["odisha", "orissa", "ओडिशा", "उड़ीसा", "bhubaneswar", "cuttack", "भुवनेश्वर"]),
    "JH": ("Jharkhand", "झारखंड", ["jharkhand", "झारखंड", "ranchi", "रांची", "jamshedpur", "जमशेदपुर", "dhanbad", "धनबाद"]),
    "CG": ("Chhattisgarh", "छत्तीसगढ़", ["chhattisgarh", "chattisgarh", "छत्तीसगढ़", "raipur", "रायपुर", "bilaspur"]),
    "UK": ("Uttarakhand", "उत्तराखंड", ["uttarakhand", "उत्तराखंड", "dehradun", "देहरादून", "haridwar", "हरिद्वार"]),
    "HP": ("Himachal Pradesh", "हिमाचल प्रदेश", ["himachal", "हिमाचल", "shimla", "शिमला"]),
    "JK": ("Jammu and Kashmir", "जम्मू-कश्मीर", ["jammu", "kashmir", "जम्मू", "कश्मीर", "srinagar"]),
    "AS": ("Assam", "असम", ["assam", "असम", "guwahati", "गुवाहाटी", "অসম", "আসাম", "গুয়াহাটি"]),
    "GA": ("Goa", "गोवा", ["goa", "गोवा", "panaji"]),
}
COVERED = {"UP", "BR", "MH", "MP", "RJ", "WB", "TN", "KA"}
AMBIGUOUS = {"UP": ["up", "यूपी"], "MP": ["mp", "एमपी"]}       # only as a bare answer to "which state?"

_L = "a-zऀ-ൿ"


def _norm(s):
    s = unicodedata.normalize("NFC", s or "").replace("‌", "").replace("‍", "").lower()
    return re.sub(r"\s+", " ", re.sub(r"[?!।॥,\"“”]", " ", s)).strip()


_KEYS = sorted(((_norm(k), code) for code, (_, _, ks) in STATES.items() for k in ks), key=lambda kc: -len(kc[0]))


def find_state(text, expecting=False):
    """State code mentioned in the text (longest keyword wins), or None."""
    t = f" {_norm(text)} "
    for k, code in _KEYS:
        tail = "(?![a-z])" if k.isascii() else ""      # English words: whole word ("goa" is not "goal");
        if re.search(rf"(?<![{_L}]){re.escape(k)}{tail}", t):   # Indian scripts: prefix ("சென்னையில்")
            return code
    if expecting:
        toks = set(re.findall(rf"[{_L}.]+", t))
        for code, words in AMBIGUOUS.items():
            if toks & {_norm(w) for w in words}:
                return code
    return None


# State names in the other scripts (home states of each language, plus the covered states where common)
NATIVE = {
    "ta": {"TN": "தமிழ்நாடு", "KA": "கர்நாடகா", "KL": "கேரளா", "MH": "மகாராஷ்டிரா", "AP": "ஆந்திரப் பிரதேசம்"},
    "bn": {"WB": "পশ্চিমবঙ্গ", "BR": "বিহার", "AS": "আসাম", "OD": "ওড়িশা", "JH": "ঝাড়খণ্ড", "UP": "উত্তরপ্রদেশ"},
    "kn": {"KA": "ಕರ್ನಾಟಕ", "MH": "ಮಹಾರಾಷ್ಟ್ರ", "TN": "ತಮಿಳುನಾಡು", "AP": "ಆಂಧ್ರಪ್ರದೇಶ", "TG": "ತೆಲಂಗಾಣ"},
    "te": {"AP": "ఆంధ్రప్రదేశ్", "TG": "తెలంగాణ", "KA": "కర్ణాటక", "TN": "తమిళనాడు", "MH": "మహారాష్ట్ర"},
    "ml": {"KL": "കേരളം", "TN": "തമിഴ്നാട്", "KA": "കർണാടക"},
    "gu": {"GJ": "ગુજરાત", "MH": "મહારાષ્ટ્ર", "RJ": "રાજસ્થાન", "MP": "મધ્ય પ્રદેશ"},
    "pa": {"PB": "ਪੰਜਾਬ", "HR": "ਹਰਿਆਣਾ", "DL": "ਦਿੱਲੀ", "RJ": "ਰਾਜਸਥਾਨ", "UP": "ਉੱਤਰ ਪ੍ਰਦੇਸ਼"},
}


def name(code, lang="en", spoken=True):
    """State name for text in `lang`. Hindi on-screen text is Roman Hinglish, so it gets the English name
    (spoken=False); everything Timbre reads gets the name in that language's script."""
    if code not in STATES:
        return ""
    en, hi, _ = STATES[code]
    if lang == "mr" or (lang == "hi" and spoken):
        return hi
    return NATIVE.get(lang, {}).get(code, en)
