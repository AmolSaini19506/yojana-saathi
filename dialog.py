"""
Conversation flow. Stateless on the server: the browser sends back `state` every turn.

Turn 1: open question ("tell me about yourself"). One sentence can fill several slots.
Then we only ask for what's still missing, and stop as soon as we can decide.
"""
import engine
import langs
import nlu
import schemes
import states

# What to say for each slot. `show` is displayed, `say` is spoken by Timbre.
Q = {
    "hi": {
        "intro": {
            "show": "नमस्ते! मैं योजना साथी हूँ। अपने बारे में बताइए: आपकी उम्र, आप क्या काम करते हैं, "
                    "और महीने की कमाई लगभग कितनी है। आप अपनी किसी भी भाषा में बोल सकते हैं।",
            "say": "नमस्ते! मैं योजना साथी हूँ। अपने बारे में बताइए: आपकी उम्र, आप क्या काम करते हैं, "
                   "और महीने की कमाई लगभग कितनी है। आप अपनी किसी भी भाषा में बोल सकते हैं।",
        },
        "age": {"show": "आपकी उम्र कितनी है?", "say": "आपकी उम्र कितनी है?"},
        "occupation": {
            "show": "आप क्या काम करते हैं? जैसे खेती, दुकान, ठेला, मज़दूरी, नौकरी, या कोई हुनर, "
                    "जैसे दर्ज़ी, बढ़ई या नाई।",
            "say": "आप क्या काम करते हैं? जैसे खेती, दुकान, ठेला, मज़दूरी, नौकरी, या कोई हुनर, "
                   "जैसे दर्ज़ी, बढ़ई या नाई।",
        },
        "land_ha": {"show": "आपके नाम पर कितनी ज़मीन है? एकड़ या बीघा में बताइए।",
                    "say": "आपके नाम पर कितनी ज़मीन है? एकड़ या बीघा में बताइए।"},
        "income_month": {"show": "महीने की कमाई लगभग कितनी है?",
                         "say": "महीने की कमाई लगभग कितनी है?"},
        "itax": {"show": "क्या आप इनकम टैक्स भरते हैं?", "say": "क्या आप इनकम टैक्स भरते हैं?"},
        "epf": {"show": "क्या आपकी सैलरी से PF कटता है, या ESIC कार्ड है?",
                "say": "क्या आपकी सैलरी से पीएफ कटता है, या ईएसआईसी कार्ड है?"},
        "state": {"show": "आप किस राज्य में रहते हैं? जैसे UP, बिहार, महाराष्ट्र।",
                  "say": "आप किस राज्य में रहते हैं? जैसे यूपी, बिहार, महाराष्ट्र।"},
        "gender": {"show": "क्या आप महिला हैं या पुरुष? कुछ योजनाएँ सिर्फ़ महिलाओं के लिए हैं।",
                   "say": "क्या आप महिला हैं या पुरुष? कुछ योजनाएँ सिर्फ़ महिलाओं के लिए हैं।"},
        "biz": {"show": "क्या आप अपना नया काम-धंधा शुरू करना चाहते हैं?",
                "say": "क्या आप अपना नया काम-धंधा शुरू करना चाहते हैं?"},
        "state_note": {"show": "{state} की राज्य योजनाएँ अभी ऐप में नहीं हैं, इसलिए ये केंद्र सरकार की योजनाएँ हैं। "
                               "राज्य की योजनाओं के लिए नज़दीकी CSC पर पूछिए।",
                       "say": "{state} की राज्य योजनाएँ अभी ऐप में नहीं हैं, इसलिए ये केंद्र सरकार की योजनाएँ हैं। राज्य की "
                              "योजनाओं के लिए नज़दीकी सीएससी केंद्र पर पूछिए।"},
        "daughter_u10": {"show": "क्या घर में 10 साल से छोटी बेटी है?",
                         "say": "क्या घर में दस साल से छोटी बेटी है?"},
        "retry": {"show": "माफ़ कीजिए, समझ नहीं आया। ", "say": "माफ़ कीजिए, समझ नहीं आया। "},
        "none": {"show": "आपके जवाबों से अभी कोई पक्की योजना नहीं मिली। नज़दीकी CSC पर एक बार ज़रूर पूछिए।",
                 "say": "आपके जवाबों से अभी कोई पक्की योजना नहीं मिली। नज़दीकी सीएससी केंद्र पर एक बार ज़रूर पूछिए।"},
        "found": {"show": "आपके लिए {n} योजनाएँ मिली हैं 👇",
                  "say": "बढ़िया! आपके लिए {n} योजनाएँ मिली हैं।"},
        "outro": {"show": "इनके लिए अपना आधार और बैंक पासबुक लेकर नज़दीकी CSC या बैंक जाइए।",
                  "say": "इनके लिए अपना आधार और बैंक पासबुक लेकर नज़दीकी सीएससी केंद्र या बैंक जाइए।"},
        "more": {"say": "बाकी योजनाएँ स्क्रीन पर देखिए।"},
        # asked back "what is that?" -> explain the term, then ask again
        "x_epf": {"show": "PF यानी प्रोविडेंट फ़ंड (Provident Fund): अगर आप किसी कंपनी या दफ़्तर में नौकरी करते हैं, तो "
                          "हर महीने सैलरी से कुछ पैसा PF खाते में कटता है। ESIC कार्ड कंपनी की तरफ़ से इलाज का बीमा होता है। "
                          "अगर आप अपना काम खुद करते हैं, या सैलरी स्लिप में PF नहीं कटता, तो जवाब है 'नहीं'।",
                  "say": "पीएफ यानी प्रोविडेंट फ़ंड: अगर आप किसी कंपनी या दफ़्तर में नौकरी करते हैं, तो हर महीने सैलरी से कुछ "
                         "पैसा पीएफ खाते में कटता है। ईएसआईसी कार्ड कंपनी की तरफ़ से इलाज का बीमा होता है। अगर आप अपना काम "
                         "खुद करते हैं, या सैलरी स्लिप में पीएफ नहीं कटता, तो जवाब है नहीं।"},
        "x_itax": {"show": "इनकम टैक्स वो टैक्स है जो साल की कमाई ज़्यादा होने पर सरकार को भरते हैं, और हर साल ITR "
                           "फ़ॉर्म भरते हैं। अगर आपने कभी ITR नहीं भरा, तो जवाब है 'नहीं'।",
                   "say": "इनकम टैक्स वो टैक्स है जो साल की कमाई ज़्यादा होने पर सरकार को भरते हैं, और हर साल आईटीआर फ़ॉर्म "
                          "भरते हैं। अगर आपने कभी आईटीआर नहीं भरा, तो जवाब है नहीं।"},
        "ok_skip": {"show": "कोई बात नहीं।", "say": "कोई बात नहीं।"},
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
        "state": {"show": "Which state do you live in?", "say": "Which state do you live in?"},
        "gender": {"show": "Are you a woman or a man? Some schemes are only for women.",
                   "say": "Are you a woman or a man? Some schemes are only for women."},
        "biz": {"show": "Do you want to start a new business of your own?",
                "say": "Do you want to start a new business of your own?"},
        "state_note": {"show": "We don't have {state}'s own schemes in the app yet, so these are central government "
                               "schemes. Ask at your nearest CSC about state schemes.",
                       "say": "We don't have {state}'s own schemes in the app yet, so these are central government "
                              "schemes. Ask at your nearest CSC about state schemes."},
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
YES_NO_SLOTS = {"itax", "epf", "daughter_u10", "biz"}
EXPLAINABLE = {"itax", "epf"}   # jargon people often ask about; Q["x_itax"] / Q["x_epf"] explain it
MAX_SPOKEN = 3         # speak the top 3 schemes (keeps the voice reply short), show all on screen


def rules():
    """{scheme id: rule} for every scheme in the app, including the "check this" ones."""
    return {s["id"]: s["rule"] for s in schemes.SCHEMES + schemes.MAYBE}


def next_slot(p: dict, asked_followups: int = 0):
    """The next detail to ask about (see engine.py), or None when the results can't change any more."""
    return engine.next_slot(rules(), p, asked_followups)


def _apply_inferences(p: dict):
    engine.infer(p)


def _count(state: dict, slot):
    """Count follow-up questions (after age / work / state) so the conversation stays short."""
    if slot and slot not in engine.CORE and slot != state.get("asked"):
        state["nq"] = state.get("nq", 0) + 1


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
        nxt = next_slot(profile, state.get("nq", 0))
        (ks, ky) = qt(lang, "ok_skip")
        if nxt:
            _count(state, nxt)
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

    nxt = next_slot(profile, state.get("nq", 0))
    if nxt:
        _count(state, nxt)
        state.update(profile=profile, asked=nxt, retries=retries)
        qs, qy = qt(lang, nxt)
        return {"state": state, "heard": got, "show": prefix_show + qs,
                "say": prefix_say + qy, "done": False, "lang": lang}

    # schemes that still hinge on something we didn't ask (question limit reached) are shown as "check these"
    _, still_open = engine.status(rules(), profile)
    eligible, maybe = schemes.match(profile, lang, open_ids=set(still_open))
    state.update(profile=profile, asked=None, retries=retries)
    note_show = note_say = ""
    st = profile.get("state")
    if st and st not in states.COVERED:
        ns_, ny_ = qt(lang, "state_note")
        note_show = "\n\n" + ns_.format(state=states.name(st, lang))
        note_say = " " + ny_.format(state=states.name(st, lang))
    if not eligible:
        ns, ny = qt(lang, "none")
        say = ny + " " + " ".join(m["speak"] for m in maybe) + note_say
        return {"state": state, "heard": got, "show": ns + note_show, "say": say.strip(),
                "done": True, "eligible": [], "maybe": maybe, "profile": profile, "lang": lang}

    n = len(eligible)
    spoken = " ".join(s["speak"] for s in eligible[:MAX_SPOKEN])
    if n > MAX_SPOKEN:
        spoken += " " + qt(lang, "more")[1]
    (fs, fy), (os_, oy) = qt(lang, "found"), qt(lang, "outro")
    say = f'{fy.format(n=spoken_num(n, lang))} {spoken} {oy}{note_say}'
    return {"state": state, "heard": got, "show": fs.format(n=n) + "\n\n" + os_ + note_show,
            "say": say, "done": True, "eligible": eligible, "maybe": maybe, "profile": profile, "lang": lang}
