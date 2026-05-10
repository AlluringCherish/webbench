/*
JavaScript file for NewsPortal web application.
Handles UI behaviors such as button clicks and dynamic content updates.
Ensures static assets support the functionality and usability of all frontend pages.
*/
// Since most navigation buttons use inline onclick handlers, this script will focus on enhancing UI interactivity.
// Example: Confirm before removing a bookmark
document.addEventListener('DOMContentLoaded', function () {
    // Attach confirmation dialog to all remove bookmark buttons
    const removeButtons = document.querySelectorAll('button[id^="remove-bookmark-button-"]');
    removeButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            const confirmed = confirm('Are you sure you want to remove this bookmark?');
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
    // Optional: Enhance search input to submit form on Enter key press (already default behavior, but ensure)
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                searchInput.form.submit();
            }
        });
    }
    // Optional: Add smooth scrolling for back to dashboard buttons
    const backButtons = document.querySelectorAll('button[id="back-to-dashboard"]');
    backButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            window.location.href = button.getAttribute('onclick').match(/'(.*?)'/)[1];
        });
    });
    // Optional: Highlight selected category in article catalog dropdown (handled server-side, but can add client-side)
    // No additional JS needed as server renders selected option.
    // Optional: For comments page, auto-submit filter form on dropdown change (already done inline onchange)
    // No additional JS needed.
    // Optional: For trending page, auto-submit time period filter form on dropdown change (already done inline onchange)
    // No additional JS needed.
    // Optional: For write comment page, no extra JS needed as form validation is handled by HTML5 required attributes.
    // No other dynamic UI behaviors specified in requirements.
});