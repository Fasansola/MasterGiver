document.addEventListener('click', (event) => {
    if (event.target.id == 'edit-element-btn') {
        editButton = event.target
        let elementContent = editButton.closest('.element-content-field')
        let elementForm = elementContent.parentNode.querySelector('.element-form-field')
        elementContent.style.display = 'none'
        elementForm.style.display = 'flex'
    }

    if (event.target.id == 'save-element-btn') {
        saveButton = event.target
        let elementForm = saveButton.closest('.element-form-field')
        let elementContent = elementForm.parentNode.querySelector('.element-content-field')
        elementForm.style.display = 'none'
        elementContent.style.display = 'flex'
        elementTextId = saveButton.dataset.id
        values = elementForm.querySelectorAll('.' + elementTextId)
        document.getElementById(elementTextId).textContent = ''
        values.forEach((value) => {
            document.getElementById(elementTextId).textContent += value.value + ' ';
        })
    }
})