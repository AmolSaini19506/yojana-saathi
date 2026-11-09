"""
Yojana Saathi: speak in Hindi/Hinglish/English, find government schemes you qualify for.

  Prisma (Gnani STT)  ->  rule-based understanding + eligibility rules  ->  Timbre (Gnani TTS)

Run:  python app.py   then open http://localhost:5000
"""
import json
import threading
import os
import re
import time
import uuid
from collections import OrderedDict, defaultdict, deque

import requests
from flask import Flask, Response, jsonify, request, send_from_directory

import ask
import dialog
import langs


# ---------------------------------------------------------------- config (.env without extra packages)

def load_env(path=".env"):
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    if not os.path.exists(here):
        return
    for line in open(here, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


load_env()
API_KEY = os.environ.get("GNANI_API_KEY", "")
STT_URL = os.environ.get("GNANI_STT_URL", "https://api.vachana.ai/stt/v3")
TTS_URL = os.environ.get("GNANI_TTS_URL", "https://api.vachana.ai/api/v1/tts/inference")
STT_MODEL = os.environ.get("PRISMA_MODEL", "prisma-v3.0")         # set to "" to use Prisma v2.5
TTS_MODEL = os.environ.get("TIMBRE_MODEL", "timbre-v3.0")
TTS_VOICE = os.environ.get("TIMBRE_VOICE", "Shivani")              # v3.0 voices speak all 10 languages

# Prisma v3.0: "indic-auto" in Auto mode; a picked language otherwise (see langs.stt_code)


def stt_code(args, stream=False):
    lang = langs.valid(args.get("lang", "hi"))
    if not STT_MODEL:                                   # Prisma v2.5: one language only, no auto-detect
        return "en-IN" if lang == "en" else "hi-IN"
    return langs.stt_code(lang, auto=args.get("auto", "1") == "1", known=args.get("known", "0") == "1", stream=stream)


# one keep-alive connection pool to Gnani: saves a TLS handshake on every STT / TTS call
HTTP = requests.Session()

app = Flask(__name__, static_folder="static")

# ---------------------------------------------------------------- protect your credits on a public site
# Each visitor (IP) gets RATE_PER_HOUR speech-to-text calls per hour (one full conversation uses ~10).
# Voice replies are spoken sentence by sentence (several short Timbre calls per reply), so TTS gets its own,
# larger allowance: TTS_RATE_FACTOR x RATE_PER_HOUR.
RATE_PER_HOUR = int(os.environ.get("RATE_PER_HOUR", "80"))
TTS_RATE_FACTOR = int(os.environ.get("TTS_RATE_FACTOR", "4"))
_hits = defaultdict(deque)


def rate_limited(kind: str = "stt") -> bool:
    ip = (request.headers.get("X-Forwarded-For") or request.remote_addr or "?").split(",")[0].strip()
    limit = RATE_PER_HOUR * (TTS_RATE_FACTOR if kind == "tts" else 1)
    now, q = time.time(), _hits[(ip, kind)]
    while q and now - q[0] > 3600:
        q.popleft()
    if len(q) >= limit:
        return True
    q.append(now)
    return False

# ---------------------------------------------------------------- optional: hands-free streaming
# Needs:  pip install flask-sock websockets
# Browser --(16 kHz PCM frames)--> /ws/stt --(x-api-key-id header)--> wss://api.vachana.ai/stt/v3/stream
STREAM_URL = os.environ.get("GNANI_STREAM_URL", "wss://api.vachana.ai/stt/v3/stream")
try:
    from flask_sock import Sock
    from websockets.sync.client import connect as ws_connect
    STREAMING_LIB = True
except ImportError:
    STREAMING_LIB = False

if STREAMING_LIB:
    sock = Sock(app)

    @sock.route("/ws/stt")
    def ws_stt(client):
        if rate_limited():
            client.send(json.dumps({"type": "error", "message": "Too many requests, try again later"}))
            return
        if not API_KEY:
            client.send(json.dumps({"type": "error", "message": "No GNANI_API_KEY set"}))
            return
        headers = {"x-api-key-id": API_KEY, "language_code": stt_code(request.args, stream=True),
                   "x-sample-rate": "16000", "format": "transcribe", "x-api-request-id": str(uuid.uuid4()),
                   # undocumented but live (checked 10 Nov 2026): words as they are spoken (partial_transcript),
                   # an explicit speech_end, then final_transcript ~0.5 s after the person stops talking
                   "x-partials": os.environ.get("STT_PARTIALS", "true")}
        if STT_MODEL:
            headers["model"] = STT_MODEL
        for env, hdr in (("VAD_MIN_SILENCE_MS", "x-min-silence-ms"), ("VAD_THRESHOLD", "x-vad-threshold")):
            if os.environ.get(env):
                headers[hdr] = os.environ[env]
        try:
            try:
                upstream = ws_connect(STREAM_URL, additional_headers=headers, open_timeout=10)
            except TypeError:                                  # older websockets versions
                upstream = ws_connect(STREAM_URL, extra_headers=headers, open_timeout=10)
        except Exception as e:
            client.send(json.dumps({"type": "error", "message": f"Could not open Prisma stream: {e}"}))
            return

        def pump_down():                                       # Prisma -> browser
            try:
                for msg in upstream:
                    client.send(msg if isinstance(msg, str) else msg.decode("utf-8", "ignore"))
            except Exception:
                pass
            finally:
                try:
                    client.close()
                except Exception:
                    pass

        threading.Thread(target=pump_down, daemon=True).start()
        try:                                                   # browser -> Prisma
            while True:
                data = client.receive()
                if data is None:
                    break
                upstream.send(data)                            # bytes = audio, str = {"type":"commit"}
        except Exception:
            pass
        finally:
            try:
                upstream.close()
            except Exception:
                pass


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/langs")
def langs_route():
    return jsonify(langs.info())


@app.get("/api/health")
def health():
    return jsonify(ok=True, gnani_key=bool(API_KEY), stt_model=STT_MODEL or "prisma-v2.5",
                   tts_model=TTS_MODEL, voice=TTS_VOICE, streaming=STREAMING_LIB and bool(API_KEY),
                   llm=all(ask.llm_config()))


@app.post("/api/stt")
def stt():
    """Browser sends 16 kHz mono WAV (max ~25 s). We forward it to Prisma."""
    if not API_KEY:
        return jsonify(error="No GNANI_API_KEY set. Add it to .env, or type your answer instead."), 503
    if rate_limited():
        return jsonify(error="Bahut zyada requests. Thodi der baad try karein / Too many requests, try later."), 429
    f = request.files.get("audio")
    if not f:
        return jsonify(error="no audio"), 400
    data = {"language_code": stt_code(request.form), "format": "transcribe"}
    if STT_MODEL:
        data["model"] = STT_MODEL
    try:
        r = HTTP.post(
            STT_URL,
            headers={"X-API-Key-ID": API_KEY, "X-API-Request-ID": str(uuid.uuid4())},
            files={"audio_file": ("speech.wav", f.read(), "audio/wav")},
            data=data,
            timeout=60,
        )
    except requests.RequestException as e:
        return jsonify(error=f"Could not reach Prisma: {e}"), 502
    try:
        body = r.json()
    except ValueError:
        return jsonify(error=f"Prisma returned {r.status_code}: {r.text[:200]}"), 502
    if r.status_code != 200 or not body.get("success", True):
        return jsonify(error=body.get("message") or body.get("detail") or body), r.status_code
    return jsonify(transcript=body.get("transcript", ""),
                   detected=body.get("detected_language_code"),
                   model=body.get("model"),
                   latency=body.get("end_to_end_latency") or body.get("processing_time"))


# Every visitor hears the same questions ("Aapki umar kitni hai?"), so Timbre audio is kept in memory:
# a repeated line comes back in milliseconds instead of ~1 s, and costs no credits. ~300 MP3 clips ≈ 10 MB.
TTS_CACHE: "OrderedDict[tuple, bytes]" = OrderedDict()
TTS_CACHE_MAX = int(os.environ.get("TTS_CACHE_MAX", "300"))
TTS_CACHE_LOCK = threading.Lock()
# Timbre allows only ONE active request per API key ("Only 1 active request is allowed at a time", checked
# 10 Nov 2026). Several visitors at once would get 429s, so calls wait their turn here instead (~0.6 s each).
TIMBRE_TURN = threading.Lock()


def _audio(body: bytes, mimetype="audio/mpeg"):
    return Response(body, mimetype=mimetype, headers={"Cache-Control": "public, max-age=86400"})


TTS_PENDING: dict = {}                       # (lang, text) -> Event, while that clip is being made


def speech_parts(text: str) -> list:
    """Split a reply into the pieces Timbre voices one by one (the page plays them in order).
    One sentence each: Timbre takes ~1.3 s + ~12 ms per character (measured 10 Nov 2026), so a long block after a
    short first sentence left a gap of seconds. A very short first sentence ("Namaste!") joins the next one."""
    parts = [x.strip() for x in re.split(r"(?<=[।!?.])\s+", str(text or "")) if x.strip()]
    if len(parts) > 1 and len(parts[0]) < 20:
        parts[:2] = [parts[0] + " " + parts[1]]
    return parts or ([str(text)] if text else [])


class TimbreError(Exception):
    def __init__(self, body, status):
        super().__init__(str(body))
        self.body, self.status = body, status


def synthesize(text: str, lang: str) -> bytes:
    """Timbre MP3 for one piece of speech: from the cache, or by waiting for the same clip already being made,
    or by making it (one Timbre call at a time, see TIMBRE_TURN)."""
    key = (lang, text)
    with TTS_CACHE_LOCK:
        if key in TTS_CACHE:
            TTS_CACHE.move_to_end(key)
            return TTS_CACHE[key]
        ev = TTS_PENDING.get(key)
        mine = ev is None
        if mine:
            ev = TTS_PENDING[key] = threading.Event()
    if not mine:                                         # someone (often our own warm-up) is making it right now
        ev.wait(30)
        with TTS_CACHE_LOCK:
            if key in TTS_CACHE:
                return TTS_CACHE[key]
        raise TimbreError("voice busy", 503)
    try:
        payload = {
            "text": text, "model": TTS_MODEL, "voice": TTS_VOICE, "language": langs.code(lang),
            "speed": 0.95,                       # a touch slower: easier for older listeners
            # MP3 is ~6x smaller than WAV (99 KB vs 603 KB for the greeting), so it reaches the phone much sooner
            "audio_config": {"sample_rate": 24000, "container": "mp3", "bitrate": "64k"},
        }
        if not TIMBRE_TURN.acquire(timeout=25):
            raise TimbreError("voice busy", 429)
        try:
            for wait in (0.3, 0.6, None):                   # 429 can still come from another server/process
                try:
                    r = HTTP.post(TTS_URL, headers={"Content-Type": "application/json", "X-API-Key-ID": API_KEY},
                                  json=payload, timeout=60)
                except requests.RequestException as e:
                    raise TimbreError(f"Could not reach Timbre: {e}", 502)
                if r.status_code != 429 or wait is None:
                    break
                time.sleep(wait)
        finally:
            TIMBRE_TURN.release()
        if r.status_code != 200 or not r.headers.get("Content-Type", "").startswith("audio"):
            try:
                err = r.json()
            except ValueError:
                err = r.text[:200]
            raise TimbreError(err, r.status_code if r.status_code != 200 else 502)
        if len(text) <= 400:
            with TTS_CACHE_LOCK:
                TTS_CACHE[key] = r.content
                while len(TTS_CACHE) > TTS_CACHE_MAX:
                    TTS_CACHE.popitem(last=False)
        return r.content
    finally:
        with TTS_CACHE_LOCK:
            TTS_PENDING.pop(key, None)
        ev.set()


def warm_speech(parts, lang):
    """Start voicing a reply as soon as it's written, in order, so each piece is (nearly) ready by the time the
    page asks for it, instead of starting only when the page asks. Counts once against the visitor's TTS limit."""
    if not API_KEY or not parts or os.environ.get("TTS_WARM", "1") != "1" or rate_limited("tts"):
        return

    def run():
        for part in parts[:8]:
            try:
                synthesize(part, lang)
            except Exception:
                return
    threading.Thread(target=run, daemon=True).start()


def with_speech(out: dict, lang: str) -> dict:
    out["say_parts"] = speech_parts(out.get("say") or "")
    warm_speech(out["say_parts"], lang)
    return out


@app.post("/api/metric")
def metric():
    """Timing marks from the page (tap -> reply -> voice), printed to the server log to find slow steps."""
    if rate_limited("metric"):
        return Response(status=204)
    body = " ".join((request.get_data(as_text=True) or "")[:1500].split())
    print("METRIC", body, flush=True)
    return Response(status=204)


@app.post("/api/tts")
def tts():
    """Text -> Timbre MP3. Returns 204 if no key, so the page can fall back to the browser voice."""
    if not API_KEY:
        return Response(status=204)
    j = request.get_json(force=True) or {}
    text, lang = (j.get("text") or "").strip(), langs.valid(j.get("lang", "hi"))
    if not text:
        return jsonify(error="empty text"), 400
    key = (lang, text)
    with TTS_CACHE_LOCK:
        cached = key in TTS_CACHE or key in TTS_PENDING
    if not cached and rate_limited("tts"):
        return jsonify(error="rate limited"), 429           # page falls back to the browser voice
    try:
        return _audio(synthesize(text, lang))
    except TimbreError as e:
        return jsonify(error=e.body), e.status


@app.post("/api/ask")
def ask_route():
    """Follow-up chat about a scheme: {text, lang, focus, eligible: [{id, name, why}]}"""
    j = request.get_json(force=True) or {}
    cards = j.get("eligible") or []
    lang = reply_lang(j)
    out = ask.answer(
        langs.for_parsing(j.get("text") or "", lang), lang, focus=j.get("focus"),
        eligible_ids=[c["id"] for c in cards] or None,
        names={c["id"]: c.get("name", c["id"]) for c in cards},
        why={c["id"]: c.get("why", "") for c in cards},
    )
    out["lang"] = lang
    return jsonify(with_speech(out, lang))


def reply_lang(j, settled=True):
    """Answer in the language the person spoke, unless they picked one in the UI (auto = false).
    settled: they've answered before, so the language only changes on clear evidence (see langs.detect)."""
    lang = langs.valid(j.get("lang") or "hi")
    if j.get("auto", True) and (j.get("text") or "").strip():
        lang = langs.detect(j["text"], j.get("detected"), lang, settled=settled)
    return lang


@app.post("/api/turn")
def turn():
    j = request.get_json(force=True) or {}
    asked = (j.get("state") or {}).get("asked")
    settled = bool(asked) and asked != "intro"            # the first answer picks the language; later ones rarely
    lang = reply_lang(j, settled)
    out = dialog.turn(j.get("state") or {}, langs.for_parsing(j.get("text") or "", lang), lang)
    return jsonify(with_speech(out, out.get("lang") or lang))


if __name__ == "__main__":
    print(f"Gnani key loaded: {bool(API_KEY)}  |  STT {STT_MODEL or 'prisma-v2.5'}  |  TTS {TTS_MODEL}/{TTS_VOICE}")
    print("Hands-free streaming:", "ON" if STREAMING_LIB else "OFF (pip install flask-sock websockets)")
    print("LLM for off-script questions:", "ON" if all(ask.llm_config()) else "OFF (answers only from kb.py)")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False, threaded=True)
