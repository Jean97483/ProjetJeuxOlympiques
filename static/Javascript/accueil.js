document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('section');
    const navLiens = document.querySelectorAll('nav ul li a');

    window.addEventListener('scroll', () => {
        let actuelle = '';

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (pageYOffset >= sectionTop - 60) {
                actuelle = section.getAttribute('id');
            }      
        });

        navLiens.forEach(a => {
            a.classList.remove('active');
            if (a.getAttribute('href').includes(actuelle)) {
                a.classList.add('active');
            }
        });
    });
});