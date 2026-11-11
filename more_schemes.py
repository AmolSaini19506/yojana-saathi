"""
Business / farming central schemes and state flagship schemes (added 9 Nov 2026).

Every amount here was checked on 9 Nov 2026 against current reports (see README "Sources"). Where sources
disagreed on an amount (Rajasthan's farmer top-up, UP's and Rajasthan's old-age pension) the scheme is left out
rather than guessed. Not added because they are not open right now: PMFME (extension ended 30 Sep 2026) and
Stand-Up India (ended March 2025; a revamp was announced in March 2026 but has not launched).

Same shape as schemes.SCHEMES. `state` = the state code the scheme belongs to (see states.py).
"""

UNORG = {"street_vendor", "labourer", "artisan", "other_self_employed"}
OWN_BUSINESS = {"shopkeeper", "street_vendor", "artisan", "other_self_employed"}


def _age(p):
    return p.get("age")


def _between(p, lo, hi):
    a = _age(p)
    return a is not None and lo <= a <= hi


def _woman(p):
    return p.get("gender") == "f"


def _income_upto(p, per_year):
    inc = p.get("income_month")
    return inc is not None and inc * 12 <= per_year


def _not_tax(p):
    return p.get("itax") is not True


def _pm_kisan(p):
    return p.get("occupation") == "farmer" and (p.get("land_ha") or 0) > 0 and _not_tax(p)


CENTRAL = [
    {
        "id": "pmegp",
        "name": "PMEGP",
        "name_hi": "प्रधानमंत्री रोज़गार सृजन कार्यक्रम",
        "benefit": "Bank loan to start a new manufacturing or service unit, with 15–35% of the project cost paid as a "
                   "government subsidy (projects up to ₹50 lakh manufacturing, ₹20 lakh service)",
        "benefit_hi": "नया काम शुरू करने के लिए बैंक लोन, जिसमें प्रोजेक्ट लागत का 15–35% सरकार सब्सिडी देती है "
                      "(उत्पादन में ₹50 लाख, सेवा में ₹20 लाख तक)",
        "speak_hi": "पीएमईजीपी: नया काम शुरू करने के लिए बैंक लोन, जिसमें लागत का पंद्रह से पैंतीस प्रतिशत सरकार देती है।",
        "speak_en": "PMEGP: a bank loan to start a new unit, with fifteen to thirty-five percent of the cost paid by the government.",
        "apply": "kviconline.gov.in (PMEGP e-portal), or the district KVIC / District Industries Centre",
        "docs": "Aadhaar, project report, category certificate if any, education certificate for bigger projects",
        "rule": lambda p: p.get("biz") is True and (_age(p) or 18) >= 18,
        "note": "Only for new units. Women, SC/ST, OBC, minorities and rural applicants get the higher subsidy. Projects "
                "above ₹10 lakh (manufacturing) or ₹5 lakh (service) need 8th pass.",
    },
    {
        "id": "kcc",
        "name": "Kisan Credit Card",
        "name_hi": "किसान क्रेडिट कार्ड",
        "benefit": "Farm loans up to ₹5 lakh; up to ₹3 lakh at 7% interest, effectively 4% if repaid on time; "
                   "no collateral up to ₹2 lakh",
        "benefit_hi": "खेती के लिए ₹5 लाख तक लोन; ₹3 लाख तक 7% ब्याज, समय पर चुकाने पर सिर्फ़ 4%; ₹2 लाख तक कोई गारंटी नहीं",
        "speak_hi": "किसान क्रेडिट कार्ड: खेती के लिए सस्ता लोन, तीन लाख तक समय पर चुकाने पर सिर्फ़ चार प्रतिशत ब्याज।",
        "speak_en": "Kisan Credit Card: cheap farm loans, just four percent interest on up to three lakh if you repay on time.",
        "apply": "Any bank branch, cooperative bank, or your nearest CSC",
        "docs": "Aadhaar, land records or tenancy papers, photo, bank account",
        "rule": lambda p: p.get("occupation") == "farmer" and (_age(p) or 18) >= 18,
        "note": "Also for tenant farmers, sharecroppers, animal husbandry and fisheries. The bank decides the final limit.",
    },
    {
        "id": "pmfby",
        "name": "PM Fasal Bima Yojana",
        "name_hi": "प्रधानमंत्री फसल बीमा योजना",
        "benefit": "Crop insurance: you pay only 2% (kharif), 1.5% (rabi) or 5% (commercial/horticulture crops) of the "
                   "sum insured; the government pays the rest",
        "benefit_hi": "फसल बीमा: आप बीमा राशि का सिर्फ़ 2% (खरीफ़), 1.5% (रबी) या 5% (नकदी/बागवानी फसल) भरते हैं, बाकी सरकार देती है",
        "speak_hi": "फसल बीमा योजना: बहुत कम प्रीमियम पर फसल का बीमा, बाकी पैसा सरकार भरती है।",
        "speak_en": "Fasal Bima: crop insurance at a very low premium, the government pays the rest.",
        "apply": "Your bank, CSC, or pmfby.gov.in before the season's cut-off date",
        "docs": "Aadhaar, land records or tenancy papers, sowing details, bank account",
        "rule": lambda p: p.get("occupation") == "farmer",
        "note": "Voluntary for all farmers, including tenants. Enrol before your state's cut-off date each season.",
    },
    {
        "id": "udyam",
        "name": "Udyam Registration (MSME)",
        "name_hi": "उद्यम रजिस्ट्रेशन (MSME)",
        "benefit": "Free government registration for your business, which opens MSME benefits such as priority bank "
                   "loans and government schemes",
        "benefit_hi": "आपके काम-धंधे का मुफ़्त सरकारी रजिस्ट्रेशन, जिससे MSME के फ़ायदे जैसे बैंक लोन में प्राथमिकता और "
                      "सरकारी योजनाएँ मिलती हैं",
        "speak_hi": "उद्यम रजिस्ट्रेशन: अपने धंधे का मुफ़्त सरकारी रजिस्ट्रेशन, जिससे लोन और दूसरी योजनाएँ आसान होती हैं।",
        "speak_en": "Udyam registration: a free government registration for your business, which makes loans and other schemes easier.",
        "apply": "udyamregistration.gov.in (free) or your nearest CSC",
        "docs": "Aadhaar, PAN, bank account",
        "rule": lambda p: (p.get("occupation") in OWN_BUSINESS or p.get("biz") is True) and (_age(p) or 18) >= 18,
        "note": "Registration is free: don't pay agents. It replaced the old Udyog Aadhaar.",
    },
]

CENTRAL_MAYBE = [
    {
        "id": "startup_india",
        "name": "Startup India",
        "name_hi": "स्टार्टअप इंडिया",
        "benefit": "Free DPIIT startup recognition: tax benefits, easier compliance, and a chance at the Seed Fund "
                   "(up to ₹20 lakh grant through incubators)",
        "benefit_hi": "मुफ़्त DPIIT स्टार्टअप मान्यता: टैक्स में छूट, आसान नियम, और इनक्यूबेटर के ज़रिए ₹20 लाख तक के सीड फ़ंड का मौका",
        "speak_hi": "अगर आपका बिज़नेस आइडिया नया और अलग है, तो स्टार्टअप इंडिया भी देखिए।",
        "speak_en": "If your business idea is new and innovative, also look at Startup India.",
        "apply": "startupindia.gov.in (free)",
        "docs": "Company, LLP or registered partnership papers, PAN, a short note on what is new about the idea",
        "rule": lambda p: p.get("biz") is True and (_age(p) or 18) >= 18,
        "note": "Only for private limited companies, LLPs and registered partnerships with an innovative idea; "
                "not sole proprietors.",
    },
]

STATE = [
    {
        "id": "up_cm_yuva", "state": "UP",
        "name": "CM-YUVA (UP)",
        "name_hi": "मुख्यमंत्री युवा उद्यमी विकास अभियान",
        "benefit": "Interest-free, collateral-free loan up to ₹5 lakh to start a business, for UP youth aged 21–40",
        "benefit_hi": "21–40 साल के युवाओं को काम शुरू करने के लिए ₹5 लाख तक बिना ब्याज, बिना गारंटी लोन",
        "speak_hi": "मुख्यमंत्री युवा उद्यमी योजना: काम शुरू करने के लिए पाँच लाख तक का बिना ब्याज लोन।",
        "speak_en": "CM Yuva scheme: an interest-free loan of up to five lakh to start a business.",
        "apply": "District Industries Centre (DIC) or the CM-YUVA portal",
        "docs": "Aadhaar, UP residence proof, education certificate (8th pass or more), project proposal, bank account",
        "rule": lambda p: p.get("state") == "UP" and p.get("biz") is True and _between(p, 21, 40),
        "note": "Interest-free when repaid on time. Minimum 8th pass.",
    },
    {
        "id": "up_kanya_sumangala", "state": "UP",
        "name": "Kanya Sumangala (UP)",
        "name_hi": "मुख्यमंत्री कन्या सुमंगला योजना",
        "benefit": "₹25,000 for your daughter, paid in 6 stages from birth to higher education",
        "benefit_hi": "बेटी के लिए ₹25,000, जन्म से उच्च शिक्षा तक 6 किस्तों में",
        "speak_hi": "कन्या सुमंगला योजना: बेटी के लिए छह किस्तों में पच्चीस हज़ार रुपये।",
        "speak_en": "Kanya Sumangala: twenty-five thousand rupees for your daughter, in six stages.",
        "apply": "mksy.up.gov.in or your nearest CSC",
        "docs": "Daughter's birth certificate, parent's Aadhaar, income certificate, bank account, photo",
        "rule": lambda p: p.get("state") == "UP" and p.get("daughter_u10") is True and _income_upto(p, 300000),
        "note": "Family income up to ₹3 lakh a year; up to 2 daughters per family.",
    },
    {
        "id": "br_mahila_rojgar", "state": "BR",
        "name": "Mahila Rozgar Yojana (Bihar)",
        "name_hi": "मुख्यमंत्री महिला रोज़गार योजना",
        "benefit": "₹10,000 to start a livelihood, and up to ₹2 lakh more after a review six months later",
        "benefit_hi": "रोज़गार शुरू करने के लिए ₹10,000, और छह महीने बाद समीक्षा पर ₹2 लाख तक की और मदद",
        "speak_hi": "मुख्यमंत्री महिला रोज़गार योजना: काम शुरू करने के लिए दस हज़ार रुपये, और बाद में दो लाख तक की मदद।",
        "speak_en": "Mahila Rozgar Yojana: ten thousand rupees to start work, and up to two lakh more later.",
        "apply": "Through your JEEViKA self-help group or the block office",
        "docs": "Aadhaar, bank account, JEEViKA self-help group membership",
        "rule": lambda p: p.get("state") == "BR" and _woman(p) and _between(p, 18, 60),
        "note": "One woman per family, through JEEViKA self-help groups.",
    },
    {
        "id": "br_vridhjan", "state": "BR", "replaces": ["old_age_pension"],
        "name": "Vridhjan Pension (Bihar)",
        "name_hi": "मुख्यमंत्री वृद्धजन पेंशन योजना",
        "benefit": "₹1,100 a month pension for everyone aged 60 and above",
        "benefit_hi": "60 साल से ऊपर सबको हर महीने ₹1,100 पेंशन",
        "speak_hi": "वृद्धजन पेंशन: साठ साल से ऊपर हर महीने ग्यारह सौ रुपये।",
        "speak_en": "Vridhjan Pension: eleven hundred rupees a month for everyone over sixty.",
        "apply": "sspmis.bihar.gov.in, the RTPS counter or your block office",
        "docs": "Aadhaar, age proof, Bihar residence proof, bank account",
        "rule": lambda p: p.get("state") == "BR" and (_age(p) or 0) >= 60,
        "note": "Not for people already getting a government pension.",
    },
    {
        "id": "mh_ladki_bahin", "state": "MH",
        "name": "Ladki Bahin (Maharashtra)",
        "name_hi": "मुख्यमंत्री माझी लाडकी बहीण योजना",
        "benefit": "₹1,500 a month for women aged 21–60 from families earning up to ₹2.5 lakh a year",
        "benefit_hi": "21–60 साल की महिलाओं को हर महीने ₹1,500, परिवार की कमाई ₹2.5 लाख साल तक हो",
        "speak_hi": "लाडकी बहीण योजना: महिलाओं को हर महीने पंद्रह सौ रुपये।",
        "speak_en": "Ladki Bahin: fifteen hundred rupees a month for women.",
        "apply": "ladakibahin.maharashtra.gov.in, your Anganwadi worker or ward office",
        "docs": "Aadhaar, Maharashtra residence proof, income certificate or ration card, Aadhaar-linked bank account",
        "rule": lambda p: p.get("state") == "MH" and _woman(p) and _between(p, 21, 60)
        and _income_upto(p, 250000) and _not_tax(p),
        "note": "Bank account must be linked to Aadhaar (e-KYC). Income-tax payers are excluded.",
    },
    {
        "id": "mh_namo_shetkari", "state": "MH",
        "name": "Namo Shetkari (Maharashtra)",
        "name_hi": "नमो शेतकरी महासन्मान निधी",
        "benefit": "₹6,000 a year from Maharashtra on top of PM-KISAN (₹12,000 in total)",
        "benefit_hi": "पीएम किसान के ऊपर महाराष्ट्र सरकार से साल के ₹6,000 और (कुल ₹12,000)",
        "speak_hi": "नमो शेतकरी योजना: पीएम किसान के ऊपर साल के छह हज़ार रुपये और।",
        "speak_en": "Namo Shetkari: six thousand rupees a year more, on top of PM Kisan.",
        "apply": "No separate form: it goes to PM-KISAN farmers. Keep e-KYC and Aadhaar bank seeding done.",
        "docs": "Same as PM-KISAN: Aadhaar, land records, Aadhaar-linked bank account",
        "rule": lambda p: p.get("state") == "MH" and _pm_kisan(p),
        "note": "Paid in 3 instalments of ₹2,000.",
    },
    {
        "id": "wb_annapurna", "state": "WB",
        "name": "Annapurna Bhandar (West Bengal)",
        "name_hi": "अन्नपूर्णा भंडार",
        "benefit": "₹3,000 a month for women aged 25–60 (replaced Lakshmir Bhandar in June 2026)",
        "benefit_hi": "25–60 साल की महिलाओं को हर महीने ₹3,000 (जून 2026 से लक्ष्मीर भंडार की जगह)",
        "speak_hi": "अन्नपूर्णा भंडार: पच्चीस से साठ साल की महिलाओं को हर महीने तीन हज़ार रुपये।",
        "speak_en": "Annapurna Bhandar: three thousand rupees a month for women aged twenty-five to sixty.",
        "apply": "Your block or municipality office, or a government camp",
        "docs": "Aadhaar, ration card, Aadhaar-linked bank account",
        "rule": lambda p: p.get("state") == "WB" and _woman(p) and _between(p, 25, 60),
        "note": "New scheme since June 2026; Lakshmir Bhandar members were moved over. Confirm at your block office.",
    },
    {
        "id": "tn_kmut", "state": "TN",
        "name": "Magalir Urimai Thogai (Tamil Nadu)",
        "name_hi": "कलैञर मगलिर उरिमै तोगै",
        "benefit": "₹1,000 a month for women heads of family (a raise to ₹2,500 was promised but has not started)",
        "benefit_hi": "परिवार की मुखिया महिला को हर महीने ₹1,000 (₹2,500 करने का वादा है, अभी शुरू नहीं हुआ)",
        "speak_hi": "मगलिर उरिमै तोगै: परिवार की मुखिया महिला को हर महीने एक हज़ार रुपये।",
        "speak_en": "Magalir Urimai Thogai: one thousand rupees a month for women heads of family.",
        "apply": "Your taluk office or the scheme's camp at the ration shop",
        "docs": "Family (ration) card, Aadhaar, bank account",
        "rule": lambda p: p.get("state") == "TN" and _woman(p) and (_age(p) or 0) >= 21 and _income_upto(p, 250000),
        "note": "For women heads of family; family income up to ₹2.5 lakh a year.",
    },
    {
        "id": "ka_gruha_lakshmi", "state": "KA",
        "name": "Gruha Lakshmi (Karnataka)",
        "name_hi": "गृह लक्ष्मी",
        "benefit": "₹2,000 a month for the woman head of the household",
        "benefit_hi": "घर की मुखिया महिला को हर महीने ₹2,000",
        "speak_hi": "गृह लक्ष्मी: घर की मुखिया महिला को हर महीने दो हज़ार रुपये।",
        "speak_en": "Gruha Lakshmi: two thousand rupees a month for the woman head of the household.",
        "apply": "sevasindhugs.karnataka.gov.in, or a Grama One / Karnataka One / Bapuji centre",
        "docs": "Ration card, Aadhaar, Aadhaar-linked bank account",
        "rule": lambda p: p.get("state") == "KA" and _woman(p) and (_age(p) or 18) >= 18 and _not_tax(p),
        "note": "Not if the woman or her husband pays income tax or files GST returns.",
    },
]

STATE_MAYBE = [
    {
        "id": "mp_ladli_behna", "state": "MP",
        "name": "Ladli Behna (MP)",
        "name_hi": "मुख्यमंत्री लाडली बहना योजना",
        "benefit": "₹1,500 a month for women aged 21–60 from families earning up to ₹2.5 lakh a year",
        "benefit_hi": "21–60 साल की महिलाओं को हर महीने ₹1,500, परिवार की कमाई ₹2.5 लाख साल तक हो",
        "speak_hi": "मध्य प्रदेश की लाडली बहना योजना भी देखिए: महिलाओं को हर महीने पंद्रह सौ रुपये। नए नाम जुड़ने के बारे में पंचायत में पूछिए।",
        "speak_en": "Also check MP's Ladli Behna: fifteen hundred rupees a month for women. Ask your panchayat whether new names are being added.",
        "apply": "Gram panchayat or ward office camps",
        "docs": "Samagra ID, Aadhaar, Aadhaar-linked bank account",
        "rule": lambda p: p.get("state") == "MP" and _woman(p) and _between(p, 21, 60)
        and _income_upto(p, 250000) and _not_tax(p),
        "note": "New names are added only in special drives, so check at your gram panchayat or ward office.",
    },
    {
        "id": "rj_maa", "state": "RJ",
        "name": "MAA Yojana (Rajasthan)",
        "name_hi": "मुख्यमंत्री आयुष्मान आरोग्य (मा) योजना",
        "benefit": "Cashless hospital treatment up to ₹25 lakh a year per family",
        "benefit_hi": "हर परिवार को साल में ₹25 लाख तक कैशलेस इलाज",
        "speak_hi": "राजस्थान की मा योजना भी देखिए: परिवार को साल में पच्चीस लाख तक का कैशलेस इलाज।",
        "speak_en": "Also check Rajasthan's MAA scheme: cashless treatment up to twenty-five lakh a year per family.",
        "apply": "Your nearest e-Mitra centre",
        "docs": "Jan Aadhaar card, Aadhaar",
        "rule": lambda p: p.get("state") == "RJ",
        "note": "Free for many families; others may need to pay a yearly premium. Ask at e-Mitra.",
    },
    {
        "id": "ka_yuva_nidhi", "state": "KA",
        "name": "Yuva Nidhi (Karnataka)",
        "name_hi": "युवा निधि",
        "benefit": "₹3,000 a month for unemployed graduates and ₹1,500 for diploma holders, for up to 2 years",
        "benefit_hi": "बेरोज़गार ग्रेजुएट को हर महीने ₹3,000, डिप्लोमा वालों को ₹1,500, 2 साल तक",
        "speak_hi": "कर्नाटक की युवा निधि भी देखिए: बेरोज़गार ग्रेजुएट को हर महीने तीन हज़ार रुपये।",
        "speak_en": "Also check Karnataka's Yuva Nidhi: three thousand rupees a month for unemployed graduates.",
        "apply": "sevasindhugs.karnataka.gov.in",
        "docs": "Degree or diploma certificate, Aadhaar, Karnataka residence proof, bank account",
        "rule": lambda p: p.get("state") == "KA" and p.get("occupation") in ("unemployed", "student") and _between(p, 18, 35),
        "note": "For degree or diploma holders who passed in 2022-23 or later and have been unemployed for 6 months.",
    },
]

WHY_KEYS = {
    "pmegp": ["biz"], "kcc": ["farmer"], "pmfby": ["farmer"], "udyam": ["business"], "startup_india": ["biz"],
    "up_cm_yuva": ["state", "age", "biz"], "up_kanya_sumangala": ["state", "daughter", "low_income"],
    "br_mahila_rojgar": ["state", "woman"], "br_vridhjan": ["state", "senior60"],
    "mh_ladki_bahin": ["state", "woman", "age"], "mh_namo_shetkari": ["state", "farmer", "land"],
    "wb_annapurna": ["state", "woman", "age"], "tn_kmut": ["state", "woman"], "ka_gruha_lakshmi": ["state", "woman"],
    "mp_ladli_behna": ["state", "woman"], "rj_maa": ["state"], "ka_yuva_nidhi": ["state", "age"],
}
WOMEN_SCHEME_STATES = {"BR", "MH", "MP", "WB", "TN", "KA"}
