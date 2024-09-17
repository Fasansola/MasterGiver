document.addEventListener('click', (event) => {
    const target = event.target;
    const expandableBox = target.closest('.expandable-box');
    
    if (!expandableBox) return;

    const readMoreBtn = expandableBox.querySelector('#read-more-btn');
    const readLessBtn = expandableBox.querySelector('#read-less-btn');
    
    if (target.closest('#read-more-btn') || target.closest('#read-less-btn')) {
        const fullText = expandableBox.querySelector('.full-text');
        const truncatedText = expandableBox.querySelector('.truncated-text');

        [fullText, truncatedText, readMoreBtn, readLessBtn].forEach(el => {
            el.classList.toggle('d-none');
            el.classList.toggle('d-flex');
        });
    }
});