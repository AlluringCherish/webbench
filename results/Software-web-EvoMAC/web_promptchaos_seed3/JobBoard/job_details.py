'''
Routes and handlers for the Job Details page of the JobBoard web application.
Displays detailed information about a specific job posting.
'''
from flask import Blueprint, render_template, abort, redirect, url_for
from services.data_loader import load_jobs, load_companies
job_details_bp = Blueprint('job_details', __name__, url_prefix='/job')
@job_details_bp.route('/<int:job_id>')
def job_details(job_id):
    """
    Render the Job Details page for a specific job.
    """
    jobs = load_jobs()
    companies = {c.company_id: c for c in load_companies()}
    job = next((j for j in jobs if j.job_id == job_id), None)
    if not job:
        abort(404)
    company = companies.get(job.company_id)
    company_name = company.company_name if company else "Unknown Company"
    job_data = {
        'job_id': job.job_id,
        'title': job.title,
        'company_name': company_name,
        'description': job.description,
        'salary_min': job.salary_min,
        'salary_max': job.salary_max,
        'location': job.location,
    }
    return render_template('job_details.html',
                           page_title="Job Details",
                           job=job_data)
@job_details_bp.route('/<int:job_id>/apply')
def apply_now(job_id):
    """
    Redirect to the application form page with job_id as query parameter.
    """
    return redirect(url_for('application_form.application_form', job_id=job_id))