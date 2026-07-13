from flask import Flask, render_template, request, redirect, url_for, flash
import os
import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATA_DIR = '.'

# Helper functions to read and write from flat files

def read_jobs():
    jobs = []
    path = os.path.join(DATA_DIR, 'jobs.txt')
    if not os.path.exists(path):
        return jobs
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 9:
                continue
            job = {
                'job_id': parts[0],
                'title': parts[1],
                'company_id': parts[2],
                'location': parts[3],
                'salary_min': parts[4],
                'salary_max': parts[5],
                'category': parts[6],
                'description': parts[7],
                'posted_date': parts[8]
            }
            jobs.append(job)
    return jobs

def write_jobs(jobs):
    path = os.path.join(DATA_DIR, 'jobs.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for job in jobs:
            line = '|'.join([
                job['job_id'], job['title'], job['company_id'], job['location'],
                job['salary_min'], job['salary_max'], job['category'], job['description'], job['posted_date']
            ])
            f.write(line + "\n")

def read_companies():
    companies = []
    path = os.path.join(DATA_DIR, 'companies.txt')
    if not os.path.exists(path):
        return companies
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 6:
                continue
            company = {
                'company_id': parts[0],
                'company_name': parts[1],
                'industry': parts[2],
                'location': parts[3],
                'employee_count': parts[4],
                'description': parts[5]
            }
            companies.append(company)
    return companies

def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split('|')
            if len(parts) < 3:
                continue
            category = {
                'category_id': parts[0],
                'category_name': parts[1],
                'description': parts[2]
            }
            categories.append(category)
    return categories

def read_applications():
    applications = []
    path = os.path.join(DATA_DIR, 'applications.txt')
    if not os.path.exists(path):
        return applications
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split('|')
            if len(parts) < 7:
                continue
            application = {
                'application_id': parts[0],
                'job_id': parts[1],
                'applicant_name': parts[2],
                'applicant_email': parts[3],
                'status': parts[4],
                'applied_date': parts[5],
                'resume_id': parts[6]
            }
            applications.append(application)
    return applications

def write_applications(applications):
    path = os.path.join(DATA_DIR, 'applications.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for app in applications:
            line = '|'.join([
                app['application_id'], app['job_id'], app['applicant_name'], app['applicant_email'],
                app['status'], app['applied_date'], app['resume_id']
            ])
            f.write(line + '\n')

def read_resumes():
    resumes = []
    path = os.path.join(DATA_DIR, 'resumes.txt')
    if not os.path.exists(path):
        return resumes
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split('|')
            if len(parts) < 6:
                continue
            resume = {
                'resume_id': parts[0],
                'applicant_name': parts[1],
                'applicant_email': parts[2],
                'filename': parts[3],
                'upload_date': parts[4],
                'summary': parts[5]
            }
            resumes.append(resume)
    return resumes

def write_resumes(resumes):
    path = os.path.join(DATA_DIR, 'resumes.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for res in resumes:
            line = '|'.join([
                res['resume_id'], res['applicant_name'], res['applicant_email'], res['filename'], res['upload_date'], res['summary']
            ])
            f.write(line + '\n')

def read_job_categories():
    mappings = []
    path = os.path.join(DATA_DIR, 'job_categories.txt')
    if not os.path.exists(path):
        return mappings
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split('|')
            if len(parts) < 3:
                continue
            mapping = {
                'mapping_id': parts[0],
                'job_id': parts[1],
                'category_id': parts[2]
            }
            mappings.append(mapping)
    return mappings


def get_company_by_id(company_id):
    companies = read_companies()
    for c in companies:
        if c['company_id'] == company_id:
            return c
    return None

def get_category_by_name(category_name):
    categories = read_categories()
    for cat in categories:
        if cat['category_name'].lower() == category_name.lower():
            return cat
    return None

def get_job_by_id(job_id):
    jobs = read_jobs()
    for job in jobs:
        if job['job_id'] == job_id:
            return job
    return None

def get_app_by_id(app_id):
    applications = read_applications()
    for app in applications:
        if app['application_id'] == app_id:
            return app
    return None

def get_resume_by_id(resume_id):
    resumes = read_resumes()
    for res in resumes:
        if res['resume_id'] == resume_id:
            return res
    return None

# Routes Implementation

@app.route('/')
def dashboard():
    # Show featured jobs (latest 3 posted)
    jobs = sorted(read_jobs(), key=lambda x: x['posted_date'], reverse=True)[:3]
    companies = read_companies()
    company_map = {c['company_id']: c['company_name'] for c in companies}
    for job in jobs:
        job['company_name'] = company_map.get(job['company_id'], 'Unknown')
    return render_template('dashboard.html', jobs=jobs)

@app.route('/jobs')
def job_listings():
    jobs = read_jobs()
    categories = read_categories()

    # Filters
    search_query = request.args.get('search_input', '').strip().lower()
    category_filter = request.args.get('category_filter', '')
    location_filter = request.args.get('location_filter', '')

    filtered_jobs = []
    for job in jobs:
        matches_search = search_query in job['title'].lower() or search_query in job['location'].lower() or search_query in get_company_by_id(job['company_id'])['company_name'].lower() if get_company_by_id(job['company_id']) else False
        matches_category = (not category_filter) or (job['category'].lower() == category_filter.lower())
        matches_location = (not location_filter) or (location_filter.lower() == job['location'].lower()) or (location_filter.lower() == 'remote' and job['location'].lower() == 'remote') or (location_filter.lower() == 'on-site' and job['location'].lower() != 'remote' and job['location'].lower() != 'hybrid') or (location_filter.lower() == 'hybrid' and job['location'].lower() == 'hybrid')

        if (not search_query or matches_search) and matches_category and matches_location:
            filtered_jobs.append(job)

    return render_template('job_listings.html', jobs=filtered_jobs, categories=categories, search_query=search_query, category_filter=category_filter, location_filter=location_filter)

@app.route('/job/<job_id>')
def job_details(job_id):
    job = get_job_by_id(job_id)
    if not job:
        flash('Job not found.')
        return redirect(url_for('dashboard'))
    company = get_company_by_id(job['company_id'])
    return render_template('job_details.html', job=job, company=company)

@app.route('/apply/<job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    job = get_job_by_id(job_id)
    if not job:
        flash('Job not found.')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()
        cover_letter = request.form.get('cover_letter', '').strip()
        resume_file = request.files.get('resume_upload')

        if not applicant_name or not applicant_email or not cover_letter or not resume_file:
            flash('Please fill all fields and upload a resume.')
            return redirect(request.url)

        # Save resume file
        filename = secure_filename(resume_file.filename)
        resume_path = os.path.join('uploads', filename)
        os.makedirs('uploads', exist_ok=True)
        resume_file.save(resume_path)

        # Add resume entry
        resumes = read_resumes()
        new_resume_id = str(int(resumes[-1]['resume_id']) + 1) if resumes else '1'
        upload_date = datetime.date.today().isoformat()
        resume_summary = cover_letter[:100].replace('\n', ' ').replace('|', ' ')
        resumes.append({
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': resume_summary
        })
        write_resumes(resumes)

        # Add application entry
        applications = read_applications()
        new_app_id = str(int(applications[-1]['application_id']) + 1) if applications else '1'
        applied_date = upload_date
        applications.append({
            'application_id': new_app_id,
            'job_id': job_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': 'Applied',
            'applied_date': applied_date,
            'resume_id': new_resume_id
        })
        write_applications(applications)

        flash('Application submitted successfully.')
        return redirect(url_for('application_tracking'))

    return render_template('application_form.html', job=job)

@app.route('/applications', methods=['GET'])
def application_tracking():
    applications = read_applications()
    jobs = read_jobs()
    companies = read_companies()

    status_filter = request.args.get('status_filter', 'All')
    filtered_apps = []

    for app in applications:
        if status_filter == 'All' or app['status'] == status_filter:
            filtered_apps.append(app)

    jobs_map = {job['job_id']: job for job in jobs}
    companies_map = {comp['company_id']: comp for comp in companies}

    # Enrich applications with job title and company name
    for app in filtered_apps:
        job = jobs_map.get(app['job_id'])
        if job:
            app['job_title'] = job['title']
            company = companies_map.get(job['company_id'])
            app['company_name'] = company['company_name'] if company else 'Unknown'
        else:
            app['job_title'] = 'Unknown'
            app['company_name'] = 'Unknown'

    return render_template('application_tracking.html', applications=filtered_apps, status_filter=status_filter)

@app.route('/application/<app_id>')
def view_application(app_id):
    application = get_app_by_id(app_id)
    if not application:
        flash('Application not found.')
        return redirect(url_for('application_tracking'))
    job = get_job_by_id(application['job_id'])
    company = get_company_by_id(job['company_id']) if job else None
    resume = get_resume_by_id(application['resume_id'])
    return render_template('view_application.html', application=application, job=job, company=company, resume=resume)

@app.route('/companies')
def companies_directory():
    companies = read_companies()
    search_query = request.args.get('search_company_input', '').strip().lower()

    if search_query:
        filtered_companies = []
        for company in companies:
            if search_query in company['company_name'].lower() or search_query in company['industry'].lower():
                filtered_companies.append(company)
    else:
        filtered_companies = companies

    return render_template('companies_directory.html', companies=filtered_companies, search_query=search_query)

@app.route('/company/<company_id>')
def company_profile(company_id):
    company = get_company_by_id(company_id)
    if not company:
        flash('Company not found.')
        return redirect(url_for('companies_directory'))

    jobs = read_jobs()
    company_jobs = [job for job in jobs if job['company_id'] == company_id]

    return render_template('company_profile.html', company=company, company_jobs=company_jobs)

@app.route('/resumes', methods=['GET', 'POST'])
def resume_management():
    resumes = read_resumes()

    if request.method == 'POST':
        if 'upload_resume_button' in request.form:
            resume_file = request.files.get('resume_file_input')
            if resume_file and resume_file.filename != '':
                filename = secure_filename(resume_file.filename)
                resume_path = os.path.join('uploads', filename)
                os.makedirs('uploads', exist_ok=True)
                resume_file.save(resume_path)

                # Add resume entry
                new_resume_id = str(int(resumes[-1]['resume_id']) + 1) if resumes else '1'
                upload_date = datetime.date.today().isoformat()
                resumes.append({
                    'resume_id': new_resume_id,
                    'applicant_name': 'Unknown',
                    'applicant_email': 'unknown@example.com',
                    'filename': filename,
                    'upload_date': upload_date,
                    'summary': ''
                })
                write_resumes(resumes)
                flash('Resume uploaded successfully.')
                return redirect(url_for('resume_management'))
            else:
                flash('No file selected for upload.')

        elif 'delete_resume_button' in request.form:
            delete_id = request.form.get('delete_resume_button')
            resumes = [res for res in resumes if res['resume_id'] != delete_id]
            write_resumes(resumes)
            flash('Resume deleted successfully.')
            return redirect(url_for('resume_management'))

    return render_template('resume_management.html', resumes=resumes)

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
            company = get_company_by_id(job['company_id'])
            if q in job['title'].lower() or (company and q in company['company_name'].lower()) or q in job['location'].lower():
                job_results.append(job)
        for company in companies:
            if q in company['company_name'].lower() or q in company['industry'].lower():
                company_results.append(company)

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)

if __name__ == '__main__':
    app.run(debug=True)
