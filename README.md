# Yojana Saathi · योजना साथी

**Speak in any of 10 Indian languages, find the government schemes you and your family qualify for, and hear the answer back in your language.**

Built by Amol and Yash for the Great Indian AI Internship Challenge, on Gnani AI's speech models.

**Live demo:** https://yojana-saathi-sg.onrender.com (free hosting: the first visit after a quiet spell can take up to a minute)

## Why

Most people don't miss government schemes because they aren't eligible. They miss them because nobody told them.
The information is spread across English websites and long forms, which hits farmers, street vendors, artisans,
small shopkeepers, homemakers, widows, students and the elderly hardest. Yojana Saathi lets them simply say who they
are and hear which schemes fit, how much money that is in a year, where to apply and which papers to bring.

## What it does

- **Listens** in Hindi, Hinglish, English and 8 more Indian languages (Gnani Prisma v3.0, live stream).
- **Asks only what matters.** After the first answer it works out which schemes are still undecided and asks about the
  one detail most of them depend on. A farmer is never asked about PF, a man is never asked about maternity benefit.
- **Checks 69 schemes** against written rules: central schemes and state schemes for 18 states.
- **Speaks the result** in the person's language (Gnani Timbre v3.0), with a "why you qualify" line on every card.
- **Adds it up:** "about ₹12,000 a year", counting only fixed yearly money (not loans, insurance cover or one-time sums).
- **One list of papers** for everything, so one trip to the CSC or bank is enough.
- **The whole family:** after one person, check for the next (mother, wife, son). The home's details are kept, each
  person gets their own list, and the family total is shown.
- **Explains any scheme by voice** ("समझाइए"): where to apply, documents, amount, helpline.
- **Shares the list on WhatsApp**, grouped by person.

## How it works

```
 Speech ──► Gnani Prisma v3.0, live stream (detects the language and when the speaker stops)
              │        (falls back to tap-to-record + Prisma REST)
              ▼
       Rule-based understanding (nlu.py)    age, work, land, income, state, village or town, ration card, house,
              │                             gas, category, widow, disability, maternity, children in school ...
              ▼
       Question engine (engine.py)          explores every scheme's rule over what is still unknown and asks
              │                             the detail that the most undecided schemes depend on
              ▼
       Eligibility rules                    69 schemes, each a small rule with a "why you qualify" line
              │
              ▼
 Voice ◄── Gnani Timbre v3.0 (text-to-speech in the conversation's language)
```

**No AI decides eligibility or invents facts.** Every rule and amount lives in code and was checked against official
sources and current reports. A question outside those facts gets "I don't know, ask the helpline or a CSC". An LLM
can optionally be connected for follow-up questions, and it may only answer from that scheme's facts.

### The question engine

Each scheme is a rule over the person's details. `engine.py` runs every rule with the unknown details filled in every
possible way. If the outcome is the same every time, the scheme is decided. If not, the engine notes which details
the outcome depends on. It then asks about the detail that the most undecided schemes depend on, in a natural order
(land and income before personal questions), and stops when no answer could change the list or after eight
follow-ups. Schemes still undecided at that point are shown as "worth checking". Details that are true for few people
(widow, pregnant, disability certificate) are asked together as one question. Adding a scheme therefore never adds a
question for people it cannot apply to.

## Run locally

```bash
pip install -r requirements.txt
cp .env.example .env        # add a Gnani API key from app.gnani.ai/voice
python app.py
```

Open http://localhost:5000 in Chrome, pick a language, tap **Start** and talk.

- **Hands-free mode** (when `flask-sock` and `websockets` are installed): the app listens after it speaks and shows
  the words live. A short pause ends the answer. Tapping the mic finishes early or interrupts the app.
- **↶ Change** on any answer rewinds the conversation to that point.
- Without those packages it uses tap-to-record. Without an API key it still runs: answers can be typed, and the
  browser's own voice is used instead of Timbre.
- The microphone needs `localhost` or HTTPS.

## Deploy

`render.yaml` deploys the app on Render (free plan, Singapore region): **New → Blueprint**, select the repo, and enter
`GNANI_API_KEY` when asked. A host that supports WebSockets is needed for hands-free mode. `RATE_PER_HOUR` (default 80)
limits Gnani calls per visitor.

## Languages

Hindi / Hinglish, English, and (beta) Bengali, Gujarati, Kannada, Malayalam, Marathi, Punjabi, Tamil and Telugu: the
10 languages Prisma v3.0 and Timbre v3.0 support.

- Until the language is known, Prisma gets `indic-auto`. `langs/__init__.py` combines Prisma's
  `detected_language_code` with the script of the text, and keeps the current language for short replies like "35".
  Choosing a language on the first screen fixes it for the conversation.
- Questions, scheme cards, the list of papers, the Q&A and the WhatsApp text all follow the language.
- Beta languages are machine-translated and not yet reviewed by native speakers; the app says so on screen. Amounts
  and rules are the same verified facts, and tests check that every translation states the same numbers. State
  schemes are translated into the state's own language where the app supports it; "worth checking" cards added in
  November 2026 still appear in English in the beta languages.

## Schemes covered (69)

**Central (41)**

| For | Schemes |
|---|---|
| Farmers | PM-KISAN · PM Kisan Maan-Dhan · Kisan Credit Card · PM Fasal Bima · Per Drop More Crop (drip and sprinkler subsidy) |
| Workers, vendors, artisans | e-Shram · PM Shram Yogi Maan-Dhan · PM SVANidhi · PM Vishwakarma · VB-G RAM G (rural job guarantee, 125 days) · *check:* construction workers' welfare board |
| Business | PM Mudra · PMEGP · Udyam registration · *check:* Startup India |
| Women and mothers | PM Matru Vandana · Janani Suraksha Yojana · PM Ujjwala · Sukanya Samriddhi · *check:* self-help groups (Lakhpati Didi) |
| Elderly, widows, disability | Old-age pension · Widow pension · Ayushman Vay Vandana (70+) · Rashtriya Vayoshri · UDID card · *check:* disability pension, ADIP aids |
| Students and youth | PM Vidyalaxmi education loan · *check:* Central Sector Scholarship, post-matric scholarships (SC / ST / OBC), NMMS, PM Internship, DDU-GKY training |
| House, food, energy | Free ration (PMGKAY) · PM Surya Ghar rooftop solar · *check:* PM Awas (Gramin), PM Awas (Urban) 2.0 |
| Insurance and pension | PM Jeevan Jyoti Bima · PM Suraksha Bima · Atal Pension Yojana · *check:* Ayushman Bharat PM-JAY |

**State (28, for 18 states plus one scheme for Gujarat)**

| State | Schemes |
|---|---|
| Uttar Pradesh | CM-YUVA · Kanya Sumangala · Old-age pension |
| Bihar | Mahila Rozgar Yojana · Vridhjan Pension |
| Maharashtra | Majhi Ladki Bahin · Namo Shetkari |
| Madhya Pradesh | *check:* Ladli Behna |
| Rajasthan | Social security pension · *check:* MAA Yojana |
| West Bengal | Annapurna Bhandar |
| Tamil Nadu | Kalaignar Magalir Urimai Thogai |
| Karnataka | Gruha Lakshmi · *check:* Yuva Nidhi |
| Delhi | Delhi Lakshmi Yojana |
| Punjab | Mawan Dheeyan Satkar Yojna |
| Odisha | Subhadra Yojana |
| Jharkhand | Maiyan Samman Yojana |
| Chhattisgarh | Mahtari Vandan Yojana |
| Himachal Pradesh | Pyari Behna Sukh-Samman Nidhi |
| Andhra Pradesh | Annadata Sukhibhava · Thalliki Vandanam · *check:* NTR Bharosa pension |
| Telangana | Rythu Bharosa · Mahalakshmi free bus travel |
| Haryana | *check:* Lado Lakshmi Yojana |
| Assam | *check:* Orunodoi |
| Gujarat | Namo Lakshmi Yojana (schoolgirls) |

"Check" means the benefit is real but who gets it depends on a list, an exam or details the app does not ask about, so
the card says to confirm instead of promising.

**Left out on purpose** (as of November 2026) because they had ended or their current status or amount could not be
confirmed: PMFME, Stand-Up India, PM-KUSUM (moving to a new phase), PM Matsya Sampada, PMKVY 4.0, health cover for gig
workers, Kerala's schemes (the government changed in 2026), Telangana's ₹2,500 for women (not started).

## Honest limits

- **A first check, not an official decision.** Rules are simplified; the app always says to confirm at a CSC, bank or
  the scheme's portal.
- **Scheme rules change.** In 2026 alone MGNREGA was replaced by VB-G RAM G, the national pensions were renamed, and
  several states launched or changed women's schemes. Every entry carries the date it was checked and needs re-checking.
- **State coverage is uneven:** one to three flagship schemes for 18 states, none yet for the others. People there get
  central schemes and are told their state's schemes are missing.
- **The yearly amount counts only fixed cash.** Pensions whose amount depends on the state are not added in.
- **Family income is approximated** by what the person says they earn.
- **Land units are approximate:** bigha ≈ 0.25 ha (Hindi), 0.134 ha (Bengali); vigha ≈ 0.16 ha (Gujarati).
- **8 of the 10 languages are beta** (see above). **Punjabi is often heard as Hindi in Auto mode**; choosing Punjabi fixes it.
- **One voice request at a time:** Timbre allows one active request per API key, so the server queues them and caches
  repeated lines.
- **The Q&A only knows the facts in the knowledge base**, by design.
- **Demo data is made up.** No real names, Aadhaar, phone or bank numbers.

## Tests

```bash
python -m pytest -q
```

291 tests cover parsing (Hinglish, Devanagari, other scripts, number words, land units), full conversations, the
question engine, every scheme entry (complete, same amounts in every language), family mode, every language pack, and
the request formats sent to Prisma and Timbre (network mocked).

## Files

| File | What it does |
|---|---|
| `app.py` | Flask server: `/ws/stt` (Prisma stream), `/api/stt` (Prisma REST), `/api/tts` (Timbre), `/api/turn`, `/api/member`, `/api/ask` |
| `nlu.py` | Extracts details from speech: "35 saal", "पंद्रह हज़ार", "do bigha", "gaon mein", "main vidhwa hoon" |
| `engine.py` | Chooses the next question from the scheme rules |
| `dialog.py` | The conversation: opening question, follow-ups, results, the next family member |
| `schemes.py`, `more_schemes.py` | The first 30 schemes, matching, and "why you qualify" reasons |
| `catalog.py`, `catalog_states.py`, `catalog_local.py` | Schemes added in November 2026 (card, rule, papers, yearly cash) and their translations |
| `states.py` | State names, cities, and which states have state schemes |
| `kb.py`, `kb_more.py` | Verified facts per scheme for the spoken Q&A |
| `ask.py` | The "समझाइए" Q&A: finds the scheme and the question, answers from the facts |
| `langs/` | Language detection and one file per beta language |
| `static/index.html` | The single-page app: mic streaming, chat, summary, cards, family, sharing |

## Sources (checked November 2026)

PIB and Cabinet decisions (PM SVANidhi, KCC, APY, PMJJBY, PMSBY, PMGKAY, PM Vidyalaxmi, VB-G RAM G, Per Drop More
Crop) · myscheme.gov.in (PM Vishwakarma) · india.gov.in (PM-SYM) · pmkisan.gov.in (helpline 155261) · NHA (Ayushman
Vay Vandana; helpline 14555) · National Scholarship Portal · NHM (Janani Suraksha Yojana) · eshram.gov.in (helpline
14434) · KVIC (PMEGP) · state government announcements and 2026 news reports for the state schemes.
