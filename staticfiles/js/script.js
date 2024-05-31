function toggleActive(event, element) {
    // Remove the "active" class from all links
    var links = document.querySelectorAll('.nav-link');
    links.forEach(function(link) {
        link.classList.remove('active');
    });

    // Add the "active" class to the clicked link
    element.classList.add('active');

    // Store the active link in session storage
    sessionStorage.setItem('activeLink', element.getAttribute('href'));
}7
