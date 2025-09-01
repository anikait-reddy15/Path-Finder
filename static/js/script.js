document.addEventListener("DOMContentLoaded", function() {
    // Select all sections that have the 'hidden' class
    const hiddenElements = document.querySelectorAll('.content-section.hidden');

    // Set up the observer options
    // The element will be considered 'visible' when 5% of it is in the viewport
    const options = {
        root: null, // observes intersections relative to the viewport
        threshold: 0.05,
    };

    // Create a new Intersection Observer
    const observer = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            // If the element is intersecting (visible)
            if (entry.isIntersecting) {
                // Remove the 'hidden' class and add 'visible' to trigger the animation
                entry.target.classList.remove('hidden');
                entry.target.classList.add('visible');
                // Stop observing the element once it's visible
                observer.unobserve(entry.target);
            }
        });
    }, options);

    // Tell the observer to watch each of the hidden elements
    hiddenElements.forEach(element => {
        observer.observe(element);
    });
});