# Canteen Calorie Estimator 🍱

Snap a photo of a Chinese canteen meal — or just describe it in one sentence —
and get an estimate of calories plus protein/carbs/fat, from a **local
open-weight vision model**. Nothing leaves your device. Built for a friend
who is cutting, for the Hacktoberfest 2026 "Build for a Friend" weekend challenge.

## Why this exists

My friend and I are both students trying to lose weight while eating at the
campus canteen three times a day. Existing calorie apps are trained on Western
food and fall apart on Chinese canteen dishes — a ladle of mapo tofu or a
scoop of braised pork belly gets wildly mis-estimated, and the oily
stir-fry style of canteen cooking is a blind spot. So I built a tiny tool
tuned for exactly that: Chinese canteen food, estimated by an open model
running on my own laptop.

## Features

- 📸 Photo or one-line text description → per-dish + total kcal, protein/carbs/fat
- 🧠 Local inference via Ollama — default **Gemma 3** (open weights, vision-capable)
- 🔒 Privacy: photos never leave the device; daily log lives in browser localStorage
- 💰 Free: no API bills, no subscriptions
- 📝 Daily log with a calorie target, so a cut actually stays on track
- 🧪 Demo mode: works (with labeled sample data) even without a local model

## Quickstart

```bash
# 1. Install Ollama from https://ollama.com, then pull a vision model
ollama pull gemma3          # default; ~3.3 GB for the 4B model

# 2. Run (from this directory)
./run.sh
# or manually: pip install -r requirements.txt && uvicorn app:app --port 8000
```

Open http://localhost:8000, upload a canteen photo (or type e.g.
"一碗米饭＋青椒炒肉＋清炒时蔬"), and hit 估算.

Requirements: Python 3.10+.

Environment variables:
- `CAL_MODEL` — model name (default `gemma3`; e.g. `qwen2.5vl` for stronger Chinese)
- `OLLAMA_URL` — Ollama endpoint (default `http://localhost:11434`)

## How the estimation works

The photo/description is sent to the local vision model with a nutritionist
system prompt written for Chinese canteen cooking (portion norms, cooking-oil
bias, conservative estimates). The model returns structured JSON —
dishes, portions, kcal and macros — which the app renders as a table plus a
daily total. No training, no fine-tuning; the "model" here is careful
prompting on top of an open-weight VLM.

## Limitations (honest)

- Estimates, not measurements — canteen portions vary; treat numbers as guidance.
- Needs a machine that can run a VLM (Gemma 3 4B ≈ 3.5 GB RAM/VRAM).
- Without Ollama running, the app falls back to clearly-labeled demo data.

## License

MIT — fork it, fine-tune it on your own canteen, make it yours.
