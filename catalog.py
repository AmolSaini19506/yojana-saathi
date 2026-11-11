"""
Schemes added from 11 Nov 2026 on: pensions, housing, maternity, students, rural work, and more states.

Every entry was checked on the web on the date in CHECKED. Where sources disagreed, the card says less instead of
guessing: no amount is shown that could not be confirmed, and such schemes go under "check this" (CHECK lists).
Things that changed in 2026 and are reflected here: MGNREGA was replaced by the VB-G RAM G Act on 1 July 2026;
the national pension programme (NSAP) was renamed Pradhan Mantri Samajik Sahayata Yojana in October 2026.
Left out because their current status could not be confirmed: PM-KUSUM (moving to a new phase), PM Matsya Sampada,
PMKVY 4.0, health cover for gig workers.

One entry holds everything for a scheme: the card in English and Hindi, where to apply, documents, a note on who it
is for, and the rule. The follow-up chat's facts are built from the same text (see kb_entries), so the card and the
chat can never disagree. Extra fields:
  cash   fixed money per year in rupees, used for the "you could get about ₹X a year" line (only where it is fixed)
  tags   documents needed, as keys of DOCS below, used for the one combined list of papers
  names  words people use for the scheme when asking about it
  local  {language: (name, benefit, spoken line)} translations for the beta languages
"""

CHECKED = "2026-11-11"

LOW_PERFORMING = {"UP", "UK", "BR", "JH", "MP", "CG", "AS", "RJ", "OD", "JK"}      # Janani Suraksha Yojana's higher rate
MANUAL_WORK = {"labourer", "farmer", "unemployed", "homemaker", "artisan", "street_vendor", "other_self_employed"}


def _age(p):
    return p.get("age")


def _between(p, lo, hi):
    a = _age(p)
    return a is not None and lo <= a <= hi


def _adult(p):
    return (_age(p) or 18) >= 18


def _woman(p):
    return p.get("gender") == "f"


def _not_tax(p):
    return p.get("itax") is not True


def _student(p):
    return p.get("occupation") == "student"


CENTRAL = [
    {
        "id": "vb_g_ram_g",
        "name": "VB-G RAM G (rural job guarantee)", "name_hi": "वीबी-जी राम जी (ग्रामीण रोज़गार गारंटी)",
        "benefit": "Up to 125 days of paid work a year for your household, at ₹300 a day or more",
        "benefit_hi": "आपके परिवार को साल में 125 दिन तक का काम, ₹300 रोज़ या उससे ज़्यादा मज़दूरी पर",
        "speak_en": "The rural job guarantee: up to one hundred and twenty-five days of paid work a year, at three hundred rupees a day or more.",
        "speak_hi": "ग्रामीण रोज़गार गारंटी: साल में एक सौ पच्चीस दिन तक का काम, तीन सौ रुपये रोज़ या उससे ज़्यादा मज़दूरी पर।",
        "apply": "Your gram panchayat office",
        "apply_hi": "अपनी ग्राम पंचायत के दफ़्तर में काम माँगिए।",
        "docs": "Aadhaar, bank account, job card (an old MGNREGA job card with e-KYC still works)",
        "docs_hi": "आधार कार्ड, बैंक खाता और जॉब कार्ड। पुराना मनरेगा जॉब कार्ड ई-केवाईसी के साथ अभी चलता है।",
        "note": "For adults in village households who will do manual work. It replaced MGNREGA on 1 July 2026.",
        "note_hi": "गाँव के उन परिवारों के लिए जिनके बड़े सदस्य हाथ का काम करने को तैयार हैं। 1 जुलाई 2026 से इसने मनरेगा की जगह ली है।",
        # no upper age in the law; we stop suggesting manual work from 70
        "rule": lambda p: p.get("rural") is True and _between(p, 18, 69) and p.get("occupation") in MANUAL_WORK and _not_tax(p),
        "why": ["rural"], "tags": ["aadhaar", "bank", "jobcard"],
        "names": ["ram g", "राम जी", "mgnrega", "manrega", "nrega", "मनरेगा", "नरेगा", "rozgar guarantee", "रोज़गार गारंटी",
                  "job card", "जॉब कार्ड"],
    },
    {
        "id": "surya_ghar",
        "name": "PM Surya Ghar (rooftop solar)", "name_hi": "पीएम सूर्य घर मुफ़्त बिजली योजना",
        "benefit": "Subsidy for solar panels on your roof: ₹30,000 for 1 kW, ₹60,000 for 2 kW, ₹78,000 for 3 kW or more",
        "benefit_hi": "छत पर सोलर पैनल के लिए सब्सिडी: 1 किलोवाट पर ₹30,000, 2 किलोवाट पर ₹60,000, 3 किलोवाट या ज़्यादा पर ₹78,000",
        "speak_en": "PM Surya Ghar: a subsidy of up to seventy-eight thousand rupees for solar panels on your roof.",
        "speak_hi": "पीएम सूर्य घर: छत पर सोलर पैनल लगाने के लिए अठहत्तर हज़ार रुपये तक की सब्सिडी।",
        "apply": "pmsuryaghar.gov.in, before you install anything",
        "apply_hi": "पैनल लगवाने से पहले {web} पर आवेदन कीजिए।",
        "docs": "Latest electricity bill, Aadhaar, bank account",
        "docs_hi": "बिजली का ताज़ा बिल, आधार कार्ड और बैंक खाता।",
        "note": "For people who own a house with a usable roof and a home electricity connection. Tenants can't apply.",
        "note_hi": "उनके लिए जिनका अपना मकान है, छत है और घरेलू बिजली कनेक्शन है। किराएदार आवेदन नहीं कर सकते।",
        "web": "pmsuryaghar.gov.in", "web_hi": "पीएम सूर्य घर डॉट जीओवी डॉट इन",
        "rule": lambda p: p.get("pucca") is True and _adult(p),
        "why": ["own_house"], "tags": ["aadhaar", "bank", "elec_bill"],
        "names": ["surya ghar", "सूर्य घर", "solar", "सोलर", "muft bijli", "मुफ़्त बिजली", "मुफ्त बिजली"],
    },
    {
        "id": "pmmvy",
        "name": "PM Matru Vandana Yojana", "name_hi": "प्रधानमंत्री मातृ वंदना योजना",
        "benefit": "₹5,000 for your first child; ₹6,000 for a second child if she is a girl",
        "benefit_hi": "पहले बच्चे पर ₹5,000; दूसरा बच्चा बेटी हो तो ₹6,000",
        "speak_en": "Matru Vandana Yojana: five thousand rupees for your first child, and six thousand for a second child if she is a girl.",
        "speak_hi": "मातृ वंदना योजना: पहले बच्चे पर पाँच हज़ार रुपये, और दूसरा बच्चा बेटी हो तो छह हज़ार रुपये।",
        "apply": "Your anganwadi centre or ASHA worker, or pmmvy.wcd.gov.in",
        "apply_hi": "अपने आंगनवाड़ी केंद्र या आशा दीदी से मिलिए, या {web} पर फ़ॉर्म भरिए।",
        "docs": "Aadhaar, mother and child protection (MCP) card, bank account in the mother's name",
        "docs_hi": "आधार कार्ड, जच्चा-बच्चा (एमसीपी) कार्ड और माँ के नाम का बैंक खाता।",
        "note": "Register during the pregnancy. Not for women in a regular government job.",
        "note_hi": "गर्भ के दौरान ही रजिस्ट्रेशन करवा लीजिए। पक्की सरकारी नौकरी वाली महिलाओं के लिए नहीं है।",
        "web": "pmmvy.wcd.gov.in", "web_hi": "पीएमएमवीवाई की वेबसाइट",
        "rule": lambda p: _woman(p) and p.get("maternity") is True and p.get("occupation") != "govt_employee",
        "why": ["maternity"], "tags": ["aadhaar", "bank", "mcp"],
        "names": ["matru vandana", "मातृ वंदना", "pmmvy", "maternity", "मातृत्व"],
    },
    {
        "id": "jsy",
        "name": "Janani Suraksha Yojana", "name_hi": "जननी सुरक्षा योजना",
        "benefit": "Cash when you deliver in a government hospital: ₹1,400 in villages and ₹1,000 in towns in 10 states "
                   "(UP, Bihar, MP, Rajasthan, Jharkhand, Chhattisgarh, Odisha, Uttarakhand, Assam, J&K); "
                   "₹700 and ₹600 for BPL, SC and ST women in other states",
        "benefit_hi": "सरकारी अस्पताल में डिलीवरी पर नकद: 10 राज्यों (यूपी, बिहार, एमपी, राजस्थान, झारखंड, छत्तीसगढ़, ओडिशा, उत्तराखंड, "
                      "असम, जम्मू-कश्मीर) में गाँव में ₹1,400 और शहर में ₹1,000; बाकी राज्यों में BPL, SC, ST महिलाओं को ₹700 और ₹600",
        "speak_en": "Janani Suraksha Yojana: cash of up to fourteen hundred rupees when you deliver in a government hospital.",
        "speak_hi": "जननी सुरक्षा योजना: सरकारी अस्पताल में डिलीवरी करवाने पर चौदह सौ रुपये तक नकद।",
        "apply": "Your ASHA worker or the government hospital where you deliver",
        "apply_hi": "अपनी आशा दीदी को बताइए, या जिस सरकारी अस्पताल में डिलीवरी हो वहीं फ़ॉर्म भरिए।",
        "docs": "Aadhaar, mother and child protection (MCP) card, bank account",
        "docs_hi": "आधार कार्ड, जच्चा-बच्चा (एमसीपी) कार्ड और बैंक खाता।",
        "note": "The money is for delivering in a government hospital or an approved private one.",
        "note_hi": "यह पैसा सरकारी या मान्यता वाले निजी अस्पताल में डिलीवरी करवाने पर मिलता है।",
        "rule": lambda p: _woman(p) and p.get("maternity") is True
        and (p.get("state") in LOW_PERFORMING or p.get("bpl") is True or p.get("category") in ("sc", "st")),
        "why": ["maternity"], "tags": ["aadhaar", "bank", "mcp"],
        "names": ["janani", "जननी", "jsy", "delivery"],
    },
    {
        "id": "ujjwala",
        "name": "PM Ujjwala Yojana", "name_hi": "प्रधानमंत्री उज्ज्वला योजना",
        "benefit": "A free LPG gas connection with no deposit, and a ₹300 subsidy on a limited number of refills each year",
        "benefit_hi": "बिना जमा राशि का मुफ़्त गैस कनेक्शन, और साल में गिने-चुने सिलेंडरों पर ₹300 की सब्सिडी",
        "speak_en": "Ujjwala Yojana: a free gas connection, and three hundred rupees off some refills each year.",
        "speak_hi": "उज्ज्वला योजना: मुफ़्त गैस कनेक्शन, और साल के कुछ सिलेंडरों पर तीन सौ रुपये की छूट।",
        "apply": "Your nearest LPG distributor, or pmuy.gov.in",
        "apply_hi": "नज़दीकी गैस एजेंसी पर जाइए, या {web} पर आवेदन कीजिए।",
        "docs": "Aadhaar, ration card, bank account",
        "docs_hi": "आधार कार्ड, राशन कार्ड और बैंक खाता।",
        "note": "For an adult woman of a poor household that has no gas connection. How many refills get the subsidy "
                "changes from year to year: ask the distributor.",
        "note_hi": "गरीब परिवार की बालिग महिला के नाम पर, जिनके घर में गैस कनेक्शन नहीं है। सब्सिडी कितने सिलेंडरों पर मिलेगी, "
                   "यह हर साल बदलता है: गैस एजेंसी से पूछ लीजिए।",
        "web": "pmuy.gov.in", "web_hi": "पीएमयूवाई डॉट जीओवी डॉट इन",
        "rule": lambda p: _woman(p) and _adult(p) and p.get("lpg") is False
        and (p.get("bpl") is True or p.get("category") in ("sc", "st")) and _not_tax(p),
        "why": ["woman", "no_lpg"], "tags": ["aadhaar", "ration", "bank"],
        "names": ["ujjwala", "उज्ज्वला", "gas connection", "गैस कनेक्शन", "lpg", "cylinder", "सिलेंडर"],
    },
    {
        "id": "old_age_pension",
        "name": "Old-age pension (PM Samajik Sahayata Yojana)", "name_hi": "वृद्धावस्था पेंशन (पीएम सामाजिक सहायता योजना)",
        "benefit": "A pension every month. The Centre gives ₹200 (₹500 from age 80) and your state adds its own amount, "
                   "so the total depends on your state",
        "benefit_hi": "हर महीने पेंशन। केंद्र ₹200 देता है (80 साल से ₹500) और राज्य अपनी तरफ़ से जोड़ता है, इसलिए कुल रकम राज्य पर निर्भर है",
        "speak_en": "Old-age pension: a pension every month. The amount depends on your state.",
        "speak_hi": "वृद्धावस्था पेंशन: हर महीने पेंशन मिलती है। रकम आपके राज्य पर निर्भर है।",
        "apply": "Gram panchayat, block office or municipal office, or your nearest CSC",
        "apply_hi": "ग्राम पंचायत, ब्लॉक दफ़्तर या नगर पालिका में, या नज़दीकी सीएससी केंद्र पर आवेदन कीजिए।",
        "docs": "Age proof, BPL ration card, Aadhaar, bank account",
        "docs_hi": "उम्र का प्रमाण, बीपीएल राशन कार्ड, आधार कार्ड और बैंक खाता।",
        "note": "For people aged 60 or more from BPL families. Until October 2026 this was the Indira Gandhi old-age pension.",
        "note_hi": "बीपीएल परिवारों के 60 साल या उससे बड़े लोगों के लिए। अक्टूबर 2026 तक इसका नाम इंदिरा गांधी वृद्धावस्था पेंशन था।",
        "rule": lambda p: _age(p) is not None and _age(p) >= 60 and p.get("bpl") is True,
        "why": ["senior60", "bpl"], "tags": ["age_proof", "ration", "aadhaar", "bank"],
        "names": ["vridhavastha", "वृद्धावस्था", "budhapa pension", "बुढ़ापा पेंशन", "old age", "samajik sahayata", "सामाजिक सहायता"],
    },
    {
        "id": "widow_pension",
        "name": "Widow pension (PM Samajik Sahayata Yojana)", "name_hi": "विधवा पेंशन (पीएम सामाजिक सहायता योजना)",
        "benefit": "A pension every month for widows. The Centre gives ₹300 and your state adds its own amount",
        "benefit_hi": "विधवा महिलाओं को हर महीने पेंशन। केंद्र ₹300 देता है और राज्य अपनी तरफ़ से जोड़ता है",
        "speak_en": "Widow pension: a pension every month. The amount depends on your state.",
        "speak_hi": "विधवा पेंशन: हर महीने पेंशन मिलती है। रकम आपके राज्य पर निर्भर है।",
        "apply": "Gram panchayat, block office or municipal office, or your nearest CSC",
        "apply_hi": "ग्राम पंचायत, ब्लॉक दफ़्तर या नगर पालिका में, या नज़दीकी सीएससी केंद्र पर आवेदन कीजिए।",
        "docs": "Husband's death certificate, BPL ration card, Aadhaar, bank account",
        "docs_hi": "पति का मृत्यु प्रमाण पत्र, बीपीएल राशन कार्ड, आधार कार्ड और बैंक खाता।",
        "note": "For widows aged 40 to 79 from BPL families. Many states also give their own widow pension from 18.",
        "note_hi": "बीपीएल परिवारों की 40 से 79 साल की विधवा महिलाओं के लिए। कई राज्य 18 साल से अपनी विधवा पेंशन भी देते हैं।",
        "rule": lambda p: p.get("widow") is True and _between(p, 40, 79) and p.get("bpl") is True,
        "why": ["widow", "bpl"], "tags": ["death_cert", "ration", "aadhaar", "bank"],
        "names": ["vidhwa pension", "विधवा पेंशन", "widow pension"],
    },
    {
        "id": "udid",
        "name": "UDID card (disability ID)", "name_hi": "यूडीआईडी कार्ड (दिव्यांग पहचान पत्र)",
        "benefit": "A free national disability ID card, accepted for every disability scheme in every state",
        "benefit_hi": "मुफ़्त राष्ट्रीय दिव्यांग पहचान पत्र, जो हर राज्य की हर दिव्यांग योजना में चलता है",
        "speak_en": "The UDID card: a free disability ID that works for every disability scheme.",
        "speak_hi": "यूडीआईडी कार्ड: मुफ़्त दिव्यांग पहचान पत्र, जो हर दिव्यांग योजना में काम आता है।",
        "apply": "swavlambancard.gov.in, or the district hospital",
        "apply_hi": "{web} पर आवेदन कीजिए, या ज़िला अस्पताल में जाइए।",
        "docs": "Aadhaar, photo, disability certificate if you already have one",
        "docs_hi": "आधार कार्ड, फ़ोटो, और दिव्यांगता प्रमाण पत्र अगर पहले से बना है।",
        "note": "Free to make. One card replaces separate certificates for each scheme.",
        "note_hi": "यह मुफ़्त बनता है। एक ही कार्ड हर योजना के अलग-अलग प्रमाण पत्रों की जगह लेता है।",
        "web": "swavlambancard.gov.in", "web_hi": "स्वावलंबन कार्ड डॉट जीओवी डॉट इन",
        "rule": lambda p: p.get("disabled") is True,
        "why": ["disabled"], "tags": ["aadhaar", "photo", "disability_cert"],
        "names": ["udid", "यूडीआईडी", "swavlamban", "स्वावलंबन", "viklang card", "दिव्यांग कार्ड"],
    },
    {
        "id": "vayoshri",
        "name": "Rashtriya Vayoshri Yojana", "name_hi": "राष्ट्रीय वयोश्री योजना",
        "benefit": "Free aids for the elderly, such as a walking stick, hearing aid, spectacles or wheelchair",
        "benefit_hi": "बुज़ुर्गों को मुफ़्त सहायक सामान, जैसे छड़ी, कान की मशीन, चश्मा या व्हीलचेयर",
        "speak_en": "Vayoshri Yojana: free aids for the elderly, like a hearing aid, spectacles or a wheelchair.",
        "speak_hi": "वयोश्री योजना: बुज़ुर्गों को मुफ़्त छड़ी, कान की मशीन, चश्मा या व्हीलचेयर।",
        "apply": "At distribution camps in your district: ask the district social welfare office or a CSC when the next one is",
        "apply_hi": "यह सामान ज़िले में लगने वाले कैंप में मिलता है। अगला कैंप कब है, यह ज़िला समाज कल्याण दफ़्तर या सीएससी केंद्र से पूछिए।",
        "docs": "Aadhaar, BPL ration card or old-age pension proof",
        "docs_hi": "आधार कार्ड, और बीपीएल राशन कार्ड या वृद्धावस्था पेंशन का प्रमाण।",
        "note": "For people aged 60 or more from BPL families.",
        "note_hi": "बीपीएल परिवारों के 60 साल या उससे बड़े लोगों के लिए।",
        "rule": lambda p: _age(p) is not None and _age(p) >= 60 and p.get("bpl") is True,
        "why": ["senior60", "bpl"], "tags": ["aadhaar", "ration"],
        "names": ["vayoshri", "वयोश्री", "hearing aid", "कान की मशीन", "wheelchair", "व्हीलचेयर"],
    },
    {
        "id": "free_ration",
        "name": "Free ration (PM Garib Kalyan Anna Yojana)", "name_hi": "मुफ़्त राशन (पीएम गरीब कल्याण अन्न योजना)",
        "benefit": "5 kg of free grain per person every month on your ration card, approved until December 2028. "
                   "The card works at any ration shop in India",
        "benefit_hi": "राशन कार्ड पर हर सदस्य को हर महीने 5 किलो मुफ़्त अनाज, दिसंबर 2028 तक मंज़ूर। कार्ड देश की किसी भी राशन दुकान पर चलता है",
        "speak_en": "Free ration: five kilos of free grain per person every month on your ration card, until December twenty twenty-eight.",
        "speak_hi": "मुफ़्त राशन: राशन कार्ड पर हर सदस्य को हर महीने पाँच किलो मुफ़्त अनाज, दिसंबर दो हज़ार अट्ठाईस तक।",
        "apply": "Your ration shop. For a new card or to add a name: the state food department or a CSC",
        "apply_hi": "अपनी राशन दुकान से लीजिए। नया कार्ड बनवाने या नाम जोड़ने के लिए राज्य के खाद्य विभाग या सीएससी केंद्र जाइए।",
        "docs": "Ration card, Aadhaar of each family member",
        "docs_hi": "राशन कार्ड और परिवार के हर सदस्य का आधार कार्ड।",
        "note": "If you work away from home, you can take your share at a ration shop there (One Nation One Ration Card).",
        "note_hi": "अगर आप घर से दूर काम करते हैं, तो वहाँ की राशन दुकान से भी अपना हिस्सा ले सकते हैं (वन नेशन वन राशन कार्ड)।",
        "rule": lambda p: p.get("bpl") is True,
        "why": ["bpl"], "tags": ["ration", "aadhaar"],
        "names": ["ration", "राशन", "anaj", "अनाज", "garib kalyan", "गरीब कल्याण"],
    },
    {
        "id": "pdmc",
        "name": "Per Drop More Crop (drip and sprinkler)", "name_hi": "पर ड्रॉप मोर क्रॉप (ड्रिप और फव्वारा सिंचाई)",
        "benefit": "Subsidy on drip or sprinkler irrigation: 55% of the cost for small and marginal farmers, 45% for others",
        "benefit_hi": "ड्रिप या फव्वारा सिंचाई लगाने पर सब्सिडी: छोटे और सीमांत किसानों को लागत का 55%, बाकी किसानों को 45%",
        "speak_en": "Per Drop More Crop: the government pays about half the cost of drip or sprinkler irrigation.",
        "speak_hi": "पर ड्रॉप मोर क्रॉप: ड्रिप या फव्वारा सिंचाई की लगभग आधी लागत सरकार देती है।",
        "apply": "Your district agriculture or horticulture office",
        "apply_hi": "ज़िले के कृषि या उद्यान विभाग के दफ़्तर में आवेदन कीजिए।",
        "docs": "Aadhaar, land records, bank account",
        "docs_hi": "आधार कार्ड, ज़मीन के कागज़ और बैंक खाता।",
        "note": "Small and marginal farmers are those with up to 2 hectares (about 5 acres).",
        "note_hi": "छोटे और सीमांत किसान यानी जिनके पास 2 हेक्टेयर (लगभग 5 एकड़) तक ज़मीन है।",
        "rule": lambda p: p.get("occupation") == "farmer" and (p.get("land_ha") or 0) > 0,
        "why": ["farmer", "land"], "tags": ["aadhaar", "land", "bank"],
        "names": ["per drop", "drip", "ड्रिप", "sprinkler", "फव्वारा", "sinchai", "सिंचाई"],
    },
    {
        "id": "pm_vidyalaxmi",
        "name": "PM Vidyalaxmi (education loan)", "name_hi": "पीएम विद्यालक्ष्मी (पढ़ाई का लोन)",
        "benefit": "Education loan with no collateral and no guarantor for students admitted to top-ranked colleges, "
                   "with interest help for families earning up to ₹8 lakh a year",
        "benefit_hi": "अच्छी रैंक वाले कॉलेज में दाखिला मिलने पर बिना गारंटी और बिना गारंटर का पढ़ाई का लोन; ₹8 लाख साल तक कमाने वाले परिवारों को ब्याज में मदद",
        "speak_en": "PM Vidyalaxmi: an education loan with no collateral for students in top-ranked colleges.",
        "speak_hi": "पीएम विद्यालक्ष्मी: अच्छी रैंक वाले कॉलेज के छात्रों को बिना गारंटी का पढ़ाई का लोन।",
        "apply": "The PM Vidyalaxmi portal (pmvidyalaxmi.co.in), then the bank you choose there",
        "apply_hi": "पीएम विद्यालक्ष्मी पोर्टल पर आवेदन कीजिए, फिर वहाँ चुने हुए बैंक से लोन मिलेगा।",
        "docs": "Admission letter, fee details, Aadhaar, family income certificate",
        "docs_hi": "दाखिले का पत्र, फ़ीस का ब्योरा, आधार कार्ड और परिवार का आय प्रमाण पत्र।",
        "note": "Only for colleges on the scheme's list of top-ranked institutions, and not for management-quota seats.",
        "note_hi": "सिर्फ़ योजना की सूची वाले अच्छी रैंक के कॉलेजों के लिए, और मैनेजमेंट कोटे की सीट पर नहीं।",
        "rule": lambda p: _student(p) and p.get("study") == "college",
        "why": ["college"], "tags": ["aadhaar", "admission", "income_cert"],
        "names": ["vidyalaxmi", "vidya lakshmi", "विद्यालक्ष्मी", "education loan", "पढ़ाई का लोन", "शिक्षा लोन"],
    },
]

# Shown as "check this": the benefit is real, but who gets it depends on a list, an exam or details we don't ask about.
CENTRAL_CHECK = [
    {
        "id": "pmay_g",
        "name": "PM Awas Yojana (Gramin)", "name_hi": "प्रधानमंत्री आवास योजना (ग्रामीण)",
        "benefit": "₹1.20 lakh to build a pucca house (₹1.30 lakh in hilly and difficult areas)",
        "benefit_hi": "पक्का मकान बनाने के लिए ₹1.20 लाख (पहाड़ी और दुर्गम इलाकों में ₹1.30 लाख)",
        "speak_en": "Also check PM Awas Yojana: one lakh twenty thousand rupees to build a pucca house. Ask your panchayat whether your name is on the list.",
        "speak_hi": "पीएम आवास योजना भी देखिए: पक्का मकान बनाने के लिए एक लाख बीस हज़ार रुपये। पंचायत में पूछिए कि आपका नाम सूची में है या नहीं।",
        "apply": "Your gram panchayat: names come from the Awaas+ survey list",
        "apply_hi": "अपनी ग्राम पंचायत में पूछिए: नाम आवास प्लस सर्वे की सूची से आते हैं।",
        "docs": "Aadhaar, bank account, job card if you have one",
        "docs_hi": "आधार कार्ड, बैंक खाता, और जॉब कार्ड अगर है।",
        "note": "For village families with no pucca house. You can't apply online yourself; the panchayat's survey list decides.",
        "note_hi": "गाँव के उन परिवारों के लिए जिनके पास पक्का मकान नहीं है। खुद ऑनलाइन आवेदन नहीं होता; पंचायत की सर्वे सूची से तय होता है।",
        "rule": lambda p: p.get("rural") is True and p.get("pucca") is False and _not_tax(p),
        "why": ["rural", "no_pucca"], "tags": ["aadhaar", "bank"],
        "names": ["awas", "आवास", "pm awas", "makaan", "मकान", "ghar banane", "घर बनाने"],
    },
    {
        "id": "pmay_u",
        "name": "PM Awas Yojana (Urban) 2.0", "name_hi": "प्रधानमंत्री आवास योजना (शहरी) 2.0",
        "benefit": "Help to build or buy your first pucca house in a town or city, including an interest subsidy of up to "
                   "₹1.80 lakh on a home loan",
        "benefit_hi": "शहर या कस्बे में पहला पक्का मकान बनाने या खरीदने में मदद, जिसमें होम लोन के ब्याज पर ₹1.80 लाख तक की सब्सिडी शामिल है",
        "speak_en": "Also check PM Awas Yojana Urban: help to build or buy your first pucca house in a town.",
        "speak_hi": "पीएम आवास योजना शहरी भी देखिए: शहर में पहला पक्का मकान बनाने या खरीदने में मदद।",
        "apply": "Your municipal office, or pmaymis.gov.in",
        "apply_hi": "अपनी नगर पालिका या नगर निगम के दफ़्तर में पूछिए, या {web} पर देखिए।",
        "docs": "Aadhaar, income proof, bank account, a declaration that the family owns no pucca house",
        "docs_hi": "आधार कार्ड, आय का प्रमाण, बैंक खाता, और यह घोषणा कि परिवार के पास कोई पक्का मकान नहीं है।",
        "note": "For town families earning up to about ₹9 lakh a year with no pucca house anywhere in India. Amounts and "
                "application dates differ by type of help: confirm at the municipal office.",
        "note_hi": "शहर के उन परिवारों के लिए जिनकी कमाई लगभग ₹9 लाख साल तक है और देश में कहीं पक्का मकान नहीं है। रकम और "
                   "आवेदन की तारीखें मदद के प्रकार पर निर्भर हैं: नगर पालिका में पक्का कर लीजिए।",
        "web": "pmaymis.gov.in", "web_hi": "पीएमएवाई एमआईएस डॉट जीओवी डॉट इन",
        "rule": lambda p: p.get("rural") is False and p.get("pucca") is False
        and (p.get("income_month") is None or p["income_month"] * 12 <= 900000),
        "why": ["no_pucca"], "tags": ["aadhaar", "income_cert", "bank"],
        "names": ["awas shehri", "आवास शहरी", "urban awas", "home loan subsidy", "होम लोन"],
    },
    {
        "id": "disability_pension",
        "name": "Disability pension (PM Samajik Sahayata Yojana)", "name_hi": "दिव्यांग पेंशन (पीएम सामाजिक सहायता योजना)",
        "benefit": "A pension every month for people with a severe disability. The Centre gives ₹300 and your state adds its own amount",
        "benefit_hi": "गंभीर दिव्यांगता वाले लोगों को हर महीने पेंशन। केंद्र ₹300 देता है और राज्य अपनी तरफ़ से जोड़ता है",
        "speak_en": "Also check the disability pension: a pension every month. The amount depends on your state.",
        "speak_hi": "दिव्यांग पेंशन भी देखिए: हर महीने पेंशन मिलती है। रकम आपके राज्य पर निर्भर है।",
        "apply": "Gram panchayat, block office or municipal office, or your nearest CSC",
        "apply_hi": "ग्राम पंचायत, ब्लॉक दफ़्तर या नगर पालिका में, या नज़दीकी सीएससी केंद्र पर आवेदन कीजिए।",
        "docs": "Disability certificate or UDID card, BPL ration card, Aadhaar, bank account",
        "docs_hi": "दिव्यांगता प्रमाण पत्र या यूडीआईडी कार्ड, बीपीएल राशन कार्ड, आधार कार्ड और बैंक खाता।",
        "note": "The central pension is for ages 18 to 79 with 80% disability, from BPL families. Many states have easier rules.",
        "note_hi": "केंद्र की पेंशन बीपीएल परिवारों के 18 से 79 साल के उन लोगों के लिए है जिनकी दिव्यांगता 80% है। कई राज्यों के नियम इससे आसान हैं।",
        "rule": lambda p: p.get("disabled") is True and _between(p, 18, 79),
        "why": ["disabled"], "tags": ["disability_cert", "ration", "aadhaar", "bank"],
        "names": ["divyang pension", "दिव्यांग पेंशन", "viklang pension", "विकलांग पेंशन", "disability pension"],
    },
    {
        "id": "adip",
        "name": "ADIP (free aids and appliances)", "name_hi": "एडिप योजना (मुफ़्त सहायक उपकरण)",
        "benefit": "Free or subsidised aids for people with disabilities, such as a wheelchair, tricycle, hearing aid or artificial limb",
        "benefit_hi": "दिव्यांग लोगों को मुफ़्त या कम दाम पर सहायक उपकरण, जैसे व्हीलचेयर, ट्राइसाइकिल, कान की मशीन या कृत्रिम अंग",
        "speak_en": "Also check the ADIP scheme: free or low-cost aids like a wheelchair or hearing aid.",
        "speak_hi": "एडिप योजना भी देखिए: व्हीलचेयर या कान की मशीन जैसे उपकरण मुफ़्त या कम दाम पर।",
        "apply": "The district disability rehabilitation centre or social welfare office, or an ALIMCO camp",
        "apply_hi": "ज़िला दिव्यांग पुनर्वास केंद्र या समाज कल्याण दफ़्तर में पूछिए, या एलिम्को के कैंप में जाइए।",
        "docs": "Disability certificate or UDID card, income certificate, Aadhaar, photo",
        "docs_hi": "दिव्यांगता प्रमाण पत्र या यूडीआईडी कार्ड, आय प्रमाण पत्र, आधार कार्ड और फ़ोटो।",
        "note": "Free for lower-income families; the income limit is checked at the centre.",
        "note_hi": "कम आय वाले परिवारों के लिए मुफ़्त है; आय की सीमा केंद्र पर जाँची जाती है।",
        "rule": lambda p: p.get("disabled") is True,
        "why": ["disabled"], "tags": ["disability_cert", "income_cert", "aadhaar", "photo"],
        "names": ["adip", "एडिप", "tricycle", "ट्राइसाइकिल", "artificial limb", "कृत्रिम अंग"],
    },
    {
        "id": "csss",
        "name": "Central Sector Scholarship (PM-USP)", "name_hi": "केंद्रीय क्षेत्र छात्रवृत्ति (पीएम-यूएसपी)",
        "benefit": "₹12,000 a year in college (₹20,000 a year in post-graduation) for students who scored in the top 20% "
                   "of their Class 12 board",
        "benefit_hi": "बारहवीं बोर्ड में ऊपर के 20% में आने वाले छात्रों को कॉलेज में ₹12,000 साल (पोस्ट-ग्रेजुएशन में ₹20,000 साल)",
        "speak_en": "Also check the Central Sector Scholarship: twelve thousand rupees a year in college if you were in the top twenty percent of your Class twelve board.",
        "speak_hi": "केंद्रीय क्षेत्र छात्रवृत्ति भी देखिए: बारहवीं बोर्ड में ऊपर के बीस प्रतिशत में आए हों तो कॉलेज में बारह हज़ार रुपये साल।",
        "apply": "National Scholarship Portal: scholarships.gov.in",
        "apply_hi": "नेशनल स्कॉलरशिप पोर्टल {web} पर आवेदन कीजिए।",
        "docs": "Class 12 marksheet, family income certificate, Aadhaar, bank account",
        "docs_hi": "बारहवीं की मार्कशीट, परिवार का आय प्रमाण पत्र, आधार कार्ड और बैंक खाता।",
        "note": "Family income must be ₹4.5 lakh a year or less, and you must be in a regular college course.",
        "note_hi": "परिवार की कमाई ₹4.5 लाख साल या कम होनी चाहिए, और आप कॉलेज के नियमित कोर्स में हों।",
        "web": "scholarships.gov.in", "web_hi": "स्कॉलरशिप्स डॉट जीओवी डॉट इन",
        "rule": lambda p: _student(p) and p.get("study") == "college",
        "why": ["college"], "tags": ["marksheet", "income_cert", "aadhaar", "bank"],
        "names": ["central sector", "pm usp", "csss", "केंद्रीय क्षेत्र"],
    },
    {
        "id": "pms",
        "name": "Post-matric scholarship (SC / ST / OBC)", "name_hi": "पोस्ट-मैट्रिक छात्रवृत्ति (SC / ST / OBC)",
        "benefit": "Fees and a monthly allowance for SC, ST and OBC students studying after Class 10",
        "benefit_hi": "दसवीं के बाद पढ़ रहे SC, ST और OBC छात्रों को फ़ीस और हर महीने भत्ता",
        "speak_en": "Also check the post-matric scholarship: fees and an allowance for SC, ST and OBC students after Class ten.",
        "speak_hi": "पोस्ट-मैट्रिक छात्रवृत्ति भी देखिए: दसवीं के बाद पढ़ रहे एससी, एसटी और ओबीसी छात्रों को फ़ीस और भत्ता।",
        "apply": "National Scholarship Portal (scholarships.gov.in) or your state's scholarship portal",
        "apply_hi": "नेशनल स्कॉलरशिप पोर्टल {web} पर, या अपने राज्य के छात्रवृत्ति पोर्टल पर आवेदन कीजिए।",
        "docs": "Caste certificate, family income certificate, last marksheet, Aadhaar, bank account",
        "docs_hi": "जाति प्रमाण पत्र, परिवार का आय प्रमाण पत्र, पिछली मार्कशीट, आधार कार्ड और बैंक खाता।",
        "note": "Family income must be about ₹2.5 lakh a year or less; the exact limit and the amount depend on the category and course.",
        "note_hi": "परिवार की कमाई लगभग ₹2.5 लाख साल या कम होनी चाहिए; पक्की सीमा और रकम वर्ग और कोर्स पर निर्भर है।",
        "web": "scholarships.gov.in", "web_hi": "स्कॉलरशिप्स डॉट जीओवी डॉट इन",
        "rule": lambda p: _student(p) and p.get("category") in ("sc", "st", "obc"),
        "why": ["student", "category"], "tags": ["caste_cert", "income_cert", "marksheet", "aadhaar", "bank"],
        "names": ["post matric", "पोस्ट मैट्रिक", "yasasvi", "यशस्वी", "scholarship", "छात्रवृत्ति", "वजीफ़ा", "वजीफा"],
    },
    {
        "id": "nmms",
        "name": "National Means-cum-Merit Scholarship", "name_hi": "राष्ट्रीय साधन-सह-योग्यता छात्रवृत्ति (एनएमएमएस)",
        "benefit": "₹12,000 a year from Class 9 to 12 for students who pass the NMMS exam in Class 8",
        "benefit_hi": "आठवीं में एनएमएमएस परीक्षा पास करने वाले छात्रों को नौवीं से बारहवीं तक ₹12,000 साल",
        "speak_en": "Also check the NMMS scholarship: twelve thousand rupees a year from Class nine to twelve for students who pass its exam in Class eight.",
        "speak_hi": "एनएमएमएस छात्रवृत्ति भी देखिए: आठवीं में इसकी परीक्षा पास करने पर नौवीं से बारहवीं तक बारह हज़ार रुपये साल।",
        "apply": "Through your school in Class 8, then on the National Scholarship Portal (scholarships.gov.in)",
        "apply_hi": "आठवीं में अपने स्कूल के ज़रिए परीक्षा का फ़ॉर्म भरिए, फिर {web} पर आवेदन कीजिए।",
        "docs": "Class 7 marksheet, family income certificate, Aadhaar, bank account",
        "docs_hi": "सातवीं की मार्कशीट, परिवार का आय प्रमाण पत्र, आधार कार्ड और बैंक खाता।",
        "note": "For students of government and aided schools whose parents earn ₹3.5 lakh a year or less.",
        "note_hi": "सरकारी और सहायता प्राप्त स्कूलों के उन छात्रों के लिए जिनके माता-पिता की कमाई ₹3.5 लाख साल या कम है।",
        "web": "scholarships.gov.in", "web_hi": "स्कॉलरशिप्स डॉट जीओवी डॉट इन",
        "rule": lambda p: _student(p) and p.get("study") == "school",
        "why": ["student"], "tags": ["marksheet", "income_cert", "aadhaar", "bank"],
        "names": ["nmms", "एनएमएमएस", "means cum merit"],
    },
    {
        "id": "pm_internship",
        "name": "PM Internship Scheme", "name_hi": "पीएम इंटर्नशिप योजना",
        "benefit": "A 12-month internship in a large company with ₹9,000 a month and a one-time ₹6,000",
        "benefit_hi": "बड़ी कंपनी में 12 महीने की इंटर्नशिप, ₹9,000 महीना और एक बार ₹6,000",
        "speak_en": "Also check the PM Internship Scheme: a one-year internship in a large company with nine thousand rupees a month.",
        "speak_hi": "पीएम इंटर्नशिप योजना भी देखिए: बड़ी कंपनी में एक साल की इंटर्नशिप, नौ हज़ार रुपये महीने के साथ।",
        "apply": "pminternship.mca.gov.in, when a round is open",
        "apply_hi": "जब आवेदन खुले हों, तब {web} पर फ़ॉर्म भरिए।",
        "docs": "Aadhaar, education certificates, bank account",
        "docs_hi": "आधार कार्ड, पढ़ाई के प्रमाण पत्र और बैंक खाता।",
        "note": "For ages 18 to 25 who are not in a full-time job or full-time course. The stipend was raised and the age "
                "range widened in 2026; rounds open and close, so check the portal.",
        "note_hi": "18 से 25 साल के उन युवाओं के लिए जो पूरे समय की नौकरी या पढ़ाई में नहीं हैं। 2026 में रकम बढ़ी और उम्र की सीमा चौड़ी हुई; "
                   "आवेदन कुछ समय के लिए ही खुलते हैं, इसलिए पोर्टल देखते रहिए।",
        "web": "pminternship.mca.gov.in", "web_hi": "पीएम इंटर्नशिप की वेबसाइट",
        "rule": lambda p: p.get("occupation") == "unemployed" and _between(p, 18, 25),
        "why": ["age"], "tags": ["aadhaar", "marksheet", "bank"],
        "names": ["internship", "इंटर्नशिप"],
    },
    {
        "id": "ddu_gky",
        "name": "DDU-GKY (free job training)", "name_hi": "दीनदयाल उपाध्याय ग्रामीण कौशल्य योजना",
        "benefit": "Free job training for village youth, with help to get placed in a job afterwards",
        "benefit_hi": "गाँव के युवाओं को मुफ़्त रोज़गार ट्रेनिंग, और उसके बाद नौकरी दिलाने में मदद",
        "speak_en": "Also check DDU-GKY: free job training for village youth, with help to find a job.",
        "speak_hi": "ग्रामीण कौशल्य योजना भी देखिए: गाँव के युवाओं को मुफ़्त ट्रेनिंग और नौकरी दिलाने में मदद।",
        "apply": "The block office or your State Rural Livelihood Mission",
        "apply_hi": "ब्लॉक दफ़्तर में या राज्य ग्रामीण आजीविका मिशन के दफ़्तर में पूछिए।",
        "docs": "Aadhaar, age proof, ration card or other proof of a poor rural household",
        "docs_hi": "आधार कार्ड, उम्र का प्रमाण, और राशन कार्ड या गरीब ग्रामीण परिवार का कोई और प्रमाण।",
        "note": "For rural youth aged 15 to 35 from poor families.",
        "note_hi": "गरीब परिवारों के 15 से 35 साल के ग्रामीण युवाओं के लिए।",
        "rule": lambda p: p.get("rural") is True and p.get("occupation") == "unemployed" and _between(p, 15, 35),
        "why": ["rural", "age"], "tags": ["aadhaar", "age_proof", "ration"],
        "names": ["ddu gky", "kaushal", "कौशल", "training", "ट्रेनिंग"],
    },
    {
        "id": "shg",
        "name": "Self-help groups (Lakhpati Didi)", "name_hi": "स्वयं सहायता समूह (लखपति दीदी)",
        "benefit": "Join a women's self-help group: group savings, bank loans with interest help, and training to start earning",
        "benefit_hi": "महिलाओं के स्वयं सहायता समूह से जुड़िए: समूह की बचत, ब्याज में मदद वाला बैंक लोन, और कमाई शुरू करने की ट्रेनिंग",
        "speak_en": "Also think about joining a women's self-help group: savings, bank loans with interest help, and training.",
        "speak_hi": "महिलाओं के स्वयं सहायता समूह से जुड़ने के बारे में भी सोचिए: बचत, ब्याज में मदद वाला लोन, और ट्रेनिंग।",
        "apply": "A self-help group in your village, the block office, or your State Rural Livelihood Mission",
        "apply_hi": "अपने गाँव के किसी समूह से जुड़िए, या ब्लॉक दफ़्तर या राज्य ग्रामीण आजीविका मिशन में पूछिए।",
        "docs": "Aadhaar, bank account",
        "docs_hi": "आधार कार्ड और बैंक खाता।",
        "note": "Loans come through the group, not directly to one person. Loan size and interest help depend on the group and the bank.",
        "note_hi": "लोन समूह के ज़रिए मिलता है, सीधे एक व्यक्ति को नहीं। लोन की रकम और ब्याज में मदद समूह और बैंक पर निर्भर है।",
        "rule": lambda p: p.get("rural") is True and _woman(p) and _adult(p) and p.get("occupation") != "govt_employee",
        "why": ["woman", "rural"], "tags": ["aadhaar", "bank"],
        "names": ["lakhpati didi", "लखपति दीदी", "self help", "स्वयं सहायता", "samuh", "समूह", "shg"],
    },
    {
        "id": "bocw",
        "name": "Construction workers' welfare board", "name_hi": "निर्माण मज़दूर कल्याण बोर्ड",
        "benefit": "If you work on building sites: register with your state's construction workers' board for help with "
                   "children's education, maternity, medical costs and a pension",
        "benefit_hi": "अगर आप मकान या सड़क बनाने का काम करते हैं: राज्य के निर्माण मज़दूर बोर्ड में रजिस्ट्रेशन करवाइए; बच्चों की पढ़ाई, "
                      "मातृत्व, इलाज और पेंशन में मदद मिलती है",
        "speak_en": "If you work on building sites, also register with your state's construction workers' board for education, medical and pension help.",
        "speak_hi": "अगर आप निर्माण का काम करते हैं, तो राज्य के निर्माण मज़दूर बोर्ड में भी रजिस्ट्रेशन करवाइए; पढ़ाई, इलाज और पेंशन में मदद मिलती है।",
        "apply": "The labour department office in your district, or a CSC",
        "apply_hi": "ज़िले के श्रम विभाग के दफ़्तर में या सीएससी केंद्र पर रजिस्ट्रेशन करवाइए।",
        "docs": "Aadhaar, proof of 90 days of construction work in the last year, photo, bank account",
        "docs_hi": "आधार कार्ड, पिछले साल में 90 दिन निर्माण के काम का प्रमाण, फ़ोटो और बैंक खाता।",
        "note": "For construction workers aged 18 to 60. What you get differs from state to state.",
        "note_hi": "18 से 60 साल के निर्माण मज़दूरों के लिए। क्या-क्या मिलेगा, यह हर राज्य में अलग है।",
        "rule": lambda p: p.get("occupation") == "labourer" and _between(p, 18, 60),
        "why": ["age"], "tags": ["aadhaar", "work_proof", "photo", "bank"],
        "names": ["bocw", "nirman", "निर्माण", "construction", "labour card", "लेबर कार्ड", "श्रमिक कार्ड"],
    },
]

STATE = []
STATE_CHECK = []


# ---------------------------------------------------------------- documents, for the one combined list of papers
# tag: (English, Hindi). Order = the order they are listed in.
DOCS = {
    "aadhaar": ("Aadhaar card", "आधार कार्ड"),
    "bank": ("bank passbook", "बैंक पासबुक"),
    "ration": ("ration card", "राशन कार्ड"),
    "photo": ("passport-size photos", "पासपोर्ट साइज़ फ़ोटो"),
    "mobile": ("mobile number linked to Aadhaar", "आधार से जुड़ा मोबाइल नंबर"),
    "land": ("land records", "ज़मीन के कागज़"),
    "income_cert": ("income certificate", "आय प्रमाण पत्र"),
    "caste_cert": ("caste certificate", "जाति प्रमाण पत्र"),
    "residence": ("residence proof", "निवास प्रमाण पत्र"),
    "age_proof": ("age proof", "उम्र का प्रमाण"),
    "pan": ("PAN card", "पैन कार्ड"),
    "marksheet": ("marksheets", "मार्कशीट"),
    "admission": ("admission letter", "दाखिले का पत्र"),
    "birth_cert": ("child's birth certificate", "बच्चे का जन्म प्रमाण पत्र"),
    "mcp": ("mother and child (MCP) card", "जच्चा-बच्चा कार्ड"),
    "death_cert": ("husband's death certificate", "पति का मृत्यु प्रमाण पत्र"),
    "disability_cert": ("disability certificate", "दिव्यांगता प्रमाण पत्र"),
    "jobcard": ("job card", "जॉब कार्ड"),
    "elec_bill": ("electricity bill", "बिजली का बिल"),
    "work_proof": ("proof of work", "काम का प्रमाण"),
    "business": ("business proof", "धंधे का प्रमाण"),
}

# the 30 schemes written before this file: documents and fixed yearly cash
OLD_TAGS = {
    "pm_kisan": ["aadhaar", "land", "bank"], "pm_kmy": ["aadhaar", "bank", "land"],
    "pm_svanidhi": ["aadhaar", "mobile"], "pm_vishwakarma": ["aadhaar", "mobile", "bank", "ration"],
    "mudra": ["aadhaar", "pan", "business", "bank"], "pm_sym": ["aadhaar", "bank", "mobile"],
    "eshram": ["aadhaar", "mobile", "bank"], "apy": ["aadhaar", "bank", "mobile"], "pmjjby": ["bank", "aadhaar"],
    "pmsby": ["bank", "aadhaar"], "sukanya": ["birth_cert", "aadhaar", "pan"], "vay_vandana": ["aadhaar"],
    "pmjay": ["aadhaar", "ration"], "pmegp": ["aadhaar"], "kcc": ["aadhaar", "land", "photo", "bank"],
    "pmfby": ["aadhaar", "land", "bank"], "udyam": ["aadhaar", "pan", "bank"], "startup_india": ["pan"],
    "up_cm_yuva": ["aadhaar", "residence", "bank"], "up_kanya_sumangala": ["birth_cert", "aadhaar", "income_cert", "bank"],
    "br_mahila_rojgar": ["aadhaar", "bank"], "br_vridhjan": ["aadhaar", "age_proof", "bank"],
    "mh_ladki_bahin": ["aadhaar", "residence", "income_cert", "bank"], "mh_namo_shetkari": ["aadhaar", "land", "bank"],
    "wb_annapurna": ["aadhaar", "bank"], "tn_kmut": ["ration", "aadhaar", "bank"],
    "ka_gruha_lakshmi": ["ration", "aadhaar", "bank"], "mp_ladli_behna": ["aadhaar", "bank"], "rj_maa": ["aadhaar"],
    "ka_yuva_nidhi": ["marksheet", "aadhaar", "residence", "bank"],
}
OLD_CASH = {"pm_kisan": 6000, "mh_namo_shetkari": 6000, "mh_ladki_bahin": 18000, "ka_gruha_lakshmi": 24000,
            "tn_kmut": 12000, "wb_annapurna": 36000, "br_vridhjan": 13200}


def all_entries():
    return CENTRAL + CENTRAL_CHECK + STATE + STATE_CHECK


for _s in all_entries():
    _s["catalog"] = True

WHY_KEYS = {s["id"]: s.get("why", []) for s in all_entries()}


def tags(sid):
    for s in all_entries():
        if s["id"] == sid:
            return s.get("tags", [])
    return OLD_TAGS.get(sid, [])


def cash(sid):
    for s in all_entries():
        if s["id"] == sid:
            return s.get("cash", 0)
    return OLD_CASH.get(sid, 0)


def kb_entries():
    """Facts for the follow-up chat, built from the cards above (same shape as kb.KB)."""
    out = {}
    for s in all_entries():
        out[s["id"]] = {
            "web": s.get("web"), "web_hi": s.get("web_hi"), "helpline": s.get("helpline"),
            "hi": {"explain": s["speak_hi"] + " " + s["note_hi"], "apply": s["apply_hi"], "docs": s["docs_hi"],
                   "who": s["note_hi"], "money": s["benefit_hi"] + "।"},
            "en": {"explain": s["speak_en"] + " " + s["note"], "apply": "Where to apply: " + s["apply"] + ".",
                   "docs": s["docs"] + ".", "who": s["note"], "money": s["benefit"] + "."},
        }
        out[s["id"]] = {k: v for k, v in out[s["id"]].items() if v is not None}
        out[s["id"]].setdefault("web", None)
    return out


def scheme_names():
    return [(s["id"], s.get("names", [])) for s in all_entries() if s.get("names")]
