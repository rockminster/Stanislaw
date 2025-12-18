#!/usr/bin/env python3
"""
Batch OCR extraction for RAF logbook pages with progress tracking.
Processes images in batches to show progress and handle errors gracefully.
"""

import json
from pathlib import Path
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import sys

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
    """Process all logbook pages with progress tracking."""
    logbook_dir = Path("images/logbook-pages")
    output_dir = Path("ocr_output")
    output_dir.mkdir(exist_ok=True)
    
    # Get all images
    image_files = sorted(logbook_dir.glob("*.jpg"))
    total = len(image_files)
    
    print(f"Starting OCR extraction for {total} logbook pages...")
    print("="*60)
    print("This will take approximately 10-15 minutes.")
    print("="*60)
    
    results = []
    successful = 0
    
    for i, img_path in enumerate(image_files, 1):
        # Progress indicator
        progress = (i / total) * 100
        print(f"\n[{i}/{total}] ({progress:.1f}%) Processing: {img_path.name}", end='', flush=True)
        
        result = extract_text(img_path)
        result['filename'] = img_path.name
        result['page_number'] = i
        results.append(result)
        
        if result['success']:
            successful += 1
            print(" ✓")
            # Show brief preview
            preview = result['text'][:150].replace('\n', ' ')
            if len(preview) > 0:
                print(f"   Preview: {preview}...")
        else:
            print(" ✗")
            if 'error' in result:
                print(f"   Error: {result['error']}")
        
        # Save intermediate results every 10 images
        if i % 10 == 0:
            temp_file = output_dir / f"extracted_progress_{i}.json"
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"   → Saved progress to {temp_file}")
    
    # Save final results
    output_file = output_dir / "extracted_all.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*60)
    print(f"✓ OCR extraction complete!")
    print(f"Results saved to: {output_file}")
    print(f"Successfully extracted: {successful}/{total} pages ({(successful/total)*100:.1f}%)")
    print("="*60)

if __name__ == "__main__":
    main()
