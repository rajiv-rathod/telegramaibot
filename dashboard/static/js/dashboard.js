// Dashboard JavaScript functionality

let currentConfig = {};
let currentPersonalities = {};
let currentEditingPersonality = null;

document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    loadInitialData();
    setupEventListeners();
    
    // Update status every 30 seconds
    setInterval(updateBotStatus, 30000);
});

function initializeDashboard() {
    // Set up navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const section = this.dataset.section;
            if (section) {
                switchSection(section);
                updateActiveNavLink(this);
            }
        });
    });
    
    // Set up range slider
    const replyProbabilitySlider = document.getElementById('reply-probability');
    if (replyProbabilitySlider) {
        replyProbabilitySlider.addEventListener('input', function() {
            document.getElementById('reply-probability-value').textContent = this.value;
        });
    }
}

function loadInitialData() {
    loadBotConfig();
    loadPersonalities();
    loadPDFs();
    updateBotStatus();
}

function setupEventListeners() {
    // Bot control buttons
    document.getElementById('start-bot')?.addEventListener('click', startBot);
    document.getElementById('stop-bot')?.addEventListener('click', stopBot);
    document.getElementById('save-all')?.addEventListener('click', saveAll);
    
    // Configuration form
    document.getElementById('config-form')?.addEventListener('submit', saveConfig);
    
    // Personality management
    document.getElementById('add-personality')?.addEventListener('click', addNewPersonality);
    document.getElementById('personality-form')?.addEventListener('submit', savePersonality);
    document.getElementById('cancel-edit')?.addEventListener('click', cancelPersonalityEdit);
    
    // PDF management
    document.getElementById('pdf-upload-form')?.addEventListener('submit', uploadPDF);
    
    // Account management
    document.getElementById('add-account')?.addEventListener('click', addAccount);
    document.getElementById('save-accounts')?.addEventListener('click', saveAccounts);
    
    // Debug logs
    document.getElementById('refresh-logs')?.addEventListener('click', refreshLogs);
    document.getElementById('clear-logs')?.addEventListener('click', clearLogs);
}

function switchSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Show selected section
    const section = document.getElementById(sectionName + '-section');
    if (section) {
        section.style.display = 'block';
    }
    
    // Update page title
    const titles = {
        'overview': 'Dashboard Overview',
        'personality': 'Personality Management',
        'pdfs': 'PDF Management',
        'config': 'Bot Configuration',
        'accounts': 'Bot Accounts',
        'debug': 'Debug & Logs'
    };
    
    document.getElementById('page-title').textContent = titles[sectionName] || 'Dashboard';
}

function updateActiveNavLink(activeLink) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    activeLink.classList.add('active');
}

// API Communication Functions
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(`/api/${endpoint}`, options);
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        showNotification('API call failed: ' + error.message, 'error');
        return null;
    }
}

async function loadBotConfig() {
    const config = await apiCall('config');
    if (config) {
        currentConfig = config;
        updateConfigUI(config);
    }
}

function updateConfigUI(config) {
    // Update form fields
    document.getElementById('reply-probability').value = config.reply_probability || 0.4;
    document.getElementById('reply-probability-value').textContent = config.reply_probability || 0.4;
    document.getElementById('context-msg-limit').value = config.context_msg_limit || 15;
    document.getElementById('max-response-tokens').value = config.max_response_tokens || 200;
    document.getElementById('min-response-delay').value = config.min_response_delay || 1.0;
    document.getElementById('max-response-delay').value = config.max_response_delay || 4.0;
    document.getElementById('typing-delay').value = config.typing_delay_per_word || 0.15;
    document.getElementById('debug-mode').checked = config.debug_mode || false;
}

async function saveConfig(e) {
    e.preventDefault();
    
    const config = {
        reply_probability: parseFloat(document.getElementById('reply-probability').value),
        context_msg_limit: parseInt(document.getElementById('context-msg-limit').value),
        max_response_tokens: parseInt(document.getElementById('max-response-tokens').value),
        min_response_delay: parseFloat(document.getElementById('min-response-delay').value),
        max_response_delay: parseFloat(document.getElementById('max-response-delay').value),
        typing_delay_per_word: parseFloat(document.getElementById('typing-delay').value),
        debug_mode: document.getElementById('debug-mode').checked,
        active_personality: currentConfig.active_personality,
        pdf_directory: currentConfig.pdf_directory
    };
    
    const result = await apiCall('config', 'POST', config);
    if (result && result.status === 'success') {
        currentConfig = config;
        showNotification('Configuration saved successfully!', 'success');
    }
}

async function loadPersonalities() {
    const personalities = await apiCall('personalities');
    if (personalities) {
        currentPersonalities = personalities;
        updatePersonalityUI(personalities);
    }
}

function updatePersonalityUI(personalities) {
    const personalityList = document.getElementById('personality-list');
    if (!personalityList) return;
    
    personalityList.innerHTML = '';
    
    Object.entries(personalities).forEach(([pid, personality]) => {
        const isActive = currentConfig.active_personality === pid;
        const isDefault = ['sylvia_default', 'professional', 'casual_friend', 'tech_expert'].includes(pid);
        
        const item = document.createElement('div');
        item.className = `personality-item mb-3 p-3 border rounded ${isActive ? 'border-primary bg-light' : ''}`;
        item.dataset.personalityId = pid;
        
        item.innerHTML = `
            <h6>${personality.name}</h6>
            <p class="text-muted small">${personality.description}</p>
            <div class="btn-group-sm">
                <button class="btn btn-primary btn-sm select-personality">Select</button>
                <button class="btn btn-outline-secondary btn-sm edit-personality">Edit</button>
                ${!isDefault ? '<button class="btn btn-outline-danger btn-sm delete-personality">Delete</button>' : ''}
            </div>
        `;
        
        // Add event listeners
        item.querySelector('.select-personality').addEventListener('click', () => selectPersonality(pid));
        item.querySelector('.edit-personality').addEventListener('click', () => editPersonality(pid));
        const deleteBtn = item.querySelector('.delete-personality');
        if (deleteBtn) {
            deleteBtn.addEventListener('click', () => deletePersonality(pid));
        }
        
        personalityList.appendChild(item);
    });
}

async function selectPersonality(personalityId) {
    currentConfig.active_personality = personalityId;
    const result = await apiCall('config', 'POST', currentConfig);
    if (result && result.status === 'success') {
        showNotification('Personality selected successfully!', 'success');
        updatePersonalityUI(currentPersonalities);
        updateCurrentPersonalityInfo(personalityId);
    }
}

function updateCurrentPersonalityInfo(personalityId) {
    const personality = currentPersonalities[personalityId];
    if (personality) {
        document.getElementById('current-personality-name').textContent = personality.name;
        document.getElementById('current-personality-desc').textContent = personality.description;
    }
}

function editPersonality(personalityId) {
    currentEditingPersonality = personalityId;
    const personality = currentPersonalities[personalityId];
    
    if (personality) {
        document.getElementById('personality-name').value = personality.name;
        document.getElementById('personality-description').value = personality.description;
        document.getElementById('personality-content').value = personality.content;
    }
    
    // Show form area (scroll to it)
    document.getElementById('personality-form').scrollIntoView({ behavior: 'smooth' });
}

function addNewPersonality() {
    currentEditingPersonality = null;
    document.getElementById('personality-form').reset();
    document.getElementById('personality-form').scrollIntoView({ behavior: 'smooth' });
}

async function savePersonality(e) {
    e.preventDefault();
    
    const name = document.getElementById('personality-name').value;
    const description = document.getElementById('personality-description').value;
    const content = document.getElementById('personality-content').value;
    
    const personalityId = currentEditingPersonality || generatePersonalityId(name);
    
    const updatedPersonalities = { ...currentPersonalities };
    updatedPersonalities[personalityId] = {
        name: name,
        description: description,
        content: content
    };
    
    const result = await apiCall('personalities', 'POST', updatedPersonalities);
    if (result && result.status === 'success') {
        currentPersonalities = updatedPersonalities;
        updatePersonalityUI(updatedPersonalities);
        cancelPersonalityEdit();
        showNotification('Personality saved successfully!', 'success');
    }
}

function generatePersonalityId(name) {
    return name.toLowerCase().replace(/[^a-z0-9]/g, '_') + '_' + Date.now();
}

function cancelPersonalityEdit() {
    currentEditingPersonality = null;
    document.getElementById('personality-form').reset();
}

async function deletePersonality(personalityId) {
    if (confirm('Are you sure you want to delete this personality?')) {
        const result = await apiCall(`personality/${personalityId}`, 'DELETE');
        if (result && result.status === 'success') {
            delete currentPersonalities[personalityId];
            updatePersonalityUI(currentPersonalities);
            showNotification('Personality deleted successfully!', 'success');
        }
    }
}

async function uploadPDF(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('pdf-file');
    const file = fileInput.files[0];
    
    if (!file) {
        showNotification('Please select a file', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/upload_pdf', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if (result.status === 'success') {
            showNotification('PDF uploaded successfully!', 'success');
            loadPDFs();
            fileInput.value = '';
        } else {
            showNotification(result.message || 'Upload failed', 'error');
        }
    } catch (error) {
        showNotification('Upload failed: ' + error.message, 'error');
    }
}

async function loadPDFs() {
    const pdfs = await apiCall('pdfs');
    if (pdfs) {
        updatePDFsUI(pdfs);
    }
}

function updatePDFsUI(pdfs) {
    const pdfList = document.getElementById('pdf-list');
    if (!pdfList) return;
    
    pdfList.innerHTML = '';
    
    pdfs.forEach(pdf => {
        const item = document.createElement('div');
        item.className = 'pdf-item mb-3 p-3 border rounded';
        
        item.innerHTML = `
            <h6>${pdf.name}</h6>
            <small class="text-muted">
                Size: ${(pdf.size / 1024 / 1024).toFixed(1)} MB | 
                Modified: ${pdf.modified}
            </small>
            <div class="mt-2">
                <button class="btn btn-outline-danger btn-sm delete-pdf" data-path="${pdf.path}">
                    <i class="fas fa-trash me-1"></i>Delete
                </button>
            </div>
        `;
        
        item.querySelector('.delete-pdf').addEventListener('click', () => deletePDF(pdf.path));
        pdfList.appendChild(item);
    });
}

async function deletePDF(path) {
    if (confirm('Are you sure you want to delete this PDF?')) {
        const result = await apiCall('delete_pdf', 'POST', { path: path });
        if (result && result.status === 'success') {
            showNotification('PDF deleted successfully!', 'success');
            loadPDFs();
        }
    }
}

async function updateBotStatus() {
    const status = await apiCall('bot/status');
    if (status) {
        document.getElementById('status-text').textContent = status.running ? 'Online' : 'Offline';
        document.getElementById('bot-status').className = `badge ${status.running ? 'bg-success' : 'bg-danger'}`;
        document.getElementById('bot-status').textContent = status.running ? 'Online' : 'Offline';
        document.getElementById('active-sessions').textContent = status.active_sessions || 0;
        document.getElementById('messages-today').textContent = status.messages_today || 0;
        document.getElementById('uptime').textContent = status.uptime || '0:00:00';
    }
}

async function startBot() {
    const result = await apiCall('bot/start', 'POST');
    if (result && result.status === 'success') {
        showNotification('Bot start command sent!', 'success');
        setTimeout(updateBotStatus, 2000);
    }
}

async function stopBot() {
    const result = await apiCall('bot/stop', 'POST');
    if (result && result.status === 'success') {
        showNotification('Bot stop command sent!', 'success');
        setTimeout(updateBotStatus, 2000);
    }
}

function addAccount() {
    const accountsList = document.getElementById('accounts-list');
    const newAccount = document.createElement('div');
    newAccount.className = 'account-item mb-3 p-3 border rounded';
    
    newAccount.innerHTML = `
        <div class="row">
            <div class="col-md-4">
                <label class="form-label">API ID</label>
                <input type="text" class="form-control account-api-id" value="">
            </div>
            <div class="col-md-4">
                <label class="form-label">API Hash</label>
                <input type="text" class="form-control account-api-hash" value="">
            </div>
            <div class="col-md-3">
                <label class="form-label">Phone</label>
                <input type="text" class="form-control account-phone" value="">
            </div>
            <div class="col-md-1 d-flex align-items-end">
                <button class="btn btn-outline-danger btn-sm remove-account">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `;
    
    newAccount.querySelector('.remove-account').addEventListener('click', () => {
        newAccount.remove();
    });
    
    accountsList.appendChild(newAccount);
}

async function saveAccounts() {
    const accountItems = document.querySelectorAll('.account-item');
    const accounts = [];
    
    accountItems.forEach(item => {
        const apiId = item.querySelector('.account-api-id').value;
        const apiHash = item.querySelector('.account-api-hash').value;
        const phone = item.querySelector('.account-phone').value;
        
        if (apiId && apiHash && phone) {
            accounts.push({
                api_id: parseInt(apiId),
                api_hash: apiHash,
                phone: phone
            });
        }
    });
    
    const result = await apiCall('accounts', 'POST', accounts);
    if (result && result.status === 'success') {
        showNotification('Accounts saved successfully!', 'success');
    }
}

async function refreshLogs() {
    const logs = await apiCall('logs');
    if (logs && logs.logs) {
        updateLogsUI(logs.logs);
    }
}

function updateLogsUI(logs) {
    const logsContent = document.getElementById('logs-content');
    if (!logsContent) return;
    
    logsContent.innerHTML = '';
    
    logs.forEach(log => {
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${log.level.toLowerCase()}`;
        logEntry.textContent = `[${log.timestamp}] ${log.level}: ${log.message}`;
        logsContent.appendChild(logEntry);
    });
    
    // Scroll to bottom
    logsContent.scrollTop = logsContent.scrollHeight;
}

function clearLogs() {
    if (confirm('Are you sure you want to clear all logs?')) {
        document.getElementById('logs-content').innerHTML = 'Logs cleared.';
        showNotification('Logs cleared!', 'success');
    }
}

async function saveAll() {
    await saveConfig(new Event('submit'));
    await saveAccounts();
    showNotification('All settings saved!', 'success');
}

function showNotification(message, type = 'info') {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'primary'} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        document.body.removeChild(toast);
    });
}

// Add delegation for dynamically added elements
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('remove-account')) {
        e.target.closest('.account-item').remove();
    }
});

// Global function for navigation (called from HTML)
window.switchSection = switchSection;