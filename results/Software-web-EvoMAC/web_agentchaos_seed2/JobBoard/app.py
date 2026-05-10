'''
Backend implementation for the 'JobBoard' web application.
- Uses Flask to serve pages and handle routing.
- Reads and writes data from/to local text files in 'data' directory.
- Supports all 9 pages as per requirements.
- No authentication; all features directly accessible.
- Website starts at '/' route serving the Dashboard page.
'''
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from datetime import datetime
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = 'jobboard_secret_key'  # Needed for flashing messages
DATA_DIR = 'data'
UPLOADS_DIR = 'uploads'
# Ensure uploads directory exists
os.makedirs(UPLOADS_DIR, exist_ok=True)
# Helper functions to read and write data files
def read_jobs():
    jobs = []
    path = os.path.join(DATA_DIR, 'jobs.txt')
    if not os.path.isfile(path):
        return jobs
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 9:
                continue
            job = {
                'job_id': parts[0],
                'title': parts[1],
                'company_id': parts[2],
                'location': parts[3],
                'salary_min': int(parts[4]),
                'salary_max': int(parts[5]),
                'category': parts[6],
                'description': parts[7],
                'posted_date': parts[8],
            }
            jobs.append(job)
    return jobs
def read_companies():
    companies = []
    path = os.path.join(DATA_DIR, 'companies.txt')
    if not os.path.isfile(path):
        return companies
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            company = {
                'company_id': parts[0],
                'company_name': parts[1],
                'industry': parts[2],
                'location': parts[3],
                'employee_count': parts[4],
                'description': parts[5],
            }
            companies.append(company)
    return companies
def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.isfile(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            category = {
                'category_id': parts[0],
                'category_name': parts[1],
                'description': parts[2],
            }
            categories.append(category)
    return categories
def read_applications():
    applications = []
    path = os.path.join(DATA_DIR, 'applications.txt')
    if not os.path.isfile(path):
        return applications
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            application = {
                'application_id': parts[0],
                'job_id': parts[1],
                'applicant_name': parts[2],
                'applicant_email': parts[3],
                'status': parts[4],
                'applied_date': parts[5],
                'resume_id': parts[6],
            }
            applications.append(application)
    return applications
def read_resumes():
    resumes = []
    path = os.path.join(DATA_DIR, 'resumes.txt')
    if not os.path.isfile(path):
        return resumes
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            resume = {
                'resume_id': parts[0],
                'applicant_name': parts[1],
                'applicant_email': parts[2],
                'filename': parts[3],
                'upload_date': parts[4],
                'summary': parts[5],
            }
            resumes.append(resume)
    return resumes
def read_job_categories():
    mappings = []
    path = os.path.join(DATA_DIR, 'job_categories.txt')
    if not os.path.isfile(path):
        return mappings
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            mapping = {
                'mapping_id': parts[0],
                'job_id': parts[1],
                'category_id': parts[2],
            }
            mappings.append(mapping)
    return mappings
def write_applications(applications):
    path = os.path.join(DATA_DIR, 'applications.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for app in applications:
            line = '|'.join([
                app['application_id'],
                app['job_id'],
                app['applicant_name'],
                app['applicant_email'],
                app['status'],
                app['applied_date'],
                app['resume_id'],
            ])
            f.write(line + '\n')
def write_resumes(resumes):
    path = os.path.join(DATA_DIR, 'resumes.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for res in resumes:
            line = '|'.join([
                res['resume_id'],
                res['applicant_name'],
                res['applicant_email'],
                res['filename'],
                res['upload_date'],
                res['summary'],
            ])
            f.write(line + '\n')
def write_jobs(jobs):
    path = os.path.join(DATA_DIR, 'jobs.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for job in jobs:
            line = '|'.join([
                job['job_id'],
                job['title'],
                job['company_id'],
                job['location'],
                str(job['salary_min']),
                str(job['salary_max']),
                job['category'],
                job['description'],
                job['posted_date'],
            ])
            f.write(line + '\n')
def write_companies(companies):
    path = os.path.join(DATA_DIR, 'companies.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for comp in companies:
            line = '|'.join([
                comp['company_id'],
                comp['company_name'],
                comp['industry'],
                comp['location'],
                comp['employee_count'],
                comp['description'],
            ])
            f.write(line + '\n')
def write_job_categories(mappings):
    path = os.path.join(DATA_DIR, 'job_categories.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for m in mappings:
            line = '|'.join([
                m['mapping_id'],
                m['job_id'],
                m['category_id'],
            ])
            f.write(line + '\n')
# Utility functions
def get_company_by_id(company_id):
    companies = read_companies()
    for c in companies:
        if c['company_id'] == company_id:
            return c
    return None
def get_job_by_id(job_id):
    jobs = read_jobs()
    for j in jobs:
        if j['job_id'] == job_id:
            return j
    return None
def get_category_name_by_category(category_name):
    # category_name is string like "Technology"
    categories = read_categories()
    for c in categories:
        if c['category_name'] == category_name:
            return c['category_name']
    return None
def get_resume_by_id(resume_id):
    resumes = read_resumes()
    for r in resumes:
        if r['resume_id'] == resume_id:
            return r
    return None
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_key])
            if val > max_id:
                max_id = val
        except:
            continue
    return str(max_id + 1)
# Routes
@app.route('/')
def dashboard():
    jobs = read_jobs()
    companies = read_companies()
    # Featured jobs: let's pick the 3 most recent jobs by posted_date descending
    featured_jobs = sorted(jobs, key=lambda x: x['posted_date'], reverse=True)[:3]
    # For each job, add company name
    for job in featured_jobs:
        company = get_company_by_id(job['company_id'])
        job['company_name'] = company['company_name'] if company else 'Unknown'
    return render_template('dashboard.html', featured_jobs=featured_jobs)
@app.route('/jobs')
def job_listings():
    jobs = read_jobs()
    companies = read_companies()
    categories = read_categories()
    # Get filters from query parameters
    search_query = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', '').strip()
    location_filter = request.args.get('location', '').strip()
    filtered_jobs = []
    for job in jobs:
        # Filter by search query in title, company name, or location
        company = get_company_by_id(job['company_id'])
        company_name = company['company_name'] if company else ''
        if search_query:
            if (search_query not in job['title'].lower() and
                search_query not in company_name.lower() and
                search_query not in job['location'].lower()):
                continue
        # Filter by category
        if category_filter and category_filter != 'All':
            if job['category'] != category_filter:
                continue
        # Filter by location
        if location_filter and location_filter != 'All':
            if location_filter == 'Remote':
                if job['location'].lower() != 'remote':
                    continue
            elif location_filter == 'On-site':
                if job['location'].lower() == 'remote':
                    continue
            elif location_filter == 'Hybrid':
                # For simplicity, treat 'Hybrid' as location containing 'Hybrid' (if any)
                if 'hybrid' not in job['location'].lower():
                    continue
        filtered_jobs.append(job)
    # Add company name to each job
    for job in filtered_jobs:
        company = get_company_by_id(job['company_id'])
        job['company_name'] = company['company_name'] if company else 'Unknown'
    return render_template('job_listings.html',
                           jobs=filtered_jobs,
                           categories=categories,
                           selected_category=category_filter,
                           selected_location=location_filter,
                           search_query=search_query)
@app.route('/jobs/<job_id>')
def job_details(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return "Job not found", 404
    company = get_company_by_id(job['company_id'])
    company_name = company['company_name'] if company else 'Unknown'
    return render_template('job_details.html', job=job, company_name=company_name)
@app.route('/apply/<job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return "Job not found", 404
    if request.method == 'POST':
        applicant_name = request.form.get('applicant-name', '').strip()
        applicant_email = request.form.get('applicant-email', '').strip()
        cover_letter = request.form.get('cover-letter', '').strip()
        resume_file = request.files.get('resume-upload')
        if not applicant_name or not applicant_email or not resume_file:
            flash('Please fill in all required fields and upload a resume.')
            return redirect(request.url)
        # Save resume file
        filename = secure_filename(resume_file.filename)
        if filename == '':
            flash('Invalid resume file.')
            return redirect(request.url)
        save_path = os.path.join(UPLOADS_DIR, filename)
        # If file exists, rename to avoid overwrite
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(save_path):
            filename = f"{base}_{counter}{ext}"
            save_path = os.path.join(UPLOADS_DIR, filename)
            counter += 1
        resume_file.save(save_path)
        # Read resumes and applications
        resumes = read_resumes()
        applications = read_applications()
        # Create new resume entry
        new_resume_id = get_next_id(resumes, 'resume_id')
        upload_date = datetime.now().strftime('%Y-%m-%d')
        # Summary: first 100 chars of cover letter or empty if none
        summary = cover_letter[:100] if cover_letter else ''
        new_resume = {
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': summary,
        }
        resumes.append(new_resume)
        write_resumes(resumes)
        # Create new application entry
        new_application_id = get_next_id(applications, 'application_id')
        applied_date = datetime.now().strftime('%Y-%m-%d')
        new_application = {
            'application_id': new_application_id,
            'job_id': job_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': 'Applied',
            'applied_date': applied_date,
            'resume_id': new_resume_id,
        }
        applications.append(new_application)
        write_applications(applications)
        flash('Application submitted successfully!')
        return redirect(url_for('application_tracking'))
    return render_template('application_form.html', job=job)
@app.route('/applications')
def application_tracking():
    applications = read_applications()
    jobs = read_jobs()
    companies = read_companies()
    status_filter = request.args.get('status', 'All')
    filtered_apps = []
    for app_ in applications:
        if status_filter != 'All' and app_['status'] != status_filter:
            continue
        # Add job title and company name
        job = get_job_by_id(app_['job_id'])
        if not job:
            continue
        company = get_company_by_id(job['company_id'])
        company_name = company['company_name'] if company else 'Unknown'
        app_copy = app_.copy()
        app_copy['job_title'] = job['title']
        app_copy['company_name'] = company_name
        filtered_apps.append(app_copy)
    return render_template('application_tracking.html',
                           applications=filtered_apps,
                           selected_status=status_filter)
@app.route('/applications/<application_id>')
def application_details(application_id):
    applications = read_applications()
    application = None
    for app_ in applications:
        if app_['application_id'] == application_id:
            application = app_
            break
    if not application:
        return "Application not found", 404
    job = get_job_by_id(application['job_id'])
    company = get_company_by_id(job['company_id']) if job else None
    resume = get_resume_by_id(application['resume_id'])
    return render_template('application_details.html',
                           application=application,
                           job=job,
                           company=company,
                           resume=resume)
@app.route('/companies')
def companies_directory():
    companies = read_companies()
    search_query = request.args.get('search', '').strip().lower()
    filtered_companies = []
    for comp in companies:
        if search_query:
            if (search_query not in comp['company_name'].lower() and
                search_query not in comp['industry'].lower()):
                continue
        filtered_companies.append(comp)
    return render_template('companies_directory.html',
                           companies=filtered_companies,
                           search_query=search_query)
@app.route('/companies/<company_id>')
def company_profile(company_id):
    company = get_company_by_id(company_id)
    if not company:
        return "Company not found", 404
    jobs = read_jobs()
    company_jobs = [job for job in jobs if job['company_id'] == company_id]
    # Add status indicators? The requirement says status indicators for jobs in company profile.
    # Since jobs don't have status, we can show posted_date or just show jobs.
    return render_template('company_profile.html',
                           company=company,
                           company_jobs=company_jobs)
@app.route('/resumes', methods=['GET', 'POST'])
def resume_management():
    resumes = read_resumes()
    if request.method == 'POST':
        # Handle resume upload
        resume_file = request.files.get('resume-file-input')
        applicant_name = request.form.get('applicant-name', '').strip()
        applicant_email = request.form.get('applicant-email', '').strip()
        summary = request.form.get('summary', '').strip()
        if not resume_file or resume_file.filename == '':
            flash('No resume file selected.')
            return redirect(request.url)
        if not applicant_name or not applicant_email:
            flash('Applicant name and email are required.')
            return redirect(request.url)
        filename = secure_filename(resume_file.filename)
        save_path = os.path.join(UPLOADS_DIR, filename)
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(save_path):
            filename = f"{base}_{counter}{ext}"
            save_path = os.path.join(UPLOADS_DIR, filename)
            counter += 1
        resume_file.save(save_path)
        new_resume_id = get_next_id(resumes, 'resume_id')
        upload_date = datetime.now().strftime('%Y-%m-%d')
        new_resume = {
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': summary,
        }
        resumes.append(new_resume)
        write_resumes(resumes)
        flash('Resume uploaded successfully.')
        return redirect(url_for('resume_management'))
    return render_template('resume_management.html', resumes=resumes)
@app.route('/resumes/delete/<resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = read_resumes()
    resume_to_delete = None
    for r in resumes:
        if r['resume_id'] == resume_id:
            resume_to_delete = r
            break
    if not resume_to_delete:
        flash('Resume not found.')
        return redirect(url_for('resume_management'))
    # Remove resume file from uploads folder
    filepath = os.path.join(UPLOADS_DIR, resume_to_delete['filename'])
    if os.path.exists(filepath):
        os.remove(filepath)
    # Remove from resumes list and write back
    resumes = [r for r in resumes if r['resume_id'] != resume_id]
    write_resumes(resumes)
    # Also remove applications that use this resume? Not specified, so we keep applications.
    flash('Resume deleted successfully.')
    return redirect(url_for('resume_management'))
@app.route('/search')
def search_results():
    query = request.args.get('q', '').strip().lower()
    jobs = read_jobs()
    companies = read_companies()
    job_results = []
    company_results = []
    if query:
        for job in jobs:
            company = get_company_by_id(job['company_id'])
            company_name = company['company_name'] if company else ''
            if (query in job['title'].lower() or
                query in company_name.lower() or
                query in job['location'].lower()):
                job_results.append(job)
        for comp in companies:
            if (query in comp['company_name'].lower() or
                query in comp['industry'].lower()):
                company_results.append(comp)
    return render_template('search_results.html',
                           query=query,
                           job_results=job_results,
                           company_results=company_results,
                           no_results=(len(job_results) == 0 and len(company_results) == 0))
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Serve uploaded resume files
    return send_from_directory(UPLOADS_DIR, filename)
# Navigation routes for buttons that redirect to other pages
@app.route('/go_to_jobs')
def go_to_jobs():
    return redirect(url_for('job_listings'))
@app.route('/go_to_applications')
def go_to_applications():
    return redirect(url_for('application_tracking'))
@app.route('/go_to_companies')
def go_to_companies():
    return redirect(url_for('companies_directory'))
@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))
@app.route('/back_to_companies')
def back_to_companies():
    return redirect(url_for('companies_directory'))
if __name__ == '__main__':
    app.run(port=5000, debug=True)