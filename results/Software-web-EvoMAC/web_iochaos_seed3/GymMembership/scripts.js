/*
JavaScript file for GymMembership web application.
Provides client-side interactivity such as filtering and navigation.
*/
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Membership Plans Page: Filter by membership type
    const planFilter = document.getElementById('plan-filter');
    if (planFilter) {
        planFilter.addEventListener('change', function () {
            const selected = this.value;
            // Redirect with filter query parameter
            if (selected === '') {
                window.location.href = '/membership_plans';
            } else {
                window.location.href = `/membership_plans?filter=${encodeURIComponent(selected)}`;
            }
        });
    }
    // Class Schedule Page: Search and filter
    const scheduleSearch = document.getElementById('schedule-search');
    const scheduleFilter = document.getElementById('schedule-filter');
    if (scheduleSearch && scheduleFilter) {
        function updateClassSchedule() {
            const searchVal = scheduleSearch.value.trim();
            const filterVal = scheduleFilter.value;
            let url = '/class_schedule?';
            if (searchVal) {
                url += `search=${encodeURIComponent(searchVal)}&`;
            }
            if (filterVal) {
                url += `filter=${encodeURIComponent(filterVal)}`;
            }
            window.location.href = url;
        }
        scheduleSearch.addEventListener('input', debounce(updateClassSchedule, 300));
        scheduleFilter.addEventListener('change', updateClassSchedule);
    }
    // Trainer Profiles Page: Search and filter
    const trainerSearch = document.getElementById('trainer-search');
    const specialtyFilter = document.getElementById('specialty-filter');
    if (trainerSearch && specialtyFilter) {
        function updateTrainerProfiles() {
            const searchVal = trainerSearch.value.trim();
            const filterVal = specialtyFilter.value;
            let url = '/trainer_profiles?';
            if (searchVal) {
                url += `search=${encodeURIComponent(searchVal)}&`;
            }
            if (filterVal) {
                url += `filter=${encodeURIComponent(filterVal)}`;
            }
            window.location.href = url;
        }
        trainerSearch.addEventListener('input', debounce(updateTrainerProfiles, 300));
        specialtyFilter.addEventListener('change', updateTrainerProfiles);
    }
    // Workout Records Page: Filter by workout type
    const filterByType = document.getElementById('filter-by-type');
    if (filterByType) {
        filterByType.addEventListener('change', function () {
            const selected = this.value;
            if (selected === '') {
                window.location.href = '/workout_records';
            } else {
                window.location.href = `/workout_records?filter=${encodeURIComponent(selected)}`;
            }
        });
    }
    // Utility: Debounce function to limit frequency of function calls
    function debounce(func, wait) {
        let timeout;
        return function () {
            const context = this, args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), wait);
        };
    }
});