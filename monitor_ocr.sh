#!/bin/bash
# Monitor OCR extraction progress

echo "=== OCR Extraction Monitor ==="
echo ""

# Check if process is running
if ps aux | grep -q "[e]xtract_all_pages.py"; then
    PID=$(ps aux | grep "[e]xtract_all_pages.py" | awk '{print $2}')
    echo "✓ OCR process is running (PID: $PID)"
    echo ""
else
    echo "✗ OCR process is not running"
    echo ""
fi

# Show latest progress
if [ -f ocr_full_extraction.log ]; then
    echo "=== Latest Progress ==="
    tail -n 20 ocr_full_extraction.log
    echo ""
    echo "=== Statistics ==="
    TOTAL_LINES=$(wc -l < ocr_full_extraction.log)
    SUCCESSFUL=$(grep -c "| ✓" ocr_full_extraction.log || echo "0")
    FAILED=$(grep -c "| ✗" ocr_full_extraction.log || echo "0")
    echo "Lines in log: $TOTAL_LINES"
    echo "Successful extractions: $SUCCESSFUL"
    echo "Failed extractions: $FAILED"
else
    echo "No log file found yet"
fi

echo ""
echo "=== Output Files ==="
ls -lh ocr_output/ 2>/dev/null || echo "No output files yet"

echo ""
echo "Commands:"
echo "  tail -f ocr_full_extraction.log  # Watch live progress"
echo "  ./monitor_ocr.sh                 # Run this script again"
