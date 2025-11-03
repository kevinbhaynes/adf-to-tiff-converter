// Global variables
let uploadedFiles = [];
let convertedBlob = null;

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const convertBtn = document.getElementById('convertBtn');
const progressContainer = document.getElementById('progressContainer');
const progressFill = document.getElementById('progressFill');
const statusMessage = document.getElementById('statusMessage');
const downloadSection = document.getElementById('downloadSection');
const downloadBtn = document.getElementById('downloadBtn');
const errorMessage = document.getElementById('errorMessage');

// Event listeners
uploadArea.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', handleFileSelect);
convertBtn.addEventListener('click', convertToTiff);

// Drag and drop functionality
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
});

// Handle file selection
function handleFileSelect(e) {
    handleFiles(e.target.files);
}

// Process selected files
function handleFiles(files) {
    uploadedFiles = Array.from(files).filter(file => 
        file.name.toLowerCase().endsWith('.adf')
    );
    
    if (uploadedFiles.length === 0) {
        showError('Please select valid ADF files');
        return;
    }
    
    displayFiles();
    convertBtn.disabled = false;
    hideError();
}

// Display uploaded files
function displayFiles() {
    fileList.innerHTML = '';
    
    uploadedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        
        const fileName = document.createElement('div');
        fileName.className = 'file-name';
        fileName.textContent = file.name;
        
        const fileSize = document.createElement('div');
        fileSize.className = 'file-size';
        fileSize.textContent = formatFileSize(file.size);
        
        const removeBtn = document.createElement('button');
        removeBtn.className = 'remove-btn';
        removeBtn.textContent = '✕';
        removeBtn.onclick = () => removeFile(index);
        
        fileItem.appendChild(fileName);
        fileItem.appendChild(fileSize);
        fileItem.appendChild(removeBtn);
        fileList.appendChild(fileItem);
    });
}

// Remove file from list
function removeFile(index) {
    uploadedFiles.splice(index, 1);
    displayFiles();
    
    if (uploadedFiles.length === 0) {
        convertBtn.disabled = true;
        fileList.innerHTML = '';
    }
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Convert ADF to TIFF
async function convertToTiff() {
    try {
        showProgress();
        updateProgress(10, 'Initializing conversion...');

        // Check if we have the required files
        const hasHdr = uploadedFiles.some(f => f.name.toLowerCase() === 'hdr.adf');
        if (!hasHdr) {
            throw new Error('Missing hdr.adf file. Please upload all ADF files from your dataset.');
        }

        updateProgress(20, 'Loading GDAL library...');

        // Use GDAL-based converter for proper GeoTIFF creation
        const tiffBlob = await processAdfFiles(uploadedFiles);

        updateProgress(90, 'Finalizing conversion...');

        convertedBlob = tiffBlob;
        downloadBtn.href = URL.createObjectURL(convertedBlob);
        downloadBtn.download = 'converted_' + Date.now() + '.tiff';

        updateProgress(100, 'Conversion complete!');

        setTimeout(() => {
            hideProgress();
            showDownload();
        }, 1000);

    } catch (error) {
        console.error('Conversion error:', error);
        showError('Error converting file: ' + error.message);
        hideProgress();
    }
}

// Process ADF files using GDAL for proper GeoTIFF creation
async function processAdfFiles(files) {
    try {
        updateProgress(30, 'Initializing GDAL converter...');

        // Try GDAL-based conversion first (produces proper GeoTIFF)
        const converter = new window.AdfToTiffConverter();

        updateProgress(40, 'Loading GDAL library...');
        await converter.initializeGdal();

        updateProgress(50, 'Reading ADF files...');
        updateProgress(60, 'Extracting spatial reference...');
        updateProgress(70, 'Converting to GeoTIFF format...');

        const tiffBlob = await converter.convertAdfToTiff(files);

        updateProgress(85, 'Applying compression and optimization...');

        return tiffBlob;

    } catch (gdalError) {
        console.warn('GDAL conversion failed, trying fallback method:', gdalError);

        // Fallback: Use SimpleAdfReader if GDAL fails
        try {
            updateProgress(50, 'Using fallback converter...');

            const simpleReader = new window.SimpleAdfReader();
            const tiffBlob = await simpleReader.parseAdfFiles(files);

            // Show warning that this may not preserve all spatial information
            console.warn('Using simplified converter - spatial reference may not be fully preserved');

            return tiffBlob;

        } catch (fallbackError) {
            // If both methods fail, provide detailed error
            throw new Error(
                'Failed to convert ADF to TIFF. ' +
                'GDAL error: ' + gdalError.message + '. ' +
                'Fallback error: ' + fallbackError.message + '. ' +
                'Please ensure you have uploaded all ADF files from the dataset.'
            );
        }
    }
}

// UI Helper functions
function showProgress() {
    progressContainer.style.display = 'block';
    convertBtn.disabled = true;
}

function hideProgress() {
    progressContainer.style.display = 'none';
    convertBtn.disabled = false;
}

function updateProgress(percent, message) {
    progressFill.style.width = percent + '%';
    progressFill.textContent = percent + '%';
    statusMessage.textContent = message;
}

function showDownload() {
    downloadSection.style.display = 'block';
}

function hideDownload() {
    downloadSection.style.display = 'none';
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('ADF to TIFF Converter initialized');
});