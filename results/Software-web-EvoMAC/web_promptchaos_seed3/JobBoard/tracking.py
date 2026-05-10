'''
Routes and handlers for the Application Tracking page of the JobBoard web application.
Displays all submitted applications with status tracking and filtering.
'''
from flask import Blueprint, render_template, request, redirect, url_for, abort
from services.data_loader import load_applications, load_jobs, load_companies
tracking_bp = Blueprint('tracking', __name__, url_prefix='/applications')
@tracking_bp.route('/')
def application_tracking():
    """
    Render the Application Tracking page with all applications and status filter.
    """
    status_filter = request.args.get('status', 'All')
    applications = load_applications()
    jobs = {j.job_id: j for j in load_jobs()}
    companies = {c.company_id: c for c in load_companies()}
    filtered_apps = []
    for app in applications:
        if status_filter != 'All' and app.status != status_filter:
            continue
        job = jobs.get(app.job_id)
        if not job:
            continue
        company = companies.get(job.company_id)
        company_name = company.company_name if company else "Unknown Company"
        filtered_apps.append({
            'application_id': app.application_id,
            'job_title': job.title,
            'company_name': company_name,
            'status': app.status,
            'applied_date': app.applied_date,
        })
    status_options = ['All', 'Applied', 'Under Review', 'Interview', 'Rejected']
    return render_template('tracking.html',
                           page_title="My Applications",
                           applications=filtered_apps,
                           status_options=status_options,
                           selected_status=status_filter)
@tracking_bp.route('/<int:application_id>')
def view_application(application_id):
    """
    Render detailed view of a specific application.
    """
    applications = load_applications()
    application = next((a for a in applications if a.application_id == application_id), None)
    if not application:
        abort(404)
    jobs = {j.job_id: j for j in load_jobs()}
    companies = {c.company_id: c for c in load_companies()}
    job = jobs.get(application.job_id)
    company = companies.get(job.company_id) if job else None
    return render_template('application_detail.html',
                           page_title="Application Details",
                           application=application,
                           job=job,
                           company=company)
@tracking_bp.route('/back-to-dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard.dashboard'))