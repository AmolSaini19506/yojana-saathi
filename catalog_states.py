"""
State schemes added on 11 Nov 2026 (same entry format as catalog.py, which imports these lists).

Each one was checked against 2026 news reports and state announcements on that date. Notes on what was found:
- Delhi's Mahila Samriddhi Yojana was renamed Delhi Lakshmi Yojana and launched on 26 Aug 2026.
- Punjab's Mukh Mantri Mawan Dheeyan Satkar Yojna was cleared in March 2026; payments were due from July 2026.
- Himachal added a family income limit of Rs 2 lakh in April 2026 and asked women to apply again.
- Rajasthan's social security pension is Rs 1,450 a month (raised from Rs 1,000 between 2024 and 2026).
- Left out: Kerala (the government changed in 2026 and had not confirmed which pensions and schemes continue),
  Telangana's Rs 2,500 for women (not started) and Cheyutha pension (reports disagree on the amount),
  Gujarat's widow pension and Vahli Dikri (amounts not confirmed).
`local` holds the card in the state's own language where the app supports it (Gujarati, Telugu, Punjabi).
`replaces` lists the general cards a state card stands in for, so the same pension is not shown twice.
"""


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


def _income_upto(p, per_year):
    inc = p.get("income_month")
    return inc is not None and inc * 12 <= per_year


def _farmer_with_land(p):
    return p.get("occupation") == "farmer" and (p.get("land_ha") or 0) > 0


def _not_govt(p):
    return p.get("occupation") != "govt_employee"


STATE = [
    {
        "id": "dl_lakshmi", "state": "DL",
        "name": "Delhi Lakshmi Yojana", "name_hi": "दिल्ली लक्ष्मी योजना",
        "benefit": "₹2,500 a month for women aged 21 to 60 from families earning under ₹2.5 lakh a year",
        "benefit_hi": "21 से 60 साल की महिलाओं को हर महीने ₹2,500, परिवार की कमाई ₹2.5 लाख साल से कम हो",
        "speak_en": "Delhi Lakshmi Yojana: two thousand five hundred rupees a month for women.",
        "speak_hi": "दिल्ली लक्ष्मी योजना: महिलाओं को हर महीने ढाई हज़ार रुपये।",
        "apply": "The Delhi government's registration portal or camps in your area",
        "apply_hi": "दिल्ली सरकार के रजिस्ट्रेशन पोर्टल पर, या अपने इलाके के कैंप में आवेदन कीजिए।",
        "docs": "Aadhaar, Delhi address proof, family income certificate, bank account",
        "docs_hi": "आधार कार्ड, दिल्ली के पते का प्रमाण, परिवार का आय प्रमाण पत्र और बैंक खाता।",
        "note": "Launched in August 2026 (earlier called Mahila Samriddhi Yojana). The family should have three or fewer children.",
        "note_hi": "अगस्त 2026 में शुरू हुई (पहले नाम महिला समृद्धि योजना था)। परिवार में तीन या कम बच्चे होने चाहिए।",
        "rule": lambda p: p.get("state") == "DL" and _woman(p) and _between(p, 21, 60) and _income_upto(p, 250000)
        and _not_tax(p) and _not_govt(p),
        "why": ["state", "woman", "age"], "cash": 30000, "tags": ["aadhaar", "residence", "income_cert", "bank"],
        "names": ["delhi lakshmi", "दिल्ली लक्ष्मी", "mahila samriddhi", "महिला समृद्धि"],
    },
    {
        "id": "pb_mawan_dheeyan", "state": "PB",
        "name": "Mawan Dheeyan Satkar Yojna (Punjab)", "name_hi": "मुख्यमंत्री मावां धीयां सत्कार योजना",
        "benefit": "₹1,000 a month for women, and ₹1,500 a month for women from Scheduled Castes",
        "benefit_hi": "महिलाओं को हर महीने ₹1,000, और अनुसूचित जाति की महिलाओं को ₹1,500",
        "speak_en": "Punjab's Mawan Dheeyan Satkar Yojna: one thousand rupees a month for women, fifteen hundred for Scheduled Caste women.",
        "speak_hi": "पंजाब की मावां धीयां सत्कार योजना: महिलाओं को हर महीने एक हज़ार रुपये, अनुसूचित जाति की महिलाओं को पंद्रह सौ।",
        "apply": "Registration camps in your constituency or a Sewa Kendra",
        "apply_hi": "अपने हलके के रजिस्ट्रेशन कैंप में या सेवा केंद्र पर आवेदन कीजिए।",
        "docs": "Aadhaar, Punjab residence proof, bank account, caste certificate for the higher amount",
        "docs_hi": "आधार कार्ड, पंजाब का निवास प्रमाण, बैंक खाता, और ज़्यादा रकम के लिए जाति प्रमाण पत्र।",
        "note": "Started in 2026: registration from April, payments from July. Income-tax payers and government employees are left out.",
        "note_hi": "2026 में शुरू हुई: अप्रैल से रजिस्ट्रेशन, जुलाई से भुगतान। इनकम टैक्स भरने वाले और सरकारी कर्मचारी इसमें नहीं आते।",
        "rule": lambda p: p.get("state") == "PB" and _woman(p) and _adult(p) and _not_tax(p) and _not_govt(p),
        "why": ["state", "woman"], "cash": 12000, "tags": ["aadhaar", "residence", "bank"],
        "names": ["mawan dheeyan", "मावां धीयां", "satkar", "सत्कार"],
        "local": {"pa": ("ਮੁੱਖ ਮੰਤਰੀ ਮਾਵਾਂ ਧੀਆਂ ਸਤਿਕਾਰ ਯੋਜਨਾ", "ਔਰਤਾਂ ਨੂੰ ਹਰ ਮਹੀਨੇ ₹1,000, ਅਤੇ ਅਨੁਸੂਚਿਤ ਜਾਤੀ ਦੀਆਂ ਔਰਤਾਂ ਨੂੰ ₹1,500",
                         "ਮਾਵਾਂ ਧੀਆਂ ਸਤਿਕਾਰ ਯੋਜਨਾ: ਔਰਤਾਂ ਨੂੰ ਹਰ ਮਹੀਨੇ ₹1,000, ਅਨੁਸੂਚਿਤ ਜਾਤੀ ਦੀਆਂ ਔਰਤਾਂ ਨੂੰ ₹1,500।")},
    },
    {
        "id": "od_subhadra", "state": "OD",
        "name": "Subhadra Yojana (Odisha)", "name_hi": "सुभद्रा योजना",
        "benefit": "₹10,000 a year for women aged 21 to 59, paid as two instalments of ₹5,000",
        "benefit_hi": "21 से 59 साल की महिलाओं को साल के ₹10,000, ₹5,000 की दो किस्तों में",
        "speak_en": "Odisha's Subhadra Yojana: ten thousand rupees a year for women, in two instalments.",
        "speak_hi": "ओडिशा की सुभद्रा योजना: महिलाओं को साल के दस हज़ार रुपये, दो किस्तों में।",
        "apply": "The Subhadra portal, or a Mo Seba Kendra / CSC",
        "apply_hi": "सुभद्रा पोर्टल पर, या मो सेवा केंद्र या सीएससी केंद्र पर आवेदन कीजिए।",
        "docs": "Aadhaar, ration card, Aadhaar-linked bank account in your own name",
        "docs_hi": "आधार कार्ड, राशन कार्ड, और आपके अपने नाम का आधार से जुड़ा बैंक खाता।",
        "note": "For women from lower-income families (ration card holders). Income-tax payers and government employees are left out.",
        "note_hi": "कम आय वाले परिवारों (राशन कार्ड वाले) की महिलाओं के लिए। इनकम टैक्स भरने वाले और सरकारी कर्मचारी इसमें नहीं आते।",
        "rule": lambda p: p.get("state") == "OD" and _woman(p) and _between(p, 21, 59) and _not_tax(p) and _not_govt(p),
        "why": ["state", "woman", "age"], "cash": 10000, "tags": ["aadhaar", "ration", "bank"],
        "names": ["subhadra", "सुभद्रा"],
    },
    {
        "id": "jh_maiyan", "state": "JH",
        "name": "Maiyan Samman Yojana (Jharkhand)", "name_hi": "मुख्यमंत्री मंईयां सम्मान योजना",
        "benefit": "₹2,500 a month for women aged 18 to 50",
        "benefit_hi": "18 से 50 साल की महिलाओं को हर महीने ₹2,500",
        "speak_en": "Jharkhand's Maiyan Samman Yojana: two thousand five hundred rupees a month for women aged eighteen to fifty.",
        "speak_hi": "झारखंड की मंईयां सम्मान योजना: अठारह से पचास साल की महिलाओं को हर महीने ढाई हज़ार रुपये।",
        "apply": "Your panchayat or ward office, or a Pragya Kendra",
        "apply_hi": "अपनी पंचायत या वार्ड के दफ़्तर में, या प्रज्ञा केंद्र पर आवेदन कीजिए।",
        "docs": "Aadhaar, ration card, Aadhaar-linked bank account",
        "docs_hi": "आधार कार्ड, राशन कार्ड और आधार से जुड़ा बैंक खाता।",
        "note": "For women of Jharkhand from ration-card families. Income-tax payers and government employees are left out.",
        "note_hi": "झारखंड के राशन कार्ड वाले परिवारों की महिलाओं के लिए। इनकम टैक्स भरने वाले और सरकारी कर्मचारी इसमें नहीं आते।",
        "rule": lambda p: p.get("state") == "JH" and _woman(p) and _between(p, 18, 50) and _not_tax(p) and _not_govt(p),
        "why": ["state", "woman", "age"], "cash": 30000, "tags": ["aadhaar", "ration", "bank"],
        "names": ["maiyan", "maiya samman", "मंईयां", "मैया सम्मान"],
    },
    {
        "id": "cg_mahtari", "state": "CG",
        "name": "Mahtari Vandan Yojana (Chhattisgarh)", "name_hi": "महतारी वंदन योजना",
        "benefit": "₹1,000 a month for married women aged 21 or more, including widows and divorced women",
        "benefit_hi": "21 साल या ज़्यादा उम्र की विवाहित महिलाओं को हर महीने ₹1,000; विधवा और तलाकशुदा महिलाएँ भी शामिल",
        "speak_en": "Chhattisgarh's Mahtari Vandan Yojana: one thousand rupees a month for married women.",
        "speak_hi": "छत्तीसगढ़ की महतारी वंदन योजना: विवाहित महिलाओं को हर महीने एक हज़ार रुपये।",
        "apply": "mahtarivandan.cgstate.gov.in, your anganwadi centre or gram panchayat",
        "apply_hi": "{web} पर, या अपने आंगनवाड़ी केंद्र या ग्राम पंचायत में आवेदन कीजिए।",
        "docs": "Aadhaar, marriage proof, Chhattisgarh residence proof, bank account in your own name",
        "docs_hi": "आधार कार्ड, विवाह का प्रमाण, छत्तीसगढ़ का निवास प्रमाण, और आपके अपने नाम का बैंक खाता।",
        "note": "Income-tax payers and government employees are left out.",
        "note_hi": "इनकम टैक्स भरने वाले और सरकारी कर्मचारी इसमें नहीं आते।",
        "web": "mahtarivandan.cgstate.gov.in", "web_hi": "महतारी वंदन की वेबसाइट",
        "rule": lambda p: p.get("state") == "CG" and _woman(p) and _age(p) is not None and _age(p) >= 21 and _not_tax(p)
        and _not_govt(p),
        "why": ["state", "woman", "age"], "cash": 12000, "tags": ["aadhaar", "residence", "bank"],
        "names": ["mahtari", "महतारी"],
    },
    {
        "id": "hp_pyari_behna", "state": "HP",
        "name": "Pyari Behna Sukh-Samman Nidhi (Himachal)", "name_hi": "इंदिरा गांधी प्यारी बहना सुख-सम्मान निधि",
        "benefit": "₹1,500 a month for women aged 18 to 59 from families earning up to ₹2 lakh a year",
        "benefit_hi": "18 से 59 साल की महिलाओं को हर महीने ₹1,500, परिवार की कमाई ₹2 लाख साल तक हो",
        "speak_en": "Himachal's Pyari Behna scheme: fifteen hundred rupees a month for women.",
        "speak_hi": "हिमाचल की प्यारी बहना सुख-सम्मान निधि: महिलाओं को हर महीने पंद्रह सौ रुपये।",
        "apply": "The Tehsil Welfare Officer's office (forms are taken on paper)",
        "apply_hi": "तहसील कल्याण अधिकारी के दफ़्तर में फ़ॉर्म जमा कीजिए; आवेदन ऑनलाइन नहीं होता।",
        "docs": "Himachal domicile certificate, age proof, Aadhaar, bank account",
        "docs_hi": "हिमाचली प्रमाण पत्र, उम्र का प्रमाण, आधार कार्ड और बैंक खाता।",
        "note": "An income limit was added in April 2026 and women were asked to apply again. It is being rolled out area by area.",
        "note_hi": "अप्रैल 2026 में आय की सीमा जोड़ी गई और महिलाओं से दोबारा आवेदन माँगा गया। यह इलाके-दर-इलाके लागू हो रही है।",
        "rule": lambda p: p.get("state") == "HP" and _woman(p) and _between(p, 18, 59) and _income_upto(p, 200000)
        and _not_tax(p) and _not_govt(p),
        "why": ["state", "woman", "age"], "cash": 18000, "tags": ["residence", "age_proof", "aadhaar", "bank"],
        "names": ["pyari behna", "प्यारी बहना", "sukh samman", "सुख सम्मान"],
    },
    {
        "id": "ap_annadata", "state": "AP",
        "name": "Annadata Sukhibhava (Andhra Pradesh)", "name_hi": "अन्नदाता सुखीभव",
        "benefit": "₹20,000 a year for farmers: ₹14,000 from the state on top of PM-KISAN's ₹6,000",
        "benefit_hi": "किसानों को साल के ₹20,000: पीएम किसान के ₹6,000 के ऊपर राज्य से ₹14,000",
        "speak_en": "Andhra's Annadata Sukhibhava: twenty thousand rupees a year for farmers, counting PM-KISAN.",
        "speak_hi": "आंध्र प्रदेश की अन्नदाता सुखीभव योजना: किसानों को पीएम किसान मिलाकर साल के बीस हज़ार रुपये।",
        "apply": "Your Rythu Seva Kendra or village secretariat",
        "apply_hi": "अपने रायतु सेवा केंद्र या ग्राम सचिवालय में पूछिए।",
        "docs": "Aadhaar, land records (pattadar passbook), bank account",
        "docs_hi": "आधार कार्ड, ज़मीन के कागज़ (पट्टादार पासबुक) और बैंक खाता।",
        "note": "Launched in August 2025. Paid in instalments along with PM-KISAN.",
        "note_hi": "अगस्त 2025 में शुरू हुई। पैसा पीएम किसान की किस्तों के साथ आता है।",
        "rule": lambda p: p.get("state") == "AP" and _farmer_with_land(p) and _not_tax(p),
        "why": ["state", "farmer", "land"], "cash": 14000, "tags": ["aadhaar", "land", "bank"],
        "names": ["annadata", "sukhibhava", "अन्नदाता"],
        "local": {"te": ("అన్నదాత సుఖీభవ", "రైతులకు సంవత్సరానికి ₹20,000: పీఎం కిసాన్ ₹6,000 తో పాటు రాష్ట్రం నుంచి ₹14,000",
                         "అన్నదాత సుఖీభవ: రైతులకు పీఎం కిసాన్‌తో కలిపి సంవత్సరానికి ₹20,000.")},
    },
    {
        "id": "ap_thalliki", "state": "AP",
        "name": "Thalliki Vandanam (Andhra Pradesh)", "name_hi": "तल्लिकि वंदनम",
        "benefit": "₹15,000 a year for every school-going child, paid to the mother",
        "benefit_hi": "स्कूल जाने वाले हर बच्चे के लिए साल के ₹15,000, माँ के खाते में",
        "speak_en": "Andhra's Thalliki Vandanam: fifteen thousand rupees a year for every school-going child, paid to the mother.",
        "speak_hi": "आंध्र प्रदेश की तल्लिकि वंदनम योजना: स्कूल जाने वाले हर बच्चे के लिए साल के पंद्रह हज़ार रुपये, माँ के खाते में।",
        "apply": "Through the child's school and your village or ward secretariat",
        "apply_hi": "बच्चे के स्कूल और अपने ग्राम या वार्ड सचिवालय के ज़रिए।",
        "docs": "Mother's Aadhaar and bank account, child's school details, ration (rice) card",
        "docs_hi": "माँ का आधार कार्ड और बैंक खाता, बच्चे के स्कूल का ब्योरा, और राशन कार्ड।",
        "note": "For every school-going child in the family, from Class 1 to 12, with regular attendance.",
        "note_hi": "परिवार के हर स्कूल जाने वाले बच्चे के लिए, पहली से बारहवीं तक, स्कूल में नियमित हाज़िरी के साथ।",
        "rule": lambda p: p.get("state") == "AP" and p.get("school_kids") is True and _not_tax(p),
        "why": ["state", "school_kids"], "cash": 15000, "tags": ["aadhaar", "bank", "ration"],
        "names": ["thalliki", "talliki", "vandanam", "तल्लिकि", "amma vodi"],
        "local": {"te": ("తల్లికి వందనం", "బడికి వెళ్లే ప్రతి బిడ్డకు సంవత్సరానికి ₹15,000, తల్లి ఖాతాలో",
                         "తల్లికి వందనం: బడికి వెళ్లే ప్రతి బిడ్డకు సంవత్సరానికి ₹15,000, తల్లి ఖాతాలో.")},
    },
    {
        "id": "tg_rythu_bharosa", "state": "TG",
        "name": "Rythu Bharosa (Telangana)", "name_hi": "रायतु भरोसा",
        "benefit": "₹12,000 per acre a year for farmers, as investment support",
        "benefit_hi": "किसानों को खेती की लागत के लिए साल के ₹12,000 प्रति एकड़",
        "speak_en": "Telangana's Rythu Bharosa: twelve thousand rupees per acre a year for farmers.",
        "speak_hi": "तेलंगाना की रायतु भरोसा योजना: किसानों को साल के बारह हज़ार रुपये प्रति एकड़।",
        "apply": "Your Agriculture Extension Officer or mandal agriculture office",
        "apply_hi": "अपने कृषि विस्तार अधिकारी या मंडल कृषि दफ़्तर में पूछिए।",
        "docs": "Pattadar passbook, Aadhaar, bank account",
        "docs_hi": "पट्टादार पासबुक, आधार कार्ड और बैंक खाता।",
        "note": "For land that is fit for cultivation. Payments have sometimes come late, so check your status at the agriculture office.",
        "note_hi": "खेती लायक ज़मीन के लिए। पैसा कभी-कभी देर से आया है, इसलिए कृषि दफ़्तर में अपना स्टेटस देख लीजिए।",
        "rule": lambda p: p.get("state") == "TG" and _farmer_with_land(p),
        "why": ["state", "farmer", "land"], "tags": ["land", "aadhaar", "bank"],
        "names": ["rythu bharosa", "raitu bharosa", "रायतु भरोसा", "rythu bandhu"],
        "local": {"te": ("రైతు భరోసా", "రైతులకు పెట్టుబడి సాయంగా ఎకరానికి సంవత్సరానికి ₹12,000",
                         "రైతు భరోసా: రైతులకు ఎకరానికి సంవత్సరానికి ₹12,000.")},
    },
    {
        "id": "tg_mahalakshmi_bus", "state": "TG",
        "name": "Mahalakshmi free bus travel (Telangana)", "name_hi": "महालक्ष्मी मुफ़्त बस यात्रा",
        "benefit": "Free travel for women and girls in the state's ordinary and express RTC buses",
        "benefit_hi": "महिलाओं और लड़कियों को राज्य की साधारण और एक्सप्रेस आरटीसी बसों में मुफ़्त यात्रा",
        "speak_en": "Telangana's Mahalakshmi scheme: free travel for women in ordinary and express RTC buses.",
        "speak_hi": "तेलंगाना की महालक्ष्मी योजना: महिलाओं को साधारण और एक्सप्रेस आरटीसी बसों में मुफ़्त यात्रा।",
        "apply": "Nothing to apply for: show ID with a Telangana address to the conductor for a zero-fare ticket",
        "apply_hi": "कोई आवेदन नहीं करना है: कंडक्टर को तेलंगाना के पते वाला पहचान पत्र दिखाइए और शून्य किराए का टिकट लीजिए।",
        "docs": "Aadhaar or another ID with a Telangana address",
        "docs_hi": "आधार कार्ड या तेलंगाना के पते वाला कोई और पहचान पत्र।",
        "note": "Running since December 2023. The ₹2,500 a month promised to women under the same name has not started.",
        "note_hi": "दिसंबर 2023 से चल रही है। इसी नाम से महिलाओं को ₹2,500 महीना देने का वादा अभी शुरू नहीं हुआ है।",
        "rule": lambda p: p.get("state") == "TG" and _woman(p),
        "why": ["state", "woman"], "tags": ["aadhaar"],
        "names": ["mahalakshmi", "महालक्ष्मी", "free bus", "मुफ़्त बस", "मुफ्त बस"],
        "local": {"te": ("మహాలక్ష్మి ఉచిత బస్సు ప్రయాణం", "మహిళలకు, బాలికలకు ఆర్టీసీ పల్లె వెలుగు, ఎక్స్‌ప్రెస్ బస్సుల్లో ఉచిత ప్రయాణం",
                         "మహాలక్ష్మి పథకం: మహిళలకు ఆర్టీసీ బస్సుల్లో ఉచిత ప్రయాణం.")},
    },
    {
        "id": "gj_namo_lakshmi", "state": "GJ",
        "name": "Namo Lakshmi Yojana (Gujarat)", "name_hi": "नमो लक्ष्मी योजना",
        "benefit": "₹50,000 in total for girls studying in Class 9 to 12, spread over the four years",
        "benefit_hi": "नौवीं से बारहवीं में पढ़ने वाली लड़कियों को चार साल में कुल ₹50,000",
        "speak_en": "Gujarat's Namo Lakshmi Yojana: fifty thousand rupees in total for girls studying in Class nine to twelve.",
        "speak_hi": "गुजरात की नमो लक्ष्मी योजना: नौवीं से बारहवीं में पढ़ने वाली लड़कियों को कुल पचास हज़ार रुपये।",
        "apply": "Through the girl's school, which registers her on the Namo Lakshmi portal",
        "apply_hi": "लड़की के स्कूल के ज़रिए: स्कूल ही नमो लक्ष्मी पोर्टल पर नाम दर्ज करता है।",
        "docs": "Girl's Aadhaar, school details, bank account of the mother or the girl",
        "docs_hi": "लड़की का आधार कार्ड, स्कूल का ब्योरा, और माँ या लड़की का बैंक खाता।",
        "note": "For girls in government, aided and private schools in Gujarat, even if they get another scholarship.",
        "note_hi": "गुजरात के सरकारी, सहायता प्राप्त और निजी स्कूलों की लड़कियों के लिए, चाहे उन्हें कोई और छात्रवृत्ति मिलती हो।",
        "rule": lambda p: p.get("state") == "GJ" and (
            (p.get("occupation") == "student" and _woman(p) and p.get("study") == "school") or p.get("school_kids") is True),
        "why": ["state", "school_kids"], "tags": ["aadhaar", "bank"],
        "names": ["namo lakshmi", "namo laxmi", "नमो लक्ष्मी"],
        "local": {"gu": ("નમો લક્ષ્મી યોજના", "ધોરણ 9 થી 12 માં ભણતી દીકરીઓને ચાર વર્ષમાં કુલ ₹50,000",
                         "નમો લક્ષ્મી યોજના: ધોરણ 9 થી 12 માં ભણતી દીકરીઓને કુલ ₹50,000.")},
    },
    {
        "id": "up_old_age", "state": "UP", "replaces": ["old_age_pension"],
        "name": "Old-age pension (Uttar Pradesh)", "name_hi": "वृद्धावस्था पेंशन (उत्तर प्रदेश)",
        "benefit": "₹1,000 a month for people aged 60 or more from poor families",
        "benefit_hi": "गरीब परिवारों के 60 साल या उससे बड़े लोगों को हर महीने ₹1,000",
        "speak_en": "UP's old-age pension: one thousand rupees a month from the age of sixty.",
        "speak_hi": "उत्तर प्रदेश की वृद्धावस्था पेंशन: साठ साल की उम्र से हर महीने एक हज़ार रुपये।",
        "apply": "sspy-up.gov.in or your nearest CSC",
        "apply_hi": "{web} पर या नज़दीकी सीएससी केंद्र पर आवेदन कीजिए।",
        "docs": "Age proof, income certificate, Aadhaar, bank account",
        "docs_hi": "उम्र का प्रमाण, आय प्रमाण पत्र, आधार कार्ड और बैंक खाता।",
        "note": "For BPL families or those with a very low income. This amount includes the central pension.",
        "note_hi": "बीपीएल परिवारों या बहुत कम आय वालों के लिए। इस रकम में केंद्र की पेंशन शामिल है।",
        "web": "sspy-up.gov.in", "web_hi": "एसएसपीवाई यूपी डॉट जीओवी डॉट इन",
        "rule": lambda p: p.get("state") == "UP" and _age(p) is not None and _age(p) >= 60
        and (p.get("bpl") is True or _income_upto(p, 46080)),
        "why": ["state", "senior60"], "cash": 12000, "tags": ["age_proof", "income_cert", "aadhaar", "bank"],
        "names": ["vridhavastha pension", "वृद्धावस्था पेंशन", "budhapa pension", "बुढ़ापा पेंशन"],
    },
    {
        "id": "rj_pension", "state": "RJ", "replaces": ["old_age_pension", "widow_pension"],
        "name": "Social security pension (Rajasthan)", "name_hi": "सामाजिक सुरक्षा पेंशन (राजस्थान)",
        "benefit": "₹1,450 a month for the elderly (women from 55, men from 58), widows and people with disabilities",
        "benefit_hi": "बुज़ुर्गों (महिलाएँ 55 साल से, पुरुष 58 साल से), विधवा महिलाओं और दिव्यांगों को हर महीने ₹1,450",
        "speak_en": "Rajasthan's social security pension: one thousand four hundred and fifty rupees a month.",
        "speak_hi": "राजस्थान की सामाजिक सुरक्षा पेंशन: हर महीने एक हज़ार चार सौ पचास रुपये।",
        "apply": "Your nearest e-Mitra centre, with your Jan Aadhaar",
        "apply_hi": "जन आधार लेकर नज़दीकी ई-मित्र केंद्र पर आवेदन कीजिए।",
        "docs": "Jan Aadhaar card, Aadhaar, bank account",
        "docs_hi": "जन आधार कार्ड, आधार कार्ड और बैंक खाता।",
        "note": "For families with a low income; the income limit is checked at e-Mitra.",
        "note_hi": "कम आय वाले परिवारों के लिए; आय की सीमा ई-मित्र पर जाँची जाती है।",
        "rule": lambda p: p.get("state") == "RJ" and (p.get("bpl") is True or _income_upto(p, 48000)) and (
            (_woman(p) and _age(p) is not None and _age(p) >= 55) or (_age(p) is not None and _age(p) >= 58)
            or p.get("widow") is True or p.get("disabled") is True),
        "why": ["state"], "cash": 17400, "tags": ["aadhaar", "bank"],
        "names": ["samajik suraksha", "सामाजिक सुरक्षा", "pension"],
    },
]

STATE_CHECK = [
    {
        "id": "hr_lado_lakshmi", "state": "HR",
        "name": "Lado Lakshmi Yojana (Haryana)", "name_hi": "दीन दयाल लाडो लक्ष्मी योजना",
        "benefit": "₹2,100 a month for women from lower-income families",
        "benefit_hi": "कम आय वाले परिवारों की महिलाओं को हर महीने ₹2,100",
        "speak_en": "Also check Haryana's Lado Lakshmi Yojana: two thousand one hundred rupees a month for women from lower-income families.",
        "speak_hi": "हरियाणा की लाडो लक्ष्मी योजना भी देखिए: कम आय वाले परिवारों की महिलाओं को हर महीने इक्कीस सौ रुपये।",
        "apply": "The Lado Lakshmi mobile app, or a CSC / Antyodaya Saral Kendra",
        "apply_hi": "लाडो लक्ष्मी मोबाइल ऐप पर, या सीएससी केंद्र या अंत्योदय सरल केंद्र पर आवेदन कीजिए।",
        "docs": "Parivar Pehchan Patra (family ID), Aadhaar, Haryana residence proof, bank account",
        "docs_hi": "परिवार पहचान पत्र, आधार कार्ड, हरियाणा का निवास प्रमाण और बैंक खाता।",
        "note": "First payments went out in November 2025. The age and family-income limits are checked from your family ID: confirm them when you apply.",
        "note_hi": "पहला भुगतान नवंबर 2025 में हुआ। उम्र और परिवार की आय की सीमा परिवार पहचान पत्र से जाँची जाती है: आवेदन के समय पक्का कर लीजिए।",
        "rule": lambda p: p.get("state") == "HR" and _woman(p) and _adult(p) and _not_tax(p) and _not_govt(p),
        "why": ["state", "woman"], "tags": ["aadhaar", "residence", "bank"],
        "names": ["lado lakshmi", "लाडो लक्ष्मी"],
    },
    {
        "id": "as_orunodoi", "state": "AS",
        "name": "Orunodoi (Assam)", "name_hi": "अरुणोदय योजना",
        "benefit": "₹1,250 a month paid to a woman of the family, for poor households",
        "benefit_hi": "गरीब परिवारों में घर की महिला के खाते में हर महीने ₹1,250",
        "speak_en": "Also check Assam's Orunodoi scheme: one thousand two hundred and fifty rupees a month for a woman of the family.",
        "speak_hi": "असम की अरुणोदय योजना भी देखिए: घर की महिला के खाते में हर महीने साढ़े बारह सौ रुपये।",
        "apply": "Application camps held by the district administration; check lists on orunodoi.assam.gov.in",
        "apply_hi": "ज़िला प्रशासन के कैंप में आवेदन होता है; सूची {web} पर देख सकते हैं।",
        "docs": "Aadhaar, ration card, bank account in the woman's name",
        "docs_hi": "आधार कार्ड, राशन कार्ड, और महिला के नाम का बैंक खाता।",
        "note": "New names are taken in drives, so ask your gaon panchayat or ward office when the next one is.",
        "note_hi": "नए नाम खास अभियान में ही जुड़ते हैं, इसलिए गाँव पंचायत या वार्ड दफ़्तर में पूछिए कि अगला कब है।",
        "web": "orunodoi.assam.gov.in", "web_hi": "अरुणोदय की वेबसाइट",
        "rule": lambda p: p.get("state") == "AS" and _woman(p) and _adult(p) and _not_tax(p) and _not_govt(p),
        "why": ["state", "woman"], "tags": ["aadhaar", "ration", "bank"],
        "names": ["orunodoi", "arunodoi", "अरुणोदय"],
    },
    {
        "id": "ap_ntr_bharosa", "state": "AP",
        "name": "NTR Bharosa pension (Andhra Pradesh)", "name_hi": "एनटीआर भरोसा पेंशन",
        "benefit": "A monthly pension for the elderly, widows and others; it was raised to ₹4,000 a month in July 2024",
        "benefit_hi": "बुज़ुर्गों, विधवा महिलाओं और दूसरों को हर महीने पेंशन; जुलाई 2024 में इसे ₹4,000 महीना किया गया था",
        "speak_en": "Also check Andhra's NTR Bharosa pension for the elderly and widows.",
        "speak_hi": "आंध्र प्रदेश की एनटीआर भरोसा पेंशन भी देखिए: बुज़ुर्गों और विधवा महिलाओं के लिए।",
        "apply": "Your village or ward secretariat",
        "apply_hi": "अपने ग्राम या वार्ड सचिवालय में आवेदन कीजिए।",
        "docs": "Aadhaar, ration (rice) card, age proof or husband's death certificate, bank account",
        "docs_hi": "आधार कार्ड, राशन कार्ड, उम्र का प्रमाण या पति का मृत्यु प्रमाण पत्र, और बैंक खाता।",
        "note": "Confirm the current amount and the income rules at the secretariat.",
        "note_hi": "मौजूदा रकम और आय के नियम सचिवालय में पक्का कर लीजिए।",
        "rule": lambda p: p.get("state") == "AP" and ((_age(p) is not None and _age(p) >= 60) or p.get("widow") is True),
        "why": ["state"], "tags": ["aadhaar", "ration", "age_proof", "bank"],
        "names": ["ntr bharosa", "एनटीआर भरोसा", "pension"],
        "local": {"te": ("ఎన్టీఆర్ భరోసా పెన్షన్", "వృద్ధులు, వితంతువులు మరియు ఇతరులకు నెలవారీ పెన్షన్; జూలై 2024 లో నెలకు ₹4,000 కి పెంచారు",
                         "ఎన్టీఆర్ భరోసా పెన్షన్ కూడా చూడండి: వృద్ధులు, వితంతువుల కోసం.")},
    },
]
