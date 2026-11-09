# Yojana Saathi · योजना साथी

**Speak in any of 10 Indian languages → find the government schemes you qualify for → hear the answer back, in your language.**

Built for the Great Indian AI Internship Challenge on Gnani AI's speech models.

**Live demo:** https://yojana-saathi-sg.onrender.com (free plan: the first visit after a quiet spell takes ~50 s to wake up)

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

Open **http://localhost:5000** in Chrome, tap **Start**, then talk.

- **Hands-free mode** (default when `flask-sock` and `websockets` are installed): after the app speaks, it listens
  automatically, and your words appear as you say them. Pause for about a second and it treats that as the end of your
  answer. Tap the mic to finish early, or tap it while the app is talking to cut in.
- **Misheard?** Every answer has a **↶ Change** button: it rewinds the conversation to that point and asks again.
- Without those packages it uses **tap-to-record**: tap, speak, tap again.

- No key yet? It still runs: type your answers in the box, and it speaks with the browser's voice instead of Timbre.
- Mic needs `localhost` or HTTPS. For a phone demo, run it on a laptop and use a tunnel (e.g. `ngrok http 5000`).

## Put it online (free, ~10 minutes) — Render

Vercel can't keep the live Prisma connection open, so hands-free mode wouldn't work there. Render runs everything.

1. Create a **new GitHub repo** and upload this folder. `.gitignore` keeps your `.env` (and key) out of it.
2. Go to **render.com** → sign in with GitHub → **New → Blueprint** → pick the repo (or paste its public URL).
   It reads `render.yaml` (free plan, Singapore region, the closest to India).
3. When it asks for `GNANI_API_KEY`, paste your key. Click **Apply**.
4. In 3–5 minutes you get a link like `https://yojana-saathi-sg.onrender.com`. HTTPS means the mic works on phones too.
5. Deployed from a public repo URL? Pushes don't auto-deploy: use **Manual Deploy → Deploy latest commit**.

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

## Schemes covered (30)

**Central (17):** PM-KISAN · PM Kisan Maan-Dhan · PM SVANidhi · PM Vishwakarma · PM Mudra · PM Shram Yogi Maan-Dhan ·
e-Shram · Atal Pension Yojana · PMJJBY · PMSBY · Sukanya Samriddhi · Ayushman Vay Vandana (70+) ·
**PMEGP** (new business, 15–35% subsidy) · **Kisan Credit Card** · **PM Fasal Bima** · **Udyam registration** ·
*"check this": Ayushman Bharat PM-JAY (depends on SECC lists), Startup India (companies/LLPs only)*

**State (13, for 8 states with ~60% of India's people):**

| State | Schemes |
|---|---|
| Uttar Pradesh | CM-YUVA (₹5 lakh interest-free business loan, 21–40) · Kanya Sumangala (₹25,000 for a daughter) |
| Bihar | Mahila Rozgar Yojana (₹10,000 + up to ₹2 lakh) · Vridhjan Pension (₹1,100/month, 60+) |
| Maharashtra | Majhi Ladki Bahin (₹1,500/month) · Namo Shetkari (₹6,000/yr on top of PM-KISAN) |
| Madhya Pradesh | *check:* Ladli Behna (₹1,500/month; new names only in special drives) |
| Rajasthan | *check:* MAA Yojana (₹25 lakh/yr cashless health cover per family) |
| West Bengal | Annapurna Bhandar (₹3,000/month, women 25–60; replaced Lakshmir Bhandar in June 2026) |
| Tamil Nadu | Kalaignar Magalir Urimai Thogai (₹1,000/month; the promised ₹2,500 hasn't started) |
| Karnataka | Gruha Lakshmi (₹2,000/month) · *check:* Yuva Nidhi (₹3,000/₹1,500 for unemployed graduates/diploma) |

The app asks **which state** (or picks it up from a city: "Lucknow se hoon"), asks **woman or man** only where a
women's scheme exists in that state (or infers it from Hindi verbs like "karti hoon"), and asks **"want to start a
business?"** only for non-farmers aged 18–60. Other states get central schemes and an honest "your state's schemes
aren't in the app yet, ask at a CSC".

**Left out on purpose (checked 9 Nov 2026):** PMFME (extension ended 30 Sep 2026, no renewal yet) and Stand-Up India
(ended March 2025; a revamp announced in March 2026 hasn't launched). Rajasthan's farmer top-up and the UP/Rajasthan
old-age pension amounts are left out because sources disagree on the amount.

## Honest limits

- **Screening, not a decision.** Rules are simplified. The app always says to confirm at a CSC, bank or portal.
- **State schemes for 8 states only**, 1–2 flagship schemes each. State schemes change often (renamed after elections,
  amounts raised), so they need re-checking more often than central ones.
- **Bigha is approximated at 0.25 ha.** It varies a lot by state.
- **8 of the 10 languages are beta:** AI-translated, not yet checked by native speakers. Fix wording in `langs/<lang>.py`.
- **Punjabi is usually heard as Hindi in Auto mode** (very similar speech). Pick Punjabi in the menu.
- **Hindi vs Marathi** share a script; we tell them apart by common words, so a one-word reply keeps the current language.
- **Land units are approximate:** bigha ≈ 0.25 ha (Hindi), 0.134 ha (Bengali), vigha ≈ 0.16 ha (Gujarati).
- **One voice at a time.** Timbre allows one active request per API key, so with many visitors at once the server
  queues voice requests (~0.6 s each). Repeated lines (the questions) are cached and play instantly.
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
- Added 9 Nov 2026 (current reports and official portals): PMEGP active in 2026-27 (KVIC tranche Oct 2026; 15–35%,
  ₹50 lakh / ₹20 lakh caps) · KCC ₹5 lakh limit (Budget 2025), 7%/4% on up to ₹3 lakh, collateral-free ₹2 lakh (PIB) ·
  PMFBY 2% / 1.5% / 5% · Udyam and DPIIT recognition free · PMFME ended 30 Sep 2026 · Stand-Up India ended Mar 2025
  (FM in Lok Sabha, Mar 2026) · Ladki Bahin ₹1,500 (Aug 2026 instalment) · Namo Shetkari ₹6,000 · Ladli Behna ₹1,500
  (Sep 2026 instalment) · Annapurna Bhandar ₹3,000 (new WB govt, June 2026) · KMUT ₹1,000 (TN CMO, May 2026) ·
  Gruha Lakshmi ₹2,000 · Yuva Nidhi ₹3,000/₹1,500 · Bihar Mahila Rozgar ₹10,000 + ₹2 lakh (cabinet, Aug 2025) ·
  Bihar pension ₹1,100 · UP CM-YUVA ₹5 lakh interest-free (21–40) · Kanya Sumangala ₹25,000 · Rajasthan MAA ₹25 lakh
