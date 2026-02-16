// DOM Elements
const scrapeForm = document.getElementById('scrapeForm');
const startBtn = document.getElementById('start-btn');
const btnText = document.querySelector('.btn-text');
const btnLoader = document.querySelector('.btn-loader');
const statusIndicator = document.getElementById('status-indicator');
const statusMessage = document.getElementById('status-message');
const statusText = document.getElementById('status');

const progressSection = document.getElementById('progress-section');
const progressFill = document.getElementById('progress-fill');
const progressPercent = document.getElementById('progress-percent');
const pagesScanned = document.getElementById('pages-scanned');
const emailsFound = document.getElementById('emails-found');
const timeElapsed = document.getElementById('time-elapsed');

const logsSection = document.getElementById('logs-section');
const logContainer = document.getElementById('log-container');
const clearLogsBtn = document.getElementById('clear-logs');

const resultsSection = document.getElementById('results-section');
const emailsList = document.getElementById('emails-list');
const downloadTxtBtn = document.getElementById('download-txt');
const downloadCsvBtn = document.getElementById('download-csv');

// State
let isScraping = false;
let startTime = null;
let intervalId = null;

// Form submission
scrapeForm.addEventListener('submit', function(e) {
    e.preventDefault();

    if (isScraping) return;

    const formData = new FormData(scrapeForm);

    // Show loading state
    setLoadingState(true);
    statusIndicator.textContent = 'Starting...';
    statusIndicator.className = 'status-active';

    fetch('/start', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'started') {
            startScraping();
        }
    })
    .catch(error => {
        console.error('Error starting scrape:', error);
        setLoadingState(false);
        statusIndicator.textContent = 'Error';
        statusIndicator.className = 'status-idle';
        alert('Failed to start extraction. Please try again.');
    });
});

// Start scraping process
function startScraping() {
    isScraping = true;
    startTime = Date.now();

    // Hide previous status message
    statusMessage.style.display = 'none';

    // Show progress and logs sections
    progressSection.style.display = 'block';
    logsSection.style.display = 'block';

    // Reset progress
    progressFill.style.width = '0%';
    progressPercent.textContent = '0%';
    pagesScanned.textContent = '0';
    emailsFound.textContent = '0';
    timeElapsed.textContent = '00:00';
    logContainer.innerHTML = '';

    // Start polling
    intervalId = setInterval(() => {
        fetch('/progress')
        .then(response => response.json())
        .then(data => {
            updateProgress(data);

            if (data.finished) {
                finishScraping(data);
            }
        })
        .catch(error => {
            console.error('Error fetching progress:', error);
        });
    }, 500);
}

// Update progress display
function updateProgress(data) {
    // Progress bar
    progressFill.style.width = data.progress + '%';
    progressPercent.textContent = data.progress + '%';

    // Stats (assuming we add these to backend response)
    if (data.pages_scanned !== undefined) {
        pagesScanned.textContent = data.pages_scanned;
    }
    if (data.emails_found !== undefined) {
        emailsFound.textContent = data.emails_found;
    }

    // Time elapsed
    if (startTime) {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
        const seconds = (elapsed % 60).toString().padStart(2, '0');
        timeElapsed.textContent = `${minutes}:${seconds}`;
    }

    // Logs
    if (data.logs && data.logs.length > 0) {
        data.logs.forEach(log => {
            addLogEntry(log);
        });
    }
}

// Add log entry
function addLogEntry(log) {
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';

    // Determine log type
    if (log.includes('[ERROR]')) {
        logEntry.classList.add('error');
    } else if (log.includes('[FOUND]')) {
        logEntry.classList.add('success');
    } else {
        logEntry.classList.add('info');
    }

    logEntry.textContent = log;
    logContainer.appendChild(logEntry);
    logContainer.scrollTop = logContainer.scrollHeight;
}

// Finish scraping
function finishScraping(data) {
    clearInterval(intervalId);
    isScraping = false;
    setLoadingState(false);

    statusIndicator.textContent = 'Complete';
    statusIndicator.className = 'status-complete';

    // Show results
    showResults(data);

    // Show status message
    console.log("Email extraction completed successfully!");
    statusText.innerText = "Email extraction completed successfully!";
    statusMessage.style.display = 'block';

    // Scroll to status message
    statusMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Show results
function showResults(data) {
    resultsSection.style.display = 'block';

    // Assuming emails are returned in the final response
    if (data.emails) {
        emailsList.innerHTML = '';
        data.emails.forEach(email => {
            const emailItem = document.createElement('div');
            emailItem.className = 'email-item';
            emailItem.textContent = email;
            emailsList.appendChild(emailItem);
        });
    }
}

// Set loading state
function setLoadingState(loading) {
    if (loading) {
        startBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'block';
    } else {
        startBtn.disabled = false;
        btnText.style.display = 'block';
        btnLoader.style.display = 'none';
    }
}

// Clear logs
clearLogsBtn.addEventListener('click', () => {
    logContainer.innerHTML = '';
});

// Download handlers
downloadTxtBtn.addEventListener('click', () => {
    downloadFile('emails.txt');
});

downloadCsvBtn.addEventListener('click', () => {
    downloadFile('emails.csv');
});

function downloadFile(filename) {
    fetch(`/download/${filename}`)
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Download failed:', error);
        alert(`Failed to download ${filename}: ${error.message}`);
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Any initialization code here
});
