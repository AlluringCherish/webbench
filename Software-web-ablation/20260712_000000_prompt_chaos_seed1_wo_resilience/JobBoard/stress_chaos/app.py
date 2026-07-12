from flask import Flask, render_template, redirect, url_for, request, flash
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to read and write data files

def read_jobs():
    jobs = []
    try:
        with open(os.path.join(DATA_DIR, 'jobs.txt'), encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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
        with open(os.path.join(DATA_DIR, 'companies.txt'), encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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


def read_applications():
    applications = []
    try:
        with open(os.path.join(DATA_DIR, 'applications.txt'), encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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
        with open(os.path.join(DATA_DIR, 'resumes.txt'), encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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


def write_resumes(resumes):
    lines = []
    for r in resumes:
        line = f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}"
        lines.append(line)
    with open(os.path.join(DATA_DIR, 'resumes.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def read_categories():
    categories = []
    try:
        with open(os.path.join(DATA_DIR, 'categories.txt'), encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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


@app.route('/')
def root_redirect():
    # Redirect to /dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Load jobs and companies to prepare featured_jobs
    jobs = read_jobs()
    companies = read_companies()

    # Compose featured_jobs list (contains job_id, title, company_name, location, salary_min, salary_max)
    # Using first N jobs as featured (arbitrary choice)
    # Map company_id to company_name
    company_map = {c['company_id']: c['company_name'] for c in companies}
    featured_jobs = []
    for job in jobs:
        company_name = company_map.get(job['company_id'], 'Unknown')
        featured_jobs.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_name,
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max']
        })

    return render_template('dashboard.html', featured_jobs=featured_jobs)


@app.route('/jobs')
def job_listings():
    search = request.args.get('search', '').strip()
    category_filter = request.args.get('category_filter', '').strip()
    location_filter = request.args.get('location_filter', '').strip()

    jobs = read_jobs()
    companies = read_companies()

    # Map company_id to company_name
    company_map = {c['company_id']: c['company_name'] for c in companies}

    filtered_jobs = []

    for job in jobs:
        # Conditions
        if search:
            search_lower = search.lower()
            if search_lower not in job['title'].lower() and search_lower not in company_map.get(job['company_id'], '').lower():
                continue
        if category_filter:
            if job['category'].lower() != category_filter.lower():
                continue
        if location_filter:
            if location_filter.lower() not in job['location'].lower():
                continue
        filtered_jobs.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_map.get(job['company_id'], 'Unknown'),
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
            'category': job['category']
        })

    return render_template('job_listings.html', jobs=filtered_jobs)


@app.route('/job/<int:job_id>')
def job_details(job_id):
    jobs = read_jobs()
    companies = read_companies()
    company_map = {c['company_id']: c['company_name'] for c in companies}

    job = None
    for j in jobs:
        if j['job_id'] == job_id:
            job = {
                'job_id': j['job_id'],
                'title': j['title'],
                'company_name': company_map.get(j['company_id'], 'Unknown'),
                'location': j['location'],
                'salary_min': j['salary_min'],
                'salary_max': j['salary_max'],
                'description': j['description']
            }
            break

    if not job:
        # Job not found, return 404 or render with empty
        return render_template('job_details.html', job=None), 404

    return render_template('job_details.html', job=job)


@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    jobs = read_jobs()
    companies = read_companies()
    company_map = {c['company_id']: c['company_name'] for c in companies}

    job = None
    for j in jobs:
        if j['job_id'] == job_id:
            job = {
                'job_id': j['job_id'],
                'title': j['title'],
                'company_name': company_map.get(j['company_id'], 'Unknown')
            }
            break

    if not job:
        return "Job not found", 404

    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()
        cover_letter = request.form.get('cover_letter', '').strip()
        resume_file = request.files.get('resume_upload')

        # Basic validation
        if not applicant_name or not applicant_email or not cover_letter or not resume_file:
            flash('All fields are required including a resume upload.')
            return render_template('application_form.html', job=job)

        # Save resume file to a directory
        uploads_dir = os.path.join('uploads', 'resumes')
        os.makedirs(uploads_dir, exist_ok=True)

        # Generate new resume_id
        resumes = read_resumes()
        max_resume_id = max((r['resume_id'] for r in resumes), default=0)
        new_resume_id = max_resume_id + 1

        filename = f'resume_{new_resume_id}_{resume_file.filename}'
        filepath = os.path.join(uploads_dir, filename)
        resume_file.save(filepath)

        # Add new resume metadata
        today = datetime.today().strftime('%Y-%m-%d')
        summary = ''  # No summary in upload form, keep empty

        new_resume = {
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': today,
            'summary': summary
        }
        resumes.append(new_resume)

        # Save resumes.txt
        lines = []
        for r in resumes:
            line = f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}"
            lines.append(line)
        with open(os.path.join(DATA_DIR, 'resumes.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        # Add new application entry
        applications = read_applications()
        max_application_id = max((a['application_id'] for a in applications), default=0)
        new_application_id = max_application_id + 1

        new_application = {
            'application_id': new_application_id,
            'job_id': job['job_id'],
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': 'Applied',
            'applied_date': today,
            'resume_id': new_resume_id
        }
        applications.append(new_application)

        # Save applications.txt
        lines = []
        for a in applications:
            line = f"{a['application_id']}|{a['job_id']}|{a['applicant_name']}|{a['applicant_email']}|{a['status']}|{a['applied_date']}|{a['resume_id']}"
            lines.append(line)
        with open(os.path.join(DATA_DIR, 'applications.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        flash('Application submitted successfully.')

        return redirect(url_for('application_tracking'))

    return render_template('application_form.html', job=job)


@app.route('/applications')
def application_tracking():
    status_filter = request.args.get('status_filter', '').strip()

    applications = read_applications()
    jobs = read_jobs()
    companies = read_companies()

    # Prepare job and company maps
    job_map = {j['job_id']: j for j in jobs}
    company_map = {c['company_id']: c['company_name'] for c in companies}

    filtered_apps = []
    for app in applications:
        if status_filter and app['status'].lower() != status_filter.lower():
            continue
        job_info = job_map.get(app['job_id'])
        if not job_info:
            continue
        company_name = company_map.get(job_info['company_id'], 'Unknown')
        filtered_apps.append({
            'application_id': app['application_id'],
            'job_title': job_info['title'],
            'company_name': company_name,
            'status': app['status'],
            'applied_date': app['applied_date']
        })

    return render_template('application_tracking.html', applications=filtered_apps)


@app.route('/companies')
def companies_directory():
    search_company = request.args.get('search_company', '').strip()

    companies = read_companies()

    filtered_companies = []
    for c in companies:
        if search_company:
            search_lower = search_company.lower()
            if search_lower not in c['company_name'].lower() and search_lower not in c['industry'].lower():
                continue
        filtered_companies.append(c)

    return render_template('companies.html', companies=filtered_companies)


@app.route('/company/<int:company_id>')
def company_profile(company_id):
    companies = read_companies()
    jobs = read_jobs()

    company = None
    for c in companies:
        if c['company_id'] == company_id:
            company = c
            break

    if not company:
        return "Company not found", 404

    # List jobs for this company
    company_jobs = []
    for job in jobs:
        if job['company_id'] == company_id:
            # status field optional, we skip it here since not in schema
            company_jobs.append({
                'job_id': job['job_id'],
                'title': job['title'],
                'status': ''  # no status given in job
            })

    return render_template('company_profile.html', company=company, jobs=company_jobs)


@app.route('/resumes', methods=['GET', 'POST'])
def resume_management():
    if request.method == 'POST':
        resume_file = request.files.get('resume_file')
        if not resume_file:
            flash('No resume file uploaded.')
            return redirect(url_for('resume_management'))

        # We do not have applicant name or email input in the POST spec so we cannot add a new resume properly.
        # According to the spec, only resume_file is uploaded via POST, no other data. So we must handle that gracefully.
        # We will save the file with a generic unknown applicant and empty summary for now.

        resumes = read_resumes()
        max_id = max((r['resume_id'] for r in resumes), default=0)
        new_id = max_id + 1

        uploads_dir = os.path.join('uploads', 'resumes')
        os.makedirs(uploads_dir, exist_ok=True)

        filename = f'resume_{new_id}_{resume_file.filename}'
        filepath = os.path.join(uploads_dir, filename)
        resume_file.save(filepath)

        today = datetime.today().strftime('%Y-%m-%d')
        new_resume = {
            'resume_id': new_id,
            'applicant_name': 'Unknown',
            'applicant_email': '',
            'filename': filename,
            'upload_date': today,
            'summary': ''
        }
        resumes.append(new_resume)
        write_resumes(resumes)

        flash('Resume uploaded successfully.')

    resumes = read_resumes()
    return render_template('resume_management.html', resumes=resumes)


@app.route('/resume/delete/<int:resume_id>', methods=['POST'])
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

    query_lower = query.lower()

    job_results = []
    for job in jobs:
        if query_lower in job['title'].lower():
            # get company name
            company_name = None
            for c in companies:
                if c['company_id'] == job['company_id']:
                    company_name = c['company_name']
                    break
            if company_name is None:
                company_name = 'Unknown'
            job_results.append({
                'job_id': job['job_id'],
                'title': job['title'],
                'company_name': company_name,
                'location': job['location']
            })

    company_results = []
    for c in companies:
        if query_lower in c['company_name'].lower() or query_lower in c['industry'].lower():
            company_results.append({
                'company_id': c['company_id'],
                'company_name': c['company_name'],
                'industry': c['industry']
            })

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)


if __name__ == '__main__':
    app.run(debug=True)
