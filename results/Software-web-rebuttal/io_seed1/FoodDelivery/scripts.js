/*
JavaScript for FoodDelivery web application.
Handles client-side interactivity such as button actions and dynamic filtering.
Enhances user experience across all frontend pages.
*/
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Example: Add event listeners for buttons if needed
    // Currently, most buttons use inline onclick handlers for navigation
    // Implement dynamic filtering for restaurants page (optional enhancement)
    const searchInput = document.getElementById('search-input');
    const cuisineFilter = document.getElementById('cuisine-filter');
    const restaurantsGrid = document.getElementById('restaurants-grid');
    if (searchInput && cuisineFilter && restaurantsGrid) {
        // We rely on server-side filtering on form submit, so no dynamic filtering here
        // But we can add a listener to submit form on Enter key in search input
        searchInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.form.submit();
            }
        });
    }
    // Implement dynamic filtering for reviews page (optional enhancement)
    const filterByRating = document.getElementById('filter-by-rating');
    if (filterByRating) {
        filterByRating.addEventListener('change', function () {
            this.form.submit();
        });
    }
    // Implement dynamic filtering for active orders page (optional enhancement)
    const statusFilter = document.getElementById('status-filter');
    if (statusFilter) {
        statusFilter.addEventListener('change', function () {
            this.form.submit();
        });
    }
    // Additional client-side enhancements can be added here as needed
});