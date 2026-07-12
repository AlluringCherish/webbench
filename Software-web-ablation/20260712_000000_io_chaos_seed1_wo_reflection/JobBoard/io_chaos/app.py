from flask import Flask, render_template, request, url_for, redirect, abort
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

DATA_DIR = 'data'

# Utility function to read data file with given fields
# Assumes pipe-separated values

def read_data_file(filename, fields, sep='|'):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    data = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(sep)
            if len(parts) != len(fields):
                continue  # malformed line
            item = {fields[i]: parts[i] for i in range(len(fields))}
            data.append(item)
    return data

# Utility function to save data to file

def save_data_file(filename, data_list, fields, sep='|'):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for item in data_list:
            line = sep.join(str(item.get(field, '')) for field in fields)
            f.write(line + '\n')

# Field definitions for files
JOB_FIELDS = ['job_id', 'title', 'company_id', 'description', 'location', 'salary_min', 'salary_max']
COMPANY_FIELDS = ['company_id', 'company_name', 'location', 'employee_count', 'industry', 'description']
JOB_CAT_FIELDS = ['cat_id', 'category_name']
APPLICATION_FIELDS = ['application_id', 'job_id', 'applicant_name', 'applicant_email', 'status', 'resume_id', 'applied_date', 'cover_letter']
RESUME_FIELDS = ['resume_id', 'applicant_name', 'applicant_email', 'filename', 'upload_date', 'summary']

# Constants for job locations
JOB_LOCATIONS = ['Remote', 'On-site', 'Hybrid']

# Load functions

def load_jobs():
    return read_data_file('jobs.txt', JOB_FIELDS)

def load_companies():
    return read_data_file('companies.txt', COMPANY_FIELDS)

def load_categories():
    return read_data_file('job_categories.txt', JOB_CAT_FIELDS)

def load_applications():
    return read_data_file('applications.txt', APPLICATION_FIELDS)

def load_resumes():
    return read_data_file('resumes.txt', RESUME_FIELDS)

# Routes

@app.route('/')
def dashboard():
    jobs = load_jobs()
    companies = load_companies()
    featured_jobs = {}

    # Compose featured jobs (assuming 'featured' means all recent jobs for dashboard)
    for job in jobs:
        company = next((c for c in companies if c['company_id'] == job['company_id']), None)
        company_name_val = company['company_name'] if company else 'Unknown'
        location_val = job['location']
        featured_jobs[job['job_id']] = {
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_name_val,
            'location': location_val,
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
        }

    return render_template('main_dashboard.html', featured_jobs=featured_jobs)

@app.route('/jobs')
def job_listings():
    jobs = load_jobs()
    companies = load_companies()
    categories = load_categories()

    # Compose job listings with company names and location string.
    jobs_list = []
    for job in jobs:
        company = next((c for c in companies if c['company_id'] == job['company_id']), None)
        company_name_val = company['company_name'] if company else 'Unknown'
        location_val = job['location']
        jobs_list.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_name_val,
            'location': location_val,
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
        })

    # categories as list of category names
    category_names = [cat['category_name'] for cat in categories]

    return render_template('jobs_list.html', jobs=jobs_list, categories=category_names, locations=JOB_LOCATIONS)

@app.route('/job/<job_id>')
def job_details(job_id):
    jobs = load_jobs()
    companies = load_companies()
    job = next((j for j in jobs if j['job_id'] == job_id), None)
    if job is None:
        abort(404)

    company = next((c for c in companies if c['company_id'] == job['company_id']), None)
    if company is None:
        abort(404)

    job_data = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': company['company_name'],
        'description': job['description'],
        'salary_min': job['salary_min'],
        'salary_max': job['salary_max'],
        'location': job['location']
    }

    return render_template('job_detail.html', job=job_data)

@app.route('/apply/<job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    jobs = load_jobs()
    companies = load_companies()
    job = next((j for j in jobs if j['job_id'] == job_id), None)
    if job is None:
        abort(404)

    company = next((c for c in companies if c['company_id'] == job['company_id']), None)

    if request.method == 'GET':
        return render_template('app_form.html', job=job, company=company)
    else:
        # Process application form
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()
        cover_letter = request.form.get('cover_letter', '').strip()
        # For resume upload, assume filename string (in real case, file handling)
        resume_file = request.form.get('resume_file', '').strip()

        if not applicant_name or not applicant_email:
            abort(400, "Applicant name and email required")

        applications = load_applications()
        new_id = 1
        if applications:
            new_id = max(int(a['application_id']) for a in applications) + 1

        new_app = {
            'application_id': str(new_id),
            'job_id': job_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': 'Applied',
            'resume_id': '',  # Not connected here
            'applied_date': '',  # Could add real date
            'cover_letter': cover_letter
        }
        applications.append(new_app)
        save_data_file('applications.txt', applications, APPLICATION_FIELDS)

        return redirect(url_for('application_tracking'))

@app.route('/applications')
def application_tracking():
    applications = load_applications()
    jobs = load_jobs()
    companies = load_companies()

    applications_display = []
    for app in applications:
        job = next((j for j in jobs if j['job_id'] == app['job_id']), None)
        if job is None:
            continue
        company = next((c for c in companies if c['company_id'] == job['company_id']), None)
        company_name = company['company_name'] if company else 'Unknown'

        applications_display.append({
            'application_id': app['application_id'],
            'job_title': job['title'],
            'company_name': company_name,
            'status': app['status'],
            'applied_date': app['applied_date']
        })

    return render_template('apl_tracking.html', applications=applications_display)

@app.route('/application/<application_id>')
def app_detail(application_id):
    applications = load_applications()
    application = next((a for a in applications if a['application_id'] == application_id), None)
    if application is None:
        abort(404)

    jobs = load_jobs()
    job = next((j for j in jobs if j['job_id'] == application['job_id']), None)
    if job is None:
        abort(404)

    resumes = load_resumes()
    resume = None
    if application['resume_id']:
        resume = next((r for r in resumes if r['resume_id'] == application['resume_id']), None)

    application_detail = {
        'application_id': application['application_id'],
        'job_id': application['job_id'],
        'applicant_name': application['applicant_name'],
        'applicant_email': application['applicant_email'],
        'status': application['status'],
        'applied_date': application['applied_date'],
        'cover_letter': application.get('cover_letter', ''),
        'resume': resume
    }

    job_info = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': 'Unknown'
    }
    companies = load_companies()
    company = next((c for c in companies if c['company_id'] == job['company_id']), None)
    if company:
        job_info['company_name'] = company['company_name']

    return render_template('application_detail.html', application=application_detail, job=job_info)

@app.route('/companies')
def companies_directory():
    companies = load_companies()
    companies_list = []
    for c in companies:
        companies_list.append({
            'company_id': c['company_id'],
            'company_name': c['company_name'],
            'industry': c.get('industry', 'Unknown'),
            'employee_count': c.get('employee_count', 'Unknown')
        })
    return render_template('comps.html', companies=companies_list)

@app.route('/company/<company_id>')
def company_profile(company_id):
    companies = load_companies()
    jobs = load_jobs()

    company = next((c for c in companies if c['company_id'] == company_id), None)
    if company is None:
        abort(404)

    company_jobs = {}
    for job in jobs:
        if job['company_id'] == company_id:
            company_jobs[job['job_id']] = {
                'job_id': job['job_id'],
                'title': job['title'],
                'status': 'Open'  # Assuming all jobs are open
            }

    company_data = {
        'company_id': company['company_id'],
        'company_name': company['company_name'],
        'industry': company.get('industry', 'Unknown'),
        'location': company.get('location', 'Unknown'),
        'description': company.get('description', ''),
        'employee_count': company.get('employee_count', 'Unknown')
    }

    return render_template('comp_profile.html', company=company_data, jobs=company_jobs)

@app.route('/resumes')
def resumes_page():
    resumes = load_resumes()
    return render_template('resume_mgmt.html', resumes=resumes)

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_email = request.form.get('applicant_email', '').strip()
    summary = request.form.get('summary', '').strip()
    resume_file = request.form.get('resume_file', '').strip()

    if not resume_file:
        abort(400, "No resume file provided")

    resumes = load_resumes()
    new_id = 1
    if resumes:
        new_id = max(int(r['resume_id']) for r in resumes) + 1

    new_resume = {
        'resume_id': str(new_id),
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'filename': resume_file,
        'upload_date': '',  # Could add date string
        'summary': summary
    }
    resumes.append(new_resume)
    save_data_file('resumes.txt', resumes, RESUME_FIELDS)
    return redirect(url_for('resumes_page'))

@app.route('/delete_resume/<resume_id>', methods=['GET'])
def delete_resume(resume_id):
    resumes = load_resumes()
    resumes = [r for r in resumes if r['resume_id'] != str(resume_id)]
    save_data_file('resumes.txt', resumes, RESUME_FIELDS)
    return redirect(url_for('resumes_page'))

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '').strip().lower()
    jobs = load_jobs()
    companies = load_companies()

    job_results = {}
    company_results = {}

    # Search jobs by title, company name, or location
    for job in jobs:
        company = next((c for c in companies if c['company_id'] == job['company_id']), None)
        company_name_val = company['company_name'] if company else 'Unknown'
        if query in job['title'].lower() or query in company_name_val.lower() or query in job['location'].lower():
            job_results[job['job_id']] = {
                'job_id': job['job_id'],
                'title': job['title'],
                'company_name': company_name_val,
                'location': job['location'],
                'salary_min': job['salary_min'],
                'salary_max': job['salary_max']
            }

    for company in companies:
        if query in company['company_name'].lower() or query in company.get('industry', '').lower():
            company_results[company['company_id']] = {
                'company_id': company['company_id'],
                'company_name': company['company_name'],
                'industry': company.get('industry', '')
            }

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)

if __name__ == '__main__':
    app.run(debug=True)
