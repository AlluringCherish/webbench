from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
import shutil

app = Flask(__name__)
app.secret_key = 'jobboard_secret_key'

# Data file paths
DATA_FOLDER = './data'
JOBS_FILE = os.path.join(DATA_FOLDER, 'jobs.txt')
COMPANIES_FILE = os.path.join(DATA_FOLDER, 'companies.txt')
CATEGORIES_FILE = os.path.join(DATA_FOLDER, 'categories.txt')
APPLICATIONS_FILE = os.path.join(DATA_FOLDER, 'applications.txt')
RESUMES_FILE = os.path.join(DATA_FOLDER, 'resumes.txt')
JOB_CATEGORIES_FILE = os.path.join(DATA_FOLDER, 'job_categories.txt')

UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper functions to read and write data

def read_data_file(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        data = [line.split('|') for line in lines if line.strip()]
    return data


def write_data_file(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        for record in data:
            f.write('|'.join(str(x) for x in record) + '\n')

# Loading data functions

def load_jobs():
    jobs_raw = read_data_file(JOBS_FILE)
    jobs = []
    for r in jobs_raw:
        if len(r) < 9:
            continue
        job = {
            'job_id': r[0], 'title': r[1], 'company_id': r[2], 'location': r[3],
            'salary_min': r[4], 'salary_max': r[5], 'category': r[6], 'description': r[7], 'posted_date': r[8]
        }
        jobs.append(job)
    return jobs


def load_companies():
    companies_raw = read_data_file(COMPANIES_FILE)
    companies = []
    for r in companies_raw:
        if len(r) < 6:
            continue
        comp = {
            'company_id': r[0], 'company_name': r[1], 'industry': r[2], 'location': r[3],
            'employee_count': r[4], 'description': r[5]
        }
        companies.append(comp)
    return companies


def load_categories():
    cats_raw = read_data_file(CATEGORIES_FILE)
    cats = []
    for r in cats_raw:
        if len(r) <3:
            continue
        cat = {'category_id': r[0], 'category_name': r[1], 'description': r[2]}
        cats.append(cat)
    return cats


def load_applications():
    apps_raw = read_data_file(APPLICATIONS_FILE)
    apps = []
    for r in apps_raw:
        if len(r) < 7:
            continue
        app_obj = {
            'application_id': r[0], 'job_id': r[1], 'applicant_name': r[2], 'applicant_email': r[3],
            'status': r[4], 'applied_date': r[5], 'resume_id': r[6]
        }
        apps.append(app_obj)
    return apps


def load_resumes():
    resumes_raw = read_data_file(RESUMES_FILE)
    resumes = []
    for r in resumes_raw:
        if len(r) < 6:
            continue
        res_obj = {
            'resume_id': r[0], 'applicant_name': r[1], 'applicant_email': r[2], 'filename': r[3],
            'upload_date': r[4], 'summary': r[5]
        }
        resumes.append(res_obj)
    return resumes


def load_job_categories():
    jc_raw = read_data_file(JOB_CATEGORIES_FILE)
    jc_list = []
    for r in jc_raw:
        if len(r) < 3:
            continue
        jc_obj = {'mapping_id': r[0], 'job_id': r[1], 'category_id': r[2]}
        jc_list.append(jc_obj)
    return jc_list

# Generate next id helper

def generate_next_id(data_list, id_key):
    max_id = 0
    for item in data_list:
        try:
            current_id = int(item[id_key])
            if current_id > max_id:
                max_id = current_id
        except:
            continue
    return str(max_id + 1)

# Find related data

def find_company(companies, company_id):
    for c in companies:
        if c['company_id'] == company_id:
            return c
    return None


def find_job(jobs, job_id):
    for j in jobs:
        if j['job_id'] == job_id:
            return j
    return None


def find_resume(resumes, resume_id):
    for r in resumes:
        if r['resume_id'] == resume_id:
            return r
    return None

# Routes

@app.route('/')
def dashboard():
    jobs = load_jobs()
    companies = load_companies()
    # For featured jobs, let's pick 5 most recent jobs
    featured_jobs = sorted(jobs, key=lambda x: x['posted_date'], reverse=True)[:5]
    return render_template('dashboard.html', featured_jobs=featured_jobs, companies=companies)

@app.route('/jobs')
def job_listings():
    search_query = request.args.get('search', '').lower()
    category_filter = request.args.get('category', '')
    location_filter = request.args.get('location', '')

    jobs = load_jobs()
    companies = load_companies()

    filtered_jobs = []
    for job in jobs:
        company = find_company(companies, job['company_id'])
        if not company:
            continue
        if search_query:
            if (search_query not in job['title'].lower() and
                search_query not in company['company_name'].lower() and
                search_query not in job['location'].lower()):
                continue
        if category_filter and category_filter != job['category']:
            continue
        if location_filter and location_filter != job['location']:
            continue
        filtered_jobs.append(job)

    categories = load_categories()

    locations = sorted(set([j['location'] for j in jobs]))

    return render_template('job_listings.html', jobs=filtered_jobs, categories=categories,
                           locations=locations, search_query=search_query, category_filter=category_filter,
                           location_filter=location_filter)

@app.route('/job/<job_id>')
def job_details(job_id):
    jobs = load_jobs()
    companies = load_companies()

    job = find_job(jobs, job_id)
    if not job:
        flash('Job not found', 'danger')
        return redirect(url_for('job_listings'))
    company = find_company(companies, job['company_id'])
    return render_template('job_details.html', job=job, company=company)

@app.route('/apply/<job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    jobs = load_jobs()
    job = find_job(jobs, job_id)
    if not job:
        flash('Job not found', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        applicant_name = request.form.get('applicant-name', '').strip()
        applicant_email = request.form.get('applicant-email', '').strip()
        cover_letter = request.form.get('cover-letter', '').strip()
        resume_file = request.files.get('resume-upload')

        if not applicant_name or not applicant_email or not resume_file:
            flash('Please fill all required fields and upload resume.', 'danger')
            return redirect(request.url)

        # Save resume file
        resume_filename = None
        if resume_file and resume_file.filename:
            resume_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{resume_file.filename}"
            filepath = os.path.join(UPLOAD_FOLDER, resume_filename)
            resume_file.save(filepath)

        # Load resumes to add new record
        resumes = load_resumes()
        new_resume_id = generate_next_id(resumes, 'resume_id')
        new_resume = [new_resume_id, applicant_name, applicant_email, resume_filename, datetime.now().strftime('%Y-%m-%d'), cover_letter[:100]]
        resumes.append(new_resume)
        write_data_file(RESUMES_FILE, resumes)

        # Load applications to add new
        applications = load_applications()
        new_app_id = generate_next_id(applications, 'application_id')
        new_application = [new_app_id, job_id, applicant_name, applicant_email, 'Under Review', datetime.now().strftime('%Y-%m-%d'), new_resume_id]
        applications.append(new_application)
        write_data_file(APPLICATIONS_FILE, applications)

        flash('Application submitted successfully!', 'success')
        return redirect(url_for('application_tracking'))

    return render_template('application_form.html', job=job)

@app.route('/applications')
def application_tracking():
    status_filter = request.args.get('status', '')
    applications = load_applications()
    jobs = load_jobs()
    companies = load_companies()

    filtered_apps = []
    for app_obj in applications:
        if status_filter and status_filter != app_obj['status']:
            continue
        job = find_job(jobs, app_obj['job_id'])
        if not job:
            continue
        company = find_company(companies, job['company_id'])
        app_obj['job_title'] = job['title']
        app_obj['company_name'] = company['company_name'] if company else 'N/A'
        filtered_apps.append(app_obj)

    statuses = sorted(set([a['status'] for a in applications]))

    return render_template('application_tracking.html', applications=filtered_apps, statuses=statuses,
                           status_filter=status_filter)

@app.route('/companies')
def companies_directory():
    search_query = request.args.get('search', '').lower()
    companies = load_companies()

    if search_query:
        companies = [c for c in companies if search_query in c['company_name'].lower() or search_query in c['industry'].lower()]

    return render_template('companies.html', companies=companies, search_query=search_query)

@app.route('/company/<company_id>')
def company_profile(company_id):
    companies = load_companies()
    jobs = load_jobs()
    company = find_company(companies, company_id)
    if not company:
        flash('Company not found', 'danger')
        return redirect(url_for('companies_directory'))

    company_jobs = [job for job in jobs if job['company_id'] == company_id]

    return render_template('company_profile.html', company=company, jobs=company_jobs)

@app.route('/resumes', methods=['GET', 'POST'])
def manage_resumes():
    if request.method == 'POST':
        if 'resume-file-input' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['resume-file-input']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        # Save file
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)

        # Add resume record - Since no name/email provided here, use placeholders
        resumes = load_resumes()
        new_resume_id = generate_next_id(resumes, 'resume_id')
        new_resume = [new_resume_id, 'Unknown', 'unknown@email.com', filename, datetime.now().strftime('%Y-%m-%d'), '']
        resumes.append(new_resume)
        write_data_file(RESUMES_FILE, resumes)

        flash('Resume uploaded successfully.', 'success')
        return redirect(url_for('manage_resumes'))

    # GET
    resumes = load_resumes()
    return render_template('resumes.html', resumes=resumes)

@app.route('/delete_resume/<resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = load_resumes()
    resume_to_delete = None
    for r in resumes:
        if r['resume_id'] == resume_id:
            resume_to_delete = r
            break
    if resume_to_delete:
        filepath = os.path.join(UPLOAD_FOLDER, resume_to_delete['filename'])
        if os.path.exists(filepath):
            os.remove(filepath)
        resumes = [r for r in resumes if r['resume_id'] != resume_id]
        write_data_file(RESUMES_FILE, resumes)
        flash('Resume deleted successfully.', 'success')
    else:
        flash('Resume not found.', 'danger')
    return redirect(url_for('manage_resumes'))

@app.route('/search')
def search_results():
    query = request.args.get('q', '').strip().lower()
    jobs = load_jobs()
    companies = load_companies()

    job_results = []
    company_results = []

    if query:
        for job in jobs:
            # Check match in title, location
            company = find_company(companies, job['company_id'])
            if not company:
                continue
            if query in job['title'].lower() or query in company['company_name'].lower() or query in job['location'].lower():
                job_results.append(job)
        for comp in companies:
            if query in comp['company_name'].lower() or query in comp['industry'].lower():
                company_results.append(comp)

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)

if __name__ == '__main__':
    app.run(debug=True)
