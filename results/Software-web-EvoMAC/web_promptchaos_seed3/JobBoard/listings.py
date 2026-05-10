'''
Routes and handlers for the Job Listings page of the JobBoard web application.
Displays all available job postings with search and filter capabilities.
'''
from flask import Blueprint, render_template, request
from services.data_loader import load_jobs, load_companies, load_categories
from datetime import datetime
listings_bp = Blueprint('listings', __name__, url_prefix='/listings')
@listings_bp.route('/')
def job_listings():
    """
    Render the Job Listings page with all jobs, search and filter options.
    Supports filtering by job title, company, location, category, and location type (Remote, On-site, Hybrid).
    Displays job cards with title, company, location, and salary range.
    """
    jobs = load_jobs()
    companies = {c.company_id: c for c in load_companies()}
    categories = load_categories()
    # Get search and filter parameters from query string
    search_query = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', '').strip()
    location_filter = request.args.get('location', '').strip()
    filtered_jobs = []
    for job in jobs:
        # Get company name for filtering and display
        company = companies.get(job.company_id)
        company_name = company.company_name if company else ""
        # Filter by search query (title, company name, location)
        if search_query:
            if (search_query not in job.title.lower() and
                search_query not in company_name.lower() and
                search_query not in job.location.lower()):
                continue
        # Filter by category
        if category_filter and category_filter != 'All':
            if job.category != category_filter:
                continue
        # Filter by location type
        if location_filter and location_filter != 'All':
            loc_lower = job.location.lower()
            if location_filter == 'Remote':
                if loc_lower != 'remote':
                    continue
            elif location_filter == 'On-site':
                # On-site means location is not remote and not hybrid
                if loc_lower == 'remote' or 'hybrid' in loc_lower:
                    continue
            elif location_filter == 'Hybrid':
                if 'hybrid' not in loc_lower:
                    continue
        filtered_jobs.append({
            'job_id': job.job_id,
            'title': job.title,
            'company_name': company_name,
            'location': job.location,
            'salary_min': job.salary_min,
            'salary_max': job.salary_max,
        })
    # Sort jobs by posted_date descending
    try:
        filtered_jobs = sorted(
            filtered_jobs,
            key=lambda j: datetime.strptime(
                next(job.posted_date for job in jobs if str(job.job_id) == str(j['job_id'])),
                '%Y-%m-%d'),
            reverse=True)
    except Exception:
        # If date parsing fails, keep original order
        pass
    # Prepare categories list for dropdown including 'All'
    category_names = ['All'] + [cat.category_name for cat in categories]
    # Location filter options
    location_options = ['All', 'Remote', 'On-site', 'Hybrid']
    return render_template('listings.html',
                           page_title="Job Listings",
                           jobs=filtered_jobs,
                           categories=category_names,
                           selected_category=category_filter or 'All',
                           locations=location_options,
                           selected_location=location_filter or 'All',
                           search_query=search_query)