"""Canteen Calorie Estimator - backend.

Snap a photo of a Chinese canteen meal (or type a description) and get an
estimate of calories + protein/carbs/fat, using a local open-weight vision
model through Ollama. Nothing leaves the device.

Demo mode: if Ollama is not reachable, the API returns a clearly-labeled
sample estimation so the UI flow can still be tried.
"""

import base64
import json
import os
import urllib.request

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
# Default to Gemma 3 (open weights, vision-capable). Swap with e.g.
# CAL_MODEL=qwen2.5vl for stronger Chinese.
MODEL = os.environ.get("CAL_MODEL", "gemma3")

SYSTEM_PROMPT = (
    "你是一位中餐营养师，擅长估算中国高校食堂菜品的热量。\n"
    "用户会给你一张食堂餐食照片，或一段文字描述。\n"
    "请识别每一道菜，按常见食堂份量估算重量，然后给出每道菜和整餐的"
    "热量（kcal）与蛋白质/碳水/脂肪（克）。\n"
    "注意：食堂大锅菜通常偏油，估算时要考虑烹调用油；不确定的地方保守估计。\n"
    "只返回 JSON，不要输出其他文字，格式如下：\n"
    '{"dishes":[{"name":"菜名","portion":"份量描述","calories":123,'
    '"protein_g":1.2,"carbs_g":2.3,"fat_g":4.5}],'
    '"total":{"calories":123,"protein_g":1.2,"carbs_g":2.3,"fat_g":4.5},'
    '"note":"一句话说明估算依据或不确定性"}'
)

# Clearly-labeled sample used when no local model is available.
DEMO_RESULT = {
    "dishes": [
        {"name": "米饭", "portion": "约200g（一碗）", "calories": 232,
         "protein_g": 5.2, "carbs_g": 51.2, "fat_g": 1.0},
        {"name": "青椒炒肉", "portion": "约150g", "calories": 285,
         "protein_g": 14.0, "carbs_g": 8.0, "fat_g": 22.0},
        {"name": "清炒时蔬", "portion": "约120g", "calories": 95,
         "protein_g": 2.5, "carbs_g": 6.0, "fat_g": 7.5},
    ],
    "total": {"calories": 612, "protein_g": 21.7, "carbs_g": 65.2, "fat_g": 30.5},
    "note": "演示数据：本地模型不可用时的示例输出，非真实估算。",
}

app = FastAPI(title="Canteen Calorie Estimator")


def _ollama_generate(image_b64: str | None, description: str) -> dict | None:
    """Call the local Ollama model. Returns parsed JSON dict, or None on failure."""
    if description:
        user_content = f"这顿饭的文字描述：{description}\n请按上面的 JSON 格式估算。"
    else:
        user_content = "请按上面的 JSON 格式估算这张照片里的餐食。"
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content,
         "images": [image_b64] if image_b64 else []},
    ]
    payload = json.dumps(
        {"model": MODEL, "messages": messages, "stream": False,
         "format": "json", "options": {"temperature": 0.2}}
    ).encode()
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/chat", data=payload,
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode())
        return json.loads(data["message"]["content"])
    except Exception:
        return None


@app.get("/api/health")
def health():
    try:
        urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=3)
        return {"model": MODEL, "ollama": "ok", "demo": False}
    except Exception:
        return {"model": MODEL, "ollama": "unreachable", "demo": True}


@app.post("/api/estimate")
async def estimate(
    file: UploadFile | None = File(default=None),
    description: str = Form(default=""),
):
    image_b64 = None
    if file is not None:
        raw = await file.read()
        if raw:
            image_b64 = base64.b64encode(raw).decode()
    if not image_b64 and not description.strip():
        return {"error": "请上传照片或输入文字描述。", "demo": True}
    result = _ollama_generate(image_b64, description.strip())
    if result is None:
        return {"demo": True, **DEMO_RESULT}
    return {"demo": False, **result}


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")
