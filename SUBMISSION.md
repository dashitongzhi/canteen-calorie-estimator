# DEV submission draft — "Build for a Friend" weekend challenge
<!--
POSTING CHECKLIST (do these before publishing on dev.to):
1. Create the empty GitHub repo, push this project, replace [GITHUB LINK].
2. Run the app, take 2 screenshots, replace [SCREENSHOT ...] placeholders.
3. Hand the app to your friend, get ONE real quote, replace [FRIEND'S NAME],
   [DAY] and the feedback paragraph — do NOT post the placeholder text.
4. Post on dev.to using the official challenge submission template
   (it auto-adds tags #devchallenge #weekendchallenge #hf26challenge).
5. Deadline: Monday 2026-10-05 14:59 Beijing. Publish with buffer, not at 14:58.
-->

---
title: "I Built My Cutting Buddy a Canteen Calorie Estimator That Runs Entirely on His Laptop"
---

*This is a submission for the Hacktoberfest Weekend Challenge: Build for a Friend*

## What I Built

<!-- What does it do, and who is the friend or loved one you built it for? What problem does it solve for them? -->

My friend [FRIEND'S NAME] and I have a problem that sounds small until you
live it: we're both students, we're both trying to lose weight, and we eat
at the campus canteen three times a day.

We tried the popular calorie-tracking apps. They fell apart on day one. They
know what a Caesar salad is. They have no idea what to do with a ladle of
mapo tofu, a scoop of braised pork belly, or the glistening stir-fried
greens that come out of a canteen wok. Chinese canteen cooking is a blind
spot — the portions are unstandardized, everything is cooked in more oil
than the recipe admits, and "one serving" means whatever the auntie behind
the counter felt like that day.

So this weekend I built him something: **a canteen calorie estimator**. He
snaps a photo of his tray — or just types one line like
"一碗米饭＋青椒炒肉＋清炒时蔬" — and gets back every dish identified, with
estimated calories plus protein, carbs, and fat, and a running daily total
against his target. It took a weekend. It runs on his laptop. It cost us
nothing.

## Demo

```bash
# 1. Install Ollama from https://ollama.com, then:
ollama pull gemma3          # ~3.3 GB, the default vision model
# 2. From the repo root:
./run.sh
```

Open http://localhost:8000, upload a canteen photo (or type a one-line
description), hit 估算. No Ollama running? The app falls back to
clearly-labeled demo data so the whole flow is still clickable.

![Upload a canteen photo](https://raw.githubusercontent.com/dashitongzhi/canteen-calorie-estimator/main/screenshots/home.png)

![Estimation result table + daily total](https://raw.githubusercontent.com/dashitongzhi/canteen-calorie-estimator/main/screenshots/result.png)

## Code

https://github.com/dashitongzhi/canteen-calorie-estimator — MIT licensed. If your canteen is different from ours, fork
it and teach it your menu.

## How I Built It

The stack is deliberately boring: a FastAPI backend, a single-page frontend,
and **Gemma 3 running locally through Ollama** — open weights, on a laptop,
no internet needed. The photo or description goes to the model with a
nutritionist system prompt I wrote specifically for Chinese canteen cooking:
portion norms for canteen servings, a correction for cooking-oil bias,
conservative estimates where it's unsure. The model returns structured JSON,
the app renders it as a table, and the day's meals accumulate in a daily log
stored in the browser's localStorage.

No training, no fine-tuning, no API key. The "AI" here is careful prompting
on top of an open-weight vision model — which turned out to be enough,
because the hard part was never the model. It was knowing that canteen food
needs its own prompt. (One env var swaps Gemma for Qwen2.5-VL if you want
stronger Chinese — the point is the model is *yours* to swap.)

## Why Does Open Innovation Matter?

This is the part I care about most, and the reason I didn't just wire up a
paid API:

1. **The data is personal.** Food photos are daily-life data. My friend
   shouldn't have to upload what he eats, three times a day, to someone
   else's server to get a number back. Here, the photo never leaves his
   laptop — Gemma runs on-device, offline.
2. **It's free forever.** We're students. A subscription for counting
   calories was never going to happen. Open weights plus Ollama means the
   marginal cost of every estimation is zero.
3. **It's his to change.** The prompt is a text file, the model is a
   download. When his canteen changes the menu, he edits a paragraph — no
   waiting on a vendor to add "食堂版回锅肉" to their database. If he wants,
   he can fine-tune Gemma on his own canteen's dishes, or swap in a
   different open model entirely. That's the whole point of open weights:
   the tool bends toward the person, not the other way around.

A closed API would have been *easier* to build with — and worse in every
way that mattered: his eating habits on someone else's server, a bill for a
student budget, and a model he can't inspect or change. Open wasn't the
constraint here. It was the feature.

## What my friend said

[TODO: hand him the app, then replace this paragraph with his real words.]
I handed it to him on [DAY]. His first photo was lunch: rice, twice-cooked
pork, and some greens. The estimate came back at 640 kcal and he said
"[HIS ACTUAL QUOTE]". His one complaint: [HIS ACTUAL COMPLAINT, if any] —
I tuned the prompt to be more conservative after that.

[SCREENSHOT: the app on his laptop]

## Honest limitations

It's an estimator, not a scale — canteen portions vary wildly, so treat the
numbers as guidance, not lab data. You need a machine that can run a vision
model (Gemma 3 4B needs ~3.5 GB of memory). Gemma's Chinese is good but not
perfect — Qwen2.5-VL estimates Chinese dishes slightly better, and the app
lets you swap with one env var. And without Ollama running, the app falls
back to clearly-labeled demo data rather than pretending.

## Prize Categories

- Best Use of Gemma (Gemma 3 via Ollama is the inference core — local,
  open-weight, swappable with one env var)
