// PNOE Report Generator - Frontend JavaScript

let currentFileId = null;
let goals = [];
let additionalMetrics = {};
let extractedData = null; // Store data from PDF or manual entry

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupFileUpload();
    setupDragAndDrop();
});

// Tab Switching
function switchTab(tabName) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
        tab.style.display = 'none';
    });

    // Remove active class from all buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    if (tabName === 'pdf') {
        document.getElementById('pdfTab').classList.add('active');
        document.getElementById('pdfTab').style.display = 'block';
        document.querySelectorAll('.tab-button')[0].classList.add('active');
    } else if (tabName === 'manual') {
        document.getElementById('manualTab').classList.add('active');
        document.getElementById('manualTab').style.display = 'block';
        document.querySelectorAll('.tab-button')[1].classList.add('active');
    }
}

// Submit Manual Data
async function submitManualData() {
    // Validate required fields
    const requiredFields = ['manual_name', 'manual_age', 'manual_gender', 'manual_weight', 'manual_vo2max_rel'];
    const missingFields = [];

    for (const fieldId of requiredFields) {
        const field = document.getElementById(fieldId);
        if (!field.value) {
            missingFields.push(field.previousElementSibling.textContent.replace(' *', ''));
        }
    }

    if (missingFields.length > 0) {
        alert('Please fill in the following required fields:\n- ' + missingFields.join('\n- '));
        return;
    }

    // Collect manual data
    const manualData = {
        patient_info: {
            name: document.getElementById('manual_name').value,
            age: parseInt(document.getElementById('manual_age').value),
            gender: document.getElementById('manual_gender').value,
            weight_kg: parseFloat(document.getElementById('manual_weight').value),
            test_date: document.getElementById('manual_test_date').value || new Date().toISOString().split('T')[0]
        },
        metabolic_data: {
            vo2max_rel: parseFloat(document.getElementById('manual_vo2max_rel').value),
            rmr: parseInt(document.getElementById('manual_rmr').value) || null
        },
        heart_rate_data: {},
        caloric_data: {},
        core_scores: {}
    };

    // Send manual data to server
    try {
        const response = await fetch('/submit_manual', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(manualData)
        });

        const data = await response.json();

        if (data.success) {
            currentFileId = data.file_id;
            extractedData = data.extracted_data;

            // Hide upload section, show customize section
            document.getElementById('uploadSection').style.display = 'none';
            document.getElementById('customizeSection').style.display = 'block';

            // Auto-fill chronological age from manual entry
            document.getElementById('chronologicalAge').value = manualData.patient_info.age;

            // Scroll to customize section
            document.getElementById('customizeSection').scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('Error submitting manual data: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        alert('Error submitting manual data: ' + error.message);
    }
}

// File Upload Setup
function setupFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const uploadArea = document.getElementById('uploadArea');

    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            showFileInfo(file);
        }
    });

    uploadBtn.addEventListener('click', uploadFile);

    // Make upload area clickable
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });
}

// Drag and Drop
function setupDragAndDrop() {
    const uploadArea = document.getElementById('uploadArea');

    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (file.type === 'application/pdf') {
                document.getElementById('fileInput').files = files;
                showFileInfo(file);
            } else {
                alert('Please upload a PDF file');
            }
        }
    });
}

// Show File Info
function showFileInfo(file) {
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileInfo').style.display = 'block';
}

// Upload File
async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select a file first');
        return;
    }

    // Show progress bar
    document.getElementById('progressBar').style.display = 'block';
    document.getElementById('uploadBtn').disabled = true;

    const formData = new FormData();
    formData.append('pdf_file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            currentFileId = data.file_id;
            displayExtractedData(data.extracted_data);

            // Hide upload section, show preview and customize sections
            document.getElementById('uploadSection').style.display = 'none';
            document.getElementById('previewSection').style.display = 'block';
            document.getElementById('customizeSection').style.display = 'block';

            // Scroll to preview
            document.getElementById('previewSection').scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Upload failed: ' + error.message);
    } finally {
        document.getElementById('progressBar').style.display = 'none';
        document.getElementById('uploadBtn').disabled = false;
    }
}

// Display Extracted Data
function displayExtractedData(data) {
    const previewDiv = document.getElementById('dataPreview');
    previewDiv.innerHTML = '';

    // Patient Info
    if (data.patient_info && Object.keys(data.patient_info).length > 0) {
        const section = createPreviewSection('Patient Information', data.patient_info);
        previewDiv.appendChild(section);
    }

    // Core Scores
    if (data.core_scores && Object.keys(data.core_scores).length > 0) {
        const section = createPreviewSection('Core Performance Scores', data.core_scores);
        previewDiv.appendChild(section);
    }

    // Caloric Data
    if (data.caloric_data && Object.keys(data.caloric_data).length > 0) {
        const section = createPreviewSection('Caloric Data', data.caloric_data);
        previewDiv.appendChild(section);
    }

    // Heart Rate Data
    if (data.heart_rate_data && Object.keys(data.heart_rate_data).length > 0) {
        const section = createPreviewSection('Heart Rate Data', data.heart_rate_data);
        previewDiv.appendChild(section);
    }

    // Metabolic Data
    if (data.metabolic_data && Object.keys(data.metabolic_data).length > 0) {
        const section = createPreviewSection('Metabolic Data', data.metabolic_data);
        previewDiv.appendChild(section);
    }
}

// Create Preview Section
function createPreviewSection(title, data) {
    const section = document.createElement('div');
    section.style.marginBottom = '1.5rem';

    const heading = document.createElement('h3');
    heading.textContent = title;
    heading.style.color = '#475569';
    heading.style.fontSize = '1.1rem';
    heading.style.marginBottom = '1rem';
    section.appendChild(heading);

    for (const [key, value] of Object.entries(data)) {
        if (key !== 'all_text' && value !== null && value !== undefined) {
            const item = document.createElement('div');
            item.className = 'preview-item';

            const label = document.createElement('div');
            label.className = 'preview-label';
            label.textContent = formatLabel(key);

            const val = document.createElement('div');
            val.className = 'preview-value';
            val.textContent = formatValue(value);

            item.appendChild(label);
            item.appendChild(val);
            section.appendChild(item);
        }
    }

    return section;
}

// Format Label
function formatLabel(key) {
    return key
        .replace(/_/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase());
}

// Format Value
function formatValue(value) {
    if (typeof value === 'number') {
        return value;
    }
    return String(value);
}

// Add Goal
function addGoal() {
    const input = document.getElementById('goalInput');
    const goalText = input.value.trim();

    if (goalText) {
        goals.push(goalText);
        renderGoals();
        input.value = '';
    }
}

// Handle Enter key in goal input
document.addEventListener('DOMContentLoaded', function() {
    const goalInput = document.getElementById('goalInput');
    if (goalInput) {
        goalInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                addGoal();
            }
        });
    }
});

// Render Goals
function renderGoals() {
    const goalsList = document.getElementById('goalsList');
    goalsList.innerHTML = '';

    goals.forEach((goal, index) => {
        const li = document.createElement('li');
        li.textContent = goal;

        const removeBtn = document.createElement('button');
        removeBtn.className = 'remove-goal';
        removeBtn.textContent = '×';
        removeBtn.onclick = function() {
            removeGoal(index);
        };

        li.appendChild(removeBtn);
        goalsList.appendChild(li);
    });
}

// Remove Goal
function removeGoal(index) {
    goals.splice(index, 1);
    renderGoals();
}

// Add Metric Row
function addMetricRow() {
    const container = document.getElementById('additionalMetrics');
    const newRow = document.createElement('div');
    newRow.className = 'metric-input';
    newRow.innerHTML = `
        <input type="text" class="form-control" placeholder="Metric name" data-type="name">
        <input type="text" class="form-control" placeholder="Value" data-type="value">
        <button class="btn btn-icon btn-secondary" onclick="this.parentElement.remove()">−</button>
    `;
    container.appendChild(newRow);
}

// Generate Report
async function generateReport() {
    if (!currentFileId) {
        alert('Please upload a file first');
        return;
    }

    const generateBtn = document.getElementById('generateBtn');
    generateBtn.disabled = true;
    generateBtn.textContent = 'Generating...';

    // Collect additional metrics
    const metricInputs = document.querySelectorAll('#additionalMetrics .metric-input');
    const metrics = {};

    metricInputs.forEach(row => {
        const nameInput = row.querySelector('[data-type="name"]');
        const valueInput = row.querySelector('[data-type="value"]');
        const name = nameInput.value.trim();
        const value = valueInput.value.trim();

        if (name && value) {
            metrics[name] = value;
        }
    });

    // Prepare data
    const bioAgeOverride = document.getElementById('biologicalAgeOverride').value;
    const reportData = {
        file_id: currentFileId,
        report_type: document.getElementById('reportType').value,
        chronological_age: parseInt(document.getElementById('chronologicalAge').value) || null,
        biological_age_override: bioAgeOverride ? parseInt(bioAgeOverride) : null,
        custom_notes: document.getElementById('customNotes').value,
        goals: goals,
        additional_metrics: metrics
    };

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reportData)
        });

        const data = await response.json();

        if (data.success) {
            // DON'T open report yet - let user add AI recommendations first!
            // Store the download URL for later
            window.basicReportUrl = data.download_url;

            // Also expose it globally for the AI download button
            window.currentFileId = currentFileId;

            // Show AI section so user can optionally add recommendations
            document.getElementById('customizeSection').style.display = 'none';
            document.getElementById('aiSection').style.display = 'block';
            document.getElementById('downloadSection').style.display = 'block';

            const downloadLink = document.getElementById('downloadLink');
            downloadLink.href = data.download_url;

            // Scroll to AI section
            document.getElementById('aiSection').scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('Error generating report: ' + data.error);
        }
    } catch (error) {
        alert('Failed to generate report: ' + error.message);
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = '🎉 Generate Report';
    }
}

// Reset Form
function resetForm() {
    // Reset all sections
    document.getElementById('uploadSection').style.display = 'block';
    document.getElementById('previewSection').style.display = 'none';
    document.getElementById('customizeSection').style.display = 'none';
    document.getElementById('downloadSection').style.display = 'none';

    // Reset form fields
    document.getElementById('fileInput').value = '';
    document.getElementById('fileInfo').style.display = 'none';
    document.getElementById('reportType').value = 'performance';
    document.getElementById('chronologicalAge').value = '';
    document.getElementById('biologicalAgeOverride').value = '';
    document.getElementById('customNotes').value = '';
    document.getElementById('goalInput').value = '';

    // Reset goals and metrics
    goals = [];
    renderGoals();

    // Reset additional metrics
    const metricsContainer = document.getElementById('additionalMetrics');
    metricsContainer.innerHTML = `
        <div class="metric-input">
            <input type="text" class="form-control" placeholder="Metric name" data-type="name">
            <input type="text" class="form-control" placeholder="Value" data-type="value">
            <button class="btn btn-icon" onclick="addMetricRow()">+</button>
        </div>
    `;

    // Reset file ID
    currentFileId = null;

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
