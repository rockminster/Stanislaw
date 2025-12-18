#!/usr/bin/env python3
"""
Advanced OCR extraction using Google Cloud Vision API.
This provides better handwriting recognition than Tesseract.

Setup:
1. Create a Google Cloud account (free tier includes 1,000 vision API calls/month)
2. Enable the Vision API
3. Create a service account and download credentials JSON
4. Set environment variable: export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
5. Install: pip install google-cloud-vision
"""

import os
import json
from pathlib import Path
import sys

def check_google_vision_setup():
    """Check if Google Cloud Vision is properly configured."""
    try:
        from google.cloud import vision
        
        credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if not credentials_path:
            print("✗ GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
            return False
        
        if not os.path.exists(credentials_path):
            print(f"✗ Credentials file not found: {credentials_path}")
            return False
        
        print("✓ Google Cloud Vision setup looks good")
        return True
        
    except ImportError:
        print("✗ google-cloud-vision not installed")
        print("  Install with: pip install google-cloud-vision")
        return False

def extract_text_google_vision(image_path):
    """
    Extract text using Google Cloud Vision API.
    Better for handwritten text than Tesseract.
    """
    from google.cloud import vision
    
    try:
        client = vision.ImageAnnotatorClient()
        
        # Read image
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)
        
        # Detect handwritten text (document text detection is best for logbooks)
        response = client.document_text_detection(image=image)
        
        if response.error.message:
            raise Exception(response.error.message)
        
        # Get full text
        full_text = response.full_text_annotation.text if response.full_text_annotation else ""
        
        # Get confidence scores
        confidences = []
        if response.full_text_annotation and response.full_text_annotation.pages:
            for page in response.full_text_annotation.pages:
                if page.confidence:
                    confidences.append(page.confidence * 100)
        
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        return {
            'text': full_text.strip(),
            'confidence': avg_confidence,
            'success': bool(full_text.strip()),
            'method': 'google_vision'
        }
        
    except Exception as e:
        print(f"Error with Google Vision API: {e}")
        return {
            'text': '',
            'confidence': 0,
            'success': False,
            'error': str(e),
            'method': 'google_vision'
        }

def process_with_google_vision(logbook_dir, output_dir, limit=None):
    """Process logbook pages using Google Cloud Vision API."""
    logbook_dir = Path(logbook_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Get all image files
    image_files = sorted(logbook_dir.glob("*.jpg"))
    
    if limit:
        image_files = image_files[:limit]
    
    print(f"Found {len(image_files)} logbook page images")
    print(f"Processing with Google Cloud Vision API...")
    print(f"Note: Free tier allows 1,000 requests/month")
    
    results = []
    
    for i, image_path in enumerate(image_files, 1):
        print(f"\nProcessing {i}/{len(image_files)}: {image_path.name}")
        
        result = extract_text_google_vision(image_path)
        result['filename'] = image_path.name
        result['page_number'] = i
        
        results.append(result)
        
        # Print preview
        if result['success']:
            preview = result['text'][:200].replace('\n', ' ')
            print(f"  ✓ Extracted (confidence: {result['confidence']:.1f}%): {preview}...")
        else:
            print(f"  ✗ Failed to extract text")
    
    # Save results
    output_file = output_dir / "extracted_text_google.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"Processing complete!")
    print(f"Results saved to: {output_file}")
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
    """Main function."""
    print("RAF Logbook OCR - Google Cloud Vision")
    print("=" * 60)
    
    if not check_google_vision_setup():
        print("\nSetup required:")
        print("1. Create Google Cloud account: https://cloud.google.com/")
        print("2. Enable Vision API")
        print("3. Create service account and download credentials")
        print("4. Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
        print("5. pip install google-cloud-vision")
        return 1
    
    # Set paths
    script_dir = Path(__file__).parent
    logbook_dir = script_dir / "images" / "logbook-pages"
    output_dir = script_dir / "ocr_output"
    
    if not logbook_dir.exists():
        print(f"Error: Logbook directory not found: {logbook_dir}")
        return 1
    
    # Process first 5 images as test
    print("\nStarting with first 5 images as a test...")
    print("(Free tier: 1,000 images/month)")
    
    results = process_with_google_vision(logbook_dir, output_dir, limit=5)
    
    print("\nNext steps:")
    print("1. Review extracted_text_google.json")
    print("2. Compare accuracy with Tesseract results")
    print("3. If satisfied, increase limit to process more images")
    print("4. Free tier allows up to 1,000 images/month")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
