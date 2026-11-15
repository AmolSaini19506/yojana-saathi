# Yojana Saathi (योजना साथी): solution pitch

**Speak in your own language. Hear which government schemes you and your family can get.**
Live: https://yojana-saathi-sg.onrender.com · Team: Amol and Yash · Great Indian AI Internship Challenge

## The problem

Most people don't miss government schemes because they aren't eligible. They miss them because nobody told them.
Scheme rules sit on English websites and in long forms, so the people they were made for (farmers, street vendors,
artisans, homemakers, widows, students and the elderly) are the least likely to find them.

## The solution

A voice-first scheme finder. A person says who they are, for example "मैं 34 साल का किसान हूँ, 2 एकड़ ज़मीन है", in
any of 10 Indian languages or Hinglish. The app asks a few short follow-up questions, then speaks back which schemes
fit, why, roughly how much money that is in a year, where to apply and which papers to bring. They can ask follow-up
questions by voice ("कौन से कागज़ चाहिए?"), check the next family member, and share the list on WhatsApp.

## How it works

```
speech -> Gnani Prisma v3.0 (live stream) -> parser -> question engine -> 69 scheme rules -> Gnani Timbre v3.0 -> voice
```

- **Gnani Prisma v3.0** turns live speech into text and detects the language.
- **A rule-based parser** reads age, work, land, income, state, village or town, ration card and more, including
  gender from how people speak ("karti hoon", "saal ka hoon").
- **A question engine** runs every scheme's rule over the details still unknown and asks only about the one that most
  undecided schemes depend on. At most five follow-ups, and never a question that can't apply.
- **69 schemes** (central, plus state schemes for 18 states), each a small rule checked against official sources.
- **Gnani Timbre v3.0** speaks every reply. Fixed lines ship as ready-made Timbre clips, so they play instantly.

## Why we built it this way

**No AI decides eligibility or invents facts.** For a welfare tool, a confident wrong answer is worse than "I don't
know". Every rule and amount lives in code with its source; a question outside those facts gets "ask the helpline or
your CSC".

## Who it is for

People more comfortable speaking than filling forms, and the children who check schemes for their parents.

## Honest limits

A first check, not an official decision. 69 schemes is not every scheme, and state coverage is uneven. 8 of the 10
languages are machine-translated and not yet reviewed by native speakers. All demo data is made up.
