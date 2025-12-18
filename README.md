# Stanislaw Rockminster Website
The story of Stanislaw Rockminster (Rochminski) - Polish RAF Pilot

This website tells the story of Stanislaw Rockminster, a brave Polish pilot who served with the Royal Air Force during World War II. The site includes his RAF logbook pages, historical documents, enriched flight data, and a timeline of significant events.

## Features

- **Hero Section**: Introduction to Stanislaw's story
- **Timeline**: Chronological display of significant events in Stanislaw's life and service
- **RAF Logbook**: Gallery of 197 original logbook page scans with OCR-extracted content
- **Original Logbook Pages**: Complete gallery of all 197 scanned logbook pages
- **Documents**: Collection of historical documents, photographs, and memorabilia
- **Complete OCR Solution**: Production-ready system processing all 197 pages with advanced parsing

## Project Structure

```
Stanislaw/
├── index.html                     # Main HTML file
├── styles.css                     # Stylesheet
├── script.js                      # JavaScript for dynamic content
├── data/
│   ├── content.json              # Structured website content (with OCR entries)
│   └── content.json.backup       # Backup of original content
├── images/
│   └── logbook-pages/            # 197 original scanned RAF logbook pages
├── ocr_output/                    # OCR extraction results
│   ├── extracted_all_pages.json  # Complete OCR text from all 197 pages
│   ├── parsed_entries.json       # Structured data extracted from OCR
│   ├── logbook_entries.json      # Website-ready logbook entries
│   ├── extraction_summary.json   # OCR statistics and metadata
│   ├── integration_report.json   # Content integration summary
│   └── progress_page_*.json      # Intermediate processing checkpoints
├── extract_all_pages.py           # Complete OCR extraction (all 197 pages)
├── parse_advanced.py              # Advanced parser with pattern matching
├── integrate_content.py           # Integrate parsed content into website
├── run_complete_pipeline.sh       # Automated full OCR pipeline
├── monitor_ocr.sh                 # Real-time progress monitoring
├── extract_batch.py               # Batch processing with progress tracking
├── extract_simple.py              # Original simplified OCR (5 pages)
├── extract_logbook_text.py        # Tesseract OCR with preprocessing
├── extract_logbook_google.py      # Google Cloud Vision OCR
├── requirements-ocr.txt           # Python dependencies
├── OCR_README.md                  # Original OCR guide
├── OCR_COMPLETE_GUIDE.md          # Complete OCR system documentation
└── README.md                      # This file
```

## Complete OCR Data Capture Solution

This repository includes a production-ready OCR system that processes **all 197 handwritten logbook pages** with advanced text extraction, intelligent parsing, and automatic website integration.

### System Architecture

**3-Stage Pipeline:**
1. **Extraction** (`extract_all_pages.py`) - OCR text from all 197 pages (~15-20 min)
2. **Parsing** (`parse_advanced.py`) - Extract structured data (aircraft, squadrons, dates)
3. **Integration** (`integrate_content.py`) - Merge into website content

### Quick Start - Complete OCR Pipeline

**Automated (Recommended):**
```bash
# Start OCR extraction in background
nohup python3 extract_all_pages.py > ocr_full_extraction.log 2>&1 &

# Run automated pipeline (waits for extraction, then parses & integrates)
./run_complete_pipeline.sh
```

**Manual Step-by-Step:**
```bash
# Step 1: Extract OCR text from all 197 pages
python3 extract_all_pages.py

# Step 2: Parse OCR results into structured data
python3 parse_advanced.py

# Step 3: Integrate into website content
python3 integrate_content.py
```

### Monitoring OCR Progress

While OCR is running:
```bash
# Quick status check
./monitor_ocr.sh

# Watch live progress  
tail -f ocr_full_extraction.log

# View statistics
cat ocr_output/extraction_summary.json
```

### OCR Features

- ✅ **Complete Coverage**: Processes all 197 pages without sampling
- ✅ **High Quality**: Multiple OCR configurations per page for best results
- ✅ **Robust**: Intermediate saves every 20 pages, graceful error handling
- ✅ **Intelligent Parsing**: Extracts aircraft, squadrons, ranks, dates, locations
- ✅ **Automatic Integration**: Seamlessly merges into website content
- ✅ **Progress Tracking**: Real-time monitoring and detailed logs
- ✅ **Backup & Safety**: Automatic backups before content updates

### Expected Results

- **Processing Time**: 15-20 minutes for all 197 pages
- **Extraction Success**: 95%+ pages with content
- **Data Extracted**: 100-300 aircraft mentions, 50-100 squadron references
- **Website Entries**: ~150-180 structured logbook entries

See [OCR_COMPLETE_GUIDE.md](OCR_COMPLETE_GUIDE.md) for detailed documentation.

**Option 2: Google Cloud Vision (Better Accuracy)**
```bash
# Setup Google Cloud credentials (free tier: 1,000 images/month)
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
pip install google-cloud-vision

# Extract text
python3 extract_logbook_google.py
```

**Note**: Handwritten text OCR is challenging. Expected accuracy is 60-80% for clear handwriting. Manual review and correction will be needed.

See [OCR_README.md](OCR_README.md) for:
- Detailed installation instructions
- Accuracy expectations
- Alternative approaches
- Troubleshooting guide

## Getting Started

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/rockminster/Stanislaw.git
   cd Stanislaw
   ```

2. Open the website:
   - Simply open `index.html` in your web browser
   - Or use a local server (recommended):
     ```bash
     # Using Python 3
     python -m http.server 8000
     
     # Using Node.js http-server
     npx http-server
     ```

3. Access the website at `http://localhost:8000`

### Adding Content

#### Adding Logbook Pages

1. Place the scanned logbook image in `images/logbook/`
2. Update `data/content.json` with the logbook entry details:
   ```json
   {
     "id": 4,
     "date": "1942-06-15",
     "title": "Combat Mission",
     "description": "Description of the flight",
     "aircraft": "Supermarine Spitfire Mk V",
     "duration": "2h 30m",
     "pilot": "Self",
     "type": "Operational",
     "image": "images/logbook/logbook_page_004.jpg"
   }
   ```
3. Alternatively, edit the `logbookData` array in `script.js`

#### Adding Documents

1. Place the document image in `images/documents/`
2. Update `data/content.json` with the document details:
   ```json
   {
     "id": 5,
     "title": "Document Title",
     "type": "Document Type",
     "description": "Description of the document",
     "image": "images/documents/document_name.jpg"
   }
   ```
3. Alternatively, edit the `documentsData` array in `script.js`

#### Adding Timeline Events

1. Update `data/content.json` with the new event:
   ```json
   {
     "date": "June 1944",
     "title": "Event Title",
     "description": "Description of the event"
   }
   ```
2. Alternatively, edit the `timelineData` array in `script.js`

## Deployment

### GitHub Pages (Recommended)

This website is fully configured for GitHub Pages deployment with:
- ✅ `.nojekyll` file (skips Jekyll processing)
- ✅ `_config.yml` for GitHub Pages configuration
- ✅ Automated deployment workflow (`.github/workflows/pages.yml`)
- ✅ All relative paths for proper asset loading

**Quick Deploy:**

1. Go to your repository settings: `https://github.com/YOUR_USERNAME/Stanislaw/settings/pages`
2. Under "Source", select:
   - **Source**: Deploy from a branch
   - **Branch**: `main` (or your current branch)
   - **Folder**: `/ (root)`
3. Click "Save"
4. Wait 1-2 minutes for deployment
5. Your site will be live at: `https://YOUR_USERNAME.github.io/Stanislaw/`

**Alternative: GitHub Actions Deployment**

The repository includes an automated workflow. To enable it:

1. Go to Settings → Pages
2. Select **Source**: GitHub Actions
3. The workflow will automatically deploy on every push to main

For detailed instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Netlify

1. Sign up for a free account at [Netlify](https://www.netlify.com/)
2. Click "Add new site" → "Import an existing project"
3. Connect to your GitHub repository
4. Deploy settings:
   - Build command: (leave empty)
   - Publish directory: `.`
5. Click "Deploy site"

### Vercel

1. Sign up for a free account at [Vercel](https://vercel.com/)
2. Click "Import Project"
3. Connect to your GitHub repository
4. Deploy with default settings

## Customization

### Styling

Edit `styles.css` to customize colors, fonts, and layout:
- Primary color: `--primary-color: #1a4d7a;`
- Secondary color: `--secondary-color: #c41e3a;`
- Other CSS variables in the `:root` selector

### Content Structure

The website is designed to be easily customizable. You can:
- Modify the HTML structure in `index.html`
- Adjust the styling in `styles.css`
- Change the data structure in `script.js` or `data/content.json`

## Browser Support

This website works in all modern browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

This project is dedicated to preserving the memory and service of Stanislaw Rockminster.

## Contributing

If you have additional information, documents, or photographs related to Stanislaw's service, please open an issue or submit a pull request.

## Contact

For questions or additional information, please open an issue in this repository.
