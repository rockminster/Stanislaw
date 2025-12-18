#!/usr/bin/env python3
"""
Process checkpoint OCR data and integrate into website immediately.
Uses the latest checkpoint file (80 pages) to start populating the site.
"""

import json
from pathlib import Path

# Load the latest checkpoint with 80 pages of OCR data
checkpoint_file = Path("ocr_output/progress_page_80.json")
print(f"Loading checkpoint: {checkpoint_file}")

with open(checkpoint_file, 'r') as f:
    ocr_data = json.load(f)

print(f"Loaded {len(ocr_data)} pages of OCR data")
print(f"Processing and parsing...")

# Now run the advanced parser on this data
# Temporarily save as the main file so parser can use it
temp_file = Path("ocr_output/extracted_all_pages.json")
with open(temp_file, 'w') as f:
    json.dump(ocr_data, f, indent=2)

print(f"Saved to {temp_file}")
print(f"Now running parser...")
