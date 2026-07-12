from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_PATH = 'data'

# Utility functions to read and write data files

def read_jobs():
    jobs = []
    try:
        with open(os.path.join(DATA_PATH, 'jobs.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 9:
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


def read_companies():
    companies = []
    try:
        with open(os.path.join(DATA_PATH, 'companies.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
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


def read_categories():
    categories = []
    try:
        with open(os.path.join(DATA_PATH, 'categories.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
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


def read_applications():
    applications = []
    try:
        with open(os.path.join(DATA_PATH, 'applications.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
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


def read_resumes():
    resumes = []
    try:
        with open(os.path.join(DATA_PATH, 'resumes.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
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


def write_jobs(jobs):
    lines = []
    for job in jobs:
        line = f"{job['job_id']}|{job['title']}|{job['company_id']}|{job['location']}|{job['salary_min']}|{job['salary_max']}|{job['category']}|{job['description']}|{job['posted_date']}"
        lines.append(line)
    with open(os.path.join(DATA_PATH, 'jobs.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def write_companies(companies):
    lines = []
    for company in companies:
        line = f"{company['company_id']}|{company['company_name']}|{company['industry']}|{company['location']}|{company['employee_count']}|{company['description']}"
        lines.append(line)
    with open(os.path.join(DATA_PATH, 'companies.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def write_categories(categories):
    lines = []
    for category in categories:
        line = f"{category['category_id']}|{category['category_name']}|{category['description']}"
        lines.append(line)
    with open(os.path.join(DATA_PATH, 'categories.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def write_applications(applications):
    lines = []
    for app in applications:
        line = f"{app['application_id']}|{app['job_id']}|{app['applicant_name']}|{app['applicant_email']}|{app['status']}|{app['applied_date']}|{app['resume_id']}"
        lines.append(line)
    with open(os.path.join(DATA_PATH, 'applications.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def write_resumes(resumes):
    lines = []
    for resume in resumes:
        line = f"{resume['resume_id']}|{resume['applicant_name']}|{resume['applicant_email']}|{resume['filename']}|{resume['upload_date']}|{resume['summary']}"
        lines.append(line)
    with open(os.path.join(DATA_PATH, 'resumes.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def read_job_by_id(job_id):
    jobs = read_jobs()
    for job in jobs:
        if job['job_id'] == job_id:
            return job
    return None


def read_company_by_id(company_id):
    companies = read_companies()
    for company in companies:
        if company['company_id'] == company_id:
            return company
    return None


def read_application_by_id(app_id):
    applications = read_applications()
    for app in applications:
        if app['application_id'] == app_id:
            return app
    return None


def read_resume_by_id(resume_id):
    resumes = read_resumes()
    for resume in resumes:
        if resume['resume_id'] == resume_id:
            return resume
    return None


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    jobs = read_jobs()
    companies = read_companies()
    # Create mapping company_id -> company_name
    company_map = {company['company_id']: company['company_name'] for company in companies}
    # Get featured jobs: In this case just return all jobs sorted by posted_date desc limited to say 5 (in case we want to show top 5 featured)
    featured_jobs = []
    # Sort jobs by posted_date descending
    try:
        sorted_jobs = sorted(jobs, key=lambda x: x['posted_date'], reverse=True)
    except Exception:
        sorted_jobs = jobs

    for job in sorted_jobs[:5]:
        featured_jobs.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_map.get(job['company_id'], 'Unknown'),
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max']
        })

    return render_template('dashboard.html', featured_jobs=featured_jobs)


@app.route('/jobs')
def job_listings():
    jobs_all = read_jobs()
    companies = read_companies()
    categories = read_categories()
    company_map = {company['company_id']: company['company_name'] for company in companies}

    # Get query params for filtering
    selected_category = request.args.get('category', '').strip()
    selected_location = request.args.get('location', '').strip()
    search_query = request.args.get('search', '').strip()

    filtered_jobs = []
    for job in jobs_all:
        # Replace company_id by company_name
        company_name = company_map.get(job['company_id'], 'Unknown')
        # Filtering by category
        if selected_category and job['category'].lower() != selected_category.lower():
            continue
        # Filtering by location
        if selected_location and selected_location.lower() not in job['location'].lower():
            continue
        # Filtering by search
        if search_query:
            if search_query.lower() not in job['title'].lower() and search_query.lower() not in company_name.lower():
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

    return render_template('job_listings.html', jobs=filtered_jobs, categories=categories,
                           selected_category=selected_category, selected_location=selected_location, search_query=search_query)


@app.route('/job/<int:job_id>')
def job_details(job_id):
    job = read_job_by_id(job_id)
    if not job:
        return "Job not found", 404
    company = read_company_by_id(job['company_id'])
    if not company:
        company = {'company_id': 0, 'company_name': 'Unknown'}

    context_job = {
        'job_id': job['job_id'],
        'title': job['title'],
        'description': job['description'],
        'location': job['location'],
        'salary_min': job['salary_min'],
        'salary_max': job['salary_max'],
        'posted_date': job['posted_date']
    }

    context_company = {
        'company_id': company['company_id'],
        'company_name': company['company_name']
    }
    return render_template('job_details.html', job=context_job, company=context_company)


@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    job = read_job_by_id(job_id)
    if not job:
        return "Job not found", 404

    # Prepare job dict for context (only necessary fields)
    context_job = {
        'job_id': job['job_id'],
        'title': job['title'],
        'description': job['description'],
        'location': job['location'],
        'salary_min': job['salary_min'],
        'salary_max': job['salary_max'],
        'posted_date': job['posted_date']
    }

    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()
        cover_letter = request.form.get('cover_letter', '').strip()
        resume_file = request.files.get('resume_file', None)

        if not applicant_name or not applicant_email or not cover_letter or not resume_file:
            flash('All fields including resume upload are required.', 'error')
            return render_template('application_form.html', job=context_job)

        # Save uploaded resume file
        filename = secure_filename(resume_file.filename)
        # Save into a resumes upload folder inside data/
        upload_folder = os.path.join(DATA_PATH, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        save_path = os.path.join(upload_folder, filename)
        resume_file.save(save_path)

        # Load existing resumes
        resumes = read_resumes()
        # create new resume_id
        new_resume_id = max([r['resume_id'] for r in resumes], default=0) + 1
        upload_date = datetime.today().strftime('%Y-%m-%d')

        # We do not have summary from form, store empty summary
        new_resume = {
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': ''
        }
        resumes.append(new_resume)
        write_resumes(resumes)

        # Create new application
        applications = read_applications()
        new_app_id = max([a['application_id'] for a in applications], default=0) + 1
        new_application = {
            'application_id': new_app_id,
            'job_id': job_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': 'Applied',
            'applied_date': upload_date,
            'resume_id': new_resume_id
        }
        applications.append(new_application)
        write_applications(applications)

        flash('Application submitted successfully.', 'success')
        return redirect(url_for('application_tracking'))

    return render_template('application_form.html', job=context_job)


@app.route('/applications')
def application_tracking():
    applications = read_applications()
    jobs = read_jobs()
    companies = read_companies()

    job_map = {job['job_id']: job for job in jobs}
    company_map = {company['company_id']: company['company_name'] for company in companies}

    status_filter = request.args.get('status', 'All')

    filtered_apps = []
    for app in applications:
        if status_filter != 'All' and app['status'] != status_filter:
            continue
        job = job_map.get(app['job_id'], None)
        if not job:
            continue
        company_name = company_map.get(job['company_id'], 'Unknown')
        filtered_apps.append({
            'application_id': app['application_id'],
            'job_title': job['title'],
            'company_name': company_name,
            'status': app['status'],
            'applied_date': app['applied_date']
        })

    return render_template('application_tracking.html', applications=filtered_apps, status_filter=status_filter)


@app.route('/application/<int:app_id>')
def view_application(app_id):
    application = read_application_by_id(app_id)
    if not application:
        return "Application not found", 404
    job = read_job_by_id(application['job_id'])
    if not job:
        job = None

    resume = read_resume_by_id(application['resume_id'])
    if not resume:
        resume = None

    return render_template('application_details.html', application=application, job=job, resume=resume)


@app.route('/companies')
def companies_directory():
    companies = read_companies()

    search_query = request.args.get('search', '').strip()
    filtered_companies = []
    if search_query:
        # case-insensitive filtering by company_name or industry
        sq = search_query.lower()
        for comp in companies:
            if sq in comp['company_name'].lower() or sq in comp['industry'].lower():
                filtered_companies.append(comp)
    else:
        filtered_companies = companies

    return render_template('companies_directory.html', companies=filtered_companies, search_query=search_query)


@app.route('/company/<int:company_id>')
def company_profile(company_id):
    company = read_company_by_id(company_id)
    if not company:
        return "Company not found", 404

    jobs = read_jobs()
    company_jobs = []
    for job in jobs:
        if job['company_id'] == company_id:
            # Only use fields: job_id, title, status assumed Open (since given no status in jobs)
            company_jobs.append({
                'job_id': job['job_id'],
                'title': job['title'],
                'status': 'Open'
            })

    return render_template('company_profile.html', company=company, jobs=company_jobs)


@app.route('/resumes', methods=['GET', 'POST'])
def resume_management():
    resumes = read_resumes()

    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()
        summary = request.form.get('summary', '').strip()
        resume_file = request.files.get('resume_file', None)

        if not applicant_name or not applicant_email or not resume_file:
            flash('Applicant name, email and resume file are required.', 'error')
            return render_template('resumes.html', resumes=resumes)

        filename = secure_filename(resume_file.filename)
        upload_folder = os.path.join(DATA_PATH, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        save_path = os.path.join(upload_folder, filename)
        resume_file.save(save_path)

        # Load existing resumes
        resumes = read_resumes()
        new_id = max([r['resume_id'] for r in resumes], default=0) + 1
        upload_date = datetime.today().strftime('%Y-%m-%d')

        new_resume = {
            'resume_id': new_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': summary
        }
        resumes.append(new_resume)
        write_resumes(resumes)

        flash('Resume uploaded successfully.', 'success')
        return redirect(url_for('resume_management'))

    return render_template('resumes.html', resumes=resumes)


@app.route('/resumes/delete/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = read_resumes()
    resumes = [r for r in resumes if r['resume_id'] != resume_id]
    write_resumes(resumes)
    return redirect(url_for('resume_management'))


@app.route('/search')
def search_results():
    query = request.args.get('query', '').strip()
    jobs = read_jobs()
    companies = read_companies()

    job_results = []
    company_results = []

    if query:
        q = query.lower()
        for job in jobs:
            company = read_company_by_id(job['company_id'])
            company_name = company['company_name'] if company else 'Unknown'
            if q in job['title'].lower() or q in company_name.lower():
                job_results.append({
                    'job_id': job['job_id'],
                    'title': job['title'],
                    'company_name': company_name,
                    'location': job['location'],
                    'salary_min': job['salary_min'],
                    'salary_max': job['salary_max'],
                    'category': job['category']
                })

        for company in companies:
            if q in company['company_name'].lower() or q in company['industry'].lower():
                company_results.append(company)

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)


if __name__ == '__main__':
    app.run(debug=True)
