from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pytesseract
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import numpy as np
import traceback
import requests
from PIL import Image
from pathlib import Path
import io
import os

app = FastAPI()

trocr_processor = TrOCRProcessor.from_pretrained('microsoft//trocr-base-handwritten')
trocr_model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten

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

@app.post("/trocr")
async def extract_trocr(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Preprocess image and run inference
        pixel_values = trocr_processor(images=image, return_tensors="pt").pixel_values
        generated_ids = trocr_model.generate(pixel_values)
        text = trocr_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return {"text": text}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})