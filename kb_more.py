"""
Verified facts (checked 9 Nov 2026) for the schemes in more_schemes.py, written to be spoken.
Merged into kb.KB at import time. Same placeholders as kb.py: {web}, {helpline}.
Hindi numbers are written as words (spoken by Timbre); English likewise.
"""

KB_MORE = {
    "pmegp": {
        "web": "kviconline.gov.in", "web_hi": "के वी आई सी की वेबसाइट", "web_en": "the KVIC PMEGP portal",
        "hi": {
            "explain": "पीएमईजीपी में नया काम-धंधा या छोटी फ़ैक्ट्री शुरू करने के लिए बैंक लोन मिलता है, और प्रोजेक्ट की लागत का "
                       "पंद्रह से पैंतीस प्रतिशत सरकार सब्सिडी के रूप में देती है। उत्पादन के लिए पचास लाख और सेवा के लिए बीस लाख "
                       "रुपये तक का प्रोजेक्ट बन सकता है।",
            "apply": "{web} पर पीएमईजीपी ई-पोर्टल में ऑनलाइन आवेदन कीजिए, या ज़िले के खादी ग्रामोद्योग या ज़िला उद्योग केंद्र जाइए।",
            "docs": "आधार कार्ड, प्रोजेक्ट रिपोर्ट, अगर हो तो जाति या श्रेणी का प्रमाण पत्र, और बड़े प्रोजेक्ट के लिए पढ़ाई का प्रमाण पत्र।",
            "who": "अठारह साल से ऊपर का कोई भी व्यक्ति जो नया काम शुरू करना चाहता है। दस लाख से बड़े उत्पादन प्रोजेक्ट या पाँच लाख से "
                   "बड़े सेवा प्रोजेक्ट के लिए आठवीं पास होना ज़रूरी है।",
            "not": "यह सिर्फ़ नए काम के लिए है। पहले से चल रहे धंधे को बढ़ाने के लिए नहीं, और जिसने किसी दूसरी सरकारी योजना में "
                   "सब्सिडी ली है उसे नहीं मिलती।",
            "money": "शहर में सामान्य वर्ग को लागत का पंद्रह प्रतिशत, गाँव में पच्चीस प्रतिशत। महिलाओं, अनुसूचित जाति, जनजाति, पिछड़े "
                     "वर्ग और अल्पसंख्यकों को शहर में पच्चीस और गाँव में पैंतीस प्रतिशत।",
            "cost": "सामान्य वर्ग को लागत का दस प्रतिशत और विशेष वर्ग को पाँच प्रतिशत खुद लगाना होता है, बाकी बैंक लोन देता है।",
            "online": "हाँ, {web} पर पूरा आवेदन ऑनलाइन होता है।",
        },
        "en": {
            "explain": "PMEGP gives a bank loan to start a new business or small unit, and the government pays fifteen to "
                       "thirty-five percent of the project cost as a subsidy. Projects can be up to fifty lakh for manufacturing "
                       "and twenty lakh for services.",
            "apply": "Apply online on {web}, or go to the district KVIC office or District Industries Centre.",
            "docs": "Aadhaar, a project report, a category certificate if you have one, and an education certificate for bigger projects.",
            "who": "Anyone above eighteen who wants to start a new unit. Projects above ten lakh in manufacturing or five lakh "
                   "in services need eighth pass.",
            "not": "Only for new units, not for growing an existing business, and not for people who already got a subsidy "
                   "under another government scheme.",
            "money": "General category: fifteen percent of the cost in cities, twenty-five in villages. Women, SC, ST, OBC and "
                     "minorities: twenty-five percent in cities and thirty-five in villages.",
            "cost": "You put in ten percent of the cost yourself, or five percent in the special categories; the bank lends the rest.",
            "online": "Yes, the whole application is online on {web}.",
        },
    },
    "kcc": {
        "web": None,
        "hi": {
            "explain": "किसान क्रेडिट कार्ड से खेती, पशुपालन या मछली पालन के लिए सस्ता लोन मिलता है। पाँच लाख रुपये तक का लोन मिल "
                       "सकता है, और तीन लाख तक समय पर चुकाने पर ब्याज सिर्फ़ चार प्रतिशत लगता है।",
            "apply": "अपने बैंक की शाखा, सहकारी बैंक या नज़दीकी सीएससी केंद्र पर फ़ॉर्म भरिए।",
            "docs": "आधार कार्ड, ज़मीन के कागज़ या बटाई का कागज़, फ़ोटो, और बैंक खाता।",
            "who": "ज़मीन वाले किसान, बटाईदार, किराये पर खेती करने वाले, और पशुपालन या मछली पालन करने वाले।",
            "money": "पाँच लाख रुपये तक का लोन। दो लाख तक कोई गारंटी नहीं चाहिए। अंतिम सीमा बैंक तय करता है।",
            "cost": "तीन लाख तक के लोन पर सात प्रतिशत ब्याज, और समय पर चुकाने पर तीन प्रतिशत की छूट, यानी सिर्फ़ चार प्रतिशत।",
        },
        "en": {
            "explain": "The Kisan Credit Card gives cheap loans for farming, animal husbandry or fisheries. You can get up to five "
                       "lakh, and on up to three lakh the interest is just four percent if you repay on time.",
            "apply": "Fill the form at your bank branch, a cooperative bank, or your nearest CSC.",
            "docs": "Aadhaar, land records or tenancy papers, a photo, and a bank account.",
            "who": "Farmers with land, tenant farmers, sharecroppers, and people in animal husbandry or fisheries.",
            "money": "Loans up to five lakh. No collateral up to two lakh. The bank decides your final limit.",
            "cost": "Seven percent interest on up to three lakh, with three percent off for paying on time, so four percent.",
        },
    },
    "pmfby": {
        "web": "pmfby.gov.in", "web_hi": "पीएम फसल बीमा की वेबसाइट", "web_en": "the PM Fasal Bima website",
        "hi": {
            "explain": "प्रधानमंत्री फसल बीमा योजना में सूखा, बाढ़, ओले या कीड़ों से फसल खराब होने पर बीमा मिलता है। किसान बहुत कम "
                       "प्रीमियम भरता है, बाकी सरकार देती है।",
            "apply": "हर सीज़न की आख़िरी तारीख से पहले अपने बैंक, सीएससी केंद्र या {web} पर फ़ॉर्म भरिए।",
            "docs": "आधार कार्ड, ज़मीन के कागज़ या बटाई का कागज़, बुवाई की जानकारी, और बैंक खाता।",
            "who": "सभी किसान, बटाईदार और किराये पर खेती करने वाले भी। यह अपनी मर्ज़ी से है।",
            "money": "फसल खराब होने पर बीमा राशि के हिसाब से नुकसान की भरपाई सीधे बैंक खाते में आती है।",
            "cost": "खरीफ़ की फसल पर बीमा राशि का दो प्रतिशत, रबी पर डेढ़ प्रतिशत, और नकदी या बागवानी फसल पर पाँच प्रतिशत।",
            "when": "हर सीज़न की अंतिम तारीख राज्य तय करता है, इसलिए बुवाई के समय ही बैंक या सीएससी पर पूछ लीजिए।",
            "online": "हाँ, {web} पर ऑनलाइन आवेदन होता है।",
        },
        "en": {
            "explain": "PM Fasal Bima insures your crop against drought, flood, hail or pests. The farmer pays a very small "
                       "premium and the government pays the rest.",
            "apply": "Fill the form at your bank, a CSC, or on {web} before each season's cut-off date.",
            "docs": "Aadhaar, land records or tenancy papers, sowing details, and a bank account.",
            "who": "All farmers, including tenants and sharecroppers. Joining is voluntary.",
            "money": "If the crop fails, compensation based on the sum insured is paid into your bank account.",
            "cost": "Two percent of the sum insured for kharif crops, one and a half for rabi, and five for commercial or horticulture crops.",
            "when": "Your state sets the cut-off date for each season, so ask at the bank or CSC when you sow.",
            "online": "Yes, you can apply online on {web}.",
        },
    },
    "udyam": {
        "web": "udyamregistration.gov.in", "web_hi": "उद्यम रजिस्ट्रेशन की सरकारी वेबसाइट", "web_en": "the Udyam registration website",
        "hi": {
            "explain": "उद्यम रजिस्ट्रेशन आपके काम-धंधे का मुफ़्त सरकारी रजिस्ट्रेशन है। इससे आपका धंधा एमएसएमई माना जाता है, और बैंक लोन में "
                       "प्राथमिकता और दूसरी सरकारी योजनाओं का फ़ायदा आसान होता है।",
            "apply": "{web} पर आधार नंबर से खुद मुफ़्त में रजिस्टर कीजिए, या नज़दीकी सीएससी केंद्र जाइए।",
            "docs": "आधार कार्ड, पैन कार्ड, और बैंक खाता।",
            "who": "दुकान, कारीगरी, सेवा या छोटा कारखाना चलाने वाला कोई भी, या जो नया धंधा शुरू कर रहा है।",
            "money": "यह सीधे पैसा नहीं देता, लेकिन इससे लोन और सरकारी योजनाएँ लेना आसान होता है।",
            "cost": "रजिस्ट्रेशन बिल्कुल मुफ़्त है। किसी एजेंट को पैसे मत दीजिए।",
            "online": "हाँ, {web} पर पूरा रजिस्ट्रेशन ऑनलाइन और मुफ़्त है।",
        },
        "en": {
            "explain": "Udyam registration is a free government registration for your business. It makes your business an MSME, "
                       "which helps with priority bank loans and other government schemes.",
            "apply": "Register yourself for free on {web} with your Aadhaar number, or go to your nearest CSC.",
            "docs": "Aadhaar, PAN, and a bank account.",
            "who": "Anyone running a shop, a craft, a service or a small unit, or starting a new business.",
            "money": "It doesn't pay money directly, but it makes loans and government schemes easier to get.",
            "cost": "Registration is completely free. Don't pay any agent.",
            "online": "Yes, registration on {web} is online and free.",
        },
    },
    "startup_india": {
        "web": "startupindia.gov.in", "web_hi": "स्टार्टअप इंडिया की वेबसाइट", "web_en": "the Startup India website",
        "hi": {
            "explain": "स्टार्टअप इंडिया में नए और अलग तरह के बिज़नेस को डीपीआईआईटी की मुफ़्त मान्यता मिलती है। इससे टैक्स में छूट, "
                       "आसान नियम, और इनक्यूबेटर के ज़रिए बीस लाख रुपये तक के सीड फ़ंड का मौका मिलता है।",
            "apply": "{web} पर मुफ़्त में आवेदन कीजिए।",
            "docs": "कंपनी, एलएलपी या रजिस्टर्ड पार्टनरशिप के कागज़, पैन कार्ड, और आपके आइडिया में क्या नया है उसकी जानकारी।",
            "who": "प्राइवेट लिमिटेड कंपनी, एलएलपी या रजिस्टर्ड पार्टनरशिप, जिसका आइडिया नया हो।",
            "not": "अकेले मालिक वाला धंधा, यानी प्रोप्राइटरशिप, इसमें नहीं आता।",
            "money": "मान्यता से सीधे पैसा नहीं मिलता। सीड फ़ंड में इनक्यूबेटर के ज़रिए बीस लाख तक का ग्रांट मिल सकता है।",
            "cost": "मान्यता के लिए कोई फ़ीस नहीं है।",
        },
        "en": {
            "explain": "Startup India gives free DPIIT recognition to new, innovative businesses. It brings tax benefits, easier "
                       "rules, and a chance at the Seed Fund of up to twenty lakh through incubators.",
            "apply": "Apply for free on {web}.",
            "docs": "Company, LLP or registered partnership papers, PAN, and a short note on what is new about your idea.",
            "who": "Private limited companies, LLPs and registered partnerships with an innovative idea.",
            "not": "Sole proprietorships are not covered.",
            "money": "Recognition itself pays nothing. The Seed Fund can give a grant of up to twenty lakh through an incubator.",
            "cost": "There is no fee for recognition.",
        },
    },
    "up_cm_yuva": {
        "web": None,
        "hi": {
            "explain": "मुख्यमंत्री युवा उद्यमी विकास अभियान में उत्तर प्रदेश के इक्कीस से चालीस साल के युवाओं को नया काम शुरू करने के लिए "
                       "पाँच लाख रुपये तक का बिना ब्याज और बिना गारंटी लोन मिलता है।",
            "apply": "ज़िला उद्योग केंद्र जाइए, या सीएम युवा पोर्टल पर ऑनलाइन आवेदन कीजिए।",
            "docs": "आधार कार्ड, उत्तर प्रदेश का निवास प्रमाण, कम से कम आठवीं पास का प्रमाण पत्र, प्रोजेक्ट का प्रस्ताव, और बैंक खाता।",
            "who": "उत्तर प्रदेश के इक्कीस से चालीस साल के युवा, जो कम से कम आठवीं पास हैं और नया काम शुरू करना चाहते हैं।",
            "money": "पहले चरण में पाँच लाख रुपये तक का लोन, समय पर चुकाने पर कोई ब्याज नहीं।",
            "cost": "समय पर किस्त चुकाने पर ब्याज सरकार भरती है, और कोई गारंटी नहीं चाहिए।",
        },
        "en": {
            "explain": "Under CM-YUVA, young people in Uttar Pradesh aged twenty-one to forty get an interest-free, "
                       "collateral-free loan of up to five lakh to start a business.",
            "apply": "Go to the District Industries Centre, or apply online on the CM-YUVA portal.",
            "docs": "Aadhaar, UP residence proof, at least eighth-pass certificate, a project proposal, and a bank account.",
            "who": "UP residents aged twenty-one to forty, at least eighth pass, starting a new business.",
            "money": "A first loan of up to five lakh, with no interest if you repay on time.",
            "cost": "The government pays the interest if you repay on time, and no collateral is needed.",
        },
    },
    "up_kanya_sumangala": {
        "web": "mksy.up.gov.in", "web_hi": "कन्या सुमंगला की वेबसाइट", "web_en": "the Kanya Sumangala website",
        "hi": {
            "explain": "मुख्यमंत्री कन्या सुमंगला योजना में उत्तर प्रदेश की बेटियों को जन्म से उच्च शिक्षा तक छह किस्तों में कुल पच्चीस हज़ार "
                       "रुपये मिलते हैं।",
            "apply": "{web} पर ऑनलाइन आवेदन कीजिए, या नज़दीकी सीएससी केंद्र जाइए।",
            "docs": "बेटी का जन्म प्रमाण पत्र, माता या पिता का आधार, आय प्रमाण पत्र, बैंक खाता, और फ़ोटो।",
            "who": "उत्तर प्रदेश के परिवार, जिनकी सालाना कमाई तीन लाख रुपये तक है। एक परिवार की ज़्यादा से ज़्यादा दो बेटियाँ।",
            "money": "कुल पच्चीस हज़ार रुपये, जन्म, टीकाकरण, और पहली, छठी, नौवीं कक्षा और उच्च शिक्षा में दाख़िले पर किस्तों में।",
            "cost": "इसमें कुछ भी जमा नहीं करना है।",
        },
        "en": {
            "explain": "Under Kanya Sumangala, daughters in Uttar Pradesh get twenty-five thousand rupees in six instalments, from "
                       "birth to higher education.",
            "apply": "Apply online on {web}, or go to your nearest CSC.",
            "docs": "Daughter's birth certificate, a parent's Aadhaar, income certificate, bank account, and a photo.",
            "who": "UP families earning up to three lakh a year. At most two daughters per family.",
            "money": "Twenty-five thousand rupees in total, paid in stages at birth, vaccination, school admissions and higher education.",
            "cost": "You don't pay anything.",
        },
    },
    "br_mahila_rojgar": {
        "web": None,
        "hi": {
            "explain": "मुख्यमंत्री महिला रोज़गार योजना में बिहार की महिलाओं को अपना रोज़गार शुरू करने के लिए पहले दस हज़ार रुपये मिलते हैं, "
                       "और छह महीने बाद समीक्षा में ज़रूरत हो तो दो लाख रुपये तक की और मदद।",
            "apply": "अपने जीविका स्वयं सहायता समूह के ज़रिए या प्रखंड कार्यालय में आवेदन कीजिए।",
            "docs": "आधार कार्ड, बैंक खाता, और जीविका समूह की सदस्यता।",
            "who": "बिहार की महिलाएँ, परिवार से एक महिला, जीविका स्वयं सहायता समूह के ज़रिए।",
            "money": "पहली किस्त दस हज़ार रुपये, और काम ठीक चलने पर दो लाख रुपये तक की और मदद।",
            "cost": "इसमें कुछ भी जमा नहीं करना है।",
        },
        "en": {
            "explain": "Under Bihar's Mahila Rozgar Yojana, women get ten thousand rupees to start their own livelihood, and up to "
                       "two lakh more after a review six months later.",
            "apply": "Apply through your JEEViKA self-help group or at the block office.",
            "docs": "Aadhaar, a bank account, and JEEViKA group membership.",
            "who": "Women in Bihar, one per family, through JEEViKA self-help groups.",
            "money": "Ten thousand rupees first, and up to two lakh more if the work is going well.",
            "cost": "You don't pay anything.",
        },
    },
    "br_vridhjan": {
        "web": "sspmis.bihar.gov.in", "web_hi": "बिहार सामाजिक सुरक्षा पेंशन की वेबसाइट", "web_en": "the Bihar pension website",
        "hi": {
            "explain": "मुख्यमंत्री वृद्धजन पेंशन योजना में बिहार के साठ साल से ऊपर के हर बुज़ुर्ग को हर महीने ग्यारह सौ रुपये पेंशन मिलती है।",
            "apply": "{web} पर, आरटीपीएस काउंटर पर, या प्रखंड कार्यालय में आवेदन कीजिए।",
            "docs": "आधार कार्ड, उम्र का प्रमाण, बिहार का निवास प्रमाण, और बैंक खाता।",
            "who": "बिहार के साठ साल या उससे ज़्यादा उम्र के लोग।",
            "not": "जो पहले से सरकारी पेंशन ले रहे हैं, उन्हें नहीं मिलती।",
            "money": "हर महीने ग्यारह सौ रुपये।",
            "cost": "इसमें कुछ भी जमा नहीं करना है।",
        },
        "en": {
            "explain": "Under Bihar's Vridhjan Pension, everyone in Bihar aged sixty or more gets eleven hundred rupees a month.",
            "apply": "Apply on {web}, at the RTPS counter, or at the block office.",
            "docs": "Aadhaar, age proof, Bihar residence proof, and a bank account.",
            "who": "Bihar residents aged sixty or more.",
            "not": "Not for people already getting a government pension.",
            "money": "Eleven hundred rupees every month.",
            "cost": "You don't pay anything.",
        },
    },
    "mh_ladki_bahin": {
        "web": "ladakibahin.maharashtra.gov.in", "web_hi": "लाडकी बहीण की वेबसाइट", "web_en": "the Ladki Bahin website",
        "hi": {
            "explain": "माझी लाडकी बहीण योजना में महाराष्ट्र की इक्कीस से साठ साल की महिलाओं को हर महीने पंद्रह सौ रुपये मिलते हैं, "
                       "अगर परिवार की सालाना कमाई ढाई लाख रुपये तक है।",
            "apply": "{web} पर, अपनी आंगनवाड़ी सेविका के पास, या वार्ड कार्यालय में आवेदन कीजिए।",
            "docs": "आधार कार्ड, महाराष्ट्र का निवास प्रमाण, आय प्रमाण पत्र या राशन कार्ड, और आधार से जुड़ा बैंक खाता।",
            "who": "महाराष्ट्र की इक्कीस से साठ साल की महिलाएँ, जिनके परिवार की कमाई ढाई लाख रुपये साल तक है।",
            "not": "इनकम टैक्स भरने वाले परिवारों की महिलाओं को नहीं मिलता।",
            "money": "हर महीने पंद्रह सौ रुपये, सीधे बैंक खाते में।",
            "cost": "इसमें कुछ भी जमा नहीं करना है। बस बैंक खाता आधार से जुड़ा और ई-केवाईसी पूरा होना चाहिए।",
        },
        "en": {
            "explain": "Under Majhi Ladki Bahin, women in Maharashtra aged twenty-one to sixty get fifteen hundred rupees a month, "
                       "if the family earns up to two and a half lakh a year.",
            "apply": "Apply on {web}, with your Anganwadi worker, or at the ward office.",
            "docs": "Aadhaar, Maharashtra residence proof, income certificate or ration card, and an Aadhaar-linked bank account.",
            "who": "Women in Maharashtra aged twenty-one to sixty, from families earning up to two and a half lakh a year.",
            "not": "Women from income-tax-paying families are not covered.",
            "money": "Fifteen hundred rupees every month, straight into the bank account.",
            "cost": "You don't pay anything. The bank account just needs to be linked to Aadhaar with e-KYC done.",
        },
    },
    "mh_namo_shetkari": {
        "web": None,
        "hi": {
            "explain": "नमो शेतकरी महासन्मान निधी में महाराष्ट्र सरकार पीएम किसान वाले किसानों को साल के छह हज़ार रुपये और देती है, "
                       "यानी कुल बारह हज़ार रुपये।",
            "apply": "अलग से फ़ॉर्म नहीं भरना है। जो किसान पीएम किसान में हैं, उन्हें अपने आप मिलता है। बस ई-केवाईसी और आधार से "
                     "बैंक खाता जुड़ा होना चाहिए।",
            "docs": "वही जो पीएम किसान में लगते हैं: आधार, ज़मीन के कागज़, और आधार से जुड़ा बैंक खाता।",
            "who": "महाराष्ट्र के वे किसान जिन्हें पीएम किसान का पैसा मिलता है।",
            "money": "साल के छह हज़ार रुपये, दो-दो हज़ार की तीन किस्तों में।",
            "cost": "इसमें कुछ भी जमा नहीं करना है।",
        },
        "en": {
            "explain": "Under Namo Shetkari, the Maharashtra government gives PM-KISAN farmers six thousand rupees a year more, "
                       "so twelve thousand in total.",
            "apply": "No separate form. Farmers in PM-KISAN get it automatically, as long as e-KYC is done and the bank account "
                     "is linked to Aadhaar.",
            "docs": "The same as PM-KISAN: Aadhaar, land records, and an Aadhaar-linked bank account.",
            "who": "Farmers in Maharashtra who receive PM-KISAN.",
            "money": "Six thousand rupees a year, in three instalments of two thousand.",
            "cost": "You don't pay anything.",
        },
    },
    "wb_annapurna": {
        "web": None,
        "hi": {
            "explain": "अन्नपूर्णा भंडार में पश्चिम बंगाल की पच्चीस से साठ साल की महिलाओं को हर महीने तीन हज़ार रुपये मिलते हैं। जून दो "
                       "हज़ार छब्बीस से यह लक्ष्मीर भंडार की जगह आई है।",
            "apply": "अपने प्रखंड या नगरपालिका कार्यालय में, या सरकारी कैंप में आवेदन कीजिए।",
            "docs": "आधार कार्ड, राशन कार्ड, और आधार से जुड़ा बैंक खाता।",
            "who": "पश्चिम बंगाल की पच्चीस से साठ साल की महिलाएँ। लक्ष्मीर भंडार वाली महिलाओं को इसमें जोड़ दिया गया है।",
            "money": "हर महीने तीन हज़ार रुपये, सीधे बैंक खाते में।",
            "cost": "इसमें कुछ भी जमा नहीं करना है।",
        },
        "en": {
            "explain": "Under Annapurna Bhandar, women in West Bengal aged twenty-five to sixty get three thousand rupees a month. "
                       "It replaced Lakshmir Bhandar in June twenty twenty-six.",
            "apply": "Apply at your block or municipality office, or at a government camp.",
            "docs": "Aadhaar, ration card, and an Aadhaar-linked bank account.",
            "who": "Women in West Bengal aged twenty-five to sixty. Lakshmir Bhandar members were moved over.",
            "money": "Three thousand rupees every month, straight into the bank account.",
            "cost": "You don't pay anything.",
        },
    },
    "tn_kmut": {
        "web": None,
        "hi": {
            "explain": "कलैञर मगलिर उरिमै तोगै में तमिलनाडु में परिवार की मुखिया महिला को हर महीने एक हज़ार रुपये मिलते हैं। नई सरकार ने "
                       "इसे पच्चीस सौ करने का वादा किया है, पर अभी एक हज़ार ही मिल रहे हैं।",
            "apply": "अपने तालुक कार्यालय में, या राशन दुकान पर लगने वाले कैंप में आवेदन कीजिए।",
            "docs": "परिवार का राशन कार्ड, आधार, और बैंक खाता।",
            "who": "तमिलनाडु में इक्कीस साल से ऊपर की, परिवार की मुखिया महिलाएँ, जिनके परिवार की कमाई ढाई लाख रुपये साल तक है।",
            "money": "हर महीने एक हज़ार रुपये, सीधे बैंक खाते में।",
            "cost": "इसमें कुछ भी जमा नहीं करना है।",
        },
        "en": {
            "explain": "Under Kalaignar Magalir Urimai Thogai, the woman head of the family in Tamil Nadu gets one thousand rupees "
                       "a month. The new government has promised twenty-five hundred, but one thousand is what is paid now.",
            "apply": "Apply at your taluk office, or at the scheme's camp at the ration shop.",
            "docs": "Family ration card, Aadhaar, and a bank account.",
            "who": "Women heads of family in Tamil Nadu, aged twenty-one or more, from families earning up to two and a half lakh a year.",
            "money": "One thousand rupees every month, straight into the bank account.",
            "cost": "You don't pay anything.",
        },
    },
    "ka_gruha_lakshmi": {
        "web": "sevasindhugs.karnataka.gov.in", "web_hi": "सेवा सिंधु की वेबसाइट", "web_en": "the Seva Sindhu website",
        "hi": {
            "explain": "गृह लक्ष्मी योजना में कर्नाटक में घर की मुखिया महिला को हर महीने दो हज़ार रुपये मिलते हैं।",
            "apply": "{web} पर, या ग्राम वन, कर्नाटक वन या बापूजी केंद्र पर आवेदन कीजिए।",
            "docs": "राशन कार्ड, आधार, और आधार से जुड़ा बैंक खाता।",
            "who": "कर्नाटक में राशन कार्ड पर घर की मुखिया के रूप में दर्ज महिला।",
            "not": "अगर महिला या उसके पति इनकम टैक्स या जीएसटी रिटर्न भरते हैं, तो नहीं मिलता।",
            "money": "हर महीने दो हज़ार रुपये, सीधे बैंक खाते में।",
            "cost": "इसमें कुछ भी जमा नहीं करना है।",
        },
        "en": {
            "explain": "Under Gruha Lakshmi, the woman head of the household in Karnataka gets two thousand rupees a month.",
            "apply": "Apply on {web}, or at a Grama One, Karnataka One or Bapuji centre.",
            "docs": "Ration card, Aadhaar, and an Aadhaar-linked bank account.",
            "who": "The woman named as head of the household on a Karnataka ration card.",
            "not": "Not if the woman or her husband pays income tax or files GST returns.",
            "money": "Two thousand rupees every month, straight into the bank account.",
            "cost": "You don't pay anything.",
        },
    },
    "mp_ladli_behna": {
        "web": None,
        "hi": {
            "explain": "लाडली बहना योजना में मध्य प्रदेश की इक्कीस से साठ साल की महिलाओं को हर महीने पंद्रह सौ रुपये मिलते हैं। नए नाम "
                       "सिर्फ़ ख़ास अभियानों में जुड़ते हैं।",
            "apply": "अपनी ग्राम पंचायत या वार्ड कार्यालय में पूछिए कि नए नाम जुड़ने का कैंप कब लगेगा।",
            "docs": "समग्र आईडी, आधार कार्ड, और आधार से जुड़ा बैंक खाता।",
            "who": "मध्य प्रदेश की इक्कीस से साठ साल की महिलाएँ, जिनके परिवार की कमाई ढाई लाख रुपये साल तक है।",
            "money": "हर महीने पंद्रह सौ रुपये, सीधे बैंक खाते में।",
            "cost": "इसमें कुछ भी जमा नहीं करना है।",
        },
        "en": {
            "explain": "Under Ladli Behna, women in Madhya Pradesh aged twenty-one to sixty get fifteen hundred rupees a month. "
                       "New names are added only in special drives.",
            "apply": "Ask at your gram panchayat or ward office when the next registration camp is.",
            "docs": "Samagra ID, Aadhaar, and an Aadhaar-linked bank account.",
            "who": "Women in Madhya Pradesh aged twenty-one to sixty, from families earning up to two and a half lakh a year.",
            "money": "Fifteen hundred rupees every month, straight into the bank account.",
            "cost": "You don't pay anything.",
        },
    },
    "rj_maa": {
        "web": None,
        "hi": {
            "explain": "मुख्यमंत्री आयुष्मान आरोग्य योजना, यानी मा योजना, में राजस्थान के परिवारों को साल में पच्चीस लाख रुपये तक का कैशलेस "
                       "इलाज मिलता है।",
            "apply": "नज़दीकी ई-मित्र केंद्र पर जन आधार कार्ड से रजिस्टर कीजिए।",
            "docs": "जन आधार कार्ड और आधार कार्ड।",
            "who": "राजस्थान के परिवार। कई परिवारों के लिए मुफ़्त है, बाकियों को सालाना प्रीमियम भरना पड़ सकता है।",
            "money": "हर परिवार को साल में पच्चीस लाख रुपये तक का कैशलेस इलाज।",
        },
        "en": {
            "explain": "The MAA scheme gives families in Rajasthan cashless hospital treatment of up to twenty-five lakh rupees a year.",
            "apply": "Register with your Jan Aadhaar card at the nearest e-Mitra centre.",
            "docs": "Jan Aadhaar card and Aadhaar.",
            "who": "Families in Rajasthan. Free for many families; others may need to pay a yearly premium.",
            "money": "Cashless treatment of up to twenty-five lakh a year per family.",
        },
    },
    "ka_yuva_nidhi": {
        "web": "sevasindhugs.karnataka.gov.in", "web_hi": "सेवा सिंधु की वेबसाइट", "web_en": "the Seva Sindhu website",
        "hi": {
            "explain": "युवा निधि में कर्नाटक के बेरोज़गार ग्रेजुएट को हर महीने तीन हज़ार रुपये और डिप्लोमा वालों को पंद्रह सौ रुपये, दो "
                       "साल तक मिलते हैं।",
            "apply": "{web} पर ऑनलाइन आवेदन कीजिए।",
            "docs": "डिग्री या डिप्लोमा का प्रमाण पत्र, आधार, कर्नाटक का निवास प्रमाण, और बैंक खाता।",
            "who": "दो हज़ार बाईस-तेईस या उसके बाद पास हुए ग्रेजुएट या डिप्लोमा वाले, जो छह महीने से बेरोज़गार हैं।",
            "money": "ग्रेजुएट को हर महीने तीन हज़ार, डिप्लोमा वालों को पंद्रह सौ रुपये, दो साल तक या नौकरी मिलने तक।",
        },
        "en": {
            "explain": "Under Yuva Nidhi, unemployed graduates in Karnataka get three thousand rupees a month, and diploma "
                       "holders fifteen hundred, for up to two years.",
            "apply": "Apply online on {web}.",
            "docs": "Degree or diploma certificate, Aadhaar, Karnataka residence proof, and a bank account.",
            "who": "Graduates or diploma holders who passed in twenty twenty-two-twenty-three or later and have been unemployed for six months.",
            "money": "Three thousand a month for graduates and fifteen hundred for diploma holders, for up to two years or until you get a job.",
        },
    },
}

# words people use to name these schemes in a question (Hindi / English / Hinglish)
SCHEME_NAMES_MORE = [
    ("pmegp", ["pmegp", "पीएमईजीपी", "rozgar srijan", "रोज़गार सृजन", "रोजगार सृजन"]),
    ("kcc", ["kisan credit", "kcc", "किसान क्रेडिट", "credit card"]),
    ("pmfby", ["fasal bima", "फसल बीमा", "crop insurance", "pmfby"]),
    ("udyam", ["udyam", "उद्यम", "msme", "एमएसएमई"]),
    ("startup_india", ["startup", "स्टार्टअप", "dpiit"]),
    ("up_cm_yuva", ["cm yuva", "yuva udyami", "युवा उद्यमी", "सीएम युवा"]),
    ("up_kanya_sumangala", ["kanya sumangala", "sumangala", "कन्या सुमंगला", "सुमंगला"]),
    ("br_mahila_rojgar", ["mahila rozgar", "mahila rojgar", "महिला रोज़गार", "महिला रोजगार", "jeevika", "जीविका"]),
    ("br_vridhjan", ["vridhjan", "vridha pension", "वृद्धजन", "वृद्धा पेंशन", "old age pension"]),
    ("mh_ladki_bahin", ["ladki bahin", "ladki behan", "लाडकी बहीण", "लाडकी बहिन", "लाडकी"]),
    ("mh_namo_shetkari", ["namo shetkari", "नमो शेतकरी", "shetkari", "शेतकरी सन्मान"]),
    ("mp_ladli_behna", ["ladli behna", "ladli bahna", "लाडली बहना", "लाडली"]),
    ("rj_maa", ["maa yojana", "मा योजना", "आयुष्मान आरोग्य", "ayushman arogya"]),
    ("wb_annapurna", ["annapurna", "अन्नपूर्णा", "lakshmir bhandar", "लक्ष्मीर भंडार"]),
    ("tn_kmut", ["magalir", "urimai", "मगलिर", "उरिमै"]),
    ("ka_gruha_lakshmi", ["gruha lakshmi", "griha lakshmi", "गृह लक्ष्मी", "गृहलक्ष्मी"]),
    ("ka_yuva_nidhi", ["yuva nidhi", "युवा निधि"]),
]
