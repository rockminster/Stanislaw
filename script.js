// Sample data - in a real application, this would be loaded from an API or database
const timelineData = [
    {
        date: "September 1939",
        title: "Poland Invaded",
        description: "Germany invades Poland, marking the beginning of World War II. Polish forces mobilize to defend their homeland."
    },
    {
        date: "1940",
        title: "Escape to England",
        description: "Following the fall of Poland, Stanislaw escapes to England to continue the fight with the RAF."
    },
    {
        date: "1941",
        title: "RAF Training",
        description: "Completion of RAF pilot training and assignment to a Polish squadron."
    },
    {
        date: "1942-1945",
        title: "Active Service",
        description: "Active combat missions over Europe, defending Britain and supporting Allied operations."
    }
];

const logbookData = [
    {
        id: 1,
        date: "15 March 1942",
        title: "Training Flight",
        description: "Navigation training exercise over the English Channel. Practice formation flying with squadron.",
        aircraft: "Supermarine Spitfire Mk V",
        duration: "2h 15m",
        pilot: "Self",
        type: "Training",
        imagePlaceholder: true
    },
    {
        id: 2,
        date: "3 April 1942",
        title: "Convoy Escort",
        description: "Escorted merchant convoy across the North Sea. No enemy contact reported.",
        aircraft: "Supermarine Spitfire Mk V",
        duration: "3h 45m",
        pilot: "Self",
        type: "Operational",
        imagePlaceholder: true
    },
    {
        id: 3,
        date: "20 May 1942",
        title: "Coastal Patrol",
        description: "Routine coastal patrol mission along the southern coast of England.",
        aircraft: "Supermarine Spitfire Mk V",
        duration: "1h 30m",
        pilot: "Self",
        type: "Patrol",
        imagePlaceholder: true
    }
];

const documentsData = [
    {
        id: 1,
        title: "RAF Service Record",
        type: "Official Document",
        description: "Official service record documenting Stanislaw's time with the Royal Air Force.",
        imagePlaceholder: true
    },
    {
        id: 2,
        title: "Squadron Photograph",
        type: "Photograph",
        description: "Group photograph of the Polish squadron, circa 1943.",
        imagePlaceholder: true
    },
    {
        id: 3,
        title: "Commendation Letter",
        type: "Letter",
        description: "Official commendation for bravery and dedication to duty.",
        imagePlaceholder: true
    },
    {
        id: 4,
        title: "Flight Certificate",
        type: "Certificate",
        description: "RAF pilot qualification certificate and credentials.",
        imagePlaceholder: true
    }
];

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
    // Render all sections
    renderTimeline();
    renderLogbook();
    renderDocuments();
    
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
