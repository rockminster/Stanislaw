#!/usr/bin/env python3
"""
Extract text from RAF logbook images using OCR.
This script processes all logbook page images and attempts to extract handwritten text.
"""

import os
import json
from pathlib import Path
import subprocess
import sys

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import cv2
        import pytesseract
        from PIL import Image
        import numpy as np
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nTo install dependencies, run:")
        print("  pip install opencv-python-headless pytesseract pillow numpy")
        print("  sudo apt-get install tesseract-ocr")
        return False

def preprocess_image(image_path):
    """
    Preprocess image to improve OCR accuracy on handwritten text.
    """
    import cv2
    import numpy as np
    
    # Read image
    img = cv2.imread(str(image_path))
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply denoising
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    
    # Increase contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    contrast = clahe.apply(denoised)
    
    # Apply adaptive thresholding
    binary = cv2.adaptiveThreshold(
        contrast, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # Morphological operations to clean up
    kernel = np.ones((1,1), np.uint8)
    morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    return morph

def extract_text_from_image(image_path, output_dir):
    """
    Extract text from a single logbook page image.
    """
    import pytesseract
    from PIL import Image
    import cv2
    
    try:
        # Preprocess the image
        preprocessed = preprocess_image(image_path)
        
        # Save preprocessed image for debugging (optional)
        preprocessed_path = output_dir / f"preprocessed_{image_path.name}"
        cv2.imwrite(str(preprocessed_path), preprocessed)
        
        # Convert to PIL Image for Tesseract
        pil_image = Image.fromarray(preprocessed)
        
        # Try multiple OCR configurations for handwritten text
        configs = [
            '--oem 1 --psm 6',  # Assume uniform block of text
            '--oem 1 --psm 4',  # Assume single column of text
            '--oem 1 --psm 3',  # Fully automatic page segmentation
        ]
        
        best_text = ""
        max_confidence = 0
        
        for config in configs:
            # Extract text
            text = pytesseract.image_to_string(pil_image, config=config)
            
            # Get confidence scores
            data = pytesseract.image_to_data(pil_image, config=config, output_type=pytesseract.Output.DICT)
            confidences = [int(conf) for conf in data['conf'] if conf != '-1']
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            if avg_confidence > max_confidence:
                max_confidence = avg_confidence
                best_text = text
        
        return {
            'text': best_text.strip(),
            'confidence': max_confidence,
            'success': bool(best_text.strip())
        }
        
    except Exception as e:
        print(f"Error processing {image_path.name}: {e}")
        return {
            'text': '',
            'confidence': 0,
            'success': False,
            'error': str(e)
        }

def process_all_logbook_pages(logbook_dir, output_dir, limit=None):
    """
    Process all logbook page images in the directory.
    
    Args:
        logbook_dir: Path to directory containing logbook images
        output_dir: Path to directory for output files
        limit: Optional limit on number of images to process (for testing)
    """
    logbook_dir = Path(logbook_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Get all image files
    image_files = sorted(logbook_dir.glob("*.jpg"))
    
    if limit:
        image_files = image_files[:limit]
    
    print(f"Found {len(image_files)} logbook page images")
    print(f"Processing images...")
    
    results = []
    
    for i, image_path in enumerate(image_files, 1):
        print(f"\nProcessing {i}/{len(image_files)}: {image_path.name}")
        
        result = extract_text_from_image(image_path, output_dir)
        result['filename'] = image_path.name
        result['page_number'] = i
        
        results.append(result)
        
        # Print preview of extracted text
        if result['success']:
            preview = result['text'][:200].replace('\n', ' ')
            print(f"  ✓ Extracted (confidence: {result['confidence']:.1f}%): {preview}...")
        else:
            print(f"  ✗ Failed to extract text")
    
    # Save results to JSON
    output_file = output_dir / "extracted_text.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"Processing complete!")
    print(f"Results saved to: {output_file}")
    print(f"Preprocessed images saved to: {output_dir}")
    print(f"{'='*60}")
    
    # Print summary
    successful = sum(1 for r in results if r['success'])
    avg_confidence = sum(r['confidence'] for r in results) / len(results) if results else 0
    
    print(f"\nSummary:")
    print(f"  Total pages processed: {len(results)}")
    print(f"  Successfully extracted: {successful}")
    print(f"  Failed: {len(results) - successful}")
    print(f"  Average confidence: {avg_confidence:.1f}%")
    
    return results

def main():
    """Main function to run OCR extraction."""
    print("RAF Logbook OCR Text Extraction")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install dependencies and try again.")
        return 1
    
    # Set paths
    script_dir = Path(__file__).parent
    logbook_dir = script_dir / "images" / "logbook-pages"
    output_dir = script_dir / "ocr_output"
    
    if not logbook_dir.exists():
        print(f"Error: Logbook directory not found: {logbook_dir}")
        return 1
    
    # Process first 10 images as a test
    print("\nStarting with first 10 images as a test...")
    print("(Remove the limit=10 parameter to process all 197 images)\n")
    
    results = process_all_logbook_pages(logbook_dir, output_dir, limit=10)
    
    print("\nNext steps:")
    print("1. Review the extracted text in ocr_output/extracted_text.json")
    print("2. Check preprocessed images in ocr_output/ to see image quality")
    print("3. If results look good, run again without the limit to process all images")
    print("4. Manually review and correct any OCR errors")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
