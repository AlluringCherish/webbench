/*
    scripts.js
    Client-side interactivity and dynamic behaviors for JobBoard web application.
    Implements search/filter functionality, navigation buttons, and UI responsiveness.
*/
document.addEventListener('DOMContentLoaded', function () {
    // Search and filter on Job Listings Page
    const searchInput = document.getElementById('search-input');
    const categoryFilter = document.getElementById('category-filter');
    const locationFilter = document.getElementById('location-filter');
    if (searchInput || categoryFilter || locationFilter) {
        // Attach event listeners to trigger filtering on change or enter
        if (searchInput) {
            searchInput.addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    applyJobFilters();
                }
            });
        }
        if (categoryFilter) {
            categoryFilter.addEventListener('change', applyJobFilters);
        }
        if (locationFilter) {
            locationFilter.addEventListener('change', applyJobFilters);
        }
    }
    function applyJobFilters() {
        const search = searchInput ? searchInput.value.trim() : '';
        const category = categoryFilter ? categoryFilter.value : '';
        const location = locationFilter ? locationFilter.value : '';
        // Build URL with query parameters and redirect
        const params = new URLSearchParams();
        if (search) params.append('search', search);
        if (category) params.append('category', category);
        if (location) params.append('location', location);
        window.location.href = '/jobs?' + params.toString();
    }
    // Search on Companies Directory Page
    const searchCompanyInput = document.getElementById('search-company-input');
    if (searchCompanyInput) {
        searchCompanyInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                applyCompanySearch();
            }
        });
    }
    function applyCompanySearch() {
        const query = searchCompanyInput.value.trim();
        if (!query) {
            // If empty, reload companies directory without search
            window.location.href = '/companies';
            return;
        }
        const params = new URLSearchParams();
        params.append('search', query);
        window.location.href = '/companies?' + params.toString();
    }
    // Search Results Page Tabs
    const resultsTabs = document.getElementById('results-tabs');
    if (resultsTabs) {
        const jobResultsTab = document.getElementById('job-results');
        const companyResultsTab = document.getElementById('company-results');
        const buttons = resultsTabs.querySelectorAll('button');
        buttons.forEach(button => {
            button.addEventListener('click', function () {
                // Remove active class from all buttons
                buttons.forEach(btn => btn.classList.remove('active'));
                // Add active class to clicked button
                this.classList.add('active');
                // Show/hide results accordingly
                if (this.dataset.tab === 'jobs') {
                    jobResultsTab.classList.add('active');
                    companyResultsTab.classList.remove('active');
                } else if (this.dataset.tab === 'companies') {
                    companyResultsTab.classList.add('active');
                    jobResultsTab.classList.remove('active');
                }
            });
        });
        // Initialize first tab active
        if (buttons.length > 0) {
            buttons[0].click();
        }
    }
    // Navigation buttons on Dashboard Page
    const browseJobsBtn = document.getElementById('browse-jobs-button');
    const myApplicationsBtn = document.getElementById('my-applications-button');
    const companiesBtn = document.getElementById('companies-button');
    if (browseJobsBtn) {
        browseJobsBtn.addEventListener('click', () => {
            window.location.href = '/jobs';
        });
    }
    if (myApplicationsBtn) {
        myApplicationsBtn.addEventListener('click', () => {
            window.location.href = '/applications';
        });
    }
    if (companiesBtn) {
        companiesBtn.addEventListener('click', () => {
            window.location.href = '/companies';
        });
    }
    // Back buttons with id 'back-to-dashboard' or 'back-to-companies'
    const backToDashboardButtons = document.querySelectorAll('#back-to-dashboard');
    backToDashboardButtons.forEach(button => {
        button.addEventListener('click', () => {
            window.location.href = '/';
        });
    });
    const backToCompaniesButtons = document.querySelectorAll('#back-to-companies');
    backToCompaniesButtons.forEach(button => {
        button.addEventListener('click', () => {
            window.location.href = '/companies';
        });
    });
    // Upload Resume Button triggers hidden file input
    const uploadResumeButton = document.getElementById('upload-resume-button');
    const resumeFileInput = document.getElementById('resume-file-input');
    if (uploadResumeButton && resumeFileInput) {
        uploadResumeButton.addEventListener('click', () => {
            resumeFileInput.click();
        });
    }
    // Optional: Show selected file name for resume upload (if needed)
    if (resumeFileInput) {
        resumeFileInput.addEventListener('change', () => {
            const fileNameDisplay = document.getElementById('resume-file-name');
            if (fileNameDisplay) {
                const fileName = resumeFileInput.files.length > 0 ? resumeFileInput.files[0].name : '';
                fileNameDisplay.textContent = fileName;
            }
        });
    }
});