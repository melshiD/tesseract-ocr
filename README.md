# OCR API with TrOCR and Tesseract

A FastAPI-based OCR service that provides both traditional printed text recognition (Tesseract) and advanced handwritten text recognition (TrOCR).

## Features

- **📄 Printed Text OCR**: Traditional OCR using Tesseract for printed documents
- **✍️ Handwritten Text Recognition**: Advanced handwriting recognition using Microsoft's TrOCR
- **🚀 Fast API**: RESTful API with automatic documentation
- **☁️ Cloud Ready**: Optimized for Render deployment with native Python

## Endpoints

### `GET /`
Returns API information and available endpoints.

### `POST /ocr` 
Traditional OCR for printed text using Tesseract.
- **Input**: Image file (PNG, JPG, etc.)
- **Output**: Extracted text with metadata

### `POST /trocr`
Handwritten text recognition using TrOCR (Microsoft transformer model).
- **Input**: Image file with handwritten text
- **Output**: Recognized handwritten text with metadata

## Quick Start

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

3. **Test the API**:
   ```bash
   python3 test_api.py
   ```

4. **Access the API**:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Deploy to Render

1. **Connect your GitHub repo** to Render
2. **Select Web Service** with these settings:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

Or use the included `render.yaml` for automatic deployment.

## Usage Examples

### cURL Examples

**Test printed text OCR:**
```bash
curl -X POST "http://localhost:8000/ocr" \
  -F "file=@your_printed_document.jpg"
```

**Test handwritten text recognition:**
```bash
curl -X POST "http://localhost:8000/trocr" \
  -F "file=@your_handwritten_note.jpg"
```

### Python Client Example

```python
import requests

# Test OCR endpoint
with open('document.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/ocr',
        files={'file': f}
    )
    result = response.json()
    print(f"Extracted text: {result['text']}")

# Test TrOCR endpoint  
with open('handwritten.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/trocr', 
        files={'file': f}
    )
    result = response.json()
    print(f"Handwritten text: {result['text']}")
```

## API Response Format

Both endpoints return JSON with this structure:
```json
{
  "text": "Extracted text content",
  "method": "tesseract|trocr-handwritten", 
  "filename": "uploaded_file.jpg"
}
```

Error responses:
```json
{
  "error": "Detailed error message"
}
```

## Dependencies

- **FastAPI**: Web framework
- **TrOCR**: Microsoft's transformer-based handwriting OCR
- **Tesseract**: Traditional OCR engine
- **PyTorch**: ML framework for TrOCR
- **Pillow**: Image processing

## Performance Notes

- **TrOCR**: Better for handwritten text, slower processing
- **Tesseract**: Better for printed text, faster processing
- **Model Loading**: TrOCR models load on startup (may take 30-60 seconds)
- **Memory Usage**: ~1-2GB RAM for TrOCR models

## Tips for Best Results

### For Tesseract (/ocr):
- Use high-contrast, clear printed text
- Ensure good lighting and minimal skew
- Works best with typed documents, books, signs

### For TrOCR (/trocr):
- Works great with handwritten notes
- Handles cursive and print handwriting
- Best with single lines of text
- Good lighting improves accuracy

## Troubleshooting

**"transformers not found"**: Run `pip install transformers`

**TrOCR loading errors**: Ensure you have enough memory (1GB+) and stable internet for model download

**Tesseract errors**: Make sure tesseract-ocr is installed on your system

**Deployment issues**: Check that all dependencies in requirements.txt are correct

## Files

- `app.py` - Main FastAPI application
- `requirements.txt` - Python dependencies
- `render.yaml` - Render deployment configuration
- `test_api.py` - API testing script
- `README.md` - This documentation

## License

Open source - feel free to modify and use for your projects!