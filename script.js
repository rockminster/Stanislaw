// Data will be loaded from content.json
let timelineData = [];
let logbookData = [];
let documentsData = [];

// Load data from JSON file
async function loadData() {
    try {
        const response = await fetch('data/content.json');
        const data = await response.json();
        
        timelineData = data.timeline || [];
        logbookData = (data.logbook || []).map(entry => ({
            ...entry,
            date: formatDate(entry.date),
            imagePlaceholder: true
        }));
        documentsData = (data.documents || []).map(doc => ({
            ...doc,
            imagePlaceholder: true
        }));
        
        // Render all sections after data is loaded
        renderTimeline();
        renderLogbook();
        renderDocuments();
    } catch (error) {
        console.error('Error loading data:', error);
        // Use fallback empty data
        renderTimeline();
        renderLogbook();
        renderDocuments();
    }
}

// Format ISO date to human-readable format
function formatDate(isoDate) {
    if (!isoDate) return '';
    const date = new Date(isoDate);
    const options = { day: 'numeric', month: 'long', year: 'numeric' };
    return date.toLocaleDateString('en-GB', options);
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
                <div class="timeline-date">${event.date}</div>
                <h3>${event.title}</h3>
                <p>${event.description}</p>
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
            <div class="logbook-image placeholder-image">
                ${entry.imagePlaceholder ? 'Logbook Page Image' : ''}
            </div>
            <div class="logbook-info">
                <div class="date">${entry.date}</div>
                <h3>${entry.title}</h3>
                <p>${entry.description}</p>
                <div class="logbook-details">
                    <div class="detail-item">
                        <span class="detail-label">Aircraft:</span>
                        <span class="detail-value">${entry.aircraft}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Duration:</span>
                        <span class="detail-value">${entry.duration}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Type:</span>
                        <span class="detail-value">${entry.type}</span>
                    </div>
                </div>
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
            <div class="document-image placeholder-image">
                ${doc.imagePlaceholder ? 'Document Image' : ''}
            </div>
            <div class="document-info">
                <h3>${doc.title}</h3>
                <span class="document-type">${doc.type}</span>
                <p>${doc.description}</p>
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
