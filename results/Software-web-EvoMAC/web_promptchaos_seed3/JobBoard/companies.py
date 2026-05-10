'''
Routes and handlers for the Companies Directory page of the JobBoard web application.
Displays all registered companies with their profiles and available jobs.
'''
from flask import Blueprint, render_template, request, redirect, url_for, abort
from services.data_loader import load_companies, load_jobs
companies_bp = Blueprint('companies', __name__, url_prefix='/companies')
@companies_bp.route('/')
def companies_directory():
    """
    Render the Companies Directory page with search functionality.
    """
    search_query = request.args.get('search', '').strip().lower()
    companies = load_companies()
    filtered_companies = []
    for company in companies:
        if search_query:
            if (search_query not in company.company_name.lower() and
                search_query not in company.industry.lower()):
                continue
        filtered_companies.append(company)
    return render_template('companies.html',
                           page_title="Company Directory",
                           companies=filtered_companies,
                           search_query=search_query)
@companies_bp.route('/<int:company_id>')
def company_profile(company_id):
    """
    Render the Company Profile page with detailed info and open jobs.
    """
    companies = load_companies()
    company = next((c for c in companies if c.company_id == company_id), None)
    if not company:
        abort(404)
    jobs = load_jobs()
    company_jobs = [job for job in jobs if job.company_id == company_id]
    return render_template('company_profile.html',
                           page_title="Company Profile",
                           company=company,
                           jobs=company_jobs)
@companies_bp.route('/back-to-dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard.dashboard'))
@companies_bp.route('/back-to-companies')
def back_to_companies():
    return redirect(url_for('companies.companies_directory'))