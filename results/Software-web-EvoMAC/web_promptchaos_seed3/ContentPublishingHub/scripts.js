/*
JavaScript for ContentPublishingHub
Provides client-side interactivity and dynamic behaviors
Supports all frontend pages as per specification
*/
// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function () {
    // Dashboard Page Interactions
    if (document.getElementById('dashboard-page')) {
        setupDashboard();
    }
    // Create Article Page Interactions
    if (document.getElementById('create-article-page')) {
        setupCreateArticle();
    }
    // Edit Article Page Interactions
    if (document.getElementById('edit-article-page')) {
        setupEditArticle();
    }
    // Version History Page Interactions
    if (document.getElementById('version-history-page')) {
        setupVersionHistory();
    }
    // My Articles Page Interactions
    if (document.getElementById('my-articles-page')) {
        setupMyArticles();
    }
    // Published Articles Page Interactions
    if (document.getElementById('published-articles-page')) {
        setupPublishedArticles();
    }
    // Content Calendar Page Interactions
    if (document.getElementById('calendar-page')) {
        setupContentCalendar();
    }
    // Article Analytics Page Interactions
    if (document.getElementById('analytics-page')) {
        setupArticleAnalytics();
    }
});
/* Dashboard Page */
function setupDashboard() {
    // Create Article button navigates to create article page
    const createBtn = document.getElementById('create-article-button');
    if (createBtn) {
        createBtn.addEventListener('click', function () {
            window.location.href = '/article/create';
        });
    }
}
/* Create Article Page */
function setupCreateArticle() {
    // Cancel button navigates back to dashboard
    const cancelBtn = document.getElementById('cancel-button');
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function (e) {
            e.preventDefault();
            if (confirm('Discard changes and return to Dashboard?')) {
                window.location.href = '/dashboard';
            }
        });
    }
}
/* Edit Article Page */
function setupEditArticle() {
    // Cancel button navigates back to dashboard
    const cancelBtn = document.getElementById('cancel-edit');
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function (e) {
            e.preventDefault();
            if (confirm('Discard changes and return to Dashboard?')) {
                window.location.href = '/dashboard';
            }
        });
    }
}
/* Version History Page */
function setupVersionHistory() {
    // Restore buttons: multiple restore buttons may exist with id pattern restore-version-<version_id>
    // Use event delegation for any restore buttons
    const versionsList = document.getElementById('versions-list');
    if (versionsList) {
        versionsList.addEventListener('click', function (e) {
            if (e.target && e.target.matches('button.restore-version-button')) {
                e.preventDefault();
                const versionId = e.target.getAttribute('data-version-id');
                if (!versionId) {
                    alert('Version ID not found.');
                    return;
                }
                if (confirm('Are you sure you want to restore this version? This will create a new version with this content.')) {
                    // Create a hidden form and submit POST to restore version
                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = window.location.pathname; // current URL
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'restore_version_id';
                    input.value = versionId;
                    form.appendChild(input);
                    document.body.appendChild(form);
                    form.submit();
                }
            }
        });
    }
    // Version comparison selector: if two versions are selected, reload page with query params
    const compareBtn = document.getElementById('compare-versions-button');
    if (compareBtn) {
        compareBtn.addEventListener('click', function (e) {
            e.preventDefault();
            const v1Select = document.getElementById('version-select-1');
            const v2Select = document.getElementById('version-select-2');
            if (!v1Select || !v2Select) {
                alert('Version selectors not found.');
                return;
            }
            const v1 = v1Select.value;
            const v2 = v2Select.value;
            if (!v1 || !v2) {
                alert('Please select two versions to compare.');
                return;
            }
            if (v1 === v2) {
                alert('Please select two different versions.');
                return;
            }
            // Reload page with query parameters
            const baseUrl = window.location.pathname;
            window.location.href = `${baseUrl}?v1=${encodeURIComponent(v1)}&v2=${encodeURIComponent(v2)}`;
        });
    }
}
/* My Articles Page */
function setupMyArticles() {
    // Filter by status dropdown triggers page reload with filter param
    const filterDropdown = document.getElementById('filter-article-status');
    if (filterDropdown) {
        filterDropdown.addEventListener('change', function () {
            const selected = filterDropdown.value;
            const url = new URL(window.location.href);
            if (selected) {
                url.searchParams.set('filter-article-status', selected);
            } else {
                url.searchParams.delete('filter-article-status');
            }
            window.location.href = url.toString();
        });
    }
    // Create New Article button navigates to create article page
    const createBtn = document.getElementById('create-new-article');
    if (createBtn) {
        createBtn.addEventListener('click', function () {
            window.location.href = '/article/create';
        });
    }
    // Back to Dashboard button
    const backBtn = document.getElementById('back-to-dashboard');
    if (backBtn) {
        backBtn.addEventListener('click', function () {
            window.location.href = '/dashboard';
        });
    }
}
/* Published Articles Page */
function setupPublishedArticles() {
    // Filter by category dropdown triggers page reload with filter param
    const filterCategory = document.getElementById('filter-published-category');
    if (filterCategory) {
        filterCategory.addEventListener('change', function () {
            const selected = filterCategory.value;
            const url = new URL(window.location.href);
            if (selected) {
                url.searchParams.set('filter-published-category', selected);
            } else {
                url.searchParams.delete('filter-published-category');
            }
            window.location.href = url.toString();
        });
    }
    // Sort by dropdown triggers page reload with sort param
    const sortDropdown = document.getElementById('sort-published');
    if (sortDropdown) {
        sortDropdown.addEventListener('change', function () {
            const selected = sortDropdown.value;
            const url = new URL(window.location.href);
            if (selected) {
                url.searchParams.set('sort-published', selected);
            } else {
                url.searchParams.delete('sort-published');
            }
            window.location.href = url.toString();
        });
    }
    // Back to Dashboard button
    const backBtn = document.getElementById('back-to-dashboard-published');
    if (backBtn) {
        backBtn.addEventListener('click', function () {
            window.location.href = '/dashboard';
        });
    }
}
/* Content Calendar Page */
function setupContentCalendar() {
    // Calendar view selector triggers page reload with calendar-view param
    const viewSelector = document.getElementById('calendar-view');
    if (viewSelector) {
        viewSelector.addEventListener('change', function () {
            const selected = viewSelector.value;
            const url = new URL(window.location.href);
            if (selected) {
                url.searchParams.set('calendar-view', selected);
            } else {
                url.searchParams.delete('calendar-view');
            }
            window.location.href = url.toString();
        });
    }
    // Schedule button - for now, alert placeholder (since scheduling UI not specified)
    const scheduleBtn = document.getElementById('schedule-button');
    if (scheduleBtn) {
        scheduleBtn.addEventListener('click', function () {
            alert('Schedule functionality is not implemented yet.');
        });
    }
    // Back to Dashboard button
    const backBtn = document.getElementById('back-to-dashboard-calendar');
    if (backBtn) {
        backBtn.addEventListener('click', function () {
            window.location.href = '/dashboard';
        });
    }
}
/* Article Analytics Page */
function setupArticleAnalytics() {
    // Back to Article button navigates back to edit article page
    const backBtn = document.getElementById('back-to-article-analytics');
    if (backBtn) {
        backBtn.addEventListener('click', function () {
            // Extract article_id from URL path: /article/<article_id>/analytics
            const pathParts = window.location.pathname.split('/');
            if (pathParts.length >= 3) {
                const articleId = pathParts[2];
                window.location.href = `/article/${articleId}/edit`;
            } else {
                window.location.href = '/dashboard';
            }
        });
    }
}