#!/usr/bin/env python3
"""
Simple OCR extraction for RAF logbook pages.
Extracts text from first 5 images to test and show real content.
"""

import json
from pathlib import Path
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

def preprocess_simple(image_path):
    """Simple image preprocessing for better OCR."""
    img = Image.open(image_path)
    
    # Convert to grayscale
    img = img.convert('L')
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    
    # Sharpen
    img = img.filter(ImageFilter.SHARPEN)
    
    return img

def extract_text(image_path):
    """Extract text from a single image."""
    try:
        # Preprocess
        img = preprocess_simple(image_path)
        
        # Extract text with different configurations
        configs = [
            '--psm 6',  # Uniform block of text
            '--psm 4',  # Single column
            '--psm 3',  # Fully automatic
        ]
        
        best_text = ""
        for config in configs:
            text = pytesseract.image_to_string(img, config=config)
            if len(text) > len(best_text):
                best_text = text
        
        return {
            'text': best_text.strip(),
            'success': bool(best_text.strip())
        }
    except Exception as e:
        return {
            'text': '',
            'success': False,
            'error': str(e)
        }

def main():
    """Process first 5 logbook pages."""
    logbook_dir = Path("images/logbook-pages")
    output_dir = Path("ocr_output")
    output_dir.mkdir(exist_ok=True)
    
    image_files = sorted(logbook_dir.glob("*.jpg"))[:5]
    
    print(f"Extracting text from {len(image_files)} logbook pages...")
    print("="*60)
    
    results = []
    for i, img_path in enumerate(image_files, 1):
        print(f"\n[{i}/{len(image_files)}] Processing: {img_path.name}")
        result = extract_text(img_path)
        result['filename'] = img_path.name
        result['page_number'] = i
        results.append(result)
        
        if result['success']:
            preview = result['text'][:300].replace('\n', ' ')
            print(f"✓ Extracted: {preview}...")
        else:
            print(f"✗ Failed")
    
    # Save results
    output_file = output_dir / "extracted_sample.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*60)
    print(f"Results saved to: {output_file}")
    print(f"Successfully extracted: {sum(1 for r in results if r['success'])}/{len(results)}")

if __name__ == "__main__":
    main()
