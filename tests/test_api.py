"""Checks the Flask routes send Gnani exactly what the docs describe (network mocked)."""
import io
import os
import sys
import wave

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["GNANI_API_KEY"] = "test-key"

import app as appmod  # noqa: E402

calls = []


class Fake:
    def __init__(self, status, json_body=None, content=b"", ctype="application/json"):
        self.status_code, self._j, self.content, self.headers = status, json_body, content, {"Content-Type": ctype}
        self.text = str(json_body)

    def json(self):
        return self._j


def fake_post(url, headers=None, files=None, data=None, json=None, timeout=None):
    calls.append(dict(url=url, headers=headers, files=files, data=data, json=json))
    if "stt" in url:
        return Fake(200, {"success": True, "transcript": "मैं 35 साल का हूं", "model": "prisma-v3.0",
                          "detected_language_code": "hi-IN", "end_to_end_latency": 0.5})
    return Fake(200, content=b"RIFF....WAVE", ctype="audio/wav")


def tiny_wav():
    b = io.BytesIO()
    with wave.open(b, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000); w.writeframes(b"\x00\x00" * 1600)
    return b.getvalue()


def test_routes():
    appmod.API_KEY = "test-key"
    appmod.HTTP.post = fake_post
    c = appmod.app.test_client()

    r = c.post("/api/stt", data={"lang": "hi", "audio": (io.BytesIO(tiny_wav()), "speech.wav")},
               content_type="multipart/form-data")
    assert r.status_code == 200 and r.get_json()["transcript"].startswith("मैं"), r.get_json()
    stt = calls[-1]
    assert stt["url"] == "https://api.vachana.ai/stt/v3"
    assert stt["headers"]["X-API-Key-ID"] == "test-key"
    # auto mode, language not known yet -> Prisma works it out itself
    assert stt["data"] == {"language_code": "indic-auto", "format": "transcribe", "model": "prisma-v3.0"}
    assert "audio_file" in stt["files"]
    # Auto mode keeps indic-auto even once the language is known (so a switch of language is still followed)
    c.post("/api/stt", data={"lang": "ta", "auto": "1", "known": "1", "audio": (io.BytesIO(tiny_wav()), "s.wav")},
           content_type="multipart/form-data")
    assert calls[-1]["data"]["language_code"] == "indic-auto"
    # picked by hand -> that language + English as a hint (REST accepts a list)
    c.post("/api/stt", data={"lang": "hi", "auto": "0", "audio": (io.BytesIO(tiny_wav()), "s.wav")},
           content_type="multipart/form-data")
    assert calls[-1]["data"]["language_code"] == "hi-IN,en-IN"
    # ...but the live stream only accepts ONE locale ("exactly one locale is required", real API, 9 Nov 2026)
    assert appmod.langs.stt_code("ta", auto=False, stream=True) == "ta-IN"
    assert appmod.langs.stt_code("ta", auto=True, known=True, stream=True) == "indic-auto"
    for lang in appmod.langs.ALL:
        assert "," not in appmod.langs.stt_code(lang, auto=False, stream=True)

    r = c.post("/api/tts", json={"text": "வணக்கம்", "lang": "ta"})
    assert calls[-1]["json"]["language"] == "ta-IN"

    # auto-detect: answering in Tamil switches the conversation to Tamil
    r = c.post("/api/turn", json={"state": {}, "text": "", "lang": "hi"}).get_json()
    r = c.post("/api/turn", json={"state": r["state"], "text": "நான் 34 வயது விவசாயி", "lang": "hi",
                                  "detected": "ta-IN", "auto": True}).get_json()
    assert r["lang"] == "ta" and r["state"]["profile"]["age"] == 34
    # ...but not when the person picked Hindi by hand
    r = c.post("/api/turn", json={"state": {}, "text": "நான் 34 வயது", "lang": "hi", "auto": False}).get_json()
    assert r["lang"] == "hi"

    r = c.post("/api/tts", json={"text": "नमस्ते", "lang": "hi"})
    assert r.status_code == 200 and r.mimetype == "audio/wav"
    tts = calls[-1]
    assert tts["url"] == "https://api.vachana.ai/api/v1/tts/inference"
    assert tts["json"]["model"] == "timbre-v3.0" and tts["json"]["voice"] == "Shivani"
    assert tts["json"]["language"] == "hi-IN" and tts["json"]["audio_config"]["container"] == "mp3"

    r = c.post("/api/turn", json={"state": {}, "text": "", "lang": "hi"})
    assert r.get_json()["state"]["asked"] == "intro"

    appmod.API_KEY = ""
    assert c.post("/api/tts", json={"text": "hi", "lang": "en"}).status_code == 204   # browser-voice fallback


if __name__ == "__main__":
    test_routes()
    print("ok   test_routes")
