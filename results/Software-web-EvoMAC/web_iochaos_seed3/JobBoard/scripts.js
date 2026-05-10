/*
JavaScript for client-side interactivity in the JobBoard web application.
Includes navigation button handlers and dynamic filtering for job listings and companies.
Also handles file upload UI interactions for resumes.
*/
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Navigation buttons on Dashboard page
    const browseJobsBtn = document.getElementById('browse-jobs-button');
    if (browseJobsBtn) {
        browseJobsBtn.addEventListener('click', function () {
            window.location.href = '/jobs';
        });
    }
    const myApplicationsBtn = document.getElementById('my-applications-button');
    if (myApplicationsBtn) {
        myApplicationsBtn.addEventListener('click', function () {
            window.location.href = '/applications';
        });
    }
    const companiesBtn = document.getElementById('companies-button');
    if (companiesBtn) {
        companiesBtn.addEventListener('click', function () {
            window.location.href = '/companies';
        });
    }
    // Back to dashboard buttons (common on multiple pages)
    const backToDashboardBtns = document.querySelectorAll('#back-to-dashboard');
    backToDashboardBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            window.location.href = '/';
        });
    });
    // Back to companies directory button on company profile page
    const backToCompaniesBtn = document.getElementById('back-to-companies');
    if (backToCompaniesBtn) {
        backToCompaniesBtn.addEventListener('click', function () {
            window.location.href = '/companies';
        });
    }
    // Job Listings Page: dynamic filtering and search
    const searchInput = document.getElementById('search-input');
    const categoryFilter = document.getElementById('category-filter');
    const locationFilter = document.getElementById('location-filter');
    if (searchInput || categoryFilter || locationFilter) {
        // Attach event listeners to trigger filtering on change or enter key
        if (searchInput) {
            searchInput.addEventListener('keydown', function (event) {
                if (event.key === 'Enter') {
                    event.preventDefault();
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
    // Companies Directory Page: search input dynamic filtering
    const searchCompanyInput = document.getElementById('search-company-input');
    if (searchCompanyInput) {
        searchCompanyInput.addEventListener('keydown', function (event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                applyCompanySearch();
            }
        });
    }
    // Resume Management Page: handle upload resume button and hidden file input
    const uploadResumeBtn = document.getElementById('upload-resume-button');
    const resumeFileInput = document.getElementById('resume-file-input');
    if (uploadResumeBtn && resumeFileInput) {
        uploadResumeBtn.addEventListener('click', function () {
            resumeFileInput.click();
        });
        resumeFileInput.addEventListener('change', function () {
            if (resumeFileInput.files.length > 0) {
                // Automatically submit the form containing the file input
                // Find the closest form ancestor
                let form = resumeFileInput.closest('form');
                if (form) {
                    form.submit();
                }
            }
        });
    }
    // Application Tracking Page: status filter change triggers filtering
    const statusFilter = document.getElementById('status-filter');
    if (statusFilter) {
        statusFilter.addEventListener('change', function () {
            // Reload page with selected status as query parameter
            const selectedStatus = statusFilter.value;
            const url = new URL(window.location.href);
            url.searchParams.set('status', selectedStatus);
            window.location.href = url.toString();
        });
    }
    // Search Results Page: tabs to switch between job results and company results
    const resultsTabs = document.getElementById('results-tabs');
    if (resultsTabs) {
        const jobResultsTab = document.getElementById('tab-job-results');
        const companyResultsTab = document.getElementById('tab-company-results');
        const jobResultsDiv = document.getElementById('job-results');
        const companyResultsDiv = document.getElementById('company-results');
        if (jobResultsTab && companyResultsTab && jobResultsDiv && companyResultsDiv) {
            jobResultsTab.addEventListener('click', function () {
                jobResultsDiv.style.display = 'block';
                companyResultsDiv.style.display = 'none';
                jobResultsTab.classList.add('active');
                companyResultsTab.classList.remove('active');
            });
            companyResultsTab.addEventListener('click', function () {
                jobResultsDiv.style.display = 'none';
                companyResultsDiv.style.display = 'block';
                jobResultsTab.classList.remove('active');
                companyResultsTab.classList.add('active');
            });
            // Initialize: show job results by default
            jobResultsTab.click();
        }
    }
});
// Function to apply filters on Job Listings page by reloading with query parameters
function applyJobFilters() {
    const searchInput = document.getElementById('search-input');
    const categoryFilter = document.getElementById('category-filter');
    const locationFilter = document.getElementById('location-filter');
    const search = searchInput ? searchInput.value.trim() : '';
    const category = categoryFilter ? categoryFilter.value : '';
    const location = locationFilter ? locationFilter.value : '';
    const url = new URL(window.location.href);
    if (search) {
        url.searchParams.set('search', search);
    } else {
        url.searchParams.delete('search');
    }
    if (category && category !== 'All') {
        url.searchParams.set('category', category);
    } else {
        url.searchParams.delete('category');
    }
    if (location && location !== 'All') {
        url.searchParams.set('location', location);
    } else {
        url.searchParams.delete('location');
    }
    window.location.href = url.toString();
}
// Function to apply search on Companies Directory page by reloading with query parameter
function applyCompanySearch() {
    const searchCompanyInput = document.getElementById('search-company-input');
    const query = searchCompanyInput ? searchCompanyInput.value.trim() : '';
    const url = new URL(window.location.href);
    if (query) {
        url.searchParams.set('search', query);
    } else {
        url.searchParams.delete('search');
    }
    window.location.href = url.toString();
}