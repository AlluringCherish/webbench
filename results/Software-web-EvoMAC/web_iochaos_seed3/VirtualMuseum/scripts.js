/*
Client-side JavaScript for VirtualMuseum web application.
Handles button actions, filtering, and navigation enhancements.
*/
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Example: Add event listeners for buttons if needed for enhanced interactivity
    // Artifact Catalog: Enable Enter key to submit search form
    const searchInput = document.getElementById('search-artifact');
    if (searchInput) {
        searchInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                document.getElementById('apply-artifact-filter').click();
            }
        });
    }
    // Exhibitions: Enable Enter key to submit filter form
    const exhibitionFilter = document.getElementById('filter-exhibition-type');
    if (exhibitionFilter) {
        exhibitionFilter.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                document.getElementById('apply-exhibition-filter').click();
            }
        });
    }
    // Audio Guides: Enable Enter key to submit language filter form
    const languageFilter = document.getElementById('filter-language');
    if (languageFilter) {
        languageFilter.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                document.getElementById('apply-language-filter').click();
            }
        });
    }
    // Visitor Tickets: Validate number input to be positive integer
    const numberOfTicketsInput = document.getElementById('number-of-tickets');
    if (numberOfTicketsInput) {
        numberOfTicketsInput.addEventListener('input', function () {
            let val = this.value;
            if (val !== '') {
                val = parseInt(val);
                if (isNaN(val) || val < 1) {
                    this.value = 1;
                }
            }
        });
    }
    // Visitor Tickets: Auto-fill current date for visit-date input if empty
    const visitDateInput = document.getElementById('visit-date');
    if (visitDateInput && !visitDateInput.value) {
        const today = new Date().toISOString().split('T')[0];
        visitDateInput.value = today;
    }
    // Visitor Tickets: Auto-fill default visit time if empty
    const visitTimeInput = document.getElementById('visit-time');
    if (visitTimeInput && !visitTimeInput.value) {
        visitTimeInput.value = '10:00';
    }
});