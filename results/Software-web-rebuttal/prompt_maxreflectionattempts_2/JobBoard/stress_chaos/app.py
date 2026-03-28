from flask import Flask, render_template, redirect, url_for, request, abort
from werkzeug.utils import secure_filename
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
DATA_DIR = 'data'
JOBS_FILE = os.path.join(DATA_DIR, 'jobs.txt')
COMPANIES_FILE = os.path.join(DATA_DIR, 'companies.txt')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.txt')
APPLICATIONS_FILE = os.path.join(DATA_DIR, 'applications.txt')
RESUMES_FILE = os.path.join(DATA_DIR, 'resumes.txt')

# Utility functions to load and save data

def load_jobs():
    jobs = []
    try:
        with open(JOBS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 9:
                    continue
                job = {
                    'job_id': int(parts[0]),
                    'title': parts[1],
                    'company_id': int(parts[2]),
                    'location': parts[3],
                    'salary_min': int(parts[4]),
                    'salary_max': int(parts[5]),
                    'category': parts[6],
                    'description': parts[7],
                    'posted_date': parts[8]
                }
                jobs.append(job)
    except FileNotFoundError:
        pass
    return jobs


def save_jobs(jobs):
    with open(JOBS_FILE, 'w', encoding='utf-8') as f:
        for job in jobs:
            line = '|'.join([
                str(job['job_id']),
                job['title'],
                str(job['company_id']),
                job['location'],
                str(job['salary_min']),
                str(job['salary_max']),
                job['category'],
                job['description'],
                job['posted_date']
            ])
            f.write(line + '\n')


def load_companies():
    companies = []
    try:
        with open(COMPANIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 6:
                    continue
                company = {
                    'company_id': int(parts[0]),
                    'company_name': parts[1],
                    'industry': parts[2],
                    'location': parts[3],
                    'employee_count': int(parts[4]),
                    'description': parts[5]
                }
                companies.append(company)
    except FileNotFoundError:
        pass
    return companies


def save_companies(companies):
    with open(COMPANIES_FILE, 'w', encoding='utf-8') as f:
        for c in companies:
            line = '|'.join([
                str(c['company_id']),
                c['company_name'],
                c['industry'],
                c['location'],
                str(c['employee_count']),
                c['description']
            ])
            f.write(line + '\n')


def load_categories():
    categories = []
    try:
        with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 3:
                    continue
                category = {
                    'category_id': int(parts[0]),
                    'category_name': parts[1],
                    'description': parts[2]
                }
                categories.append(category)
    except FileNotFoundError:
        pass
    return categories


def save_categories(categories):
    with open(CATEGORIES_FILE, 'w', encoding='utf-8') as f:
        for c in categories:
            line = '|'.join([
                str(c['category_id']),
                c['category_name'],
                c['description']
            ])
            f.write(line + '\n')


def load_applications():
    applications = []
    try:
        with open(APPLICATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                application = {
                    'application_id': int(parts[0]),
                    'job_id': int(parts[1]),
                    'applicant_name': parts[2],
                    'applicant_email': parts[3],
                    'status': parts[4],
                    'applied_date': parts[5],
                    'resume_id': int(parts[6])
                }
                applications.append(application)
    except FileNotFoundError:
        pass
    return applications


def save_applications(applications):
    with open(APPLICATIONS_FILE, 'w', encoding='utf-8') as f:
        for a in applications:
            line = '|'.join([
                str(a['application_id']),
                str(a['job_id']),
                a['applicant_name'],
                a['applicant_email'],
                a['status'],
                a['applied_date'],
                str(a['resume_id'])
            ])
            f.write(line + '\n')


def load_resumes():
    resumes = []
    try:
        with open(RESUMES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 6:
                    continue
                resume = {
                    'resume_id': int(parts[0]),
                    'applicant_name': parts[1],
                    'applicant_email': parts[2],
                    'filename': parts[3],
                    'upload_date': parts[4],
                    'summary': parts[5]
                }
                resumes.append(resume)
    except FileNotFoundError:
        pass
    return resumes


def save_resumes(resumes):
    with open(RESUMES_FILE, 'w', encoding='utf-8') as f:
        for r in resumes:
            line = '|'.join([
                str(r['resume_id']),
                r['applicant_name'],
                r['applicant_email'],
                r['filename'],
                r['upload_date'],
                r['summary']
            ])
            f.write(line + '\n')

# Helper functions

def get_company_by_id(company_id):
    companies = load_companies()
    for c in companies:
        if c['company_id'] == company_id:
            return c
    return None


def get_job_by_id(job_id):
    jobs = load_jobs()
    for j in jobs:
        if j['job_id'] == job_id:
            return j
    return None


def get_resume_by_id(resume_id):
    resumes = load_resumes()
    for r in resumes:
        if r['resume_id'] == resume_id:
            return r
    return None


def get_application_by_id(application_id):
    applications = load_applications()
    for a in applications:
        if a['application_id'] == application_id:
            return a
    return None


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    jobs = load_jobs()
    companies = load_companies()
    # Build featured_jobs list of dict with required keys
    featured_jobs = []
    # Limit featured jobs to 5 most recent posted_date - sorted descending
    # posted_date is string, sort by datetime for accuracy
    jobs_sorted = sorted(jobs, key=lambda x: datetime.datetime.strptime(x['posted_date'], '%Y-%m-%d'), reverse=True)
    for job in jobs_sorted[:5]:
        company = get_company_by_id(job['company_id'])
        if not company:
            continue
        featured_jobs.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company['company_name'],
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
        })
    return render_template('dashboard.html', featured_jobs=featured_jobs)


@app.route('/jobs')
def job_listings():
    jobs = load_jobs()
    companies = load_companies()
    categories_list = load_categories()
    categories = [c['category_name'] for c in categories_list]

    # Get filter query parameters
    selected_category = request.args.get('category', None)
    if selected_category == '':
        selected_category = None
    selected_location = request.args.get('location', None)
    if selected_location == '':
        selected_location = None

    # Compile unique locations from jobs
    locations = sorted(list(set(j['location'] for j in jobs)))

    # Filter jobs
    filtered_jobs = []
    for job in jobs:
        if selected_category and job['category'] != selected_category:
            continue
        if selected_location and job['location'] != selected_location:
            continue
        company = get_company_by_id(job['company_id'])
        company_name = company['company_name'] if company else 'Unknown'
        filtered_jobs.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_name,
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
            'category': job['category'],
        })

    return render_template('job_listings.html', jobs=filtered_jobs, categories=categories, locations=locations, selected_category=selected_category, selected_location=selected_location)


@app.route('/job/<int:job_id>')
def job_details(job_id):
    job = get_job_by_id(job_id)
    if not job:
        abort(404)
    company = get_company_by_id(job['company_id'])
    company_name = company['company_name'] if company else 'Unknown'
    job_dict = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': company_name,
        'description': job['description'],
        'location': job['location'],
        'salary_min': job['salary_min'],
        'salary_max': job['salary_max']
    }
    return render_template('job_details.html', job=job_dict)


@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    job = get_job_by_id(job_id)
    if not job:
        abort(404)
    company = get_company_by_id(job['company_id'])
    company_name = company['company_name'] if company else 'Unknown'

    if request.method == 'GET':
        job_info = {
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_name
        }
        return render_template('application_form.html', job=job_info)

    # POST handling
    applicant_name = request.form.get('applicant_name')
    applicant_email = request.form.get('applicant_email')
    cover_letter = request.form.get('cover_letter', '')
    resume_file = request.files.get('resume_file')

    # Validate essential fields
    if not applicant_name or not applicant_email or not resume_file:
        # Could add flash message or error display; here just rerender the form with error message
        job_info = {
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_name
        }
        return render_template('application_form.html', job=job_info)

    # Save resume file (simulate saving only filename; no actual file storage required by spec)
    filename = secure_filename(resume_file.filename)
    # We are not saving files physically as no instruction provided

    # Create new resume entry
    resumes = load_resumes()
    existing_ids = [r['resume_id'] for r in resumes]
    new_resume_id = max(existing_ids, default=0) + 1

    upload_date = datetime.datetime.now().strftime('%Y-%m-%d')
    new_resume = {
        'resume_id': new_resume_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'filename': filename,
        'upload_date': upload_date,
        'summary': ''
    }
    resumes.append(new_resume)
    save_resumes(resumes)

    # Create new application entry
    applications = load_applications()
    existing_app_ids = [a['application_id'] for a in applications]
    new_application_id = max(existing_app_ids, default=0) + 1

    applied_date = upload_date
    new_application = {
        'application_id': new_application_id,
        'job_id': job['job_id'],
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'status': 'Applied',
        'applied_date': applied_date,
        'resume_id': new_resume_id
    }
    applications.append(new_application)
    save_applications(applications)

    # After submission, redirect to application tracking page
    return redirect(url_for('application_tracking'))


@app.route('/applications')
def application_tracking():
    # status filter query param
    selected_status = request.args.get('status', None)
    if selected_status == '':
        selected_status = None

    status_options = ["All", "Applied", "Under Review", "Interview", "Rejected"]

    applications = load_applications()
    jobs = load_jobs()
    companies = load_companies()

    filtered_applications = []
    for app in applications:
        if selected_status and selected_status != "All" and app['status'] != selected_status:
            continue
        job = get_job_by_id(app['job_id'])
        if not job:
            continue
        company = get_company_by_id(job['company_id'])
        company_name = company['company_name'] if company else 'Unknown'
        filtered_applications.append({
            'application_id': app['application_id'],
            'job_title': job['title'],
            'company_name': company_name,
            'status': app['status'],
            'applied_date': app['applied_date']
        })

    return render_template('application_tracking.html', applications=filtered_applications, status_options=status_options, selected_status=selected_status)


@app.route('/application/<int:application_id>')
def application_details(application_id):
    application = get_application_by_id(application_id)
    if not application:
        abort(404)

    job = get_job_by_id(application['job_id'])
    company = get_company_by_id(job['company_id']) if job else None

    resume = get_resume_by_id(application['resume_id'])

    application_dict = {
        'application_id': application['application_id'],
        'job_title': job['title'] if job else 'Unknown',
        'company_name': company['company_name'] if company else 'Unknown',
        'applicant_name': application['applicant_name'],
        'applicant_email': application['applicant_email'],
        'status': application['status'],
        'applied_date': application['applied_date'],
        'resume_filename': resume['filename'] if resume else '',
        'cover_letter': ''  # Not stored with application; spec only asks for cover letter in form - so empty
    }

    return render_template('application_details.html', application=application_dict)


@app.route('/companies')
def companies_directory():
    companies = load_companies()
    search_query = request.args.get('search', None)
    if search_query == '':
        search_query = None

    filtered_companies = []
    if search_query:
        search_lower = search_query.lower()
        for c in companies:
            if search_lower in c['company_name'].lower():
                filtered_companies.append(c)
    else:
        filtered_companies = companies

    # Provide only required fields per spec
    companies_data = []
    for c in filtered_companies:
        companies_data.append({
            'company_id': c['company_id'],
            'company_name': c['company_name'],
            'industry': c['industry'],
            'employee_count': c['employee_count']
        })

    return render_template('companies.html', companies=companies_data, search_query=search_query)


@app.route('/company/<int:company_id>')
def company_profile(company_id):
    company = get_company_by_id(company_id)
    if not company:
        abort(404)

    jobs = load_jobs()
    company_jobs = []
    for job in jobs:
        if job['company_id'] == company_id:
            company_jobs.append({
                'job_id': job['job_id'],
                'title': job['title'],
                'status': 'Open'  # as specified, typically 'Open'
            })

    company_dict = {
        'company_id': company['company_id'],
        'company_name': company['company_name'],
        'industry': company['industry'],
        'location': company['location'],
        'description': company['description'],
        'employee_count': company['employee_count']
    }

    return render_template('company_profile.html', company=company_dict, jobs=company_jobs)


@app.route('/resumes')
def resume_management():
    resumes = load_resumes()
    return render_template('resume_management.html', resumes=resumes)


@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    applicant_name = request.form.get('applicant_name')
    applicant_email = request.form.get('applicant_email')
    summary = request.form.get('summary', '')
    resume_file = request.files.get('resume_file')

    if not applicant_name or not applicant_email or not resume_file:
        # Redirect back to resume_management if invalid
        return redirect(url_for('resume_management'))

    filename = secure_filename(resume_file.filename)
    # File storage is not specified - omit actual saving

    resumes = load_resumes()
    existing_ids = [r['resume_id'] for r in resumes]
    new_resume_id = max(existing_ids, default=0) + 1

    upload_date = datetime.datetime.now().strftime('%Y-%m-%d')
    new_resume = {
        'resume_id': new_resume_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'filename': filename,
        'upload_date': upload_date,
        'summary': summary
    }
    resumes.append(new_resume)
    save_resumes(resumes)

    return redirect(url_for('resume_management'))


@app.route('/delete_resume/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = load_resumes()
    resumes = [r for r in resumes if r['resume_id'] != resume_id]
    save_resumes(resumes)
    return redirect(url_for('resume_management'))


@app.route('/search')
def search_results():
    query = request.args.get('q', '')
    query_lower = query.lower()

    jobs = load_jobs()
    companies = load_companies()

    job_results = []
    company_results = []

    if query:
        for job in jobs:
            if (query_lower in job['title'].lower()) or (query_lower in job['category'].lower()):
                company = get_company_by_id(job['company_id'])
                company_name = company['company_name'] if company else 'Unknown'
                job_results.append({
                    'job_id': job['job_id'],
                    'title': job['title'],
                    'company_name': company_name,
                    'location': job['location'],
                    'salary_min': job['salary_min'],
                    'salary_max': job['salary_max']
                })

        for c in companies:
            if query_lower in c['company_name'].lower() or query_lower in c['industry'].lower() or query_lower in c['location'].lower():
                company_results.append({
                    'company_id': c['company_id'],
                    'company_name': c['company_name'],
                    'industry': c['industry'],
                    'location': c['location']
                })

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)


if __name__ == '__main__':
    app.run(debug=True)
