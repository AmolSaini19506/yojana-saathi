"""
Yojana Saathi: the conversation and the eligibility logic behind the voice app.

    nlu.py      pulls details (age, work, land, income, state ...) out of what the person said
    engine.py   decides which question to ask next, from the scheme rules
    dialog.py   holds the conversation: questions, results, the next family member
    schemes.py  matches a profile against every scheme and explains why each one fits
    ask.py      answers follow-up questions about one scheme ("Samjhaiye"), only from verified facts
    states.py   state names and cities, and which states have state schemes
    data/       the schemes themselves and the facts the Q&A answers from
    langs/      language detection and the eight beta language packs

app.py (one level up) serves this over HTTP and talks to Gnani's Prisma and Timbre models.
"""
