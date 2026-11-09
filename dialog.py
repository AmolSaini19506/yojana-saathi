"""
Conversation flow. Stateless on the server: the browser sends back `state` every turn.

Turn 1: open question ("tell me about yourself"). One sentence can fill several slots.
Then we only ask for what's still missing, and stop as soon as we can decide.
"""
import langs
import nlu
import schemes

# What to say for each slot. `show` is displayed, `say` is spoken by Timbre.
Q = {
    "hi": {
        "intro": {
            "show": "Namaste! Main Yojana Saathi hoon. Apne baare mein bataiye: umar, kya kaam karte hain, "
                    "aur mahine ki kamai lagbhag kitni hai. Aap apni kisi bhi bhasha mein bol sakte hain.",
            "say": "नमस्ते! मैं योजना साथी हूँ। अपने बारे में बताइए: आपकी उम्र, आप क्या काम करते हैं, "
                   "और महीने की कमाई लगभग कितनी है। आप अपनी किसी भी भाषा में बोल सकते हैं।",
        },
        "age": {"show": "Aapki umar kitni hai?", "say": "आपकी उम्र कितनी है?"},
        "occupation": {
            "show": "Aap kya kaam karte hain? Jaise kheti, dukaan, thela, mazdoori, naukri, "
                    "ya koi hunar jaise darzi, barhai, nai.",
            "say": "आप क्या काम करते हैं? जैसे खेती, दुकान, ठेला, मज़दूरी, नौकरी, या कोई हुनर, "
                   "जैसे दर्ज़ी, बढ़ई या नाई।",
        },
        "land_ha": {"show": "Aapke naam par kitni zameen hai? Acre ya bigha mein bataiye.",
                    "say": "आपके नाम पर कितनी ज़मीन है? एकड़ या बीघा में बताइए।"},
        "income_month": {"show": "Mahine ki kamai lagbhag kitni hai?",
                         "say": "महीने की कमाई लगभग कितनी है?"},
        "itax": {"show": "Kya aap income tax bharte hain?", "say": "क्या आप इनकम टैक्स भरते हैं?"},
        "epf": {"show": "Kya aapka PF katta hai, ya ESIC card hai?",
                "say": "क्या आपकी सैलरी से पीएफ कटता है, या ईएसआईसी कार्ड है?"},
        "daughter_u10": {"show": "Kya ghar mein 10 saal se chhoti beti hai?",
                         "say": "क्या घर में दस साल से छोटी बेटी है?"},
        "retry": {"show": "Maaf kijiye, samajh nahi aaya. ", "say": "माफ़ कीजिए, समझ नहीं आया। "},
        "none": {"show": "Aapke jawabon se abhi koi pakki yojana nahi mili. Nazdeeki CSC par ek baar zaroor poochhiye.",
                 "say": "आपके जवाबों से अभी कोई पक्की योजना नहीं मिली। नज़दीकी सीएससी केंद्र पर एक बार ज़रूर पूछिए।"},
        "found": {"show": "Aapke liye {n} yojanayein mili hain 👇",
                  "say": "बढ़िया! आपके लिए {n} योजनाएँ मिली हैं।"},
        "outro": {"show": "Inke liye apna Aadhaar aur bank passbook lekar nazdeeki CSC ya bank jaiye.",
                  "say": "इनके लिए अपना आधार और बैंक पासबुक लेकर नज़दीकी सीएससी केंद्र या बैंक जाइए।"},
        "more": {"say": "बाकी योजनाएँ स्क्रीन पर देखिए।"},
        # asked back "what is that?" -> explain the term, then ask again
        "x_epf": {"show": "PF matlab Provident Fund: agar aap kisi company ya office mein naukri karte hain, to har mahine "
                          "salary se kuch paisa PF khate mein katta hai. ESIC card company ki taraf se ilaaj ka beema hota hai. "
                          "Agar aap apna kaam khud karte hain, ya salary slip mein PF nahi katta, to jawab hai 'nahi'.",
                  "say": "पीएफ यानी प्रोविडेंट फ़ंड: अगर आप किसी कंपनी या दफ़्तर में नौकरी करते हैं, तो हर महीने सैलरी से कुछ "
                         "पैसा पीएफ खाते में कटता है। ईएसआईसी कार्ड कंपनी की तरफ़ से इलाज का बीमा होता है। अगर आप अपना काम "
                         "खुद करते हैं, या सैलरी स्लिप में पीएफ नहीं कटता, तो जवाब है नहीं।"},
        "x_itax": {"show": "Income tax woh tax hai jo saal ki kamai zyada hone par sarkar ko bharte hain, aur har saal ITR "
                           "form bharte hain. Agar aapne kabhi ITR nahi bhara, to jawab hai 'nahi'.",
                   "say": "इनकम टैक्स वो टैक्स है जो साल की कमाई ज़्यादा होने पर सरकार को भरते हैं, और हर साल आईटीआर फ़ॉर्म "
                          "भरते हैं। अगर आपने कभी आईटीआर नहीं भरा, तो जवाब है नहीं।"},
        "ok_skip": {"show": "Koi baat nahi.", "say": "कोई बात नहीं।"},
    },
    "en": {
        "intro": {
            "show": "Namaste! I'm Yojana Saathi. Tell me about yourself: your age, what work you do, "
                    "and roughly how much you earn in a month. You can speak in your own language.",
            "say": "Namaste! I'm Yojana Saathi. Tell me about yourself: your age, what work you do, "
                   "and roughly how much you earn in a month. You can speak in your own language.",
        },
        "age": {"show": "How old are you?", "say": "How old are you?"},
        "occupation": {"show": "What work do you do? For example farming, a shop, a street cart, daily wage work, "
                               "a job, or a craft like tailoring or carpentry.",
                       "say": "What work do you do? For example farming, a shop, a street cart, daily wage work, "
                              "a job, or a craft like tailoring or carpentry."},
        "land_ha": {"show": "How much land is in your name? Tell me in acres or bigha.",
                    "say": "How much land is in your name? Tell me in acres or bigha."},
        "income_month": {"show": "Roughly how much do you earn in a month?",
                         "say": "Roughly how much do you earn in a month?"},
        "itax": {"show": "Do you pay income tax?", "say": "Do you pay income tax?"},
        "epf": {"show": "Is PF deducted from your salary, or do you have an ESIC card?",
                "say": "Is PF deducted from your salary, or do you have an ESIC card?"},
        "daughter_u10": {"show": "Do you have a daughter younger than 10?",
                         "say": "Do you have a daughter younger than ten?"},
        "retry": {"show": "Sorry, I didn't catch that. ", "say": "Sorry, I didn't catch that. "},
        "none": {"show": "I couldn't find a definite match from your answers. Please ask once at your nearest CSC.",
                 "say": "I couldn't find a definite match from your answers. Please ask once at your nearest CSC."},
        "found": {"show": "I found {n} schemes for you 👇", "say": "Great news! I found {n} schemes for you."},
        "outro": {"show": "Take your Aadhaar and bank passbook to the nearest CSC or bank to apply.",
                  "say": "Take your Aadhaar and bank passbook to the nearest CSC or bank to apply."},
        "more": {"say": "See the rest on the screen."},
        "x_epf": {"show": "PF means Provident Fund: if you have a salaried job at a company or office, part of your salary "
                          "is cut every month and put into a PF account. ESIC is a health insurance card given through your "
                          "employer. If you work for yourself, or no PF is cut from your salary slip, the answer is no.",
                  "say": "PF means Provident Fund: if you have a salaried job at a company or office, part of your salary "
                         "is cut every month and put into a PF account. ESIC is a health insurance card given through your "
                         "employer. If you work for yourself, or no PF is cut from your salary slip, the answer is no."},
        "x_itax": {"show": "Income tax is the tax people with higher yearly earnings pay to the government, filing an ITR "
                           "form every year. If you have never filed an ITR, the answer is no.",
                   "say": "Income tax is the tax people with higher yearly earnings pay to the government, filing an ITR "
                          "form every year. If you have never filed an ITR, the answer is no."},
        "ok_skip": {"show": "No problem.", "say": "No problem."},
    },
}

HI_NUM = ["शून्य", "एक", "दो", "तीन", "चार", "पाँच", "छह", "सात", "आठ", "नौ", "दस", "ग्यारह", "बारह", "तेरह"]
EN_NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
          "eleven", "twelve", "thirteen"]


def spoken_num(n, lang):
    if lang not in ("hi", "en"):
        return str(n)                    # Timbre reads digits in every language
    words = HI_NUM if lang == "hi" else EN_NUM
    return words[n] if 0 <= n < len(words) else str(n)


def qt(lang, key):
    """(show, say) for one of the lines above, in any language."""
    p = langs.pack(lang)
    if p:
        line = p.Q[key]
        return line, line                 # language packs: same text on screen and in voice
    d = Q[lang][key]
    return d.get("show", d.get("say", "")), d.get("say", d.get("show", ""))


MAX_RETRIES = 1        # re-ask a slot once, then move on
YES_NO_SLOTS = {"itax", "epf", "daughter_u10"}
EXPLAINABLE = {"itax", "epf"}   # jargon people often ask about; Q["x_itax"] / Q["x_epf"] explain it
MAX_SPOKEN = 3         # speak the top 3 schemes (keeps the voice reply short), show all on screen


def needed_slots(p: dict):
    """Which slots still matter, in the order we'd ask them."""
    slots = ["age", "occupation"]
    occ = p.get("occupation")
    if occ == "farmer":
        slots.append("land_ha")
    slots.append("income_month")
    inc = p.get("income_month")
    if not (inc is not None and inc * 12 <= 500000):   # ≤ ₹5 lakh a year owes no income tax under either regime
        slots.append("itax")
    age = p.get("age")
    if occ in ("salaried_private", "labourer", "other_self_employed", "street_vendor", "artisan") \
            and (age is None or age <= 59):
        slots.append("epf")
    if age is None or 18 <= age <= 60:
        slots.append("daughter_u10")
    return slots


def next_slot(p: dict):
    for s in needed_slots(p):
        if s not in p:
            return s
    return None


def _apply_inferences(p: dict):
    inc = p.get("income_month")
    if "itax" not in p and inc is not None and inc * 12 <= 500000:
        p["itax"] = False
    if p.get("occupation") == "govt_employee":
        p.setdefault("epf", True)


def turn(state: dict, text: str, lang: str = "hi") -> dict:
    lang = langs.valid(lang)
    state = dict(state or {})
    profile = dict(state.get("profile") or {})
    asked = state.get("asked")
    retries = dict(state.get("retries") or {})

    # first call: no text yet -> greet
    if not text and not asked:
        state.update(profile=profile, asked="intro", retries={})
        show, say = qt(lang, "intro")
        return {"state": state, "show": show, "say": say, "done": False, "lang": lang}

    # They asked back ("PF kya hota hai?") or said they don't know ("pata nahi") instead of answering.
    # For yes/no questions check this first: "वो क्या होता है?" must not count as "yes" because of "है".
    explained = list(state.get("explained") or [])
    clar = nlu.clarify(text, lang) if (text and asked and asked != "intro") else None
    if clar and asked not in YES_NO_SLOTS:
        if asked in nlu.extract(text, expecting=asked, lang=lang):
            clar = None                    # "pata nahi, shayad 10 hazaar" still answered the question
    if clar == "dontknow":
        profile[asked] = None              # unknown: rules treat it as "not true", nobody loses eligibility
        _apply_inferences(profile)
        nxt = next_slot(profile)
        (ks, ky) = qt(lang, "ok_skip")
        if nxt:
            state.update(profile=profile, asked=nxt, retries=retries, explained=explained)
            qs, qy = qt(lang, nxt)
            return {"state": state, "heard": {}, "show": ks + " " + qs, "say": ky + " " + qy, "done": False,
                    "lang": lang}
        text = ""                          # nothing left to ask: fall through to the results
    elif clar == "what" and asked in EXPLAINABLE and asked not in explained:
        explained.append(asked)
        state.update(profile=profile, asked=asked, retries=retries, explained=explained)
        (xs, xy), (qs, qy) = qt(lang, "x_" + asked), qt(lang, asked)
        return {"state": state, "heard": {}, "show": xs + "\n\n" + qs, "say": xy + " " + qy, "done": False,
                "lang": lang}
    elif clar == "what":
        text = ""                          # a question we can't explain: treat as not understood (asks again)
    state["explained"] = explained

    got = nlu.extract(text or "", expecting=None if asked == "intro" else asked, lang=lang)
    if asked == "daughter_u10":
        # "haan, 12 saal ki hai" -> not under 10
        ages = [n["value"] for n in nlu.find_numbers(text, lang) if n["unit"] in ("age", None)]
        if ages and got.get("daughter_u10") is not False:
            got["daughter_u10"] = min(ages) < 10
        got.pop("age", None)
    for k, v in got.items():
        if k.startswith("_"):
            continue
        if k not in profile or k == asked:
            profile[k] = v
    if got.get("occupation") == "artisan" and got.get("trade"):
        profile["trade"] = got["trade"]
    _apply_inferences(profile)

    prefix_show = prefix_say = ""
    if asked and asked != "intro" and asked not in profile:
        if retries.get(asked, 0) < MAX_RETRIES:
            retries[asked] = retries.get(asked, 0) + 1
            state.update(profile=profile, asked=asked, retries=retries)
            (rs, ry), (qs, qy) = qt(lang, "retry"), qt(lang, asked)
            return {"state": state, "heard": got, "show": rs.rstrip() + " " + qs,
                    "say": ry.rstrip() + " " + qy, "done": False, "lang": lang}
        profile[asked] = None          # give up on this slot, rules treat None as unknown

    nxt = next_slot(profile)
    if nxt:
        state.update(profile=profile, asked=nxt, retries=retries)
        qs, qy = qt(lang, nxt)
        return {"state": state, "heard": got, "show": prefix_show + qs,
                "say": prefix_say + qy, "done": False, "lang": lang}

    eligible, maybe = schemes.match(profile, lang)
    state.update(profile=profile, asked=None, retries=retries)
    if not eligible:
        ns, ny = qt(lang, "none")
        say = ny + " " + " ".join(m["speak"] for m in maybe)
        return {"state": state, "heard": got, "show": ns, "say": say.strip(),
                "done": True, "eligible": [], "maybe": maybe, "profile": profile, "lang": lang}

    n = len(eligible)
    spoken = " ".join(s["speak"] for s in eligible[:MAX_SPOKEN])
    if n > MAX_SPOKEN:
        spoken += " " + qt(lang, "more")[1]
    (fs, fy), (os_, oy) = qt(lang, "found"), qt(lang, "outro")
    say = f'{fy.format(n=spoken_num(n, lang))} {spoken} {oy}'
    return {"state": state, "heard": got, "show": fs.format(n=n) + "\n\n" + os_,
            "say": say, "done": True, "eligible": eligible, "maybe": maybe, "profile": profile, "lang": lang}
