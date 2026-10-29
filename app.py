import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path

import requests
from flask import Flask, jsonify, render_template, request

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)
LOG = DATA / "ghost_sessions.jsonl"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")
app = Flask(__name__)
SYSTEM = "You are GhostShell, a fictional haunted terminal for Halloween. Be eerie, playful, and concise. Never claim to be a real ghost. Never execute commands or claim they were run. Do not request secrets. Keep dangerous requests fictional and harmless."

def save_event(mode, prompt, reply, model):
    event = {"timestamp": datetime.now(timezone.utc).isoformat(), "mode": mode, "prompt": prompt[:1000], "reply": reply[:4000], "model": model}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

def ask_ollama(prompt, mode):
    response = requests.post(f"{OLLAMA_URL.rstrip('/')}/api/generate", json={"model": OLLAMA_MODEL, "prompt": f"{SYSTEM}\nMode: {mode}\nUser: {prompt}", "stream": False}, timeout=90)
    response.raise_for_status()
    return response.json().get("response", "").strip() or "…the terminal answered with silence."

def fallback(mode):
    if mode == "story":
        return "At 03:17, a file appeared on a machine that had never been online. Its name was yesterday.txt. Inside was one line: You forgot to shut me down. The cursor blinked twice, then the file vanished."
    return random.choice(["The cursor blinks. Something on the other side of the screen is waiting.", "A forgotten process stirs in the dark. It knows this is only a simulation.", "A cold pixel flickers. Nothing was executed; the haunting is only a story."])

@app.get("/")
def index():
    return render_template("index.html", model=OLLAMA_MODEL)

@app.get("/api/status")
def status():
    try:
        response = requests.get(f"{OLLAMA_URL.rstrip('/')}/api/tags", timeout=3)
        response.raise_for_status()
        models = [item.get("name", "") for item in response.json().get("models", [])]
        return jsonify(ok=True, ollama=True, model=OLLAMA_MODEL, model_available=OLLAMA_MODEL in models, models=models)
    except requests.RequestException:
        return jsonify(ok=True, ollama=False, model=OLLAMA_MODEL, model_available=False, models=[])

@app.post("/api/whisper")
def whisper():
    body = request.get_json(silent=True) or {}
    prompt = str(body.get("message", "")).strip()[:1000]
    mode = str(body.get("mode", "terminal"))
    if not prompt:
        return jsonify(error="Type a message first."), 400
    if mode not in {"terminal", "story"}:
        mode = "terminal"
    try:
        reply = ask_ollama(prompt, mode)
        source = "ollama"
    except (requests.RequestException, ValueError):
        reply = fallback(mode)
        source = "fallback"
    save_event(mode, prompt, reply, OLLAMA_MODEL if source == "ollama" else "offline-fallback")
    return jsonify(reply=reply, source=source, model=OLLAMA_MODEL)

@app.get("/api/memories")
def memories():
    events = []
    if LOG.exists():
        for line in LOG.read_text(encoding="utf-8").splitlines()[-20:]:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return jsonify(events=list(reversed(events)))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
