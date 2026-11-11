# Yojana Saathi · योजना साथी

**Speak in any of 10 Indian languages, find the government schemes you qualify for, and hear the answer back in your language.**

Built by Amol and Yash for the Great Indian AI Internship Challenge, on Gnani AI's speech models.

**Live demo:** https://yojana-saathi-sg.onrender.com (free hosting: the first visit after a quiet spell can take up to a minute)

## Why

Most people don't miss government schemes because they aren't eligible. They miss them because nobody told them.
The information is spread across English websites and long forms, which hits farmers, street vendors, artisans,
small shopkeepers, homemakers and the elderly hardest. Yojana Saathi lets them simply say who they are and hear
which schemes fit, where to apply and what to bring.

## How it works

```
 Speech ──► Gnani Prisma v3.0, live stream (detects the language and when the speaker stops)
              │        (falls back to tap-to-record + Prisma REST)
              ▼
       Rule-based understanding (nlu.py)    age, work, land, income, state, gender, tax, PF, daughter under 10
              │
              ▼
       Short dialog (dialog.py)             asks only for what's still missing
              │
              ▼
       Eligibility rules                    30 schemes: central + 8 states, each with a "why you qualify" line
              │
              ▼
 Voice ◄── Gnani Timbre v3.0 (text-to-speech in the conversation's language)
              │
              ▼
   "समझाइए" (Explain) on any scheme → voice Q&A: where to apply, documents, amount, helpline
   Share the list on WhatsApp
```

**No AI decides eligibility or invents facts.** Every rule and amount lives in code (`schemes.py`, `more_schemes.py`,
`kb.py`, `kb_more.py`), checked against official sources. A question outside those facts gets "I don't know, ask the
helpline or a CSC". An LLM can optionally be connected for follow-up questions, and it may only answer from that
scheme's facts.

## Run locally

```bash
pip install -r requirements.txt
cp .env.example .env        # add a Gnani API key from app.gnani.ai/voice
python app.py
```

Open http://localhost:5000 in Chrome, tap **Start** and talk.

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
- Questions, scheme cards, the "why you qualify" line, the Q&A and the WhatsApp text all follow the language.
- Beta languages are one file each in `langs/`. They are machine-translated and not yet reviewed by native speakers,
  and the app says so on screen. Amounts and rules are the same verified facts. `tests/test_langs.py` checks that every
  pack is complete and states the same numbers.

## Schemes covered (30)

**Central:** PM-KISAN · PM Kisan Maan-Dhan · PM SVANidhi · PM Vishwakarma · PM Mudra · PM Shram Yogi Maan-Dhan ·
e-Shram · Atal Pension Yojana · PMJJBY · PMSBY · Sukanya Samriddhi · Ayushman Vay Vandana (70+) · PMEGP ·
Kisan Credit Card · PM Fasal Bima · Udyam registration · *to check: Ayushman Bharat PM-JAY, Startup India*

**State:**

| State | Schemes |
|---|---|
| Uttar Pradesh | CM-YUVA · Kanya Sumangala |
| Bihar | Mahila Rozgar Yojana · Vridhjan Pension |
| Maharashtra | Majhi Ladki Bahin · Namo Shetkari |
| Madhya Pradesh | *to check:* Ladli Behna |
| Rajasthan | *to check:* MAA Yojana |
| West Bengal | Annapurna Bhandar |
| Tamil Nadu | Kalaignar Magalir Urimai Thogai |
| Karnataka | Gruha Lakshmi · *to check:* Yuva Nidhi |

The app asks for the state (or picks it up from a city name), asks about gender only where that state has a women's
scheme, and asks about starting a business only for non-farmers aged 18–60. For other states it lists central schemes
and says that state schemes aren't covered yet.

Left out on purpose (as of Nov 2026): PMFME (ended 30 Sep 2026) and Stand-Up India (ended March 2025), plus amounts
where sources disagree.

## Honest limits

- **A first check, not an official decision.** Rules are simplified; the app always says to confirm at a CSC, bank or
  the scheme's portal.
- **State schemes for 8 states only**, and they change often, so they need regular re-checking.
- **Land units are approximate:** bigha ≈ 0.25 ha (Hindi), 0.134 ha (Bengali); vigha ≈ 0.16 ha (Gujarati).
- **8 of the 10 languages are beta** (see above).
- **Punjabi is often heard as Hindi in Auto mode**; choosing Punjabi fixes it.
- **One voice request at a time:** Timbre allows one active request per API key, so the server queues them and caches
  repeated lines.
- **The Q&A only knows the facts in the knowledge base**, by design.
- **Demo data is made up.** No real names, Aadhaar, phone or bank numbers.

## Tests

```bash
python -m pytest -q
```

They cover parsing (Hinglish, Devanagari, other scripts, number words, land units), full conversations, every
language pack, state rules, and the request formats sent to Prisma and Timbre (network mocked).

## Files

| File | What it does |
|---|---|
| `app.py` | Flask server: `/ws/stt` (Prisma stream), `/api/stt` (Prisma REST), `/api/tts` (Timbre), `/api/turn`, `/api/ask` |
| `nlu.py` | Extracts details from speech: "35 saal", "पंद्रह हज़ार", "do bigha", "10-12 hazaar", "tax nahi bharta" |
| `dialog.py` | Opens with one question, then asks only what's missing |
| `schemes.py`, `more_schemes.py`, `states.py` | Scheme rules, benefits and "why you qualify" reasons |
| `kb.py`, `kb_more.py` | Verified facts per scheme for the spoken Q&A |
| `ask.py` | The "समझाइए" Q&A: finds the scheme and the question, answers from the facts |
| `langs/` | Language detection and one file per beta language |
| `static/index.html` | The single-page app: mic streaming, chat, result cards, language choice |

## Sources (checked Nov 2026)

PIB and Cabinet decisions (PM SVANidhi, KCC, APY, PMJJBY, PMSBY) · myscheme.gov.in (PM Vishwakarma) · india.gov.in
(PM-SYM) · pmkisan.gov.in (exclusions; helpline 155261) · NHA (Ayushman Vay Vandana; helpline 14555) · Ministry of
Finance (Mudra Tarun Plus) · India Post / DEA (Sukanya Samriddhi) · eshram.gov.in (helpline 14434) · KVIC (PMEGP) ·
state government announcements for the state schemes (2025–26).
