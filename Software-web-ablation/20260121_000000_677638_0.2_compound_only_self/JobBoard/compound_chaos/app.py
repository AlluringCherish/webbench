import os
from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime

app = Flask(__name__)

# Directory paths for data and uploads
DATA_DIR = 'data'
UPLOAD_DIR = os.path.join(DATA_DIR, 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

# File paths
JOBS_FILE = os.path.join(DATA_DIR, 'jobs.txt')
COMPANIES_FILE = os.path.join(DATA_DIR, 'companies.txt')
APPLICATIONS_FILE = os.path.join(DATA_DIR, 'applications.txt')
RESUMES_FILE = os.path.join(DATA_DIR, 'resumes.txt')
JOB_CATEGORIES_FILE = os.path.join(DATA_DIR, 'job_categories.txt')

# --- Helper functions ---

def load_jobs():
    jobs = []
    if not os.path.isfile(JOBS_FILE):
        return jobs
    try:
        with open(JOBS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 9:
                    continue
                job_id, title, company_id, location, salary_min, salary_max, category, description, posted_date = parts
                try:
                    jobs.append({
                        'job_id': int(job_id),
                        'title': title,
                        'company_id': int(company_id),
                        'location': location,
                        'salary_min': int(salary_min),
                        'salary_max': int(salary_max),
                        'category': category,
                        'description': description,
                        'posted_date': posted_date
                    })
                except ValueError:
                    continue
    except:
        pass
    return jobs

def load_companies():
    companies = []
    if not os.path.isfile(COMPANIES_FILE):
        return companies
    try:
        with open(COMPANIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                company_id, company_name, industry, location, employee_count, description = parts
                try:
                    companies.append({
                        'company_id': int(company_id),
                        'company_name': company_name,
                        'industry': industry,
                        'location': location,
                        'employee_count': int(employee_count),
                        'description': description
                    })
                except ValueError:
                    continue
    except:
        pass
    return companies

def load_applications():
    applications = []
    if not os.path.isfile(APPLICATIONS_FILE):
        return applications
    try:
        with open(APPLICATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                application_id, job_id, applicant_name, applicant_email, status, applied_date, resume_id = parts
                try:
                    applications.append({
                        'application_id': int(application_id),
                        'job_id': int(job_id),
                        'applicant_name': applicant_name,
                        'applicant_email': applicant_email,
                        'status': status,
                        'applied_date': applied_date,
                        'resume_id': int(resume_id)
                    })
                except ValueError:
                    continue
    except:
        pass
    return applications

def save_applications(applications):
    try:
        with open(APPLICATIONS_FILE, 'w', encoding='utf-8') as f:
            for a in applications:
                f.write(f"{a['application_id']}|{a['job_id']}|{a['applicant_name']}|{a['applicant_email']}|{a['status']}|{a['applied_date']}|{a['resume_id']}\n")
    except:
        pass

def load_resumes():
    resumes = []
    if not os.path.isfile(RESUMES_FILE):
        return resumes
    try:
        with open(RESUMES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                resume_id, applicant_name, applicant_email, filename, upload_date, summary = parts
                try:
                    resumes.append({
                        'resume_id': int(resume_id),
                        'applicant_name': applicant_name,
                        'applicant_email': applicant_email,
                        'filename': filename,
                        'upload_date': upload_date,
                        'summary': summary
                    })
                except ValueError:
                    continue
    except:
        pass
    return resumes

def save_resumes(resumes):
    try:
        with open(RESUMES_FILE, 'w', encoding='utf-8') as f:
            for r in resumes:
                f.write(f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}\n")
    except:
        pass

# Routes
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    jobs = load_jobs()
    companies = load_companies()
    company_map = {c['company_id']: c['company_name'] for c in companies}

    try:
        sorted_jobs = sorted(jobs, key=lambda j: datetime.strptime(j['posted_date'], '%Y-%m-%d'), reverse=True)
    except:
        sorted_jobs = jobs

    featured_jobs = []
    for j in sorted_jobs[:5]:
        company_name = company_map.get(j['company_id'], '')
        featured_jobs.append({
            'job_id': j['job_id'],
            'title': j['title'],
            'company_name': company_name,
            'location': j['location'],
            'salary_min': j['salary_min'],
            'salary_max': j['salary_max']
        })

    return render_template('dashboard.html', featured_jobs=featured_jobs)

@app.route('/jobs')
def job_listings():
    search = request.args.get('search', '').strip().lower()
    category = request.args.get('category', '').strip()
    location = request.args.get('location', '').strip().lower()

    jobs = load_jobs()
    companies = load_companies()
    company_map = {c['company_id']: c['company_name'] for c in companies}

    filtered_jobs = []
    categories_set = set()
    locations_set = set()

    for job in jobs:
        categories_set.add(job['category'])
        locations_set.add(job['location'])

    for job in jobs:
        title_lower = job['title'].lower()
        company_name = company_map.get(job['company_id'], '')
        company_lower = company_name.lower()

        if search and search not in title_lower and search not in company_lower:
            continue
        if category and category != job['category']:
            continue
        if location and location not in job['location'].lower():
            continue

        filtered_jobs.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company': company_name,
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
            'category': job['category']
        })

    categories = sorted(categories_set)
    locations = sorted(locations_set)

    return render_template('job_listings.html', jobs=filtered_jobs, categories=categories, locations=locations)

@app.route('/job/<int:job_id>')
def job_details(job_id):
    jobs = load_jobs()
    companies = load_companies()

    job = next((j for j in jobs if j['job_id'] == job_id), None)
    if not job:
        abort(404)

    company = next((c for c in companies if c['company_id'] == job['company_id']), None)
    company_name = company['company_name'] if company else ''

    job_dict = {
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

    return render_template('job_details.html', job=job_dict)

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    jobs = load_jobs()
    companies = load_companies()

    job = next((j for j in jobs if j['job_id'] == job_id), None)
    if not job:
        abort(404)

    company = next((c for c in companies if c['company_id'] == job['company_id']), None)

    job_dict = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': company['company_name'] if company else '',
        'location': job['location'],
        'salary_min': job['salary_min'],
        'salary_max': job['salary_max'],
        'category': job['category'],
        'description': job['description'],
        'posted_date': job['posted_date']
    }

    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()
        cover_letter = request.form.get('cover_letter', '').strip()
        resume_file = request.files.get('resume_upload')

        if not applicant_name or not applicant_email or not resume_file:
            return render_template('application_form.html', job=job_dict, error='Please fill all required fields.')

        resumes = load_resumes()
        new_resume_id = max([r['resume_id'] for r in resumes], default=0) + 1
        filename_original = resume_file.filename
        filename = f"{new_resume_id}_{filename_original}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            resume_file.save(filepath)
        except:
            return render_template('application_form.html', job=job_dict, error='Failed to save resume file.')

        upload_date = datetime.now().strftime('%Y-%m-%d')
        cover_letter_filename = f"{new_resume_id}_cover_letter.txt"
        cover_letter_filepath = os.path.join(app.config['UPLOAD_FOLDER'], cover_letter_filename)
        try:
            with open(cover_letter_filepath, 'w', encoding='utf-8') as cl_file:
                cl_file.write(cover_letter)
        except:
            pass

        resumes.append({
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': ''
        })
        save_resumes(resumes)

        applications = load_applications()
        new_application_id = max([a['application_id'] for a in applications], default=0) + 1
        applied_date = datetime.now().strftime('%Y-%m-%d')

        applications.append({
            'application_id': new_application_id,
            'job_id': job_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': 'Applied',
            'applied_date': applied_date,
            'resume_id': new_resume_id
        })
        save_applications(applications)

        return redirect(url_for('application_tracking'))

    return render_template('application_form.html', job=job_dict)

def save_resumes(resumes):
    try:
        with open(RESUMES_FILE, 'w', encoding='utf-8') as f:
            for r in resumes:
                f.write(f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}\n")
    except:
        pass

@app.route('/applications')
def application_tracking():
    status_filter = request.args.get('status', '').strip().lower()

    applications = load_applications()
    jobs = load_jobs()
    companies = load_companies()

    job_map = {j['job_id']: j for j in jobs}
    company_map = {c['company_id']: c for c in companies}

    filtered_apps = []
    status_set = set()
    for app in applications:
        status_set.add(app['status'])
    status_list = sorted(status_set)

    for app in applications:
        if status_filter and app['status'].lower() != status_filter:
            continue
        job = job_map.get(app['job_id'])
        if not job:
            continue
        company = company_map.get(job['company_id'])
        if not company:
            continue

        filtered_apps.append({
            'application_id': app['application_id'],
            'job_title': job['title'],
            'company': company['company_name'],
            'status': app['status'],
            'applied_date': app['applied_date']
        })

    return render_template('application_tracking.html', applications=filtered_apps, statuses=status_list)

@app.route('/application/<int:application_id>')
def application_detail(application_id):
    applications = load_applications()
    jobs = load_jobs()
    companies = load_companies()
    resumes = load_resumes()

    app_obj = next((a for a in applications if a['application_id'] == application_id), None)
    if not app_obj:
        abort(404)

    job = next((j for j in jobs if j['job_id'] == app_obj['job_id']), None)
    if not job:
        abort(404)

    company = next((c for c in companies if c['company_id'] == job['company_id']), None)
    if not company:
        abort(404)

    resume = next((r for r in resumes if r['resume_id'] == app_obj['resume_id']), None)
    resume_filename = resume['filename'] if resume else ''

    cover_letter_filename = f"{app_obj['resume_id']}_cover_letter.txt"
    cover_letter_filepath = os.path.join(app.config['UPLOAD_FOLDER'], cover_letter_filename)
    cover_letter_text = ''
    if os.path.isfile(cover_letter_filepath):
        try:
            with open(cover_letter_filepath, 'r', encoding='utf-8') as cl_file:
                cover_letter_text = cl_file.read()
        except:
            cover_letter_text = ''

    application = {
        'application_id': app_obj['application_id'],
        'job_title': job['title'],
        'company': company['company_name'],
        'status': app_obj['status'],
        'applied_date': app_obj['applied_date'],
        'applicant_name': app_obj['applicant_name'],
        'applicant_email': app_obj['applicant_email'],
        'resume_filename': resume_filename,
        'cover_letter': cover_letter_text
    }

    return render_template('application_detail.html', application=application)

@app.route('/companies')
def companies_directory():
    search = request.args.get('search', '').strip().lower()
    companies = load_companies()

    filtered_companies = []
    for company in companies:
        if search and search not in company['company_name'].lower():
            continue
        filtered_companies.append({
            'company_id': company['company_id'],
            'company_name': company['company_name'],
            'industry': company['industry'],
            'employee_count': company['employee_count']
        })

    return render_template('companies.html', companies=filtered_companies)

@app.route('/company/<int:company_id>')
def company_profile(company_id):
    companies = load_companies()
    jobs = load_jobs()

    company = next((c for c in companies if c['company_id'] == company_id), None)
    if not company:
        abort(404)

    company_jobs = []
    for job in jobs:
        if job['company_id'] == company_id:
            company_jobs.append({
                'job_id': job['job_id'],
                'title': job['title'],
                'status': 'Open'
            })

    company_dict = {
        'company_id': company['company_id'],
        'company_name': company['company_name'],
        'industry': company['industry'],
        'location': company['location'],
        'employee_count': company['employee_count'],
        'description': company['description']
    }

    return render_template('company_profile.html', company=company_dict, jobs=company_jobs)

@app.route('/resumes')
def resume_management():
    resumes = load_resumes()
    return render_template('resumes.html', resumes=resumes)

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_email = request.form.get('applicant_email', '').strip()
    summary = request.form.get('summary', '').strip()
    resume_file = request.files.get('resume_file')

    if not applicant_name or not applicant_email or not resume_file:
        return redirect(url_for('resume_management'))

    resumes = load_resumes()
    new_resume_id = max([r['resume_id'] for r in resumes], default=0) + 1

    filename_orig = resume_file.filename
    filename = f"{new_resume_id}_{filename_orig}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        resume_file.save(filepath)
    except:
        return redirect(url_for('resume_management'))

    upload_date = datetime.now().strftime('%Y-%m-%d')
    resumes.append({
        'resume_id': new_resume_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'filename': filename,
        'upload_date': upload_date,
        'summary': summary
    })
    save_resumes(resumes)
    return redirect(url_for('resume_management'))

@app.route('/delete_resume/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = load_resumes()
    resume = next((r for r in resumes if r['resume_id'] == resume_id), None)
    if resume:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], resume['filename'])
        try:
            if os.path.isfile(filepath):
                os.remove(filepath)
        except:
            pass
        resumes = [r for r in resumes if r['resume_id'] != resume_id]
        save_resumes(resumes)
    return redirect(url_for('resume_management'))

@app.route('/search')
def search_results():
    query = request.args.get('query', '').strip().lower()
    jobs = load_jobs()
    companies = load_companies()

    company_map = {c['company_id']: c for c in companies}

    job_results = []
    company_results = []

    if query:
        for job in jobs:
            company = company_map.get(job['company_id'], {})
            company_name = company.get('company_name', '')
            if query in job['title'].lower() or query in company_name.lower():
                job_results.append({
                    'job_id': job['job_id'],
                    'title': job['title'],
                    'company': company_name,
                    'location': job['location'],
                    'salary_min': job['salary_min'],
                    'salary_max': job['salary_max'],
                    'category': job['category']
                })
        for company in companies:
            if query in company['company_name'].lower():
                company_results.append({
                    'company_id': company['company_id'],
                    'company_name': company['company_name'],
                    'industry': company['industry'],
                    'employee_count': company['employee_count']
                })

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)

if __name__ == '__main__':
    app.run(debug=True)
