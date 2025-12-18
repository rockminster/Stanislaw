# GitHub Pages Deployment Guide

This website is configured to be deployed via GitHub Pages.

## Automatic Deployment

The site is configured to deploy automatically from this branch. GitHub Pages will serve the static files directly without any build process.

## Configuration Files

- **`.nojekyll`** - Tells GitHub Pages to skip Jekyll processing and serve files as-is
- **`_config.yml`** - Optional Jekyll configuration (for compatibility)
- **`index.html`** - Main entry point for the website

## Deployment Steps

### Option 1: Deploy from Branch (Recommended)

1. Go to your repository settings: `https://github.com/rockminster/Stanislaw/settings/pages`
2. Under "Source", select your branch (e.g., `copilot/create-stanislaw-rockminster-website`)
3. Click "Save"
4. GitHub will automatically deploy the site
5. Your site will be available at: `https://rockminster.github.io/Stanislaw/`

### Option 2: Deploy from Root Directory

If deploying from the main/master branch:
1. Merge this PR to main
2. Go to Settings → Pages
3. Select "Deploy from branch"
4. Choose "main" branch and "/ (root)" folder
5. Save and wait for deployment

## Accessing Your Site

Once deployed, your site will be available at:
- **Public URL**: `https://rockminster.github.io/Stanislaw/`
- **Custom Domain**: You can configure a custom domain in Settings → Pages

## Updating Content

The website loads content dynamically from `data/content.json`. To update:

1. Edit `data/content.json` with new logbook entries, timeline events, or documents
2. Commit and push changes
3. GitHub Pages will automatically redeploy (usually takes 1-2 minutes)

## File Structure for GitHub Pages

```
/
├── index.html          # Main page (entry point)
├── styles.css          # Styling
├── script.js           # JavaScript
├── .nojekyll           # Disables Jekyll processing
├── _config.yml         # GitHub Pages configuration
├── data/
│   └── content.json    # Dynamic content
└── images/
    ├── logbook-pages/  # 197 RAF logbook scans
    ├── logbook/        # Additional logbook images
    └── documents/      # Historical documents
```

## Troubleshooting

### Site Not Loading
- Check that GitHub Pages is enabled in Settings → Pages
- Verify the correct branch is selected
- Wait 1-2 minutes for initial deployment

### Images Not Showing
- Ensure image paths in `content.json` are relative (e.g., `images/logbook-pages/...`)
- Check that `.nojekyll` file exists to prevent Jekyll from excluding files

### Content Not Updating
- Clear your browser cache
- Check that `data/content.json` is valid JSON
- Verify changes were committed and pushed to the correct branch

## Local Testing

To test the site locally before deploying:

```bash
# Simple Python server
python3 -m http.server 8000

# Or use Node.js
npx http-server
```

Then visit `http://localhost:8000` in your browser.

## Performance

GitHub Pages serves static files efficiently:
- **Fast Loading**: No server-side processing
- **Global CDN**: Content delivered from edge servers worldwide
- **HTTPS**: Automatic SSL certificate
- **Free Hosting**: No cost for public repositories

## Limitations

- **File Size**: Individual files should be < 100 MB
- **Bandwidth**: 100 GB/month soft limit
- **Build Time**: Site updates within 1-2 minutes
- **No Server-Side Code**: Pure static HTML/CSS/JS only

## Support

For GitHub Pages issues:
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Pages Status](https://www.githubstatus.com/)

For website content issues, refer to the main [README.md](README.md).
