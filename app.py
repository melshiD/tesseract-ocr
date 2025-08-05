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

# Global variables to store models (will be loaded on first request)
trocr_processor = None
trocr_model = None

def load_trocr_models():
    """Lazy loading function for TrOCR models"""
    global trocr_processor, trocr_model
    
    if trocr_processor is None or trocr_model is None:
        print("Loading TrOCR models (first request)...")
        trocr_processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
        trocr_model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
        print("TrOCR models loaded successfully!")
    
    return trocr_processor, trocr_model

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

@app.get("/")
async def root():
    return {
        "message": "OCR API with Tesseract and TrOCR",
        "endpoints": {
            "/ocr": "Traditional OCR for printed text (Tesseract)",
            "/trocr": "Handwritten text recognition (TrOCR)"
        },
        "usage": "POST image files to /ocr or /trocr endpoints"
    }

@app.post("/ocr")
async def extract_text(file: UploadFile = File(...)):
    try:
        print(f"Processing OCR request for file: {file.filename}")
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        text = pytesseract.image_to_string(image)
        print(f"OCR completed, extracted {len(text)} characters")
        return {"text": text, "method": "tesseract", "filename": file.filename}
    except Exception as e:
        print(f"OCR error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": f"OCR failed: {str(e)}"})

@app.post("/trocr")
async def extract_trocr(file: UploadFile = File(...)):
    try:
        print(f"Processing TrOCR request for file: {file.filename}")
        
        # Load models on first request (lazy loading)
        processor, model = load_trocr_models()
        
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        
        print(f"Image loaded: {image.size} pixels")

        # Preprocess image and run inference
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values)
        text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        print(f"TrOCR completed, extracted text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        return {"text": text, "method": "trocr-handwritten", "filename": file.filename}
    except Exception as e:
        print(f"TrOCR error: {str(e)}")
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": f"TrOCR failed: {str(e)}"})