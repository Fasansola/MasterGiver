let causes = document.querySelectorAll('.causes-items')
let causesCheck = document.querySelectorAll('.causes-check')
let boxesContainer = document.querySelectorAll('.items-container')


document.getElementById('causes-btn').addEventListener('click', () => {
    causesCheck.forEach(cause => {
        let itemIndex = Array.from(causesCheck).indexOf(cause) 
        if (cause.checked) {
            causes[itemIndex].style.display = 'flex'
            causes[itemIndex].dataset.id = itemIndex
        } else {
            causes[itemIndex].style.display = ''
        }
    })
    boxesContainer[0].style.display = 'flex'
    causesField.value = '';
    toggleDropdown(causesDropdown, false);
    filterList(causesField, '.causes-check');
})


// FOR SKILLS


let skills = document.querySelectorAll('.skills-items')
let skillsCheck = document.querySelectorAll('.skills-check')


document.getElementById('skills-btn').addEventListener('click', () => {
    skillsCheck.forEach(skill => {
        let itemIndex = Array.from(skillsCheck).indexOf(skill) 
        if (skill.checked) {
            skills[itemIndex].style.display = 'flex'
        } else {
            skills[itemIndex].style.display = ''
        }
    })
    boxesContainer[1].style.display = 'flex'
    skillsField.value = '';
    toggleDropdown(skillsDropdown, false);
    filterList(skillsField, '.skills-check');
})

document.addEventListener('click', (event) => {
    if (!event.target.classList.contains('skill-causes-items')) {
        if (event.target.matches(':focus') == true && event.target.id != "what_i_care_about")
            toggleDropdown(causesDropdown, false)
        if (event.target.matches(':focus') == true && event.target.id != "giving_skills")
            toggleDropdown(skillsDropdown, false)
    }
})


// FILTER CAUSES AND SKILLS

// FUNCTIONS

function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}


function filterList(inputField, itemSelector) {
    const filter = inputField.value.toUpperCase();
    const items = document.querySelectorAll(itemSelector);
    items.forEach(item => {
        item.parentNode.style.display = item.value.toUpperCase().includes(filter) ? '' : 'none';
    });
}

// FUNCTIONS ASSIGNMENTS

const causesField = document.getElementById('what_i_care_about');
const skillsField = document.getElementById('giving_skills');
const filterCauses = () => filterList(causesField, '.causes-check');
const filterSkills = () => filterList(skillsField, '.skills-check');


// FUNCTION CALLS & EVENT LISTENERS

causesField.addEventListener('input', debounce(filterCauses, 100));
causesField.addEventListener('', debounce(filterCauses, 100));
skillsField.addEventListener('input', debounce(filterSkills, 100));




// MANAGE DROPDOWNS

// FUNCTIONS

function toggleDropdown(dropdown, isVisible) {
    dropdown.style.visibility = isVisible ? 'visible' : 'hidden';
    dropdown.style.opacity = isVisible ? '1' : '0';
    dropdown.style.transform = isVisible ? 'translateY(0)' : 'translateY(-10px)';
}

// FUNCTIONS ASSIGNMENTS

const causesDropdown = document.getElementById('causes-dropdown');
const skillsDropdown = document.getElementById('skills-dropdown');


causesField.addEventListener('focus', () => toggleDropdown(causesDropdown, true));
skillsField.addEventListener('focus', () => toggleDropdown(skillsDropdown, true));
