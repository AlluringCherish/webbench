from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Data file read/write functions

def read_jobs():
    path = os.path.join(DATA_DIR, 'jobs.txt')
    jobs = []
    if not os.path.isfile(path):
        return jobs
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)<9:
                continue
            try:
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
            except:
                continue
    return jobs

def save_jobs(jobs):
    path = os.path.join(DATA_DIR, 'jobs.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for j in jobs:
            line = f"{j['job_id']}|{j['title']}|{j['company_id']}|{j['location']}|{j['salary_min']}|{j['salary_max']}|{j['category']}|{j['description']}|{j['posted_date']}"
            f.write(line + '\n')

def read_companies():
    path = os.path.join(DATA_DIR, 'companies.txt')
    companies = []
    if not os.path.isfile(path):
        return companies
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)<6:
                continue
            try:
                company = {
                    'company_id': int(parts[0]),
                    'company_name': parts[1],
                    'industry': parts[2],
                    'location': parts[3],
                    'employee_count': int(parts[4]),
                    'description': parts[5]
                }
                companies.append(company)
            except:
                continue
    return companies

def save_companies(companies):
    path = os.path.join(DATA_DIR, 'companies.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for c in companies:
            line = f"{c['company_id']}|{c['company_name']}|{c['industry']}|{c['location']}|{c['employee_count']}|{c['description']}"
            f.write(line + '\n')

def read_categories():
    path = os.path.join(DATA_DIR, 'categories.txt')
    categories = []
    if not os.path.isfile(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)<3:
                continue
            try:
                category = {
                    'category_id': int(parts[0]),
                    'category_name': parts[1],
                    'description': parts[2]
                }
                categories.append(category)
            except:
                continue
    return categories

def save_categories(categories):
    path = os.path.join(DATA_DIR, 'categories.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for c in categories:
            line = f"{c['category_id']}|{c['category_name']}|{c['description']}"
            f.write(line + '\n')

def read_applications():
    path = os.path.join(DATA_DIR, 'applications.txt')
    apps = []
    if not os.path.isfile(path):
        return apps
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)<7:
                continue
            try:
                app = {
                    'application_id': int(parts[0]),
                    'job_id': int(parts[1]),
                    'applicant_name': parts[2],
                    'applicant_email': parts[3],
                    'status': parts[4],
                    'applied_date': parts[5],
                    'resume_id': int(parts[6])
                }
                apps.append(app)
            except:
                continue
    return apps

def save_applications(applications):
    path = os.path.join(DATA_DIR, 'applications.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for a in applications:
            line = f"{a['application_id']}|{a['job_id']}|{a['applicant_name']}|{a['applicant_email']}|{a['status']}|{a['applied_date']}|{a['resume_id']}"
            f.write(line + '\n')

def read_resumes():
    path = os.path.join(DATA_DIR, 'resumes.txt')
    resumes = []
    if not os.path.isfile(path):
        return resumes
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)<6:
                continue
            try:
                resume = {
                    'resume_id': int(parts[0]),
                    'applicant_name': parts[1],
                    'applicant_email': parts[2],
                    'filename': parts[3],
                    'upload_date': parts[4],
                    'summary': parts[5]
                }
                resumes.append(resume)
            except:
                continue
    return resumes

def save_resumes(resumes):
    path = os.path.join(DATA_DIR, 'resumes.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in resumes:
            line = f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}"
            f.write(line + '\n')

# Helpers

def get_next_id(items, id_field):
    if not items:
        return 1
    try:
        return max(item[id_field] for item in items) + 1
    except:
        return 1

def get_job_by_id(job_id):
    for job in read_jobs():
        if job['job_id'] == job_id:
            return job
    return None

def get_company_by_id(company_id):
    for comp in read_companies():
        if comp['company_id'] == company_id:
            return comp
    return None

def get_application_by_id(application_id):
    for app in read_applications():
        if app['application_id'] == application_id:
            return app
    return None

def get_resume_by_id(resume_id):
    for r in read_resumes():
        if r['resume_id'] == resume_id:
            return r
    return None

def get_category_names():
    return [c['category_name'] for c in read_categories()]

def get_job_locations():
    locs = set()
    for job in read_jobs():
        locs.add(job['location'])
    return sorted(locs)

# Routes

@app.route('/')
def root_redirect_dashboard():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    jobs = read_jobs()
    jobs_sorted = sorted(jobs, key=lambda j: j['posted_date'], reverse=True)
    featured_jobs = []
    count = 0
    for job in jobs_sorted:
        if count >= 5:
            break
        company = get_company_by_id(job['company_id'])
        if not company:
            continue
        featured_jobs.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company['company_name'],
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max']
        })
        count += 1
    latest_jobs = featured_jobs.copy()
    categories = [{'category_id': c['category_id'], 'category_name': c['category_name']} for c in read_categories()]
    return render_template('dashboard.html', featured_jobs=featured_jobs, latest_jobs=latest_jobs, categories=categories)

@app.route('/jobs', methods=['GET', 'POST'])
def job_listings_page():
    jobs = read_jobs()
    categories = get_category_names()
    locations = get_job_locations()
    selected_category = None
    selected_location = None
    search_query = None
    if request.method == 'POST':
        search_query = request.form.get('search_input')
        if search_query:
            search_query = search_query.strip() or None
        selected_category = request.form.get('category_filter')
        if selected_category:
            selected_category = selected_category.strip() or None
        selected_location = request.form.get('location_filter')
        if selected_location:
            selected_location = selected_location.strip() or None
    filtered_jobs = []
    for job in jobs:
        if selected_category and job['category'] != selected_category:
            continue
        if selected_location and job['location'] != selected_location:
            continue
        company = get_company_by_id(job['company_id'])
        if not company:
            continue
        if search_query:
            sq = search_query.lower()
            if not (sq in job['title'].lower() or sq in company['company_name'].lower() or sq in job['location'].lower()):
                continue
        filtered_jobs.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company['company_name'],
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max']
        })
    return render_template('jobs.html', jobs=filtered_jobs, categories=categories, locations=locations, selected_category=selected_category, selected_location=selected_location, search_query=search_query)

@app.route('/jobs', methods=['POST'])
def job_listings_page_search():
    # Per spec, POST only route calls job_listings_page with POST form data
    return job_listings_page()

@app.route('/job/<int:job_id>')
def job_details_page(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return "Job not found", 404
    company = get_company_by_id(job['company_id'])
    company_name = company['company_name'] if company else 'Unknown'
    job_out = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': company_name,
        'location': job['location'],
        'salary_min': job['salary_min'],
        'salary_max': job['salary_max'],
        'category': job['category'],
        'description': job['description'],
        'posted_date': job['posted_date']
    }
    return render_template('job_details.html', job=job_out)

@app.route('/job/<int:job_id>/apply', methods=['GET'])
def application_form_page(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return "Job not found", 404
    company = get_company_by_id(job['company_id'])
    company_name = company['company_name'] if company else 'Unknown'
    job_out = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': company_name
    }
    return render_template('application_form.html', job=job_out)

@app.route('/job/<int:job_id>/apply', methods=['POST'])
def submit_application(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return "Job not found", 404
    company = get_company_by_id(job['company_id'])
    company_name = company['company_name'] if company else 'Unknown'
    job_out = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': company_name
    }

    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_email = request.form.get('applicant_email', '').strip()
    cover_letter = request.form.get('cover_letter', '').strip()
    resume_file = request.files.get('resume_upload')

    form_errors = {}

    if not applicant_name:
        form_errors['applicant_name'] = 'Applicant name is required.'
    if not applicant_email:
        form_errors['applicant_email'] = 'Applicant email is required.'
    elif '@' not in applicant_email or '.' not in applicant_email:
        form_errors['applicant_email'] = 'Invalid email address.'
    if not cover_letter:
        form_errors['cover_letter'] = 'Cover letter is required.'
    if not resume_file or resume_file.filename == '':
        form_errors['resume_upload'] = 'Resume file is required.'

    if form_errors:
        return render_template('application_form.html', job=job_out, form_errors=form_errors)

    resumes = read_resumes()
    new_resume_id = get_next_id(resumes, 'resume_id')

    resumes_dir = os.path.join(DATA_DIR, 'resumes')
    os.makedirs(resumes_dir, exist_ok=True)

    orig_filename = os.path.basename(resume_file.filename)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    saved_filename = f"{new_resume_id}_{timestamp}_{orig_filename}"
    save_path = os.path.join(resumes_dir, saved_filename)
    resume_file.save(save_path)

    upload_date = datetime.utcnow().strftime('%Y-%m-%d')

    new_resume = {
        'resume_id': new_resume_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'filename': saved_filename,
        'upload_date': upload_date,
        'summary': ''
    }
    resumes.append(new_resume)
    save_resumes(resumes)

    applications = read_applications()
    new_app_id = get_next_id(applications, 'application_id')
    new_application = {
        'application_id': new_app_id,
        'job_id': job['job_id'],
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'status': 'Applied',
        'applied_date': upload_date,
        'resume_id': new_resume_id
    }
    applications.append(new_application)
    save_applications(applications)

    return redirect(url_for('application_tracking_page'))

@app.route('/applications')
def application_tracking_page():
    applications = read_applications()
    status_filter = request.args.get('status_filter')
    if status_filter and status_filter.strip() == '':
        status_filter = None

    apps_out = []
    jobs = read_jobs()
    for app in applications:
        if status_filter and app['status'] != status_filter:
            continue
        job = None
        for j in jobs:
            if j['job_id'] == app['job_id']:
                job = j
                break
        if not job:
            continue
        company = get_company_by_id(job['company_id'])
        company_name = company['company_name'] if company else 'Unknown'
        apps_out.append({
            'application_id': app['application_id'],
            'job_title': job['title'],
            'company_name': company_name,
            'status': app['status'],
            'applied_date': app['applied_date']
        })
    return render_template('applications_tracking.html', applications=apps_out, status_filter=status_filter)

@app.route('/application/<int:application_id>')
def application_detail_page(application_id):
    application = get_application_by_id(application_id)
    if not application:
        return "Application not found", 404
    job = get_job_by_id(application['job_id'])
    if not job:
        return "Job not found", 404
    company = get_company_by_id(job['company_id'])
    company_name = company['company_name'] if company else 'Unknown'
    resume = get_resume_by_id(application['resume_id'])
    resume_filename = resume['filename'] if resume else ''
    app_out = {
        'application_id': application['application_id'],
        'job_title': job['title'],
        'company_name': company_name,
        'applicant_name': application['applicant_name'],
        'applicant_email': application['applicant_email'],
        'status': application['status'],
        'applied_date': application['applied_date'],
        'resume_filename': resume_filename,
        'cover_letter': ''  # cover letter not stored
    }
    return render_template('application_detail.html', application=app_out)

@app.route('/companies')
def companies_directory_page():
    companies = read_companies()
    search_query = request.args.get('search_query')
    if search_query:
        search_query = search_query.strip() or None
    if search_query:
        sq = search_query.lower()
        filtered = [c for c in companies if sq in c['company_name'].lower()]
    else:
        filtered = companies
    out = []
    for c in filtered:
        out.append({
            'company_id': c['company_id'],
            'company_name': c['company_name'],
            'industry': c['industry'],
            'employee_count': c['employee_count']
        })
    return render_template('companies.html', companies=out, search_query=search_query)

@app.route('/company/<int:company_id>')
def company_profile_page(company_id):
    company = get_company_by_id(company_id)
    if not company:
        return "Company not found", 404
    jobs = read_jobs()
    company_jobs = []
    for job in jobs:
        if job['company_id'] == company_id:
            company_jobs.append({
                'job_id': job['job_id'],
                'title': job['title'],
                'status': 'Open'
            })
    company_out = {
        'company_id': company['company_id'],
        'company_name': company['company_name'],
        'industry': company['industry'],
        'location': company['location'],
        'employee_count': company['employee_count'],
        'description': company['description']
    }
    return render_template('company_profile.html', company=company_out, jobs=company_jobs)

@app.route('/resumes')
def resume_management_page():
    resumes = read_resumes()
    out = []
    for r in resumes:
        out.append({
            'resume_id': r['resume_id'],
            'filename': r['filename'],
            'upload_date': r['upload_date'],
            'summary': r['summary']
        })
    return render_template('resumes.html', resumes=out)

@app.route('/resumes/upload', methods=['POST'])
def upload_resume():
    resume_file = request.files.get('resume_file')
    summary = request.form.get('summary')
    if summary:
        summary = summary.strip()
    form_errors = {}
    if not resume_file or resume_file.filename == '':
        form_errors['resume_file'] = 'Resume file is required.'
    if form_errors:
        resumes = read_resumes()
        out = []
        for r in resumes:
            out.append({
                'resume_id': r['resume_id'],
                'filename': r['filename'],
                'upload_date': r['upload_date'],
                'summary': r['summary']
            })
        return render_template('resumes.html', resumes=out, form_errors=form_errors)
    resumes = read_resumes()
    new_resume_id = get_next_id(resumes, 'resume_id')
    resumes_dir = os.path.join(DATA_DIR, 'resumes')
    os.makedirs(resumes_dir, exist_ok=True)
    orig_filename = os.path.basename(resume_file.filename)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    saved_filename = f"{new_resume_id}_{timestamp}_{orig_filename}"
    save_path = os.path.join(resumes_dir, saved_filename)
    resume_file.save(save_path)
    upload_date = datetime.utcnow().strftime('%Y-%m-%d')
    new_resume = {
        'resume_id': new_resume_id,
        'applicant_name': '',
        'applicant_email': '',
        'filename': saved_filename,
        'upload_date': upload_date,
        'summary': summary or ''
    }
    resumes.append(new_resume)
    save_resumes(resumes)
    return redirect(url_for('resume_management_page'))

@app.route('/resume/<int:resume_id>/delete', methods=['POST'])
def delete_resume(resume_id):
    resumes = read_resumes()
    resume_to_delete = None
    for r in resumes:
        if r['resume_id'] == resume_id:
            resume_to_delete = r
            break
    if resume_to_delete:
        filename = resume_to_delete['filename']
        filepath = os.path.join(DATA_DIR, 'resumes', filename)
        if os.path.isfile(filepath):
            try:
                os.remove(filepath)
            except:
                pass
        resumes = [r for r in resumes if r['resume_id'] != resume_id]
        save_resumes(resumes)
    return redirect(url_for('resume_management_page'))

@app.route('/search')
def search_results_page():
    query = request.args.get('query')
    if query:
        query = query.strip()
        q_lower = query.lower()
    else:
        query = ''
        q_lower = ''
    job_results = []
    company_results = []
    if query:
        jobs = read_jobs()
        companies = read_companies()
        for job in jobs:
            company = get_company_by_id(job['company_id'])
            if not company:
                continue
            if (q_lower in job['title'].lower() or
                q_lower in company['company_name'].lower() or
                q_lower in job['location'].lower()):
                job_results.append({
                    'job_id': job['job_id'],
                    'title': job['title'],
                    'company_name': company['company_name'],
                    'location': job['location'],
                    'salary_min': job['salary_min'],
                    'salary_max': job['salary_max']
                })
        for company in companies:
            if q_lower in company['company_name'].lower() or q_lower in company['industry'].lower():
                company_results.append({
                    'company_id': company['company_id'],
                    'company_name': company['company_name'],
                    'industry': company['industry']
                })
    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)


if __name__ == '__main__':
    app.run(debug=True)
