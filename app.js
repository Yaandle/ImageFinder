// Handle number submission to get the class name
document.getElementById('numberForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    fetch('/submit', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').textContent = 'Class Name: ' + data.position;
    })
    .catch(error => {
        document.getElementById('result').textContent = 'Error: ' + error;
    });
});

// Handle image upload form submission and filter prediction
document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    var className = document.getElementById('result').textContent.replace('Class Name: ', '');
    formData.append('class_name', className); // Append the class name to the form data

    // Assuming you only want to call one of these routes
    // Comment out or remove the one you don't want to use.
    // If you want to use both, you need to adjust the logic to handle two separate requests.
    
    // For object detection
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
            downloadLink.textContent = 'Download Results';
            document.getElementById('odResult').textContent = '';
        } else {
            document.getElementById('odResult').textContent = data.message;
        }
    })
    .catch(error => {
        document.getElementById('odResult').textContent = 'Error: ' + error;
    });
    
    // For predict and filter
    fetch('/predict_filter', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Check if 'filtered_images' is an array before trying to join
        if(Array.isArray(data.filtered_images)) {
            document.getElementById('odResult').textContent = 'Filtered Images: ' + data.filtered_images.join(', ');
        } else {
            // Handle the case where 'filtered_images' is not an array
            document.getElementById('odResult').textContent = 'Error: filtered_images is not an array.';
        }
    })
    .catch(error => {
        document.getElementById('odResult').textContent = 'Error: ' + error;
    });
});
