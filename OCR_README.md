# RAF Logbook OCR Text Extraction

This directory contains tools to extract handwritten text from Stanislaw Rockminster's RAF logbook images using Optical Character Recognition (OCR).

## Overview

The `extract_logbook_text.py` script uses Tesseract OCR with advanced image preprocessing to extract text from the 197 handwritten logbook page images. The script:

1. **Preprocesses images** for better OCR accuracy:
   - Converts to grayscale
   - Applies denoising to reduce image artifacts
   - Enhances contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
   - Applies adaptive thresholding for better text separation
   - Uses morphological operations to clean up the image

2. **Runs multiple OCR configurations** to find the best results
3. **Calculates confidence scores** for each extraction
4. **Saves all extracted text** to JSON for further processing
5. **Saves preprocessed images** for quality review

## Installation

### 1. Install System Dependencies

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng python3-pip
```

#### macOS:
```bash
brew install tesseract
```

#### Windows:
Download and install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki

### 2. Install Python Dependencies

```bash
pip install -r requirements-ocr.txt
```

Or manually:
```bash
pip install opencv-python-headless pytesseract pillow numpy
```

## Usage

### Quick Start (Test Mode)

Process the first 10 logbook pages to test the setup:

```bash
python3 extract_logbook_text.py
```

This will:
- Process the first 10 images
- Save extracted text to `ocr_output/extracted_text.json`
- Save preprocessed images to `ocr_output/` for review

### Process All Pages

To process all 197 logbook pages, edit `extract_logbook_text.py` and remove the `limit=10` parameter on line 174:

```python
# Change this:
results = process_all_logbook_pages(logbook_dir, output_dir, limit=10)

# To this:
results = process_all_logbook_pages(logbook_dir, output_dir)
```

Then run:
```bash
python3 extract_logbook_text.py
```

**Note:** Processing all 197 high-resolution images may take 10-30 minutes depending on your system.

## Output

### extracted_text.json

Contains all extracted text with metadata:

```json
[
  {
    "filename": "PXL_20251120_133047379.RAW-01.COVER.jpg",
    "page_number": 1,
    "text": "Extracted text content...",
    "confidence": 72.5,
    "success": true
  },
  ...
]
```

### Preprocessed Images

Saved in `ocr_output/preprocessed_*.jpg` - review these to see how the images were enhanced for OCR.

## Accuracy Notes

**Handwritten text OCR is challenging.** Expected accuracy:

- **Printed text**: 95-99% accuracy
- **Clear handwriting**: 60-80% accuracy
- **Unclear/cursive handwriting**: 30-50% accuracy

### Improving Accuracy

1. **Review preprocessed images**: If text looks unclear in preprocessed images, adjust preprocessing parameters
2. **Manual review required**: OCR output will need human review and correction
3. **Focus on key pages**: Identify most important logbook entries for manual transcription
4. **Combine approaches**: Use OCR as a starting point, then manually correct

## Alternative Approaches

If Tesseract results are insufficient:

### 1. Google Cloud Vision API (Free Tier Available)
- More accurate for handwriting
- Free tier: 1,000 images/month
- Documentation: https://cloud.google.com/vision/docs/ocr

### 2. Azure Computer Vision (Free Tier Available)
- Excellent handwriting recognition
- Free tier: 5,000 images/month
- Documentation: https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/

### 3. Manual Transcription
- Most accurate but time-consuming
- Focus on key entries (first/last pages, significant dates)
- Can be combined with OCR (use OCR for bulk, manually correct important entries)

## Next Steps

After extracting text:

1. **Review JSON output**: Check `ocr_output/extracted_text.json`
2. **Identify patterns**: Look for date formats, aircraft types, mission types
3. **Parse structured data**: Extract dates, aircraft, locations, etc.
4. **Update content.json**: Incorporate real logbook entries into the website
5. **Link images to text**: Associate each logbook page image with its extracted content

## Troubleshooting

### "tesseract: command not found"
- Tesseract is not installed or not in PATH
- Install system package (see Installation section)

### Poor OCR accuracy
- Handwritten text is inherently difficult for OCR
- Try alternative cloud-based OCR services (Google Vision, Azure)
- Consider manual transcription for key pages

### Out of memory errors
- Processing 197 high-res images uses significant RAM
- Process in smaller batches (adjust the limit parameter)
- Reduce image size in preprocessing (add downscaling step)

## Contributing

If you improve the OCR accuracy or preprocessing:
1. Test on multiple logbook pages
2. Document changes in this README
3. Share average confidence score improvements

## License

This OCR extraction tool is provided as-is for the Stanislaw Rockminster website project.
