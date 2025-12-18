// Data will be loaded from content.json
let timelineData = [];
let logbookData = [];
let documentsData = [];
let logbookPagesData = [];

// Load data from JSON file
async function loadData() {
    try {
        const response = await fetch('data/content.json');
        const data = await response.json();
        
        timelineData = data.timeline || [];
        logbookData = (data.logbook || []).map(entry => ({
            ...entry,
            date: formatDate(entry.date)
        }));
        documentsData = data.documents || [];
        
        // Load logbook page images
        await loadLogbookPages();
        
        // Render all sections after data is loaded
        renderTimeline();
        renderLogbook();
        renderLogbookPages();
        renderDocuments();
    } catch (error) {
        console.error('Error loading data:', error);
        // Use fallback empty data
        renderTimeline();
        renderLogbook();
        renderLogbookPages();
        renderDocuments();
    }
}

// Load all logbook page images
async function loadLogbookPages() {
    try {
        // List of all logbook page timestamps
        const timestamps = '133047379,133054657,133058605,133104141,133137052,133200045,133206954,133249547,133253973,133257515,133305273,133315430,133325252,133329636,133334265,133341097,133347454,133352064,133358148,133415903,133432347,133437204,133442077,133447184,133452043,133456133,133502158,133510739,133517617,133533606,133549111,133554337,133607984,133618218,133631815,133636627,133641179,133645698,133653500,133709575,133728518,133733862,133739592,133743326,133747594,133750781,133757199,133803087,133810396,133821545,133835718,133842871,133848760,133854701,133859968,133925550,133937592,133958465,134008667,134014544,134020102,134023412,134029097,134055797,134113088,134119718,134125997,134133151,134139395,134147099,134153415,134205810,134211953,134216506,134221172,134225524,134230007,134235989,134307243,134312871,134327565,134333852,134339529,134344294,134354739,134407099,134418393,134424503,134430885,134434335,134441056,134450007,134453004,134509384,134525327,134616848,134625541,134638959,134647014,134650696,134702944,134717700,134749445,134805096,134810369,134818085,134821717,134825127,134830006,134834468,134839886,134849317,134854670,134858589,135005640,135012785,135030131,135046732,135053644,135103133,135109561,135112912,135116160,135119237,135122267,135126451,135131342,135134874,135138006,135141475,135151478,135247165,135251327,135254740,135258082,135301960,135305886,135311911,135319323,135340149,135344384,135348713,135358321,135412234,135417016,135421372,135425370,135429521,135432616,135437021,135441214,135447612,135456175,135507040,135532376,135544619,135551473,135558999,135606400,135612670,135616902,135621277,135627513,135631154,135634577,135637496,135640619,135650087,135704498,135708085,135715002,135719599,135724100,135727479,135730384,135734673,135737650,135742498,135748716,135753392,135759423,135807770,143254868,143309023,143320876,143325932,143417150,143431697,143443284,143453549,143518545,143531337,143642135,143708386,143815329,143905139,143924791'.split(',');
        
        timestamps.forEach((timestamp, index) => {
            logbookPagesData.push({
                id: index + 1,
                image: `images/logbook-pages/PXL_20251120_${timestamp}.RAW-01.COVER.jpg`,
                pageNumber: `Page ${index + 1} of ${timestamps.length}`
            });
        });
        
    } catch (error) {
        console.error('Error loading logbook pages:', error);
    }
}

// Format ISO date to human-readable format
function formatDate(isoDate) {
    if (!isoDate) return '';
    const date = new Date(isoDate);
    const options = { day: 'numeric', month: 'long', year: 'numeric' };
    return date.toLocaleDateString('en-GB', options);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Function to render image or placeholder
function renderImage(imagePath, altText, className) {
    if (imagePath && imagePath.trim() !== '') {
        return `<img src="${escapeHtml(imagePath)}" alt="${escapeHtml(altText)}" class="${className}">`;
    }
    return `<div class="${className} placeholder-image">${escapeHtml(altText)}</div>`;
}

// Function to render timeline events
function renderTimeline() {
    const container = document.getElementById('timeline-container');
    
    if (timelineData.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>Timeline events will be added soon.</p></div>';
        return;
    }
    
    container.innerHTML = timelineData.map(event => `
        <div class="timeline-event">
            <div class="timeline-marker"></div>
            <div class="timeline-content">
                <div class="timeline-date">${escapeHtml(event.date)}</div>
                <h3>${escapeHtml(event.title)}</h3>
                <p>${escapeHtml(event.description)}</p>
            </div>
        </div>
    `).join('');
}

// Function to render logbook entries
function renderLogbook() {
    const container = document.getElementById('logbook-container');
    
    if (logbookData.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>Logbook entries will be added soon.</p></div>';
        return;
    }
    
    container.innerHTML = logbookData.map(entry => `
        <div class="logbook-entry">
            ${renderImage(entry.image, 'Logbook Page Image', 'logbook-image')}
            <div class="logbook-info">
                <div class="date">${escapeHtml(entry.date)}</div>
                <h3>${escapeHtml(entry.title)}</h3>
                <p>${escapeHtml(entry.description)}</p>
                <div class="logbook-details">
                    <div class="detail-item">
                        <span class="detail-label">Aircraft:</span>
                        <span class="detail-value">${escapeHtml(entry.aircraft)}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Duration:</span>
                        <span class="detail-value">${escapeHtml(entry.duration)}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Type:</span>
                        <span class="detail-value">${escapeHtml(entry.type)}</span>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// Function to render logbook pages gallery
function renderLogbookPages() {
    const container = document.getElementById('logbook-pages-container');
    
    if (logbookPagesData.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>Logbook pages are being digitized.</p></div>';
        return;
    }
    
    container.innerHTML = logbookPagesData.map(page => `
        <div class="logbook-page-item">
            ${renderImage(page.image, escapeHtml(page.pageNumber), 'logbook-page-image')}
            <div class="logbook-page-info">
                <div class="page-number">${escapeHtml(page.pageNumber)}</div>
            </div>
        </div>
    `).join('');
}

// Function to render documents
function renderDocuments() {
    const container = document.getElementById('documents-container');
    
    if (documentsData.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>Documents will be added soon.</p></div>';
        return;
    }
    
    container.innerHTML = documentsData.map(doc => `
        <div class="document-card">
            ${renderImage(doc.image, 'Document Image', 'document-image')}
            <div class="document-info">
                <h3>${escapeHtml(doc.title)}</h3>
                <span class="document-type">${escapeHtml(doc.type)}</span>
                <p>${escapeHtml(doc.description)}</p>
            </div>
        </div>
    `).join('');
}

// Smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', () => {
    // Load data and render all sections
    loadData();
    
    // Add smooth scrolling to navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});
