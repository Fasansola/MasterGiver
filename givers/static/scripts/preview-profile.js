document.addEventListener('DOMContentLoaded', () => {
    // Handle edit button clicks
    document.addEventListener('click', (event) => {
        const target = event.target;
        const button = target.closest('[id^="edit-"][id$="-btn"]');
        if (button) {
            console.log(button)
            const fieldName = button.id.replace('edit-', '').replace('-btn', '');
            const formDiv = document.querySelector(`#${fieldName}_input`).closest('.element-form-field');
            const contentDiv = event.target.closest('.element-content-field');
            
            contentDiv.style.display = 'none';
            formDiv.style.display = 'flex';
        }
    });

    // Handle save button clicks
    document.addEventListener('click', (event) => {
        const target = event.target;
        const button = target.closest('[id^="save-"][id$="-btn"]');
            if (button) {
            const fieldName = button.id.replace('save-', '').replace('-btn', '');
            const formDiv = event.target.closest('.element-form-field');
            const contentDiv = formDiv.previousElementSibling;
            const displayElement = contentDiv.querySelector(`#${fieldName}`);
            const inputElement = formDiv.querySelector(`#${fieldName}_input`);
            
            contentDiv.style.display = 'flex';
            formDiv.style.display = 'none';
            
            if (inputElement.tagName.toLowerCase() === 'textarea') {
                displayElement.textContent = inputElement.value;
            } else {
                displayElement.textContent = inputElement.value;
            }
        }
    });
});