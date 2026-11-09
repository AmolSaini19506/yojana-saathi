"""
Central government schemes + eligibility rules.

Rules checked against official / news sources in Nov 2026 (see README "Sources").
These are simplified screening rules, not a legal eligibility decision: every result
tells the user to confirm at a CSC, bank or the official portal.
"""
import langs

UNORGANISED = {"street_vendor", "labourer", "artisan", "other_self_employed"}
NON_FARM_BUSINESS = {"shopkeeper", "street_vendor", "artisan", "other_self_employed"}

TRADE_HI = {
    "carpenter": "बढ़ई", "blacksmith": "लोहार", "goldsmith": "सुनार", "potter": "कुम्हार",
    "cobbler": "मोची", "mason": "राजमिस्त्री", "tailor": "दर्ज़ी", "barber": "नाई",
    "washerman": "धोबी", "garland_maker": "माली", "locksmith": "ताला बनाने वाले",
    "sculptor": "मूर्तिकार", "basket_maker": "टोकरी-चटाई बनाने वाले", "toy_maker": "खिलौना बनाने वाले",
    "fishing_net_maker": "जाल बनाने वाले", "boat_maker": "नाव बनाने वाले", "armourer": "अस्त्र बनाने वाले",
    "tool_maker": "औज़ार बनाने वाले",
}


def _age(p):
    return p.get("age")


def _not_tax(p):
    return p.get("itax") is not True


def _no_pf(p):
    return p.get("epf") is not True


SCHEMES = [
    {
        "id": "pm_kisan",
        "name": "PM-KISAN",
        "name_hi": "पीएम किसान सम्मान निधि",
        "benefit": "₹6,000 a year, paid as three ₹2,000 instalments into your bank account",
        "benefit_hi": "साल के ₹6,000, तीन किस्तों में सीधे बैंक खाते में",
        "speak_hi": "पीएम किसान सम्मान निधि: हर साल छह हज़ार रुपये, दो-दो हज़ार की तीन किस्तों में।",
        "speak_en": "PM Kisan: six thousand rupees every year, in three instalments of two thousand.",
        "apply": "pmkisan.gov.in or your nearest CSC",
        "docs": "Aadhaar, land records in your name, bank account linked to Aadhaar, e-KYC",
        "rule": lambda p: p.get("occupation") == "farmer" and (p.get("land_ha") or 0) > 0 and _not_tax(p),
        "note": "Land must be in your name. Income-tax payers, government employees and pensioners "
                "getting ₹10,000+ a month are excluded.",
    },
    {
        "id": "pm_kmy",
        "name": "PM Kisan Maan-Dhan",
        "name_hi": "पीएम किसान मानधन योजना",
        "benefit": "₹3,000 a month pension after 60. You pay ₹55–₹200 a month, the government matches it",
        "benefit_hi": "60 साल के बाद ₹3,000 महीना पेंशन। आप ₹55–₹200 महीना जमा करें, उतना ही सरकार देगी",
        "speak_hi": "पीएम किसान मानधन: साठ साल के बाद हर महीने तीन हज़ार रुपये पेंशन।",
        "speak_en": "PM Kisan Maan-Dhan: a pension of three thousand rupees a month after sixty.",
        "apply": "Nearest CSC (Common Service Centre)",
        "docs": "Aadhaar, savings bank account, land records",
        "rule": lambda p: p.get("occupation") == "farmer" and _age(p) is not None and 18 <= _age(p) <= 40
        and 0 < (p.get("land_ha") or 0) <= 2 and _no_pf(p),
        "note": "For small and marginal farmers with up to 2 hectares (about 5 acres).",
    },
    {
        "id": "pm_svanidhi",
        "name": "PM SVANidhi",
        "name_hi": "पीएम स्वनिधि",
        "benefit": "Collateral-free loans of ₹15,000, then ₹25,000, then ₹50,000, 7% interest subsidy, "
                   "cashback up to ₹1,600 on digital payments",
        "benefit_hi": "बिना गारंटी लोन: पहले ₹15,000, फिर ₹25,000, फिर ₹50,000। ब्याज पर 7% सब्सिडी",
        "speak_hi": "पीएम स्वनिधि: ठेले और रेहड़ी वालों के लिए बिना गारंटी लोन, पहले पंद्रह हज़ार, फिर पच्चीस हज़ार, फिर पचास हज़ार।",
        "speak_en": "PM SVANidhi: collateral-free loans for street vendors, fifteen thousand, then twenty-five, then fifty thousand.",
        "apply": "pmsvanidhi.mohua.gov.in, a bank, or your nearest CSC",
        "docs": "Aadhaar, mobile number, vending certificate or letter of recommendation from the urban local body",
        "rule": lambda p: p.get("occupation") == "street_vendor" and (_age(p) or 18) >= 18,
        "note": "Lending runs till 31 March 2030. Mainly for vendors in towns, cities and peri-urban areas.",
    },
    {
        "id": "pm_vishwakarma",
        "name": "PM Vishwakarma",
        "name_hi": "पीएम विश्वकर्मा योजना",
        "benefit": "₹15,000 toolkit voucher, training with ₹500/day stipend, loans up to ₹3 lakh at 5% "
                   "(₹1 lakh, then ₹2 lakh)",
        "benefit_hi": "₹15,000 का टूलकिट, ट्रेनिंग में ₹500 रोज़, और 5% ब्याज पर ₹3 लाख तक लोन",
        "speak_hi": "पीएम विश्वकर्मा: पंद्रह हज़ार का टूलकिट, ट्रेनिंग में पाँच सौ रुपये रोज़, और पाँच प्रतिशत ब्याज पर तीन लाख तक का लोन।",
        "speak_en": "PM Vishwakarma: a fifteen thousand rupee toolkit, five hundred rupees a day during training, and loans up to three lakh at five percent.",
        "apply": "pmvishwakarma.gov.in through your nearest CSC",
        "docs": "Aadhaar, mobile number, bank account, ration card",
        "rule": lambda p: p.get("occupation") == "artisan" and (_age(p) or 18) >= 18,
        "note": "Only one member per family. Not if you took a similar government self-employment loan "
                "(PMEGP, Mudra, SVANidhi) in the last 5 years.",
    },
    {
        "id": "mudra",
        "name": "PM Mudra Yojana",
        "name_hi": "प्रधानमंत्री मुद्रा योजना",
        "benefit": "Collateral-free business loans: Shishu up to ₹50,000, Kishor up to ₹5 lakh, "
                   "Tarun up to ₹10 lakh (Tarun Plus up to ₹20 lakh after repaying Tarun)",
        "benefit_hi": "बिना गारंटी बिज़नेस लोन: शिशु ₹50,000 तक, किशोर ₹5 लाख तक, तरुण ₹10 लाख तक",
        "speak_hi": "मुद्रा योजना: दुकान या छोटे धंधे के लिए बिना गारंटी लोन, पचास हज़ार से दस लाख रुपये तक।",
        "speak_en": "Mudra Yojana: collateral-free loans for your shop or small business, from fifty thousand up to ten lakh rupees.",
        "apply": "Any bank branch, or online at jansamarth.in / udyamimitra.in",
        "docs": "Aadhaar, PAN, business proof, bank statement",
        "rule": lambda p: p.get("occupation") in NON_FARM_BUSINESS and (_age(p) or 18) >= 18,
        "note": "For non-farm income-generating businesses. Interest rate is set by the bank.",
    },
    {
        "id": "pm_sym",
        "name": "PM Shram Yogi Maan-Dhan",
        "name_hi": "पीएम श्रम योगी मानधन",
        "benefit": "₹3,000 a month pension after 60. You pay ₹55–₹200 a month, the government matches it",
        "benefit_hi": "60 साल के बाद ₹3,000 महीना पेंशन। आप ₹55–₹200 महीना जमा करें, उतना ही सरकार देगी",
        "speak_hi": "श्रम योगी मानधन: साठ साल के बाद हर महीने तीन हज़ार रुपये पेंशन। आप जितना जमा करेंगे, उतना ही सरकार डालेगी।",
        "speak_en": "Shram Yogi Maan-Dhan: three thousand rupees a month pension after sixty. The government matches what you save.",
        "apply": "Nearest CSC (Common Service Centre)",
        "docs": "Aadhaar, savings or Jan Dhan bank account, mobile number",
        "rule": lambda p: p.get("occupation") in UNORGANISED and _age(p) is not None and 18 <= _age(p) <= 40
        and p.get("income_month") is not None and p["income_month"] <= 15000 and _no_pf(p) and _not_tax(p),
        "note": "For unorganised workers earning ₹15,000 a month or less, not in EPF/ESIC/NPS.",
    },
    {
        "id": "eshram",
        "name": "e-Shram Card",
        "name_hi": "ई-श्रम कार्ड",
        "benefit": "Free national ID for unorganised workers that links you to welfare schemes",
        "benefit_hi": "असंगठित मज़दूरों के लिए मुफ़्त पहचान कार्ड, जिससे सरकारी योजनाएँ जुड़ती हैं",
        "speak_hi": "ई-श्रम कार्ड: मुफ़्त में बनता है, और इससे बाकी सरकारी योजनाएँ जुड़ जाती हैं।",
        "speak_en": "e-Shram card: free to make, and it links you to other government schemes.",
        "apply": "eshram.gov.in or your nearest CSC",
        "docs": "Aadhaar, mobile number linked to Aadhaar, bank account",
        "rule": lambda p: p.get("occupation") in UNORGANISED | {"shopkeeper"} and _age(p) is not None
        and 16 <= _age(p) <= 59 and _no_pf(p) and _not_tax(p),
        "note": "Not for EPFO/ESIC members or income-tax payers.",
    },
    {
        "id": "apy",
        "name": "Atal Pension Yojana",
        "name_hi": "अटल पेंशन योजना",
        "benefit": "Guaranteed pension of ₹1,000–₹5,000 a month after 60, based on what you contribute",
        "benefit_hi": "60 साल के बाद ₹1,000 से ₹5,000 महीना पक्की पेंशन",
        "speak_hi": "अटल पेंशन योजना: साठ साल के बाद हर महीने एक हज़ार से पाँच हज़ार रुपये तक पक्की पेंशन।",
        "speak_en": "Atal Pension Yojana: a guaranteed pension of one to five thousand rupees a month after sixty.",
        "apply": "Your bank or post office branch",
        "docs": "Aadhaar, savings bank account, mobile number",
        "rule": lambda p: _age(p) is not None and 18 <= _age(p) <= 40 and _not_tax(p),
        "note": "Income-tax payers can't join (since Oct 2022).",
    },
    {
        "id": "pmjjby",
        "name": "PM Jeevan Jyoti Bima",
        "name_hi": "प्रधानमंत्री जीवन ज्योति बीमा",
        "benefit": "₹2 lakh life insurance for ₹436 a year",
        "benefit_hi": "सिर्फ़ ₹436 साल में ₹2 लाख का जीवन बीमा",
        "speak_hi": "जीवन ज्योति बीमा: साल के सिर्फ़ चार सौ छत्तीस रुपये में दो लाख का जीवन बीमा।",
        "speak_en": "Jeevan Jyoti Bima: two lakh rupees of life insurance for just four hundred and thirty-six rupees a year.",
        "apply": "Your bank, post office, or the bank's app",
        "docs": "Savings bank account with auto-debit, Aadhaar",
        "rule": lambda p: _age(p) is not None and 18 <= _age(p) <= 50,
        "note": "Premium is auto-debited once a year.",
    },
    {
        "id": "pmsby",
        "name": "PM Suraksha Bima",
        "name_hi": "प्रधानमंत्री सुरक्षा बीमा",
        "benefit": "₹2 lakh accident insurance for ₹20 a year",
        "benefit_hi": "सिर्फ़ ₹20 साल में ₹2 लाख का दुर्घटना बीमा",
        "speak_hi": "सुरक्षा बीमा: साल के सिर्फ़ बीस रुपये में दो लाख का दुर्घटना बीमा।",
        "speak_en": "Suraksha Bima: two lakh rupees of accident insurance for just twenty rupees a year.",
        "apply": "Your bank, post office, or the bank's app",
        "docs": "Savings bank account with auto-debit, Aadhaar",
        "rule": lambda p: _age(p) is not None and 18 <= _age(p) <= 70,
        "note": "Covers accidental death and disability.",
    },
    {
        "id": "sukanya",
        "name": "Sukanya Samriddhi Yojana",
        "name_hi": "सुकन्या समृद्धि योजना",
        "benefit": "High-interest, tax-free savings account for your daughter's education and marriage",
        "benefit_hi": "बेटी की पढ़ाई और शादी के लिए ज़्यादा ब्याज वाला, टैक्स-फ़्री बचत खाता",
        "speak_hi": "सुकन्या समृद्धि: बेटी के नाम पर ज़्यादा ब्याज वाला बचत खाता।",
        "speak_en": "Sukanya Samriddhi: a high-interest savings account in your daughter's name.",
        "apply": "Post office or bank branch",
        "docs": "Daughter's birth certificate, parent's Aadhaar and PAN",
        "rule": lambda p: p.get("daughter_u10") is True,
        "note": "Account must be opened before the girl turns 10.",
    },
    {
        "id": "vay_vandana",
        "name": "Ayushman Vay Vandana",
        "name_hi": "आयुष्मान वय वंदना कार्ड",
        "benefit": "₹5 lakh a year of free hospital treatment, no income limit",
        "benefit_hi": "हर साल ₹5 लाख तक मुफ़्त अस्पताल इलाज, कोई आय सीमा नहीं",
        "speak_hi": "आयुष्मान वय वंदना: सत्तर साल से ऊपर सबको हर साल पाँच लाख तक का मुफ़्त इलाज, कमाई कितनी भी हो।",
        "speak_en": "Ayushman Vay Vandana: free hospital treatment up to five lakh a year for everyone above seventy, whatever their income.",
        "apply": "Ayushman app, beneficiary.nha.gov.in, or your nearest CSC",
        "docs": "Aadhaar (age is checked from Aadhaar)",
        "rule": lambda p: _age(p) is not None and _age(p) >= 70,
        "note": "Every citizen aged 70+ is eligible.",
    },
]

# Shown as "check this" rather than "eligible": eligibility depends on lists we can't see.
MAYBE = [
    {
        "id": "pmjay",
        "name": "Ayushman Bharat PM-JAY",
        "name_hi": "आयुष्मान भारत",
        "benefit": "₹5 lakh a year free hospital treatment for eligible poor families",
        "benefit_hi": "पात्र परिवारों के लिए हर साल ₹5 लाख तक मुफ़्त इलाज",
        "speak_hi": "आयुष्मान भारत कार्ड भी चेक कीजिए, शायद आपका परिवार उसकी लिस्ट में हो।",
        "speak_en": "Also check Ayushman Bharat, your family may be on its list.",
        "apply": "Check your name with Aadhaar on beneficiary.nha.gov.in or the Ayushman app",
        "docs": "Aadhaar, ration card",
        "rule": lambda p: p.get("income_month") is not None and p["income_month"] <= 15000
        and (_age(p) or 0) < 70,
        "note": "Depends on SECC 2011 and state lists, so we can't confirm it from your answers.",
    },
]


# ---------------------------------------------------------------- "why you qualify"

def _fragments(p, lang):
    hi = lang == "hi"
    age, inc, occ = p.get("age"), p.get("income_month"), p.get("occupation")
    trade = TRADE_HI.get(p.get("trade"), "") if hi else (p.get("trade") or "").replace("_", " ")
    f = {
        "farmer": "आप किसान हैं" if hi else "you are a farmer",
        "land": "आपके नाम पर ज़मीन है" if hi else "you have land in your name",
        "small_land": "आपकी ज़मीन दो हेक्टेयर से कम है" if hi else "your land is under two hectares",
        "no_tax": "आप इनकम टैक्स नहीं भरते" if hi else "you don't pay income tax",
        "age": (f"आपकी उम्र {age} साल है" if hi else f"you are {age}") if age is not None else None,
        "vendor": "आप ठेला या रेहड़ी लगाते हैं" if hi else "you are a street vendor",
        "artisan": (f"आप {trade} का काम करते हैं" if hi else f"you work as a {trade}") if trade else
                   ("आप हुनर वाला काम करते हैं" if hi else "you work in a traditional trade"),
        "business": "आप अपना काम-धंधा करते हैं" if hi else "you run your own business",
        "unorganised": "आप असंगठित क्षेत्र में काम करते हैं" if hi else "you work in the unorganised sector",
        "income": (f"आपकी कमाई ₹{inc:,} महीना है" if hi else f"you earn ₹{inc:,} a month") if inc is not None else None,
        "low_income": (f"आपकी कमाई ₹{inc:,} महीना है" if hi else f"you earn ₹{inc:,} a month") if inc is not None else None,
        "no_pf": "आपका पीएफ़ नहीं कटता" if hi else "you're not in PF or ESIC",
        "daughter": "आपकी बेटी दस साल से छोटी है" if hi else "you have a daughter under ten",
        "senior": "आपकी उम्र सत्तर साल या ज़्यादा है" if hi else "you are seventy or older",
    }
    if occ == "shopkeeper":
        f["unorganised"] = "आप छोटा धंधा करते हैं" if hi else "you run a small business"
    if p.get("itax") is not False:
        f["no_tax"] = None
    if p.get("epf") is not False:
        f["no_pf"] = None
    return f


WHY_KEYS = {
    "pm_kisan": ["farmer", "land", "no_tax"], "pm_kmy": ["farmer", "age", "small_land"],
    "pm_svanidhi": ["vendor"], "pm_vishwakarma": ["artisan"], "mudra": ["business"],
    "pm_sym": ["unorganised", "age", "income", "no_pf"], "eshram": ["unorganised", "age", "no_tax"],
    "apy": ["age", "no_tax"], "pmjjby": ["age"], "pmsby": ["age"], "sukanya": ["daughter"],
    "vay_vandana": ["senior"], "pmjay": ["low_income"],
}


def _pack_fragments(p, pk):
    """Same reasons as _fragments(), from a language pack's WHY templates."""
    W = pk.WHY
    age, inc, occ = p.get("age"), p.get("income_month"), p.get("occupation")
    f = {k: W.get(k) for k in ("farmer", "land", "small_land", "no_tax", "vendor", "artisan", "business",
                               "unorganised", "no_pf", "daughter", "senior")}
    f["age"] = W["age"].format(age=age) if age is not None else None
    f["income"] = f["low_income"] = W["income"].format(inc=f"{inc:,}") if inc is not None else None
    if occ == "shopkeeper":
        f["unorganised"] = W.get("shop", f["unorganised"])
    if p.get("itax") is not False:
        f["no_tax"] = None
    if p.get("epf") is not False:
        f["no_pf"] = None
    return f


def why(sid, profile, lang="hi"):
    pk = langs.pack(lang)
    f = _pack_fragments(profile, pk) if pk else _fragments(profile, lang)
    parts = [f[k] for k in WHY_KEYS.get(sid, []) if f.get(k)]
    if not parts:
        return ""
    joiner = pk.UI["and"] if pk else (" और " if lang == "hi" else " and ")
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + joiner + parts[-1]


def match(profile: dict, lang: str = "hi"):
    """Return (eligible, maybe) lists of public scheme dicts, each with a `why` reason."""
    pk = langs.pack(lang)

    def public(s):
        out = {k: v for k, v in s.items() if k != "rule"}
        if s["id"] == "pm_vishwakarma" and profile.get("trade") in TRADE_HI and lang == "hi":
            out["trade_hi"] = TRADE_HI[profile["trade"]]
        out["why"] = why(s["id"], profile, lang)
        # fields in the conversation's language: name_local / benefit_local on the card, speak for Timbre
        if pk:
            out["name_local"], out["benefit_local"], out["speak"] = pk.SCHEMES[s["id"]]
        elif lang == "hi":
            out["name_local"], out["benefit_local"], out["speak"] = s["name_hi"], s["benefit_hi"], s["speak_hi"]
        else:
            out["name_local"], out["benefit_local"], out["speak"] = s["name_hi"], s["benefit"], s["speak_en"]
        return out

    eligible = [public(s) for s in SCHEMES if _safe(s["rule"], profile)]
    maybe = [public(s) for s in MAYBE if _safe(s["rule"], profile)]
    # if someone got APY *and* a matched-contribution pension, keep both; they stack
    return eligible, maybe


def _safe(rule, profile):
    try:
        return bool(rule(profile))
    except Exception:
        return False
