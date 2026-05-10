'''
Routes and handlers for the Search Results page of the JobBoard web application.
Displays search results for jobs and companies.
'''
from flask import Blueprint, render_template, request
from services.data_loader import load_jobs, load_companies
search_results_bp = Blueprint('search_results', __name__, url_prefix='/search')
@search_results_bp.route('/')
def search_results():
    """
    Render the Search Results page with results for jobs and companies.
    """
    query = request.args.get('q', '').strip().lower()
    tab = request.args.get('tab', 'jobs')  # 'jobs' or 'companies'
    jobs = load_jobs()
    companies = load_companies()
    job_results = []
    company_results = []
    if query:
        for job in jobs:
            if (query in job.title.lower() or
                query in job.location.lower()):
                job_results.append(job)
        for company in companies:
            if (query in company.company_name.lower() or
                query in company.industry.lower()):
                company_results.append(company)
    no_results = (len(job_results) == 0 and len(company_results) == 0)
    return render_template('search_results.html',
                           page_title="Search Results",
                           search_query=query,
                           tab=tab,
                           job_results=job_results,
                           company_results=company_results,
                           no_results=no_results)