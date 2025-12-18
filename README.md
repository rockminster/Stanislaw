# Stanislaw Rockminster Website
The story of Stanislaw Rockminster (Rochminski) - Polish RAF Pilot

This website tells the story of Stanislaw Rockminster, a brave Polish pilot who served with the Royal Air Force during World War II. The site includes his RAF logbook pages, historical documents, enriched flight data, and a timeline of significant events.

## Features

- **Hero Section**: Introduction to Stanislaw's story
- **Timeline**: Chronological display of significant events in Stanislaw's life and service
- **RAF Logbook**: Gallery of 197 original logbook page scans with enriched data
- **Original Logbook Pages**: Complete gallery of all 197 scanned logbook pages
- **Documents**: Collection of historical documents, photographs, and memorabilia
- **OCR Text Extraction**: Tools to extract and transcribe handwritten logbook content

## Project Structure

```
Stanislaw/
├── index.html                 # Main HTML file
├── styles.css                 # Stylesheet
├── script.js                  # JavaScript for dynamic content
├── data/
│   └── content.json          # Structured data for timeline, logbook, and documents
├── images/
│   ├── logbook-pages/        # 197 scanned images of RAF logbook pages
│   ├── logbook/              # Placeholder directory for enriched logbook images
│   └── documents/            # Historical documents and photographs
├── extract_logbook_text.py   # OCR script using Tesseract (free, open-source)
├── extract_logbook_google.py # OCR script using Google Cloud Vision (better accuracy)
├── requirements-ocr.txt      # Python dependencies for OCR
├── OCR_README.md             # Detailed OCR extraction guide
└── README.md                 # This file
```

## Extracting Text from Logbook Pages

The repository includes OCR (Optical Character Recognition) tools to extract handwritten text from the 197 logbook page images. See [OCR_README.md](OCR_README.md) for detailed instructions.

### Quick Start - OCR Extraction

**Option 1: Free Tesseract OCR (Open Source)**
```bash
# Install dependencies
sudo apt-get install tesseract-ocr tesseract-ocr-eng
pip install -r requirements-ocr.txt

# Extract text from first 10 pages (test)
python3 extract_logbook_text.py
```

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

### GitHub Pages

1. Go to your repository settings
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select the branch (e.g., `main`) and folder (`/root`)
4. Click "Save"
5. Your site will be available at `https://YOUR_USERNAME.github.io/Stanislaw/`

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
