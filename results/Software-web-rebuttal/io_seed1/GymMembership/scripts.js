/*
JavaScript file for GymMembership web application.
Handles client-side behaviors such as button actions, dynamic filtering, and navigation.
*/
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Example: Add event listeners for buttons if needed
    // Since most buttons use inline onclick with location.href, no extra JS needed for navigation
    // Dynamic filtering for membership plans page (optional enhancement)
    const planFilter = document.getElementById('plan-filter');
    if (planFilter) {
        planFilter.addEventListener('change', function () {
            this.form.submit();
        });
    }
    // Dynamic filtering for class schedule page
    const scheduleFilter = document.getElementById('schedule-filter');
    if (scheduleFilter) {
        scheduleFilter.addEventListener('change', function () {
            this.form.submit();
        });
    }
    // Dynamic filtering for trainer profiles page
    const specialtyFilter = document.getElementById('specialty-filter');
    if (specialtyFilter) {
        specialtyFilter.addEventListener('change', function () {
            this.form.submit();
        });
    }
    // Dynamic filtering for workout records page
    const workoutFilter = document.getElementById('filter-by-type');
    if (workoutFilter) {
        workoutFilter.addEventListener('change', function () {
            this.form.submit();
        });
    }
    // Search inputs with form submission on Enter key
    const scheduleSearch = document.getElementById('schedule-search');
    if (scheduleSearch) {
        scheduleSearch.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.form.submit();
            }
        });
    }
    const trainerSearch = document.getElementById('trainer-search');
    if (trainerSearch) {
        trainerSearch.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.form.submit();
            }
        });
    }
});