from fastapi import FastAPI, File, UploadFile
import pytesseract
from PIL import Image
import io

app = FastAPI()

@app.post("/ocr")
async def extract_text(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    return {"text": text}
