document.addEventListener('DOMContentLoaded', () => {
    const accordions = document.querySelectorAll('.accordion-item');

    accordions.forEach(item => {
        const header = item.querySelector('.accordion-header');
        const content = item.querySelector('.accordion-content');

        header.addEventListener('click', () => {
            // Toggle active class on header
            header.classList.toggle('active');

            // Toggle content visibility
            if (header.classList.contains('active')) {
                content.style.maxHeight = content.scrollHeight + 'px';
                content.style.padding = '1rem';
            } else {
                content.style.maxHeight = '0';
                content.style.padding = '0 1rem';
            }
        });
    });
});

