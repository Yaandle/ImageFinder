function addEventListenerSafely(selector, event, handler) {
    const element = document.getElementById(selector);
    if (element) {
        element.addEventListener(event, handler);
    } else {
        console.error(`Element with ID '${selector}' not found.`);
    }
}

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
            storedClassName = data.position.toString();
            document.getElementById('result').textContent = 'Class Name: ' + storedClassName;
        } else {
            document.getElementById('result').textContent = 'Number not found or server error';
        }
    })
    .catch(error => {
        document.getElementById('result').textContent = 'Error: ' + error.message;
    });
}

function handleUploadFormSubmit(event) {
    event.preventDefault();
    var formData = new FormData(this);

    document.getElementById('odResult').textContent = 'Uploading and processing...';

    fetch('/object_detection', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        if (data.zip_file_base64) {
            var downloadLink = document.getElementById('downloadLink');
            downloadLink.href = 'data:application/zip;base64,' + data.zip_file_base64;
            downloadLink.download = 'results.zip';
            downloadLink.style.display = 'block';
            document.getElementById('odResult').textContent = 'Object detection completed. Download the results below.';
        } else {
            document.getElementById('odResult').textContent = 'No results to download.';
        }
    })
    .catch(error => {
        document.getElementById('odResult').textContent = 'Error: ' + error.message;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    addEventListenerSafely('numberForm', 'submit', handleNumberFormSubmit);
    addEventListenerSafely('uploadForm', 'submit', handleUploadFormSubmit);
});
