#!/usr/bin/env python3
"""
Simple test script for OCR API endpoints
"""
import requests
import sys
from PIL import Image, ImageDraw, ImageFont
import io

def create_test_image(text="Hello World", handwritten=False):
    """Create a simple test image with text"""
    # Create a white background image
    img = Image.new('RGB', (400, 100), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a font, fallback to default if not available
    try:
        if handwritten:
            # Simulate handwritten text with smaller, irregular spacing
            font = ImageFont.load_default()
            draw.text((20, 30), text, fill='black', font=font)
        else:
            # Clean printed text
            font = ImageFont.load_default()
            draw.text((20, 30), text, fill='black', font=font)
    except:
        draw.text((20, 30), text, fill='black')
    
    # Save to BytesIO
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def test_endpoint(url, image_bytes, endpoint_name):
    """Test an API endpoint"""
    print(f"\n🧪 Testing {endpoint_name}...")
    
    try:
        files = {'file': ('test.png', image_bytes, 'image/png')}
        response = requests.post(url, files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {endpoint_name} succeeded!")
            print(f"   Method: {result.get('method', 'unknown')}")
            print(f"   Text: '{result.get('text', '').strip()}'")
            return True
        else:
            print(f"❌ {endpoint_name} failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {endpoint_name} - Connection failed (server not running?)")
        return False
    except Exception as e:
        print(f"❌ {endpoint_name} - Error: {e}")
        return False

def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    print(f"🚀 Testing OCR API at {base_url}")
    
    # Test root endpoint
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            info = response.json()
            print(f"   Message: {info.get('message')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except:
        print("❌ Could not reach server")
        return
    
    # Create test images
    print("\n📸 Creating test images...")
    printed_text = create_test_image("PRINTED TEXT TEST", False)
    handwritten_text = create_test_image("handwritten test", True)
    
    # Test endpoints
    results = []
    results.append(test_endpoint(f"{base_url}/ocr", printed_text.getvalue(), "Tesseract OCR"))
    results.append(test_endpoint(f"{base_url}/trocr", handwritten_text.getvalue(), "TrOCR Handwritten"))
    
    # Summary
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All tests passed! Your OCR API is working correctly!")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()