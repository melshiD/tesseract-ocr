from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pytesseract
from kraken import binarization, pageseg, rpred
import numpy as np
from PIL import Image
import io

app = FastAPI()

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
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert('L') #grayscale

    # Binarize and segment
    img = binarization.nlbin(image)
    seg = pageseg.segment(img)
    model = rpred.load_any('default') #or use custom model
    preds = rpred.rpred(model, img, seg)

    text = "\n".join([pred.prediction for pred in preds])
    return {"text" : text}