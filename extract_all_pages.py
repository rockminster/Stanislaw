#!/usr/bin/env python3
"""
Complete OCR extraction for all 197 RAF logbook pages.
Runs extraction with progress tracking, error handling, and intermediate saves.
Designed to run for hours if needed to capture all data.
"""

import json
from pathlib import Path
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import sys
import time
from datetime import datetime

def preprocess_image(image_path):
    """Enhanced image preprocessing for better OCR accuracy."""
    img = Image.open(image_path)
    
    # Convert to grayscale
    img = img.convert('L')
    
    # Enhance contrast significantly
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.5)
    
    # Enhance sharpness
    sharpener = ImageEnhance.Sharpness(img)
    img = sharpener.enhance(2.0)
    
    # Apply sharpening filter
    img = img.filter(ImageFilter.SHARPEN)
    
    return img

def extract_text_from_image(image_path):
    """Extract text from a single image with multiple OCR passes."""
    try:
        # Preprocess the image
        img = preprocess_image(image_path)
        
        # Try multiple OCR configurations for best results
        configs = [
            '--psm 6 --oem 3',  # Uniform block of text, default OCR engine
            '--psm 4 --oem 3',  # Single column of text
            '--psm 3 --oem 3',  # Fully automatic page segmentation
            '--psm 11 --oem 3', # Sparse text
        ]
        
        best_text = ""
        best_config = ""
        
        for config in configs:
            try:
                text = pytesseract.image_to_string(img, config=config)
                if len(text.strip()) > len(best_text.strip()):
                    best_text = text
                    best_config = config
            except Exception as e:
                continue
        
        return {
            'text': best_text.strip(),
            'success': bool(best_text.strip()),
            'config_used': best_config,
            'char_count': len(best_text.strip())
        }
    except Exception as e:
        return {
            'text': '',
            'success': False,
            'error': str(e),
            'char_count': 0
        }

def save_progress(results, output_dir, page_num):
    """Save intermediate progress."""
    progress_file = output_dir / f"progress_page_{page_num}.json"
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    return progress_file

def main():
    """Process all 197 logbook pages with comprehensive OCR extraction."""
    start_time = time.time()
    
    logbook_dir = Path("images/logbook-pages")
    output_dir = Path("ocr_output")
    output_dir.mkdir(exist_ok=True)
    
    # Get all images sorted by filename
    image_files = sorted(logbook_dir.glob("*.jpg"))
    total_pages = len(image_files)
    
    print("="*70)
    print(f"COMPLETE OCR EXTRACTION - RAF LOGBOOK")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    print(f"Total pages to process: {total_pages}")
    print(f"Estimated time: {total_pages * 4} - {total_pages * 6} seconds (~{(total_pages * 5) / 60:.1f} minutes)")
    print("="*70)
    print()
    
    results = []
    successful_extractions = 0
    total_chars_extracted = 0
    
    for i, img_path in enumerate(image_files, 1):
        page_start = time.time()
        
        # Progress indicator
        progress_pct = (i / total_pages) * 100
        elapsed = time.time() - start_time
        avg_time_per_page = elapsed / i if i > 0 else 0
        remaining_pages = total_pages - i
        eta_seconds = remaining_pages * avg_time_per_page
        eta_minutes = eta_seconds / 60
        
        print(f"[{i:3d}/{total_pages}] ({progress_pct:5.1f}%) {img_path.name}")
        print(f"         Elapsed: {elapsed/60:.1f}m | ETA: {eta_minutes:.1f}m", end=' ')
        sys.stdout.flush()
        
        # Extract text
        result = extract_text_from_image(img_path)
        result['filename'] = img_path.name
        result['page_number'] = i
        result['processing_time'] = time.time() - page_start
        
        results.append(result)
        
        if result['success']:
            successful_extractions += 1
            total_chars_extracted += result['char_count']
            print(f"| ✓ {result['char_count']:4d} chars")
            
            # Show first line preview
            if result['text']:
                first_line = result['text'].split('\n')[0][:70]
                print(f"         → {first_line}")
        else:
            print("| ✗ FAILED")
            if 'error' in result:
                print(f"         Error: {result['error']}")
        
        print()
        
        # Save progress every 20 pages
        if i % 20 == 0 or i == total_pages:
            progress_file = save_progress(results, output_dir, i)
            success_rate = (successful_extractions / i) * 100
            print(f"         [CHECKPOINT] Progress saved: {success_rate:.1f}% success rate")
            print()
    
    # Save final complete results
    final_output = output_dir / "extracted_all_pages.json"
    with open(final_output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Generate summary
    total_time = time.time() - start_time
    success_rate = (successful_extractions / total_pages) * 100
    avg_chars_per_page = total_chars_extracted / successful_extractions if successful_extractions > 0 else 0
    
    print()
    print("="*70)
    print("EXTRACTION COMPLETE")
    print("="*70)
    print(f"Total pages processed: {total_pages}")
    print(f"Successful extractions: {successful_extractions} ({success_rate:.1f}%)")
    print(f"Failed extractions: {total_pages - successful_extractions}")
    print(f"Total characters extracted: {total_chars_extracted:,}")
    print(f"Average chars per page: {avg_chars_per_page:.0f}")
    print(f"Total processing time: {total_time/60:.1f} minutes")
    print(f"Average time per page: {total_time/total_pages:.1f} seconds")
    print("="*70)
    print(f"Results saved to: {final_output}")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Save summary
    summary = {
        'total_pages': total_pages,
        'successful': successful_extractions,
        'failed': total_pages - successful_extractions,
        'success_rate': success_rate,
        'total_characters': total_chars_extracted,
        'avg_chars_per_page': avg_chars_per_page,
        'processing_time_minutes': total_time / 60,
        'avg_time_per_page': total_time / total_pages,
        'completed_at': datetime.now().isoformat()
    }
    
    summary_file = output_dir / "extraction_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Summary saved to: {summary_file}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] OCR extraction stopped by user.")
        print("Partial results have been saved in ocr_output/progress_*.json files")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[ERROR] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
