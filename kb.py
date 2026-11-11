"""
Verified facts per scheme, written to be spoken. The follow-up chat answers ONLY from here.

Placeholders: {web} -> website (shown as a URL, spoken as words), {helpline} -> number (spoken digit by digit).
Intents: explain, apply, docs, who, not, money, cost, when, online, family, helpline
Sources: see README. Helplines included only where confirmed on an official site.
"""

KB = {
    "pm_kisan": {
        "web": "pmkisan.gov.in", "web_hi": "पीएम किसान डॉट जीओवी डॉट इन", "web_en": "pm kisan dot gov dot in",
        "helpline": "155261",
        "hi": {
            "explain": "पीएम किसान सम्मान निधि में सरकार ज़मीन वाले किसान परिवारों को हर साल छह हज़ार रुपये देती है। "
                       "यह पैसा दो-दो हज़ार की तीन किस्तों में, लगभग हर चार महीने में, सीधे बैंक खाते में आता है।",
            "apply": "नज़दीकी सीएससी केंद्र जाइए, या {web} पर न्यू फ़ार्मर रजिस्ट्रेशन में आधार नंबर डालकर खुद फ़ॉर्म भरिए। "
                     "उसके बाद ई-केवाईसी ज़रूर करवाइए, वरना किस्त रुक सकती है।",
            "docs": "आधार कार्ड, आपके नाम की ज़मीन के कागज़ जैसे खतौनी, और आधार से जुड़ा बैंक खाता।",
            "who": "जिन किसान परिवारों के नाम पर खेती की ज़मीन है, वो इसके हकदार हैं।",
            "not": "इनकम टैक्स भरने वाले, सरकारी कर्मचारी, दस हज़ार रुपये महीने से ज़्यादा पेंशन पाने वाले, "
                   "और डॉक्टर, वकील, सीए जैसे पेशेवर इसमें नहीं आते।",
            "money": "साल के छह हज़ार रुपये, दो-दो हज़ार की तीन किस्तों में।",
            "cost": "इसमें आपको कुछ भी जमा नहीं करना है।",
            "when": "किस्त लगभग हर चार महीने में आती है। अपना स्टेटस {web} पर बेनिफ़िशियरी स्टेटस में देख सकते हैं।",
            "online": "हाँ, {web} पर आधार से रजिस्ट्रेशन और ओटीपी से ई-केवाईसी खुद कर सकते हैं।",
            "family": "एक परिवार में, यानी पति, पत्नी और नाबालिग बच्चों में, एक ही व्यक्ति को यह पैसा मिलता है।",
        },
        "en": {
            "explain": "Under PM-KISAN the government gives land-owning farmer families six thousand rupees a year, "
                       "in three instalments of two thousand, roughly every four months, straight into the bank account.",
            "apply": "Go to your nearest CSC, or register yourself on {web} under New Farmer Registration with your Aadhaar. "
                     "Then complete e-KYC, otherwise instalments can stop.",
            "docs": "Aadhaar, land records in your name, and a bank account linked to Aadhaar.",
            "who": "Farmer families who have cultivable land in their name.",
            "not": "Income-tax payers, government employees, pensioners getting over ten thousand a month, "
                   "and professionals like doctors, lawyers and CAs are excluded.",
            "money": "Six thousand rupees a year, in three instalments of two thousand.",
            "cost": "You don't pay anything.",
            "when": "Instalments come roughly every four months. Check your status on {web} under Beneficiary Status.",
            "online": "Yes, you can register on {web} with Aadhaar and do OTP-based e-KYC yourself.",
            "family": "Only one person per family, meaning husband, wife and minor children, gets the money.",
        },
    },
    "pm_kmy": {
        "web": None,
        "hi": {
            "explain": "पीएम किसान मानधन छोटे किसानों की पेंशन योजना है। आप हर महीने पचपन से दो सौ रुपये जमा करते हैं, "
                       "उतना ही सरकार डालती है, और साठ साल के बाद हर महीने तीन हज़ार रुपये पेंशन मिलती है।",
            "apply": "आधार और बैंक पासबुक लेकर नज़दीकी सीएससी केंद्र जाइए। वहीं रजिस्ट्रेशन होगा।",
            "docs": "आधार कार्ड, बचत बैंक खाता, और ज़मीन के कागज़।",
            "who": "अठारह से चालीस साल के किसान, जिनके पास दो हेक्टेयर, यानी लगभग पाँच एकड़ तक ज़मीन है।",
            "not": "जो पहले से एनपीएस, ईएसआईसी या ईपीएफ़ओ जैसी किसी योजना में हैं, वो इसमें नहीं आते।",
            "money": "साठ साल के बाद हर महीने तीन हज़ार रुपये पेंशन, ज़िंदगी भर।",
            "cost": "उम्र के हिसाब से पचपन से दो सौ रुपये महीना। अठारह साल में पचपन रुपये, चालीस साल में दो सौ रुपये। "
                    "उतना ही सरकार भी डालती है।",
            "when": "पेंशन साठ साल की उम्र से शुरू होती है, तब तक हर महीने जमा करना होता है।",
            "family": "पति और पत्नी दोनों छोटे किसान हैं तो दोनों अलग-अलग जुड़ सकते हैं। "
                      "किसान की मृत्यु के बाद पति या पत्नी को आधी पेंशन मिलती है।",
        },
        "en": {
            "explain": "PM Kisan Maan-Dhan is a pension for small farmers. You save fifty-five to two hundred rupees a month, "
                       "the government adds the same, and after sixty you get three thousand rupees a month.",
            "apply": "Take your Aadhaar and bank passbook to the nearest CSC. They register you there.",
            "docs": "Aadhaar, a savings bank account, and land records.",
            "who": "Farmers aged eighteen to forty with up to two hectares, about five acres, of land.",
            "not": "People already in NPS, ESIC or EPFO are excluded.",
            "money": "Three thousand rupees a month for life after sixty.",
            "cost": "Fifty-five to two hundred rupees a month depending on your age when you join. "
                    "The government matches it.",
            "when": "The pension starts at sixty. Until then you contribute every month.",
            "family": "If husband and wife are both small farmers, both can join separately. "
                      "After the farmer's death the spouse gets half the pension.",
        },
    },
    "pm_svanidhi": {
        "web": "pmsvanidhi.mohua.gov.in", "web_hi": "पीएम स्वनिधि की वेबसाइट", "web_en": "the PM SVANidhi website",
        "hi": {
            "explain": "पीएम स्वनिधि ठेला, रेहड़ी और फेरी वालों के लिए बिना गारंटी का लोन है। पहले पंद्रह हज़ार, "
                       "उसे समय पर चुकाने पर पच्चीस हज़ार, और फिर पचास हज़ार रुपये का लोन मिलता है।",
            "apply": "{web} पर मोबाइल नंबर और ओटीपी से फ़ॉर्म भरिए, या किसी बैंक या सीएससी केंद्र पर जाइए।",
            "docs": "आधार कार्ड, मोबाइल नंबर, बैंक खाता, और नगर निकाय से मिला वेंडिंग सर्टिफ़िकेट या सिफ़ारिश पत्र।",
            "who": "शहरों, कस्बों और उनके आसपास सड़क पर सामान बेचने वाले वेंडर।",
            "not": "यह सिर्फ़ स्ट्रीट वेंडर के लिए है। पक्की दुकान वालों के लिए मुद्रा योजना है।",
            "money": "पहला लोन पंद्रह हज़ार, दूसरा पच्चीस हज़ार, तीसरा पचास हज़ार रुपये। समय पर चुकाने पर ब्याज पर "
                     "सात प्रतिशत सब्सिडी, और डिजिटल पेमेंट पर सोलह सौ रुपये तक कैशबैक।",
            "cost": "कोई गारंटी नहीं चाहिए। पहला लोन लगभग बारह महीने में किस्तों में चुकाना होता है।",
            "when": "इस योजना में लोन इकतीस मार्च दो हज़ार तीस तक मिलेंगे।",
            "online": "हाँ, {web} पर ऑनलाइन आवेदन होता है।",
        },
        "en": {
            "explain": "PM SVANidhi gives street vendors collateral-free loans: fifteen thousand first, "
                       "twenty-five thousand after repaying on time, then fifty thousand.",
            "apply": "Apply on {web} with your mobile number and OTP, or go to a bank or CSC.",
            "docs": "Aadhaar, mobile number, bank account, and a vending certificate or letter of recommendation "
                    "from the urban local body.",
            "who": "Street vendors in cities, towns and peri-urban areas.",
            "not": "It's only for street vendors. Shop owners should look at Mudra instead.",
            "money": "Loans of fifteen, twenty-five and fifty thousand. Seven percent interest subsidy if you repay on time, "
                     "and up to sixteen hundred rupees cashback on digital payments.",
            "cost": "No collateral. The first loan is repaid in instalments over about twelve months.",
            "when": "Loans are available until thirty-first March twenty thirty.",
            "online": "Yes, you can apply online on {web}.",
        },
    },
    "pm_vishwakarma": {
        "web": "pmvishwakarma.gov.in", "web_hi": "पीएम विश्वकर्मा की वेबसाइट", "web_en": "the PM Vishwakarma website",
        "hi": {
            "explain": "पीएम विश्वकर्मा अठारह पारंपरिक हुनर वाले कारीगरों के लिए है, जैसे बढ़ई, लोहार, दर्ज़ी, नाई, कुम्हार। "
                       "इसमें ट्रेनिंग, पंद्रह हज़ार का टूलकिट, और पाँच प्रतिशत ब्याज पर तीन लाख तक का लोन मिलता है।",
            "apply": "आधार, मोबाइल और बैंक खाते के साथ नज़दीकी सीएससी केंद्र जाइए। वहाँ {web} पर रजिस्ट्रेशन होगा, "
                     "फिर ग्राम पंचायत या नगर निकाय से जाँच होगी।",
            "docs": "आधार कार्ड, मोबाइल नंबर, बैंक खाता, और राशन कार्ड।",
            "who": "अठारह साल से ऊपर के कारीगर, जो इन अठारह हुनर में से किसी में अपना काम खुद करते हैं।",
            "not": "परिवार में एक ही व्यक्ति ले सकता है। जिनके परिवार में सरकारी नौकरी है, या जिन्होंने पिछले पाँच साल में "
                   "मुद्रा, स्वनिधि या पीएमईजीपी जैसा लोन लिया है, वो इसमें नहीं आते।",
            "money": "ट्रेनिंग में पाँच सौ रुपये रोज़, पंद्रह हज़ार का टूलकिट, और पहले एक लाख फिर दो लाख का लोन, "
                     "पाँच प्रतिशत ब्याज पर।",
            "cost": "लोन पर सिर्फ़ पाँच प्रतिशत ब्याज है, और कोई गारंटी नहीं चाहिए।",
            "when": "पहले ट्रेनिंग, फिर टूलकिट, फिर पहला लोन। पहला लोन अठारह महीने में और दूसरा तीस महीने में चुकाना होता है।",
            "online": "रजिस्ट्रेशन सीएससी केंद्र से {web} पर होता है।",
            "family": "परिवार में से सिर्फ़ एक सदस्य इस योजना में रजिस्टर हो सकता है।",
        },
        "en": {
            "explain": "PM Vishwakarma is for artisans in eighteen traditional trades like carpenters, blacksmiths, tailors, "
                       "barbers and potters. You get training, a fifteen thousand rupee toolkit, and loans up to three lakh "
                       "at five percent.",
            "apply": "Go to the nearest CSC with Aadhaar, mobile and bank details. They register you on {web}, "
                     "then the gram panchayat or urban body verifies you.",
            "docs": "Aadhaar, mobile number, bank account, and ration card.",
            "who": "Artisans aged eighteen or more, self-employed in one of the eighteen trades.",
            "not": "Only one member per family. Not for families with a government employee, or anyone who took a similar "
                   "government loan like Mudra, SVANidhi or PMEGP in the last five years.",
            "money": "Five hundred rupees a day during training, a fifteen thousand toolkit, and loans of one lakh then two lakh "
                     "at five percent.",
            "cost": "Just five percent interest on the loan, with no collateral.",
            "when": "Training first, then the toolkit, then the first loan. The first loan is repaid over eighteen months, "
                    "the second over thirty.",
            "online": "Registration is done on {web} through a CSC.",
            "family": "Only one member of a family can register.",
        },
    },
    "mudra": {
        "web": "jansamarth.in", "web_hi": "जनसमर्थ पोर्टल", "web_en": "the JanSamarth portal",
        "hi": {
            "explain": "मुद्रा योजना में दुकान या छोटे धंधे के लिए बिना गारंटी लोन मिलता है। शिशु में पचास हज़ार तक, "
                       "किशोर में पाँच लाख तक, और तरुण में दस लाख रुपये तक।",
            "apply": "किसी भी बैंक की शाखा में जाइए, या {web} पर ऑनलाइन आवेदन कीजिए।",
            "docs": "आधार, पैन कार्ड, धंधे का सबूत, बैंक स्टेटमेंट, और बड़े लोन के लिए बिज़नेस प्लान।",
            "who": "खेती के अलावा कोई भी छोटा कमाई वाला धंधा करने वाले, जैसे दुकान, सर्विस या छोटा कारखाना।",
            "not": "सीधे खेती के लिए यह लोन नहीं है। बीस लाख वाला तरुण प्लस लोन सिर्फ़ उन्हें मिलता है जो पहले तरुण लोन चुका चुके हैं।",
            "money": "शिशु पचास हज़ार तक, किशोर पाँच लाख तक, तरुण दस लाख तक, और तरुण प्लस बीस लाख तक।",
            "cost": "कोई गारंटी नहीं चाहिए। ब्याज दर बैंक तय करता है।",
            "online": "हाँ, {web} पर ऑनलाइन आवेदन होता है।",
        },
        "en": {
            "explain": "Mudra gives collateral-free loans for a shop or small business: Shishu up to fifty thousand, "
                       "Kishor up to five lakh, and Tarun up to ten lakh.",
            "apply": "Go to any bank branch, or apply online on {web}.",
            "docs": "Aadhaar, PAN, proof of business, bank statements, and a business plan for bigger loans.",
            "who": "Anyone running a small non-farm business, like a shop, a service or a small unit.",
            "not": "It isn't for farming itself. The twenty lakh Tarun Plus loan is only for people who have repaid a Tarun loan.",
            "money": "Shishu up to fifty thousand, Kishor up to five lakh, Tarun up to ten lakh, Tarun Plus up to twenty lakh.",
            "cost": "No collateral. The bank sets the interest rate.",
            "online": "Yes, you can apply online on {web}.",
        },
    },
    "pm_sym": {
        "web": None,
        "hi": {
            "explain": "श्रम योगी मानधन असंगठित मज़दूरों की पेंशन योजना है। आप हर महीने पचपन से दो सौ रुपये जमा करते हैं, "
                       "उतना ही सरकार डालती है, और साठ साल के बाद हर महीने तीन हज़ार रुपये पेंशन मिलती है।",
            "apply": "आधार और बैंक पासबुक लेकर नज़दीकी सीएससी केंद्र जाइए। उसके बाद हर महीने पैसा खाते से अपने आप कटेगा।",
            "docs": "आधार कार्ड, बचत या जनधन बैंक खाता, और मोबाइल नंबर। कमाई का सर्टिफ़िकेट नहीं चाहिए, खुद घोषणा करनी होती है।",
            "who": "अठारह से चालीस साल के असंगठित मज़दूर, जैसे रेहड़ी वाले, रिक्शा चालक, घरेलू कामगार, "
                   "जिनकी कमाई पंद्रह हज़ार रुपये महीना या उससे कम है।",
            "not": "इनकम टैक्स भरने वाले, और जो ईपीएफ़, ईएसआईसी या एनपीएस में हैं।",
            "money": "साठ साल के बाद हर महीने तीन हज़ार रुपये पेंशन।",
            "cost": "अठारह साल में पचपन रुपये महीना, पच्चीस में अस्सी, तीस में एक सौ पाँच, पैंतीस में एक सौ पचास, "
                    "और चालीस में दो सौ रुपये। उतना ही सरकार भी डालती है।",
            "when": "साठ साल की उम्र तक हर महीने जमा करना होता है, फिर पेंशन शुरू होती है।",
            "family": "आपकी मृत्यु के बाद पति या पत्नी को आधी पेंशन मिलती रहती है।",
        },
        "en": {
            "explain": "Shram Yogi Maan-Dhan is a pension for unorganised workers. You save fifty-five to two hundred rupees "
                       "a month, the government adds the same, and after sixty you get three thousand rupees a month.",
            "apply": "Take Aadhaar and your bank passbook to the nearest CSC. After that the amount is auto-debited monthly.",
            "docs": "Aadhaar, a savings or Jan Dhan account, and a mobile number. No income certificate, just a self-declaration.",
            "who": "Unorganised workers aged eighteen to forty, like street vendors, rickshaw drivers and domestic workers, "
                   "earning fifteen thousand a month or less.",
            "not": "Income-tax payers, and members of EPF, ESIC or NPS.",
            "money": "Three thousand rupees a month after sixty.",
            "cost": "Fifty-five rupees a month if you join at eighteen, eighty at twenty-five, one hundred and five at thirty, "
                    "one hundred and fifty at thirty-five, and two hundred at forty. The government matches it.",
            "when": "You contribute monthly until sixty, then the pension starts.",
            "family": "After your death your spouse keeps getting half the pension.",
        },
    },
    "eshram": {
        "web": "eshram.gov.in", "web_hi": "ई-श्रम डॉट जीओवी डॉट इन", "web_en": "e shram dot gov dot in",
        "helpline": "14434",
        "hi": {
            "explain": "ई-श्रम कार्ड असंगठित मज़दूरों का राष्ट्रीय पहचान पत्र है। इसमें एक यूनिवर्सल अकाउंट नंबर मिलता है, "
                       "और इसी से सरकार आपको दूसरी योजनाओं से जोड़ती है।",
            "apply": "{web} पर आधार से जुड़े मोबाइल नंबर और ओटीपी से खुद रजिस्टर कीजिए, या सीएससी केंद्र जाइए।",
            "docs": "आधार कार्ड, आधार से जुड़ा मोबाइल नंबर, और बैंक खाता।",
            "who": "सोलह से उनसठ साल के असंगठित मज़दूर, जैसे रेहड़ी वाले, घरेलू कामगार, गिग वर्कर और खेतिहर मज़दूर।",
            "not": "ईपीएफ़ओ या ईएसआईसी के सदस्य, और इनकम टैक्स भरने वाले।",
            "money": "कार्ड सीधे पैसा नहीं देता, लेकिन इससे सरकारी योजनाओं का फ़ायदा आप तक आसानी से पहुँचता है।",
            "cost": "रजिस्ट्रेशन मुफ़्त है, और कार्ड कभी एक्सपायर नहीं होता।",
            "online": "हाँ, {web} पर चौबीसों घंटे रजिस्ट्रेशन हो सकता है।",
        },
        "en": {
            "explain": "The e-Shram card is a national ID for unorganised workers. You get a Universal Account Number, "
                       "and the government uses it to connect you to other schemes.",
            "apply": "Register yourself on {web} with your Aadhaar-linked mobile and OTP, or go to a CSC.",
            "docs": "Aadhaar, a mobile number linked to Aadhaar, and a bank account.",
            "who": "Unorganised workers aged sixteen to fifty-nine, like street vendors, domestic workers, gig workers "
                   "and farm labourers.",
            "not": "EPFO or ESIC members, and income-tax payers.",
            "money": "The card doesn't pay money directly, but it makes it easier for scheme benefits to reach you.",
            "cost": "Registration is free and the card never expires.",
            "online": "Yes, registration on {web} is open twenty-four hours.",
        },
    },
    "apy": {
        "web": None,
        "hi": {
            "explain": "अटल पेंशन योजना में आप हर महीने थोड़ा पैसा जमा करते हैं, और साठ साल के बाद हर महीने "
                       "एक हज़ार से पाँच हज़ार रुपये तक की पक्की पेंशन मिलती है।",
            "apply": "जिस बैंक या पोस्ट ऑफ़िस में आपका बचत खाता है, वहाँ फ़ॉर्म भरिए। कई बैंकों के ऐप में भी यह विकल्प है।",
            "docs": "आधार कार्ड, बचत बैंक खाता, और मोबाइल नंबर।",
            "who": "अठारह से चालीस साल का कोई भी भारतीय, जिसका बचत खाता हो।",
            "not": "एक अक्टूबर दो हज़ार बाईस से, इनकम टैक्स भरने वाले इसमें नहीं जुड़ सकते।",
            "money": "साठ साल के बाद एक, दो, तीन, चार या पाँच हज़ार रुपये महीना, जो आप चुनें।",
            "cost": "यह उम्र और पेंशन पर निर्भर है। अठारह साल में जुड़ें तो बयालीस से दो सौ दस रुपये महीना, "
                    "चालीस साल में दो सौ इक्यानवे से चौदह सौ चौवन रुपये महीना।",
            "when": "कम से कम बीस साल जमा करना होता है, और पेंशन साठ साल से शुरू होती है।",
            "family": "आपके बाद पति या पत्नी को वही पेंशन मिलती है, और दोनों के बाद जमा पैसा नॉमिनी को मिलता है।",
        },
        "en": {
            "explain": "Under Atal Pension Yojana you save a small amount every month, and after sixty you get a guaranteed "
                       "pension of one to five thousand rupees a month.",
            "apply": "Fill the form at the bank or post office where you have a savings account. Many bank apps have it too.",
            "docs": "Aadhaar, a savings account, and a mobile number.",
            "who": "Any Indian aged eighteen to forty with a savings account.",
            "not": "Since first October twenty twenty-two, income-tax payers can't join.",
            "money": "One, two, three, four or five thousand rupees a month after sixty, as you choose.",
            "cost": "It depends on your age and pension. Joining at eighteen costs forty-two to two hundred and ten rupees a month; "
                    "at forty, two hundred and ninety-one to fourteen hundred and fifty-four.",
            "when": "You contribute for at least twenty years and the pension starts at sixty.",
            "family": "After you, your spouse gets the same pension, and after both of you the nominee gets the savings.",
        },
    },
    "pmjjby": {
        "web": None,
        "hi": {
            "explain": "जीवन ज्योति बीमा एक साल का जीवन बीमा है। साल के चार सौ छत्तीस रुपये में, किसी भी कारण से मृत्यु होने पर "
                       "परिवार को दो लाख रुपये मिलते हैं।",
            "apply": "अपने बैंक या पोस्ट ऑफ़िस में फ़ॉर्म भरिए, या बैंक के ऐप से जुड़िए। प्रीमियम हर साल खाते से अपने आप कटता है।",
            "docs": "बचत बैंक खाता, आधार, और नॉमिनी का नाम।",
            "who": "अठारह से पचास साल के लोग, जिनका बैंक या पोस्ट ऑफ़िस में खाता है।",
            "not": "पचास साल से ऊपर के नए लोग नहीं जुड़ सकते। जुड़ने के पहले तीस दिन में बीमारी से मृत्यु पर दावा नहीं मिलता, "
                   "दुर्घटना पर मिलता है।",
            "money": "मृत्यु पर परिवार को दो लाख रुपये।",
            "cost": "साल के चार सौ छत्तीस रुपये, यानी रोज़ का लगभग सवा रुपया।",
            "when": "बीमा जून से मई तक एक साल का होता है, और हर साल रिन्यू होता है।",
        },
        "en": {
            "explain": "Jeevan Jyoti Bima is one-year life insurance. For four hundred and thirty-six rupees a year, "
                       "your family gets two lakh rupees if you die from any cause.",
            "apply": "Fill the form at your bank or post office, or join through your bank's app. The premium is auto-debited yearly.",
            "docs": "A savings account, Aadhaar, and your nominee's name.",
            "who": "People aged eighteen to fifty with a bank or post office account.",
            "not": "New members can't join after fifty. Deaths from illness in the first thirty days aren't covered; accidents are.",
            "money": "Two lakh rupees to your family on death.",
            "cost": "Four hundred and thirty-six rupees a year, about one rupee twenty a day.",
            "when": "Cover runs June to May and renews every year.",
        },
    },
    "pmsby": {
        "web": None,
        "hi": {
            "explain": "सुरक्षा बीमा दुर्घटना का बीमा है। साल के सिर्फ़ बीस रुपये में, दुर्घटना में मृत्यु या पूरी विकलांगता पर "
                       "दो लाख, और आंशिक विकलांगता पर एक लाख रुपये मिलते हैं।",
            "apply": "अपने बैंक या पोस्ट ऑफ़िस में फ़ॉर्म भरिए, या बैंक के ऐप से जुड़िए। प्रीमियम हर साल खाते से अपने आप कटता है।",
            "docs": "बचत बैंक खाता, आधार, और नॉमिनी का नाम।",
            "who": "अठारह से सत्तर साल के लोग, जिनका बैंक या पोस्ट ऑफ़िस में खाता है।",
            "not": "यह सिर्फ़ दुर्घटना को कवर करता है, बीमारी से मृत्यु को नहीं।",
            "money": "दुर्घटना में मृत्यु या पूरी विकलांगता पर दो लाख, आंशिक विकलांगता पर एक लाख रुपये।",
            "cost": "साल के सिर्फ़ बीस रुपये, जो खाते से अपने आप कटते हैं।",
        },
        "en": {
            "explain": "Suraksha Bima is accident insurance. For just twenty rupees a year you get two lakh for accidental death "
                       "or total disability, and one lakh for partial disability.",
            "apply": "Fill the form at your bank or post office, or join through your bank's app. The premium is auto-debited yearly.",
            "docs": "A savings account, Aadhaar, and your nominee's name.",
            "who": "People aged eighteen to seventy with a bank or post office account.",
            "not": "It only covers accidents, not death from illness.",
            "money": "Two lakh for accidental death or total disability, one lakh for partial disability.",
            "cost": "Just twenty rupees a year, auto-debited.",
        },
    },
    "sukanya": {
        "web": None,
        "hi": {
            "explain": "सुकन्या समृद्धि बेटी के नाम पर एक बचत खाता है, जिस पर अच्छा ब्याज मिलता है और जो टैक्स-फ़्री है। "
                       "यह पैसा बेटी की पढ़ाई या शादी के लिए जमा होता है।",
            "apply": "बेटी का जन्म प्रमाण पत्र लेकर पोस्ट ऑफ़िस या बैंक जाइए, और कम से कम ढाई सौ रुपये से खाता खुलवाइए।",
            "docs": "बेटी का जन्म प्रमाण पत्र, माता या पिता का आधार और पैन कार्ड, और फ़ोटो।",
            "who": "दस साल से छोटी बेटी के माता-पिता या अभिभावक।",
            "not": "एक परिवार में ज़्यादा से ज़्यादा दो बेटियों के खाते खुल सकते हैं, जुड़वाँ होने पर तीन।",
            "money": "हाल में इस पर लगभग आठ दशमलव दो प्रतिशत सालाना ब्याज मिल रहा है। सरकार हर तिमाही दर तय करती है।",
            "cost": "साल में कम से कम ढाई सौ रुपये और ज़्यादा से ज़्यादा डेढ़ लाख रुपये।",
            "when": "पंद्रह साल तक पैसा जमा करना होता है, और खाता इक्कीस साल में पूरा होता है।",
            "family": "एक परिवार में दो बेटियों तक के खाते खुल सकते हैं, जुड़वाँ होने पर तीन।",
        },
        "en": {
            "explain": "Sukanya Samriddhi is a tax-free savings account in your daughter's name with a good interest rate, "
                       "meant for her education or marriage.",
            "apply": "Take her birth certificate to a post office or bank and open the account with at least two hundred and fifty rupees.",
            "docs": "Daughter's birth certificate, a parent's Aadhaar and PAN, and photos.",
            "who": "Parents or guardians of a girl under ten.",
            "not": "At most two daughters per family, or three with twins.",
            "money": "Recently it has paid about eight point two percent a year. The government sets the rate every quarter.",
            "cost": "At least two hundred and fifty and at most one and a half lakh rupees a year.",
            "when": "You deposit for fifteen years and the account matures in twenty-one.",
            "family": "Up to two daughters per family can have accounts, three with twins.",
        },
    },
    "vay_vandana": {
        "web": "beneficiary.nha.gov.in", "web_hi": "आयुष्मान ऐप या उसकी वेबसाइट", "web_en": "the Ayushman app or website",
        "helpline": "14555",
        "hi": {
            "explain": "आयुष्मान वय वंदना कार्ड से सत्तर साल से ऊपर के हर बुज़ुर्ग को हर साल पाँच लाख रुपये तक का मुफ़्त इलाज मिलता है, "
                       "सरकारी और योजना से जुड़े प्राइवेट अस्पतालों में। इसमें कमाई की कोई शर्त नहीं है।",
            "apply": "आयुष्मान ऐप या {web} पर आधार से कार्ड बनाइए, या नज़दीकी सीएससी केंद्र जाइए।",
            "docs": "बस आधार कार्ड। उम्र आधार से ही जाँची जाती है।",
            "who": "सत्तर साल या उससे ज़्यादा उम्र का हर भारतीय नागरिक।",
            "not": "सीजीएचएस या ईसीएचएस वालों को इनमें से एक योजना चुननी होती है।",
            "money": "हर साल पाँच लाख रुपये तक का कैशलेस इलाज। अगर परिवार पहले से आयुष्मान में है, "
                     "तो बुज़ुर्ग को अलग से पाँच लाख का टॉप-अप मिलता है।",
            "cost": "बिल्कुल मुफ़्त।",
            "online": "हाँ, आयुष्मान ऐप पर आधार से कुछ मिनट में कार्ड बन जाता है।",
        },
        "en": {
            "explain": "The Ayushman Vay Vandana card gives everyone over seventy free treatment up to five lakh rupees a year "
                       "in government and empanelled private hospitals, with no income condition.",
            "apply": "Make the card with Aadhaar on {web}, or go to the nearest CSC.",
            "docs": "Just Aadhaar. Age is checked from Aadhaar.",
            "who": "Every Indian citizen aged seventy or more.",
            "not": "People on CGHS or ECHS have to choose one scheme.",
            "money": "Up to five lakh rupees of cashless treatment a year. If the family is already in Ayushman Bharat, "
                     "the senior gets a separate five lakh top-up.",
            "cost": "Completely free.",
            "online": "Yes, the card can be made with Aadhaar on the Ayushman app in a few minutes.",
        },
    },
    "pmjay": {
        "web": "beneficiary.nha.gov.in", "web_hi": "आयुष्मान ऐप या उसकी वेबसाइट", "web_en": "the Ayushman app or website",
        "helpline": "14555",
        "hi": {
            "explain": "आयुष्मान भारत में पात्र परिवारों को हर साल पाँच लाख रुपये तक का मुफ़्त इलाज मिलता है। "
                       "पात्रता सरकारी सूची से तय होती है, इसलिए पहले अपना नाम चेक करना होगा।",
            "apply": "{web} पर आधार डालकर अपना नाम चेक कीजिए। नाम हो तो वहीं कार्ड बन जाता है।",
            "docs": "आधार कार्ड और राशन कार्ड।",
            "who": "दो हज़ार ग्यारह की सामाजिक-आर्थिक जनगणना और राज्य की सूचियों में शामिल परिवार।",
            "money": "पूरे परिवार के लिए हर साल पाँच लाख रुपये तक का कैशलेस इलाज।",
            "cost": "मुफ़्त।",
        },
        "en": {
            "explain": "Ayushman Bharat gives eligible families free treatment up to five lakh rupees a year. "
                       "Eligibility comes from government lists, so first check your name.",
            "apply": "Check your name with Aadhaar on {web}. If you're listed, the card is made right there.",
            "docs": "Aadhaar and ration card.",
            "who": "Families on the 2011 socio-economic census list and state lists.",
            "money": "Up to five lakh rupees of cashless treatment a year for the whole family.",
            "cost": "Free.",
        },
    },
}

# words people use to name a scheme in a question
SCHEME_NAMES = [
    ("pm_kmy", ["kisan maandhan", "kisan mandhan", "kisan maan dhan", "किसान मानधन", "किसान मान धन"]),
    ("pm_sym", ["shram yogi", "shramyogi", "श्रम योगी", "maandhan", "mandhan", "मानधन"]),
    ("pm_kisan", ["pm kisan", "kisan samman", "samman nidhi", "पीएम किसान", "किसान सम्मान", "सम्मान निधि", "6000", "छह हज़ार"]),
    ("pm_svanidhi", ["svanidhi", "swanidhi", "स्वनिधि"]),
    ("pm_vishwakarma", ["vishwakarma", "vishvakarma", "विश्वकर्मा", "toolkit", "टूलकिट"]),
    ("mudra", ["mudra", "मुद्रा"]),
    ("eshram", ["e shram", "eshram", "e-shram", "ई-श्रम", "ई श्रम", "shram card", "श्रम कार्ड"]),
    ("apy", ["atal", "अटल"]),
    ("pmjjby", ["jeevan jyoti", "jivan jyoti", "जीवन ज्योति", "life insurance", "jeevan bima", "436"]),
    ("pmsby", ["suraksha bima", "सुरक्षा बीमा", "accident", "durghatna", "दुर्घटना", "20 rupaye", "बीस रुपये"]),
    ("sukanya", ["sukanya", "सुकन्या"]),
    ("vay_vandana", ["vay vandana", "वय वंदना", "70 saal", "सत्तर साल"]),
    ("pmjay", ["ayushman bharat", "आयुष्मान भारत", "ayushman", "आयुष्मान"]),
]

# intent keywords; first match by priority order wins
INTENTS = [
    ("back", ["wapas", "vapas", "back", "baaki yojana", "sab yojana", "बाकी योजना", "वापस", "bas itna", "dhanyavad",
              "dhanyawad", "shukriya", "thank", "धन्यवाद", "शुक्रिया"]),
    ("helpline", ["helpline", "help line", "number", "phone", "call", "shikayat", "complaint", "हेल्पलाइन", "नंबर",
                  "फ़ोन", "फोन", "शिकायत", "कॉल"]),
    ("online", ["online", "website", "app", "mobile se", "phone se", "ghar baithe", "ऑनलाइन", "वेबसाइट", "ऐप",
                "घर बैठे", "मोबाइल से"]),
    ("docs", ["kagaz", "kaagaz", "kagzat", "document", "dastavez", "papers", "proof", "कागज़", "कागज", "दस्तावेज़",
              "दस्तावेज", "डॉक्यूमेंट", "कागजात"]),
    ("cost", ["premium", "jama", "contribution", "bharna", "bharni", "dena padega", "deni padegi", "fees", "fee",
              "kharcha", "kharch", "प्रीमियम", "जमा", "भरना", "देना पड़ेगा", "फीस", "खर्चा", "खर्च", "interest", "byaj",
              "ब्याज"]),
    ("family", ["biwi", "patni", "wife", "pati", "husband", "parivar", "family", "gharwali", "beta", "bete", "beti",
                "पत्नी", "पति", "परिवार", "बेटा", "बेटी", "मृत्यु के बाद", "after death"]),
    ("not", ["kisko nahi", "kise nahi", "kaun nahi", "nahi milega", "not eligible", "nahi mil", "excluded",
             "किसको नहीं", "किसे नहीं", "कौन नहीं", "नहीं मिलेगा", "शर्त", "shart", "condition"]),
    ("when", ["kab", "kitne din", "kitna time", "samay", "kab tak", "kab se", "when", "how long", "कब", "कितने दिन",
              "समय", "कितना टाइम"]),
    ("apply", ["kahan", "kaha", "kaise", "apply", "aavedan", "avedan", "form", "registration", "register", "jaana",
               "jaun", "कहाँ", "कहां", "कैसे", "आवेदन", "फ़ॉर्म", "फॉर्म", "रजिस्ट्रेशन", "where", "how do i"]),
    ("money", ["kitna", "kitne", "paisa", "paise", "rupaye", "amount", "milega", "milta", "labh", "fayda", "faayda",
               "benefit", "कितना", "कितने", "पैसा", "पैसे", "लाभ", "फ़ायदा", "फायदा", "मिलेगा", "मिलता", "how much"]),
    ("who", ["kaun", "kisko", "kise", "eligible", "patra", "yogya", "haqdar", "कौन", "किसको", "किसे", "पात्र",
             "योग्य", "हकदार", "who can"]),
    ("explain", ["samjhao", "samjhaiye", "batao", "bataiye", "kya hai", "explain", "dobara", "phir se", "detail",
                 "समझाइए", "समझाओ", "बताइए", "बताओ", "क्या है", "फिर से", "दोबारा", "what is", "tell me"]),
]

# business / farming / state schemes added 9 Nov 2026 (see kb_more.py)
from kb_more import KB_MORE, SCHEME_NAMES_MORE  # noqa: E402

KB.update(KB_MORE)
SCHEME_NAMES += SCHEME_NAMES_MORE

# schemes added from 11 Nov 2026: their facts are built from the scheme cards (see catalog.py)
import catalog  # noqa: E402

KB.update(catalog.kb_entries())
SCHEME_NAMES += catalog.scheme_names()
