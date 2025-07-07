import os
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from nudenet import NudeDetector

app = FastAPI(title="NSFW Moderation via NudeDetector")

# Загружаем одну модель при старте
detector = NudeDetector()           # скачает вес 8-9 МБ при первом запуске
THRESHOLD = 0.7                     # score > 0.7 = NSFW

@app.post("/moderate")
async def moderate(file: UploadFile = File(...)):
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(415, "Разрешены только .jpg и .png")

    img_bytes = await file.read()
    if not img_bytes:
        raise HTTPException(400, "Пустой файл")

    # NudeDetector принимает путь, поэтому пишем во временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(img_bytes)
        tmp_path = tmp.name

    try:
        detections = detector.detect(tmp_path)   # список словарей
        unsafe_score = max((d["score"] for d in detections), default=0.0)
    finally:
        os.remove(tmp_path)

    if unsafe_score > THRESHOLD:
        return {"status": "REJECTED", "reason": "NSFW content"}
    return {"status": "OK"}
