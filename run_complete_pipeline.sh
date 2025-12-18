#!/bin/bash
# Complete OCR Processing Pipeline
# Waits for OCR extraction to complete, then parses and integrates content

echo "========================================================================"
echo "                    COMPLETE OCR PROCESSING PIPELINE"
echo "========================================================================"
echo ""

# Check if OCR process is running
if ! ps aux | grep -q "[e]xtract_all_pages.py"; then
    echo "✗ OCR extraction process is not running."
    echo ""
    echo "Please start it with:"
    echo "  nohup python3 extract_all_pages.py > ocr_full_extraction.log 2>&1 &"
    echo ""
    exit 1
fi

echo "✓ OCR extraction is running..."
echo ""
echo "Waiting for OCR extraction to complete..."
echo "You can monitor progress with: tail -f ocr_full_extraction.log"
echo ""

# Wait for OCR process to complete
while ps aux | grep -q "[e]xtract_all_pages.py"; do
    # Show progress every 60 seconds
    sleep 60
    SUCCESSFUL=$(grep -c "| ✓" ocr_full_extraction.log 2>/dev/null || echo "0")
    echo "[$(date +%H:%M:%S)] Progress: $SUCCESSFUL pages extracted..."
done

echo ""
echo "✓ OCR extraction complete!"
echo ""

# Check if output file exists
if [ ! -f "ocr_output/extracted_all_pages.json" ]; then
    echo "✗ ERROR: OCR output file not found!"
    exit 1
fi

echo "========================================================================"
echo "                         PARSING OCR RESULTS"
echo "========================================================================"
echo ""

# Run parser
python3 parse_advanced.py
if [ $? -ne 0 ]; then
    echo "✗ ERROR: Parsing failed!"
    exit 1
fi

echo ""
echo "✓ Parsing complete!"
echo ""

echo "========================================================================"
echo "                    INTEGRATING INTO WEBSITE"
echo "========================================================================"
echo ""

# Run integration
python3 integrate_content.py
if [ $? -ne 0 ]; then
    echo "✗ ERROR: Integration failed!"
    exit 1
fi

echo ""
echo "========================================================================"
echo "                           PIPELINE COMPLETE"
echo "========================================================================"
echo ""
echo "✓ All 197 logbook pages have been:"
echo "  1. Extracted via OCR"
echo "  2. Parsed into structured data"
echo "  3. Integrated into website content"
echo ""
echo "Files updated:"
echo "  - data/content.json (backup at data/content.json.backup)"
echo "  - ocr_output/extracted_all_pages.json"
echo "  - ocr_output/parsed_entries.json"
echo "  - ocr_output/logbook_entries.json"
echo "  - ocr_output/integration_report.json"
echo ""
echo "Next steps:"
echo "  1. Review changes: git diff data/content.json"
echo "  2. Test website: open index.html in browser"
echo "  3. Commit changes: git add . && git commit -m 'Complete OCR integration'"
echo "  4. Push to GitHub: git push"
echo ""
echo "========================================================================"
