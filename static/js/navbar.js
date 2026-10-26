function scrollToSection(sectionId) {
    const targetSection = document.getElementById(sectionId);
    targetSection.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

