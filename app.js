// Function to add event listeners safely
function addEventListenerSafely(selector, event, handler) {
    const element = document.getElementById(selector);
    if (element) {
        element.addEventListener(event, handler);
    } else {
        console.error(`Element with ID '${selector}' not found.`);
    }
}

// Handler for 'numberForm' submit event
function handleNumberFormSubmit(event) {
    event.preventDefault();
    var formData = new FormData(this);
    fetch('/submit', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.number && data.position !== undefined) {
            storedClassName = data.position.toString(); // Ensure it's a string
            document.getElementById('result').textContent = 'Class Name: ' + storedClassName;
        } else {
            document.getElementById('result').textContent = 'Number not found or server error';
        }
    })
    .catch(error => {
        document.getElementById('result').textContent = 'Error: ' + error.message;
    });
}

// Handler for 'uploadForm' submit event
function handleUploadFormSubmit(event) {
    event.preventDefault();
    var formData = new FormData(this);
    fetch('/object_detection', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data.zip_file_base64) {
            var downloadLink = document.getElementById('downloadLink');
            downloadLink.href = 'data:application/zip;base64,' + data.zip_file_base64;
            downloadLink.download = 'results.zip';
            downloadLink.style.display = 'block';
            document.getElementById('odResult').textContent = '';
        } else {
            document.getElementById('odResult').textContent = 'No results to download.';
        }
    })
    .catch(error => {
        document.getElementById('odResult').textContent = 'Error: ' + error.message;
    });
}

// Handler for 'predictFilterForm' submit event
function handlePredictFilterFormSubmit(event) {
    event.preventDefault();
    var formData = new FormData(); 
    formData.append('class_name', storedClassName); 

    fetch('/predict_filter', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(Array.isArray(data.filtered_images)) {
            document.getElementById('odResult').textContent = 'Filtered Images: ' + data.filtered_images.join(', ');
        } else {
            document.getElementById('odResult').textContent = 'No images matching the class name were found.';
        }
    })
    .catch(error => {
        document.getElementById('odResult').textContent = 'Error: ' + error.message;
    });
}

// Adding event listeners when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    addEventListenerSafely('numberForm', 'submit', handleNumberFormSubmit);
    addEventListenerSafely('uploadForm', 'submit', handleUploadFormSubmit);
    addEventListenerSafely('predictFilterForm', 'submit', handlePredictFilterFormSubmit);
});
