from flask import Flask, render_template, redirect, url_for, request, flash
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_PATH = 'data'

# Helpers to load and save data

def load_jobs():
    jobs = []
    path = os.path.join(DATA_PATH, 'jobs.txt')
    if not os.path.exists(path):
        return jobs
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
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
                except (IndexError, ValueError):
                    continue
    return jobs

def save_jobs(jobs):
    path = os.path.join(DATA_PATH, 'jobs.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for job in jobs:
            line = f"{job['job_id']}|{job['title']}|{job['company_id']}|{job['location']}|{job['salary_min']}|{job['salary_max']}|{job['category']}|{job['description']}|{job['posted_date']}"
            f.write(line + '\n')


def load_companies():
    companies = []
    path = os.path.join(DATA_PATH, 'companies.txt')
    if not os.path.exists(path):
        return companies
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
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
                except (IndexError, ValueError):
                    continue
    return companies

def save_companies(companies):
    path = os.path.join(DATA_PATH, 'companies.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for company in companies:
            line = f"{company['company_id']}|{company['company_name']}|{company['industry']}|{company['location']}|{company['employee_count']}|{company['description']}"
            f.write(line + '\n')


def load_categories():
    categories = []
    path = os.path.join(DATA_PATH, 'categories.txt')
    if not os.path.exists(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                try:
                    category = {
                        'category_id': int(parts[0]),
                        'category_name': parts[1],
                        'description': parts[2]
                    }
                    categories.append(category)
                except (IndexError, ValueError):
                    continue
    return categories

def save_categories(categories):
    path = os.path.join(DATA_PATH, 'categories.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for category in categories:
            line = f"{category['category_id']}|{category['category_name']}|{category['description']}"
            f.write(line + '\n')


def load_applications():
    applications = []
    path = os.path.join(DATA_PATH, 'applications.txt')
    if not os.path.exists(path):
        return applications
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                try:
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
                except (IndexError, ValueError):
                    continue
    return applications

def save_applications(applications):
    path = os.path.join(DATA_PATH, 'applications.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for app in applications:
            line = f"{app['application_id']}|{app['job_id']}|{app['applicant_name']}|{app['applicant_email']}|{app['status']}|{app['applied_date']}|{app['resume_id']}"
            f.write(line + '\n')


def load_resumes():
    resumes = []
    path = os.path.join(DATA_PATH, 'resumes.txt')
    if not os.path.exists(path):
        return resumes
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
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
                except (IndexError, ValueError):
                    continue
    return resumes

def save_resumes(resumes):
    path = os.path.join(DATA_PATH, 'resumes.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for res in resumes:
            line = f"{res['resume_id']}|{res['applicant_name']}|{res['applicant_email']}|{res['filename']}|{res['upload_date']}|{res['summary']}"
            f.write(line + '\n')


# Helper function to find company by id

def get_company_by_id(company_id):
    companies = load_companies()
    for c in companies:
        if c['company_id'] == company_id:
            return c
    return None

# Helper to get job by id

def get_job_by_id(job_id):
    jobs = load_jobs()
    for j in jobs:
        if j['job_id'] == job_id:
            return j
    return None

# Helper to get category names from jobs

def get_all_categories_from_jobs():
    cats = set()
    jobs = load_jobs()
    for job in jobs:
        cats.add(job['category'])
    return sorted(list(cats))

# Helper to get all unique locations from jobs

def get_all_locations_from_jobs():
    locs = set()
    jobs = load_jobs()
    for job in jobs:
        locs.add(job['location'])
    return sorted(list(locs))


# ------------------- Routes -------------------

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    jobs = load_jobs()
    companies = load_companies()
    # Prepare featured_jobs with required keys
    featured_jobs = []
    for job in jobs[:5]:  # demo: first 5 jobs as featured
        company = get_company_by_id(job['company_id'])
        company_name = company['company_name'] if company else 'Unknown'
        featured_jobs.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_name,
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max']
        })
    return render_template('dashboard.html', featured_jobs=featured_jobs)

@app.route('/jobs', methods=['GET', 'POST'])
def jobs_listings():
    jobs = load_jobs()
    categories = get_all_categories_from_jobs()
    locations = get_all_locations_from_jobs()
    filters = {
        'categories': categories,
        'locations': locations
    }

    filtered_jobs = []
    if request.method == 'POST':
        search_term = request.form.get('search_input', '').strip().lower()
        category_filter = request.form.get('category_filter', '').strip()
        location_filter = request.form.get('location_filter', '').strip()

        for job in jobs:
            # Search in title, company_name, location
            company = get_company_by_id(job['company_id'])
            company_name = company['company_name'] if company else ''
            text_search_target = f"{job['title']} {company_name} {job['location']}'.lower()"

            if search_term and search_term not in text_search_target:
                continue
            if category_filter and category_filter != job['category']:
                continue
            if location_filter and location_filter != job['location']:
                continue

            filtered_jobs.append({
                'job_id': job['job_id'],
                'title': job['title'],
                'company_name': company_name,
                'location': job['location'],
                'salary_min': job['salary_min'],
                'salary_max': job['salary_max'],
                'category': job['category']
            })
    else:
        # GET - show all jobs
        for job in jobs:
            company = get_company_by_id(job['company_id'])
            company_name = company['company_name'] if company else ''
            filtered_jobs.append({
                'job_id': job['job_id'],
                'title': job['title'],
                'company_name': company_name,
                'location': job['location'],
                'salary_min': job['salary_min'],
                'salary_max': job['salary_max'],
                'category': job['category']
            })

    return render_template('job_listings.html', jobs=filtered_jobs, filters=filters)

@app.route('/job/<int:job_id>')
def job_details(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return "Job not found", 404
    company = get_company_by_id(job['company_id'])
    company_name = company['company_name'] if company else ''
    job_info = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': company_name,
        'location': job['location'],
        'salary_min': job['salary_min'],
        'salary_max': job['salary_max'],
        'description': job['description'],
        'category': job['category']
    }
    return render_template('job_details.html', job=job_info)

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return "Job not found", 404
    company = get_company_by_id(job['company_id'])
    job_info = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': company['company_name'] if company else ''
    }

    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()
        cover_letter = request.form.get('cover_letter', '').strip()
        resume_file = request.files.get('resume_file')

        errors = []
        if not applicant_name:
            errors.append('Applicant name is required.')
        if not applicant_email:
            errors.append('Applicant email is required.')
        if not resume_file or resume_file.filename == '':
            errors.append('Resume file is required.')

        if errors:
            # Return form with errors
            return render_template('application_form.html', job=job_info, errors=errors,
                                   form_fields={'applicant_name': applicant_name, 'applicant_email': applicant_email, 'cover_letter': cover_letter})

        # Save resume file to a local 'uploads' folder (create if not exist)
        upload_folder = os.path.join('uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        filename = resume_file.filename
        save_path = os.path.join(upload_folder, filename)
        resume_file.save(save_path)

        # Load resumes, assign new resume_id
        resumes = load_resumes()
        new_resume_id = max([r['resume_id'] for r in resumes], default=0) + 1
        # Add summary as first 100 chars of cover_letter or '' if empty
        summary = (cover_letter[:100]) if cover_letter else ''
        new_resume = {
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': datetime.now().strftime('%Y-%m-%d'),
            'summary': summary
        }
        resumes.append(new_resume)
        save_resumes(resumes)

        # Add application record
        applications = load_applications()
        new_application_id = max([a['application_id'] for a in applications], default=0) + 1
        new_application = {
            'application_id': new_application_id,
            'job_id': job_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': 'Applied',
            'applied_date': datetime.now().strftime('%Y-%m-%d'),
            'resume_id': new_resume_id
        }
        applications.append(new_application)
        save_applications(applications)

        return render_template('application_submitted.html')

    return render_template('application_form.html', job=job_info)

@app.route('/applications', methods=['GET', 'POST'])
def application_tracking():
    applications = load_applications()
    jobs = load_jobs()

    # Map job_id to title and company_name
    job_map = {}
    for job in jobs:
        company = get_company_by_id(job['company_id'])
        company_name = company['company_name'] if company else ''
        job_map[job['job_id']] = (job['title'], company_name)

    status_filter = 'All'
    if request.method == 'POST':
        status_filter = request.form.get('status_filter', 'All')

    filtered_apps = []
    for app in applications:
        if status_filter != 'All' and app['status'] != status_filter:
            continue
        job_title, company_name = job_map.get(app['job_id'], ('Unknown', ''))
        filtered_apps.append({
            'application_id': app['application_id'],
            'job_title': job_title,
            'company_name': company_name,
            'status': app['status'],
            'applied_date': app['applied_date']
        })

    return render_template('application_tracking.html', applications=filtered_apps)

@app.route('/companies', methods=['GET', 'POST'])
def companies_directory():
    companies = load_companies()

    if request.method == 'POST':
        search_query = request.form.get('company_search_query', '').strip().lower()
        if search_query:
            filtered = []
            for c in companies:
                if search_query in c['company_name'].lower() or search_query in c['industry'].lower():
                    filtered.append(c)
            companies = filtered

    # Only pass required keys
    companies_out = []
    for c in companies:
        companies_out.append({
            'company_id': c['company_id'],
            'company_name': c['company_name'],
            'industry': c['industry'],
            'employee_count': c['employee_count']
        })

    return render_template('companies_directory.html', companies=companies_out)

@app.route('/company/<int:company_id>')
def company_profile(company_id):
    company = get_company_by_id(company_id)
    if not company:
        return "Company not found", 404
    jobs = load_jobs()
    # Filter jobs for this company
    company_jobs = []
    for job in jobs:
        if job['company_id'] == company_id:
            company_jobs.append({
                'job_id': job['job_id'],
                'title': job['title'],
                'status': 'Open'  # specification suggests status like 'Open'
            })

    company_info = {
        'company_id': company['company_id'],
        'company_name': company['company_name'],
        'industry': company['industry'],
        'location': company['location'],
        'description': company['description'],
        'employee_count': company['employee_count']
    }

    return render_template('company_profile.html', company=company_info, company_jobs=company_jobs)

@app.route('/resumes', methods=['GET', 'POST'])
def resume_management():
    resumes = load_resumes()

    if request.method == 'POST':
        # Handle resume deletion
        delete_resume_id = request.form.get('delete_resume_id')
        if delete_resume_id:
            try:
                delete_id_int = int(delete_resume_id)
                resumes = [r for r in resumes if r['resume_id'] != delete_id_int]
                save_resumes(resumes)
            except ValueError:
                pass

        else:
            resume_file = request.files.get('resume_file')
            if not resume_file or resume_file.filename == '':
                # no file submitted, just render with existing resumes
                return render_template('resume_management.html', resumes=resumes)

            filename = resume_file.filename
            upload_folder = os.path.join('uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            save_path = os.path.join(upload_folder, filename)
            resume_file.save(save_path)

            # Add to resumes.txt
            applicant_name = request.form.get('applicant_name', '').strip() or 'Unknown'
            applicant_email = request.form.get('applicant_email', '').strip() or 'unknown@example.com'
            resumes = load_resumes()
            new_resume_id = max([r['resume_id'] for r in resumes], default=0) + 1
            new_resume = {
                'resume_id': new_resume_id,
                'applicant_name': applicant_name,
                'applicant_email': applicant_email,
                'filename': filename,
                'upload_date': datetime.now().strftime('%Y-%m-%d'),
                'summary': ''
            }
            resumes.append(new_resume)
            save_resumes(resumes)

    return render_template('resume_management.html', resumes=resumes)

@app.route('/search')
def search_results():
    query = request.args.get('query', '').strip()
    jobs = load_jobs()
    companies = load_companies()

    job_results = []
    company_results = []

    if query:
        lower_query = query.lower()
        # Search jobs (title, company_name, location)
        for job in jobs:
            company = get_company_by_id(job['company_id'])
            company_name = company['company_name'] if company else ''
            haystack = f"{job['title']} {company_name} {job['location']}'.lower()"
            if lower_query in haystack:
                job_results.append({
                    'job_id': job['job_id'],
                    'title': job['title'],
                    'company_name': company_name,
                    'location': job['location'],
                    'salary_min': job['salary_min'],
                    'salary_max': job['salary_max']
                })

        # Search companies (company_name, industry)
        for c in companies:
            if lower_query in c['company_name'].lower() or lower_query in c['industry'].lower():
                company_results.append({
                    'company_id': c['company_id'],
                    'company_name': c['company_name'],
                    'industry': c['industry']
                })

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)


if __name__ == '__main__':
    app.run(debug=True)
