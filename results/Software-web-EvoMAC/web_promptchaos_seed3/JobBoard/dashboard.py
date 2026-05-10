'''
Routes and handlers for the Dashboard page of the JobBoard web application.
Displays featured jobs, latest opportunities, and navigation buttons to other pages.
'''
from flask import Blueprint, render_template, url_for, redirect
from services.data_loader import load_jobs, load_companies
from datetime import datetime
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='')
@dashboard_bp.route('/')
def dashboard():
    """
    Render the Dashboard page with featured jobs and navigation buttons.
    Featured jobs are the latest 3 jobs sorted by posted_date descending.
    """
    jobs = load_jobs()
    companies = {c.company_id: c for c in load_companies()}
    # Sort jobs by posted_date descending
    try:
        jobs_sorted = sorted(jobs, key=lambda j: datetime.strptime(j.posted_date, '%Y-%m-%d'), reverse=True)
    except Exception:
        # fallback if date parsing fails
        jobs_sorted = jobs
    featured_jobs = jobs_sorted[:3]  # top 3 latest jobs
    # Prepare featured jobs data with company names
    featured_jobs_data = []
    for job in featured_jobs:
        company = companies.get(job.company_id)
        company_name = company.company_name if company else "Unknown Company"
        featured_jobs_data.append({
            'job_id': job.job_id,
            'title': job.title,
            'company_name': company_name,
            'location': job.location,
            'salary_min': job.salary_min,
            'salary_max': job.salary_max,
        })
    return render_template('dashboard.html',
                           page_title="Job Board Dashboard",
                           featured_jobs=featured_jobs_data)
@dashboard_bp.route('/browse-jobs')
def browse_jobs():
    return redirect(url_for('listings.job_listings'))
@dashboard_bp.route('/my-applications')
def my_applications():
    return redirect(url_for('tracking.application_tracking'))
@dashboard_bp.route('/companies')
def companies():
    return redirect(url_for('companies.companies_directory'))