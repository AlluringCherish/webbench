from flask import Flask, render_template, redirect, url_for, request, flash
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to read/write pipe-delimited files

def read_jobs():
    jobs = []
    path = os.path.join(DATA_DIR, 'jobs.txt')
    if not os.path.exists(path):
        return jobs
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 9:
                continue
            job = {
                'job_id': int(fields[0]),
                'title': fields[1],
                'company_id': int(fields[2]),
                'location': fields[3],
                'salary_min': int(fields[4]),
                'salary_max': int(fields[5]),
                'category': fields[6],
                'description': fields[7],
                'posted_date': fields[8]
            }
            jobs.append(job)
    return jobs

def write_jobs(jobs):
    path = os.path.join(DATA_DIR, 'jobs.txt')
    with open(path, 'w', encoding='utf-8') as f:
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


def read_companies():
    companies = []
    path = os.path.join(DATA_DIR, 'companies.txt')
    if not os.path.exists(path):
        return companies
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 6:
                continue
            company = {
                'company_id': int(fields[0]),
                'company_name': fields[1],
                'industry': fields[2],
                'location': fields[3],
                'employee_count': int(fields[4]),
                'description': fields[5]
            }
            companies.append(company)
    return companies

def write_companies(companies):
    path = os.path.join(DATA_DIR, 'companies.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for comp in companies:
            line = '|'.join([
                str(comp['company_id']),
                comp['company_name'],
                comp['industry'],
                comp['location'],
                str(comp['employee_count']),
                comp['description']
            ])
            f.write(line + '\n')


def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 3:
                continue
            category = {
                'category_id': int(fields[0]),
                'category_name': fields[1],
                'description': fields[2]
            }
            categories.append(category)
    return categories


def write_categories(categories):
    path = os.path.join(DATA_DIR, 'categories.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for cat in categories:
            line = '|'.join([
                str(cat['category_id']),
                cat['category_name'],
                cat['description']
            ])
            f.write(line + '\n')


def read_applications():
    applications = []
    path = os.path.join(DATA_DIR, 'applications.txt')
    if not os.path.exists(path):
        return applications
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 7:
                continue
            app = {
                'application_id': int(fields[0]),
                'job_id': int(fields[1]),
                'applicant_name': fields[2],
                'applicant_email': fields[3],
                'status': fields[4],
                'applied_date': fields[5],
                'resume_id': int(fields[6])
            }
            applications.append(app)
    return applications


def write_applications(applications):
    path = os.path.join(DATA_DIR, 'applications.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for app in applications:
            line = '|'.join([
                str(app['application_id']),
                str(app['job_id']),
                app['applicant_name'],
                app['applicant_email'],
                app['status'],
                app['applied_date'],
                str(app['resume_id'])
            ])
            f.write(line + '\n')


def read_resumes():
    resumes = []
    path = os.path.join(DATA_DIR, 'resumes.txt')
    if not os.path.exists(path):
        return resumes
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 6:
                continue
            res = {
                'resume_id': int(fields[0]),
                'applicant_name': fields[1],
                'applicant_email': fields[2],
                'filename': fields[3],
                'upload_date': fields[4],
                'summary': fields[5]
            }
            resumes.append(res)
    return resumes


def write_resumes(resumes):
    path = os.path.join(DATA_DIR, 'resumes.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for res in resumes:
            line = '|'.join([
                str(res['resume_id']),
                res['applicant_name'],
                res['applicant_email'],
                res['filename'],
                res['upload_date'],
                res['summary']
            ])
            f.write(line + '\n')


# Utility functions

def get_company_by_id(company_id):
    companies = read_companies()
    for company in companies:
        if company['company_id'] == company_id:
            return company
    return None

def get_job_by_id(job_id):
    jobs = read_jobs()
    for job in jobs:
        if job['job_id'] == job_id:
            return job
    return None

def get_application_by_id(app_id):
    applications = read_applications()
    for application in applications:
        if application['application_id'] == app_id:
            return application
    return None

def get_resume_by_id(resume_id):
    resumes = read_resumes()
    for resume in resumes:
        if resume['resume_id'] == resume_id:
            return resume
    return None


def get_category_by_name(name):
    categories = read_categories()
    for cat in categories:
        if cat['category_name'] == name:
            return cat
    return None


def filter_jobs_by_search(jobs, search_input, category_filter, location_filter):
    # Filter jobs by search input (title, company_name, location), category, and location
    companies = read_companies()
    company_dict = {c['company_id']: c['company_name'] for c in companies}
    filtered = []
    search_lower = search_input.lower() if search_input else ''
    category_filter_lower = category_filter.lower() if category_filter else ''
    location_filter_lower = location_filter.lower() if location_filter else ''

    for job in jobs:
        # Compose searchable strings
        title = job['title'].lower()
        comp_name = company_dict.get(job['company_id'], '').lower()
        loc = job['location'].lower()

        if search_lower:
            if (search_lower not in title and search_lower not in comp_name and search_lower not in loc):
                continue
        if category_filter_lower and category_filter_lower != 'all':
            if job['category'].lower() != category_filter_lower:
                continue
        if location_filter_lower and location_filter_lower != 'all':
            if loc != location_filter_lower:
                continue
        filtered.append(job)
    return filtered


def get_locations():
    jobs = read_jobs()
    locations = set()
    for job in jobs:
        loc = job['location']
        if loc:
            locations.add(loc)
    return sorted(locations)

# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    jobs = read_jobs()
    companies = read_companies()
    company_dict = {c['company_id']: c['company_name'] for c in companies}
    # Define featured jobs as first 5 jobs by posted date descending
    sorted_jobs = sorted(jobs, key=lambda j: j['posted_date'], reverse=True)
    featured_jobs = sorted_jobs[:5]
    latest_jobs = sorted_jobs[:5]

    # Build the job dicts required for template
    def job_brief(job):
        return {
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_dict.get(job['company_id'], 'Unknown'),
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max']
        }

    featured_jobs_display = [job_brief(j) for j in featured_jobs]
    latest_jobs_display = [job_brief(j) for j in latest_jobs]

    return render_template('dashboard.html', featured_jobs=featured_jobs_display, latest_jobs=latest_jobs_display)


@app.route('/jobs', methods=['GET'])
def job_listings():
    jobs = read_jobs()
    companies = read_companies()
    company_dict = {c['company_id']: c['company_name'] for c in companies}
    categories = read_categories()
    locations = get_locations()

    jobs_display = []
    for job in jobs:
        jobs_display.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_dict.get(job['company_id'], 'Unknown'),
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
            'category': job['category']
        })

    return render_template('job_listings.html', jobs=jobs_display, categories=categories, locations=locations)


@app.route('/jobs', methods=['POST'])
def job_listings_search():
    search_input = request.form.get('search_input', '').strip()
    category_filter = request.form.get('category_filter', '').strip()
    location_filter = request.form.get('location_filter', '').strip()

    jobs = read_jobs()
    companies = read_companies()
    company_dict = {c['company_id']: c['company_name'] for c in companies}
    categories = read_categories()
    locations = get_locations()

    filtered_jobs = filter_jobs_by_search(jobs, search_input, category_filter, location_filter)

    jobs_display = []
    for job in filtered_jobs:
        jobs_display.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_dict.get(job['company_id'], 'Unknown'),
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
            'category': job['category']
        })

    return render_template('job_listings.html', jobs=jobs_display, categories=categories, locations=locations)


@app.route('/job/<int:job_id>')
def job_details(job_id):
    job = get_job_by_id(job_id)
    if job is None:
        return "Job not found", 404
    company = get_company_by_id(job['company_id'])
    if company is None:
        company = {'company_id': 0, 'company_name': 'Unknown'}

    job_data = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_id': job['company_id'],
        'location': job['location'],
        'salary_min': job['salary_min'],
        'salary_max': job['salary_max'],
        'category': job['category'],
        'description': job['description'],
        'posted_date': job['posted_date']
    }
    company_data = {
        'company_id': company['company_id'],
        'company_name': company['company_name']
    }

    return render_template('job_details.html', job=job_data, company=company_data)


@app.route('/job/<int:job_id>/apply', methods=['GET'])
def application_form(job_id):
    job = get_job_by_id(job_id)
    if job is None:
        return "Job not found", 404
    job_data = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_id': job['company_id'],
        'location': job['location'],
        'salary_min': job['salary_min'],
        'salary_max': job['salary_max'],
        'category': job['category'],
        'description': job['description'],
        'posted_date': job['posted_date']
    }
    return render_template('application_form.html', job=job_data)


@app.route('/job/<int:job_id>/apply', methods=['POST'])
def submit_application(job_id):
    job = get_job_by_id(job_id)
    if job is None:
        return "Job not found", 404

    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_email = request.form.get('applicant_email', '').strip()
    resume_file = request.files.get('resume_file')
    cover_letter = request.form.get('cover_letter', '').strip()

    if not applicant_name or not applicant_email or not resume_file:
        flash('Applicant name, email, and resume file are required.')
        return redirect(url_for('application_form', job_id=job_id))

    # Save the resume file to resumes folder
    resumes_folder = os.path.join('static', 'resumes')
    os.makedirs(resumes_folder, exist_ok=True)
    filename = resume_file.filename
    if not filename:
        flash('Invalid resume file.')
        return redirect(url_for('application_form', job_id=job_id))

    # Avoid overwriting by prefixing timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    save_filename = f"{timestamp}_{filename}"
    resume_path = os.path.join(resumes_folder, save_filename)
    resume_file.save(resume_path)

    # Update resumes.txt
    resumes = read_resumes()
    new_resume_id = 1
    if resumes:
        new_resume_id = max(r['resume_id'] for r in resumes) + 1
    upload_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # Summary placeholder: first 100 chars of cover letter or empty
    summary = cover_letter[:100] if cover_letter else ''

    new_resume = {
        'resume_id': new_resume_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'filename': save_filename,
        'upload_date': upload_date,
        'summary': summary
    }
    resumes.append(new_resume)
    write_resumes(resumes)

    # Add application record
    applications = read_applications()
    new_app_id = 1
    if applications:
        new_app_id = max(a['application_id'] for a in applications) + 1
    applied_date = datetime.datetime.now().strftime('%Y-%m-%d')

    new_application = {
        'application_id': new_app_id,
        'job_id': job_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'status': 'Applied',
        'applied_date': applied_date,
        'resume_id': new_resume_id
    }
    applications.append(new_application)
    write_applications(applications)

    flash('Application submitted successfully!')
    return redirect(url_for('job_details', job_id=job_id))


@app.route('/applications', methods=['GET'])
def application_tracking():
    status_filter = request.args.get('status_filter', '').strip()
    applications = read_applications()
    jobs = read_jobs()
    companies = read_companies()
    job_dict = {j['job_id']: j for j in jobs}
    company_dict = {c['company_id']: c for c in companies}

    filtered_apps = []
    if status_filter:
        filtered_apps = [a for a in applications if a['status'].lower() == status_filter.lower()]
    else:
        filtered_apps = applications

    applications_display = []
    for app in filtered_apps:
        job = job_dict.get(app['job_id'])
        if job is None:
            continue
        company = company_dict.get(job['company_id'])
        if company is None:
            continue

        applications_display.append({
            'application_id': app['application_id'],
            'job_title': job['title'],
            'company_name': company['company_name'],
            'status': app['status'],
            'applied_date': app['applied_date']
        })

    return render_template('application_tracking.html', applications=applications_display, status_filter=status_filter)


@app.route('/application/<int:app_id>')
def view_application(app_id):
    application = get_application_by_id(app_id)
    if application is None:
        return "Application not found", 404
    job = get_job_by_id(application['job_id'])
    if job is None:
        return "Related job not found", 404

    # Pass full application and job dicts
    return render_template('application_details.html', application=application, job=job)


@app.route('/companies')
def companies_directory():
    companies = read_companies()
    return render_template('companies.html', companies=companies)


@app.route('/company/<int:company_id>')
def company_profile(company_id):
    company = get_company_by_id(company_id)
    if company is None:
        return "Company not found", 404

    jobs = read_jobs()

    # Filter jobs for this company
    company_jobs_raw = [j for j in jobs if j['company_id'] == company_id]

    company_jobs = []
    for job in company_jobs_raw:
        # Only fields needed: job_id, title, status
        # Status is not defined in job schema, so likely default open, but spec mentions status in company_jobs listing
        # Since not specified, we will assume all jobs are open with status 'Open'
        company_jobs.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'status': 'Open'
        })

    return render_template('company_profile.html', company=company, company_jobs=company_jobs)


@app.route('/resumes')
def resumes_management():
    resumes = read_resumes()
    return render_template('resumes.html', resumes=resumes)


@app.route('/resumes/upload', methods=['POST'])
def upload_resume():
    resume_file = request.files.get('resume_file')
    if not resume_file or not resume_file.filename:
        flash('No resume file selected for upload.')
        return redirect(url_for('resumes_management'))

    filename = resume_file.filename
    resumes_folder = os.path.join('static', 'resumes')
    os.makedirs(resumes_folder, exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    save_filename = f"{timestamp}_{filename}"
    resume_path = os.path.join(resumes_folder, save_filename)
    resume_file.save(resume_path)

    # Add new resume record with minimal info
    resumes = read_resumes()
    new_resume_id = 1
    if resumes:
        new_resume_id = max(r['resume_id'] for r in resumes) + 1

    upload_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # Since no applicant_name/email or summary provided, we store empty strings
    new_resume = {
        'resume_id': new_resume_id,
        'applicant_name': '',
        'applicant_email': '',
        'filename': save_filename,
        'upload_date': upload_date,
        'summary': ''
    }
    resumes.append(new_resume)
    write_resumes(resumes)

    flash('Resume uploaded successfully.')
    return redirect(url_for('resumes_management'))


@app.route('/resume/<int:resume_id>/delete', methods=['POST'])
def delete_resume(resume_id):
    resumes = read_resumes()
    resume_to_delete = None
    for r in resumes:
        if r['resume_id'] == resume_id:
            resume_to_delete = r
            break
    if not resume_to_delete:
        flash('Resume not found.')
        return redirect(url_for('resumes_management'))

    # Delete file from disk
    resumes_folder = os.path.join('static', 'resumes')
    filepath = os.path.join(resumes_folder, resume_to_delete['filename'])
    if os.path.exists(filepath):
        os.remove(filepath)

    # Remove from resumes.txt
    updated_resumes = [r for r in resumes if r['resume_id'] != resume_id]
    write_resumes(updated_resumes)

    flash('Resume deleted successfully.')
    return redirect(url_for('resumes_management'))


@app.route('/search')
def search_results():
    query = request.args.get('query', '').strip()
    jobs = read_jobs()
    companies = read_companies()

    query_lower = query.lower()

    job_results = []
    company_results = []

    if query:
        # Search jobs by title, company_name, location
        company_dict = {c['company_id']: c for c in companies}
        for job in jobs:
            comp = company_dict.get(job['company_id'])
            if not comp:
                continue
            if (query_lower in job['title'].lower() or
                query_lower in comp['company_name'].lower() or
                query_lower in job['location'].lower()):
                job_results.append({
                    'job_id': job['job_id'],
                    'title': job['title'],
                    'company_name': comp['company_name'],
                    'location': job['location'],
                    'salary_min': job['salary_min'],
                    'salary_max': job['salary_max']
                })

        # Search companies by name, industry, location
        for comp in companies:
            if (query_lower in comp['company_name'].lower() or
                query_lower in comp['industry'].lower() or
                query_lower in comp['location'].lower()):
                company_results.append({
                    'company_id': comp['company_id'],
                    'company_name': comp['company_name'],
                    'industry': comp['industry'],
                    'location': comp['location']
                })

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)


if __name__ == '__main__':
    app.run(debug=True)
