/**
 * This module handles the functionality for uploading and displaying a profile image.
 * It listens for changes on the file input, updates the profile picture preview,
 * and displays the name of the selected file.
 */

/**
 * Initializes the image upload functionality.
 * This function should be called when the DOM is ready.
 */
export function initializeImageUpload() {
    const fileInput = document.getElementById('upload-image');
    const profilePic = document.getElementById('profile-picture');
    const fileChosen = document.getElementById('file-chosen');

    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        
        // Update the profile picture preview if a file is selected
        if (file) {
            profilePic.src = URL.createObjectURL(file);
        }

        // Update the file name display
        if (this.files && this.files.length > 0) {
            fileChosen.textContent = this.files[0].name;
        } else {
            fileChosen.textContent = 'No file chosen';
        }
    });
}