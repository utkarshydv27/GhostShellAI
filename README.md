# 👻 GhostShell AI — The Terminal That Remembers

A spooky, local-first terminal experience powered by an open-weight model through Ollama. Whisper to a fictional ghost, generate eerie stories, and keep a local archive of sessions.

**Hacktoberfest Open-Source AI Challenge · Week 4: Ghost in the Machine**

## Features
- Terminal Whispers and Ghost Story modes
- Ollama model status and configurable model
- Built-in fictional fallback if Ollama is offline (not AI inference)
- Local JSONL session archive, excluded from Git
- Safe simulated terminal: it never executes shell commands

## Requirements
Python 3.10+ and [Ollama](https://ollama.com/). Default model: `qwen2.5:1.5b`.

## Windows setup
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
ollama pull qwen2.5:1.5b
python app.py
```
Open http://127.0.0.1:5000. If activation is blocked, use ` .\.venv\Scripts\python.exe -m pip install -r requirements.txt` and ` .\.venv\Scripts\python.exe app.py`.

## Offline mode
After downloading Ollama and the model, local inference can work without internet. The stylesheet loads Google Fonts online; remove its `@import` line for a fully offline UI. The fallback is not AI inference.

## Configure model
```powershell
$env:OLLAMA_MODEL = "qwen2.5:1.5b"
$env:OLLAMA_URL = "http://localhost:11434"
python app.py
```

## Privacy
Prompts go to the Ollama server configured by `OLLAMA_URL` (local by default). No hosted LLM API is called. Logs stay in `data/ghost_sessions.jsonl`; do not put secrets in prompts.

## API
- `GET /api/status`
- `POST /api/whisper` with `{"message":"What is in the dark?","mode":"terminal"}` or mode `story`
- `GET /api/memories`

## Why open innovation matters
GhostShell uses local inference rather than a closed hosted AI API. The model and prompt can be swapped or customized, and prompts can stay on a computer the user controls. After setup and model download, inference can work offline without a per-request hosted model API bill (hardware and electricity still cost money). A closed API may be more capable on some tasks, but depends on external service availability, pricing, and sending prompts to a provider.

Built for the [Hacktoberfest Open-Source AI Challenge — Week 4](https://dev.to/challenges/hacktoberfest-week4-2026-10-26). Test it, record a demo, and add the actual repository/demo links before submitting.

## License
Application code is MIT licensed. The selected model has separate licence terms.
