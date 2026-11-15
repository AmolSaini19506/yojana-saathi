"""
Make the saved voice clips for the app's fixed lines, so they play at once instead of waiting for Timbre.

The greeting, every question, the "found N schemes" line and each scheme's spoken summary never change, so their
Timbre audio is made once and kept in voice/<lang>/ (see app.voice_file). Run it again after changing a line: only
missing clips are made. Needs GNANI_API_KEY in .env.

    python tools/make_voice.py            # Hindi and English
    python tools/make_voice.py hi ta      # chosen languages
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app       # noqa: E402
import dialog    # noqa: E402
import langs     # noqa: E402
import schemes   # noqa: E402

# lines filled in at run time (amounts, state names, document lists) can't be made in advance
TEMPLATES = {"state_note", "saved", "docs_all", "found"}
# not questions: never follow "no problem" / "sorry, I didn't catch that"
NOT_QUESTIONS = {"intro", "retry", "none", "outro", "more", "ok_skip", "member_intro", "x_epf", "x_itax"}


def keys(lang):
    k = set(dialog.Q["en"])
    p = langs.pack(lang)
    if p:
        k |= set(p.Q)
    return sorted(k - TEMPLATES)


def lines(lang):
    say = lambda key: dialog.qt(lang, key)[1]          # noqa: E731
    out = []
    for k in keys(lang):
        text = say(k)
        if "{" in text:
            continue
        out.append(text)
        if k not in NOT_QUESTIONS:                      # the same question after "no problem" or a re-ask
            out.append(say("ok_skip") + " " + text)
            out.append(say("retry").rstrip() + " " + text)
    for n in range(1, 16):
        out.append(say("found").format(n=dialog.spoken_num(n, lang)))
    for s in schemes.SCHEMES + schemes.MAYBE:
        line = s.get("speak_hi") if lang == "hi" else s.get("speak_en") if lang == "en" else None
        if line:
            out.append(line)
    parts = []
    for text in out:
        for part in app.speech_parts(text):
            if part not in parts:
                parts.append(part)
    return parts


def main(chosen):
    if not app.API_KEY:
        sys.exit("GNANI_API_KEY is not set (.env)")
    made = have = failed = 0
    for lang in chosen:
        for part in lines(lang):
            if os.path.exists(app.voice_file(part, lang)):
                have += 1
                continue
            t = time.time()
            try:
                app.synthesize(part, lang)
                made += 1
                print(f"{lang} {time.time() - t:4.1f}s  {part[:60]}", flush=True)
            except app.TimbreError as e:
                failed += 1
                print(f"{lang} FAILED {e.status}: {part[:60]}", flush=True)
    print(f"made {made}, already there {have}, failed {failed}")


if __name__ == "__main__":
    main([langs.valid(x) for x in sys.argv[1:]] or ["hi", "en"])
