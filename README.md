# Yojana Saathi · योजना साथी

**Speak in any of 10 Indian languages → find the government schemes you qualify for → hear the answer back, in your language.**

Built for the Great Indian AI Internship Challenge on Gnani AI's speech models.

```
 You speak ──► Prisma v3.0 live stream (hands-free; detects when you stop talking)
                 │          (falls back to tap-to-record + Prisma REST)
                 ▼
          Rule-based understanding (nlu.py)      age, work, land, income, tax, PF, daughter <10
                 │
                 ▼
          Eligibility rules (schemes.py)         12 central schemes + 1 "check this", each with "why you qualify"
                 │
                 ▼
 You hear ◄── Timbre v3.0 (text-to-speech, Hindi voice "Shivani")
                 │
                 ▼
   "Samjhaiye" on any scheme → voice Q&A: where to apply, documents, cost, helpline, family…
   answered from verified facts in kb.py. Unknown → "I don't know, ask the helpline/CSC". Never guesses.
                 │
                 ▼
   Share the list on WhatsApp with one tap (for the person who'll actually go to the CSC)
```

Every amount it speaks comes from `schemes.py` / `kb.py`. An LLM is optional and, if switched on,
may only answer from those same facts.

## Run it (5 minutes)

```bash
pip install -r requirements.txt
cp .env.example .env        # then paste your Gnani API key into .env
python app.py
```

Open **http://localhost:5000** in Chrome, tap anywhere, then talk.

- **Hands-free mode** (default when `flask-sock` and `websockets` are installed): after the app speaks, it listens
  automatically. Pause for about a second and it treats that as the end of your answer. Tap the mic to finish early.
- Without those packages it uses **tap-to-record**: tap, speak, tap again.

- No key yet? It still runs: type your answers in the box, and it speaks with the browser's voice instead of Timbre.
- Mic needs `localhost` or HTTPS. For a phone demo, run it on a laptop and use a tunnel (e.g. `ngrok http 5000`).

## Put it online (free, ~10 minutes) — Render

Vercel can't keep the live Prisma connection open, so hands-free mode wouldn't work there. Render runs everything.

1. Create a **new GitHub repo** and upload this folder. `.gitignore` keeps your `.env` (and key) out of it.
2. Go to **render.com** → sign in with GitHub → **New → Blueprint** → pick the repo. It reads `render.yaml`.
3. When it asks for `GNANI_API_KEY`, paste your key. Click **Apply**.
4. In 3–5 minutes you get a link like `https://yojana-saathi.onrender.com`. HTTPS means the mic works on phones too.

Notes:
- The free plan sleeps after ~15 minutes idle; the first visit then takes ~50 seconds to wake up.
  Open the link yourself a minute before recording the demo.
- Each visitor gets `RATE_PER_HOUR` (default 80) Gnani calls per hour, so strangers can't drain your 5,000 credits.
  Check usage at app.gnani.ai/voice.

## Languages (auto-detected)

Hindi / Hinglish, English, and (beta) Bengali, Gujarati, Kannada, Malayalam, Marathi, Punjabi, Tamil, Telugu:
the 10 languages Gnani Prisma v3.0 and Timbre v3.0 support.

- Until the app knows your language it sends Prisma `language_code=indic-auto`. Prisma returns
  `detected_language_code`; `langs/__init__.py` also checks the script of the text (so typed answers work) and keeps
  the current language for short replies like "35" or "yes". After that it hints `<lang>-IN,en-IN`.
- Replies, questions, scheme cards, the "why you qualify" line, the Samjhaiye chat and the WhatsApp text all switch.
  Timbre speaks them with `language=<lang>-IN`.
- The menu at the top can force a language (Auto is the default).
- **Beta** languages are one file each in `langs/` (`ta.py`, `bn.py`, ...), translated by an AI assistant and not yet
  checked by a native speaker; the app says so on screen. Amounts and rules are the same verified facts, written as
  digits (Timbre reads digits and ₹ in every language). `tests/test_langs.py` checks every pack is complete, that
  all 8 packs state the same numbers, and that a sample answer in each language is understood.
- Live check (9 Nov 2026, Timbre reading a sample → Prisma `indic-auto`): 9 of 10 languages detected correctly and
  parsed (age, job, land, income). Punjabi came back as Hindi (the sentence is nearly identical); picking ਪੰਜਾਬੀ in the
  menu gives Gurmukhi.

## Test

```bash
python -m pytest -q           # all tests
python tests/test_flow.py     # Hinglish / Devanagari / English parsing + full conversations
python tests/test_api.py      # checks requests to Prisma and Timbre match Gnani's docs (network mocked)
```

## Files

| File | What it does |
|---|---|
| `app.py` | Flask server. `/ws/stt` → Prisma live stream, `/api/stt` → Prisma REST, `/api/tts` → Timbre, `/api/turn` → checker, `/api/ask` → scheme chat |
| `nlu.py` | Pulls slots out of messy speech: "35 saal", "पंद्रह हज़ार", "do bigha", "10-12 hazaar", "tax nahi bharta" |
| `dialog.py` | Asks an open question first, then only what's still missing. Re-asks once, then moves on |
| `kb.py` | Verified facts per scheme (Hindi + English), written to be spoken; helplines only where confirmed |
| `ask.py` | "Samjhaiye" chat: finds the scheme + question type, answers from `kb.py`, optional grounded LLM |
| `schemes.py` | Scheme data, benefits (English + Hindi), where to apply, documents, rules |
| `langs/` | Language detection (`__init__.py`) + one file per beta language: questions, cards, facts, keywords |
| `static/index.html` | Mic → 16 kHz WAV in the browser → Prisma; chat; result cards; language menu |

## Schemes covered

PM-KISAN · PM Kisan Maan-Dhan · PM SVANidhi · PM Vishwakarma · PM Mudra · PM Shram Yogi Maan-Dhan ·
e-Shram · Atal Pension Yojana · PMJJBY · PMSBY · Sukanya Samriddhi · Ayushman Vay Vandana (70+) ·
*Ayushman Bharat PM-JAY shown as "check this", because it depends on SECC lists*

## Honest limits

- **Screening, not a decision.** Rules are simplified. The app always says to confirm at a CSC, bank or portal.
- **Central schemes only.** No state schemes yet; that's the obvious next step.
- **Bigha is approximated at 0.25 ha.** It varies a lot by state.
- **8 of the 10 languages are beta:** AI-translated, not yet checked by native speakers. Fix wording in `langs/<lang>.py`.
- **Punjabi is usually heard as Hindi in Auto mode** (very similar speech). Pick Punjabi in the menu.
- **Hindi vs Marathi** share a script; we tell them apart by common words, so a one-word reply keeps the current language.
- **Land units are approximate:** bigha ≈ 0.25 ha (Hindi), 0.134 ha (Bengali), vigha ≈ 0.16 ha (Gujarati).
- **Live mode sends whole phrases, not word by word.** Gnani's stream returns a transcript when you pause.
- **The chat only knows what's in `kb.py`.** That's on purpose: it says "I don't know" rather than invent rules.
- **Demo data is synthetic.** No real people's voices, Aadhaar numbers or phone numbers.

## Sources for scheme rules (checked Nov 2026)

- PM SVANidhi restructuring (₹15k / ₹25k / ₹50k, till Mar 2030): PIB, Cabinet decision 27 Aug 2025
- PM-SYM (18–40, ≤₹15,000/month, not EPF/ESIC/NPS, not taxpayer): india.gov.in
- PM Vishwakarma (18 trades, ₹15,000 toolkit, ₹3 lakh at 5%): myscheme.gov.in
- APY (18–40, no taxpayers since 1 Oct 2022), PMJJBY (₹436, 18–50), PMSBY (₹20, 18–70): PIB / DFS
- PM-KISAN exclusions (taxpayers, govt employees, pensioners ≥₹10,000): pmkisan.gov.in
- PM-KMY (18–40, up to 2 ha): vikaspedia / PIB
- Ayushman Vay Vandana (all 70+, ₹5 lakh, no income test): NHA, launched 29 Oct 2024
- Mudra (Shishu / Kishor / Tarun / Tarun Plus up to ₹20 lakh): MoF notification, Oct 2024
- Sukanya Samriddhi (girl under 10, ₹250–₹1.5 lakh/yr, 15 yrs deposit, matures at 21, max 2 daughters): India Post / DEA
- Helplines: PM-KISAN 155261 (pmkisan.gov.in), e-Shram 14434 (eshram.gov.in), Ayushman 14555 (NHA)
