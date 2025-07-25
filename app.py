from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pytesseract
from kraken import binarization, pageseg, rpred
import numpy as np
import traceback
from PIL import Image
from pathlib import Path
import io
import os

app = FastAPI()

MODEL_PATH = "app/models/handwriting.mlmodel"
MODEL_URL = "https://kraken-models.mittagqi.dev/models/2023-07-12-handwriting.mlmodel"

def ensure_model():
    if not Path(MODEL_PATH).exists():
        print("Downloading Kraken model at runtime...")
        os.makedirs(os.path.dirname(MODEL_PATH), exists_ok=True)
        r = requests.get(MODEL_URL)
        r.raise_for_status()
        with open(MODEL_PATH, "wb") as f:
            f.write(r.content)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5501",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/ocr")
async def extract_text(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    return {"text": text}

@app.post("/kraken")
async def extract_handwriting(file: UploadFile = File(...)):
    try:
        ensure_model()

        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert('L')  # grayscale

        # Binarize and segment
        img = binarization.nlbin(image)
        seg = pageseg.segment(img)
        model = rpred.load_model(MODEL_PATH)
        preds = rpred.rpred(model, img, seg)

        text = "\n".join([pred.prediction for pred in preds])
        return {"text": text}

    except Exception as e:
        print("KRAKEN ERROR:", traceback.format_exc())  # Show full traceback in Render logs
        return JSONResponse(status_code=500, content={"error": str(e)})