'''
Main backend Python application file for the JobBoard web application.
Handles routing, data reading/writing from/to local text files in the `data/` directory,
and serves the HTML templates. Implements all functionalities including browsing jobs,
submitting resumes, tracking applications, viewing company profiles, managing job applications,
and search. No authentication required; all features are directly accessible.
'''
import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
app = Flask(__name__)
app.secret_key = 'jobboard_secret_key'  # Needed for flashing messages
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads', 'resumes')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
# Utility functions for file operations and data parsing
def read_file_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines
def write_file_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
def parse_jobs():
    jobs = []
    lines = read_file_lines('jobs.txt')
    for line in lines:
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
            'posted_date': parts[8]
        }
        jobs.append(job)
    return jobs
def parse_companies():
    companies = []
    lines = read_file_lines('companies.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) != 6:
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
def parse_categories():
    categories = []
    lines = read_file_lines('categories.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) != 3:
            continue
        category = {
            'category_id': parts[0],
            'category_name': parts[1],
            'description': parts[2]
        }
        categories.append(category)
    return categories
def parse_applications():
    applications = []
    lines = read_file_lines('applications.txt')
    for line in lines:
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
            'resume_id': parts[6]
        }
        applications.append(application)
    return applications
def parse_resumes():
    resumes = []
    lines = read_file_lines('resumes.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) != 6:
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
def parse_job_categories():
    mappings = []
    lines = read_file_lines('job_categories.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) != 3:
            continue
        mapping = {
            'mapping_id': parts[0],
            'job_id': parts[1],
            'category_id': parts[2]
        }
        mappings.append(mapping)
    return mappings
def get_company_by_id(company_id):
    companies = parse_companies()
    for c in companies:
        if c['company_id'] == company_id:
            return c
    return None
def get_job_by_id(job_id):
    jobs = parse_jobs()
    for j in jobs:
        if j['job_id'] == job_id:
            return j
    return None
def get_category_name_by_id(category_id):
    categories = parse_categories()
    for c in categories:
        if c['category_id'] == category_id:
            return c['category_name']
    return None
def get_resume_by_id(resume_id):
    resumes = parse_resumes()
    for r in resumes:
        if r['resume_id'] == resume_id:
            return r
    return None
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def generate_new_id(items, id_field):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_field])
            if val > max_id:
                max_id = val
        except Exception:
            continue
    return str(max_id + 1)
# ROUTES
@app.route('/')
def dashboard():
    # Show featured jobs (e.g., latest 3 jobs by posted_date descending)
    jobs = parse_jobs()
    jobs_sorted = sorted(jobs, key=lambda x: x['posted_date'], reverse=True)
    featured_jobs = jobs_sorted[:3]
    # Enrich featured jobs with company name
    for job in featured_jobs:
        company = get_company_by_id(job['company_id'])
        job['company_name'] = company['company_name'] if company else 'Unknown'
    # Pass URLs for navigation buttons to template for JS usage
    urls = {
        'jobs': url_for('job_listings'),
        'applications': url_for('application_tracking'),
        'companies': url_for('companies_directory')
    }
    return render_template('dashboard.html', featured_jobs=featured_jobs, urls=urls)
@app.route('/jobs')
def job_listings():
    jobs = parse_jobs()
    companies = {c['company_id']: c for c in parse_companies()}
    categories = parse_categories()
    # Get filters from query parameters
    search_query = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', '')
    location_filter = request.args.get('location', '')
    filtered_jobs = []
    for job in jobs:
        # Filter by search query (title, company name, location)
        company_name = companies.get(job['company_id'], {}).get('company_name', '').lower()
        if search_query:
            if (search_query not in job['title'].lower() and
                search_query not in company_name and
                search_query not in job['location'].lower()):
                continue
        # Filter by category
        if category_filter and category_filter != 'All':
            if job['category'] != category_filter:
                continue
        # Filter by location
        if location_filter and location_filter != 'All':
            # Location filter values: Remote, On-site, Hybrid
            # We check if job['location'] matches the filter roughly
            loc = job['location'].lower()
            if location_filter == 'Remote' and 'remote' not in loc:
                continue
            elif location_filter == 'On-site' and 'remote' in loc:
                continue
            elif location_filter == 'Hybrid':
                # Hybrid means both remote and on-site possible, but we have no explicit data
                # So we skip filtering for hybrid or treat as no filter
                pass
        filtered_jobs.append(job)
    # Enrich jobs with company name
    for job in filtered_jobs:
        company = companies.get(job['company_id'])
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
        flash('Job not found.', 'error')
        return redirect(url_for('job_listings'))
    company = get_company_by_id(job['company_id'])
    company_name = company['company_name'] if company else 'Unknown'
    return render_template('job_details.html', job=job, company_name=company_name)
@app.route('/apply/<job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    job = get_job_by_id(job_id)
    if not job:
        flash('Job not found.', 'error')
        return redirect(url_for('job_listings'))
    if request.method == 'POST':
        applicant_name = request.form.get('applicant-name', '').strip()
        applicant_email = request.form.get('applicant-email', '').strip()
        cover_letter = request.form.get('cover-letter', '').strip()
        resume_file = request.files.get('resume-upload')
        if not applicant_name or not applicant_email or not resume_file or resume_file.filename == '':
            flash('Please fill all required fields and upload a resume.', 'error')
            return render_template('application_form.html', job=job)
        if not allowed_file(resume_file.filename):
            flash('Unsupported file type for resume. Allowed types: pdf, doc, docx, txt.', 'error')
            return render_template('application_form.html', job=job)
        # Save resume file
        filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{resume_file.filename}"
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        resume_file.save(save_path)
        # Add resume metadata to resumes.txt
        resumes = parse_resumes()
        new_resume_id = generate_new_id(resumes, 'resume_id')
        upload_date = datetime.datetime.now().strftime('%Y-%m-%d')
        summary = cover_letter[:100].replace('\n', ' ')  # simple summary from cover letter
        resumes.append({
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': summary
        })
        # Write resumes back
        lines = []
        for r in resumes:
            line = '|'.join([r['resume_id'], r['applicant_name'], r['applicant_email'], r['filename'], r['upload_date'], r['summary']])
            lines.append(line)
        write_file_lines('resumes.txt', lines)
        # Add application to applications.txt
        applications = parse_applications()
        new_application_id = generate_new_id(applications, 'application_id')
        applied_date = datetime.datetime.now().strftime('%Y-%m-%d')
        status = 'Applied'
        applications.append({
            'application_id': new_application_id,
            'job_id': job_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': status,
            'applied_date': applied_date,
            'resume_id': new_resume_id
        })
        # Write applications back
        lines = []
        for a in applications:
            line = '|'.join([a['application_id'], a['job_id'], a['applicant_name'], a['applicant_email'], a['status'], a['applied_date'], a['resume_id']])
            lines.append(line)
        write_file_lines('applications.txt', lines)
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('job_listings'))
    return render_template('application_form.html', job=job)
@app.route('/applications')
def application_tracking():
    applications = parse_applications()
    jobs = {j['job_id']: j for j in parse_jobs()}
    companies = {c['company_id']: c for c in parse_companies()}
    status_filter = request.args.get('status', 'All')
    filtered_apps = []
    for app_ in applications:
        if status_filter != 'All' and app_['status'] != status_filter:
            continue
        job = jobs.get(app_['job_id'])
        if not job:
            continue
        company = companies.get(job['company_id'])
        filtered_apps.append({
            'application_id': app_['application_id'],
            'job_title': job['title'],
            'company_name': company['company_name'] if company else 'Unknown',
            'status': app_['status'],
            'applied_date': app_['applied_date']
        })
    return render_template('application_tracking.html',
                           applications=filtered_apps,
                           selected_status=status_filter)
@app.route('/applications/<application_id>')
def view_application(application_id):
    applications = parse_applications()
    application = None
    for a in applications:
        if a['application_id'] == application_id:
            application = a
            break
    if not application:
        flash('Application not found.', 'error')
        return redirect(url_for('application_tracking'))
    job = get_job_by_id(application['job_id'])
    company = get_company_by_id(job['company_id']) if job else None
    resume = get_resume_by_id(application['resume_id'])
    return render_template('application_tracking.html',
                           applications=[{
                               'application_id': application['application_id'],
                               'job_title': job['title'] if job else 'Unknown',
                               'company_name': company['company_name'] if company else 'Unknown',
                               'status': application['status'],
                               'applied_date': application['applied_date'],
                               'applicant_name': application['applicant_name'],
                               'applicant_email': application['applicant_email'],
                               'resume': resume,
                               'cover_letter': None  # cover letter not stored separately
                           }],
                           selected_status='All',
                           single_view=True)
@app.route('/companies')
def companies_directory():
    companies = parse_companies()
    search_query = request.args.get('search', '').strip().lower()
    filtered_companies = []
    for c in companies:
        if search_query:
            if search_query not in c['company_name'].lower() and search_query not in c['industry'].lower():
                continue
        filtered_companies.append(c)
    return render_template('companies_directory.html',
                           companies=filtered_companies,
                           search_query=search_query)
@app.route('/companies/<company_id>')
def company_profile(company_id):
    company = get_company_by_id(company_id)
    if not company:
        flash('Company not found.', 'error')
        return redirect(url_for('companies_directory'))
    jobs = parse_jobs()
    company_jobs = [job for job in jobs if job['company_id'] == company_id]
    # Sort jobs by posted_date descending
    company_jobs = sorted(company_jobs, key=lambda x: x['posted_date'], reverse=True)
    return render_template('company_profile.html',
                           company=company,
                           jobs=company_jobs)
@app.route('/resumes', methods=['GET', 'POST'])
def resume_management():
    resumes = parse_resumes()
    if request.method == 'POST':
        # Upload new resume
        if 'resume-file-input' not in request.files:
            flash('No file part in the request.', 'error')
            return redirect(url_for('resume_management'))
        file = request.files['resume-file-input']
        if file.filename == '':
            flash('No selected file.', 'error')
            return redirect(url_for('resume_management'))
        if not allowed_file(file.filename):
            flash('Unsupported file type for resume. Allowed types: pdf, doc, docx, txt.', 'error')
            return redirect(url_for('resume_management'))
        # Save file
        filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        # Add to resumes.txt
        new_resume_id = generate_new_id(resumes, 'resume_id')
        upload_date = datetime.datetime.now().strftime('%Y-%m-%d')
        # We do not have applicant info here, so leave blank or generic
        applicant_name = 'Unknown'
        applicant_email = 'unknown@example.com'
        summary = ''
        resumes.append({
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': summary
        })
        lines = []
        for r in resumes:
            line = '|'.join([r['resume_id'], r['applicant_name'], r['applicant_email'], r['filename'], r['upload_date'], r['summary']])
            lines.append(line)
        write_file_lines('resumes.txt', lines)
        flash('Resume uploaded successfully.', 'success')
        return redirect(url_for('resume_management'))
    return render_template('resume_management.html', resumes=resumes)
@app.route('/resumes/delete/<resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = parse_resumes()
    resume_to_delete = None
    for r in resumes:
        if r['resume_id'] == resume_id:
            resume_to_delete = r
            break
    if not resume_to_delete:
        flash('Resume not found.', 'error')
        return redirect(url_for('resume_management'))
    # Remove file from uploads folder
    filepath = os.path.join(UPLOAD_FOLDER, resume_to_delete['filename'])
    if os.path.exists(filepath):
        os.remove(filepath)
    # Remove from resumes list
    resumes = [r for r in resumes if r['resume_id'] != resume_id]
    # Write back updated resumes
    lines = []
    for r in resumes:
        line = '|'.join([r['resume_id'], r['applicant_name'], r['applicant_email'], r['filename'], r['upload_date'], r['summary']])
        lines.append(line)
    write_file_lines('resumes.txt', lines)
    flash('Resume deleted successfully.', 'success')
    return redirect(url_for('resume_management'))
@app.route('/search')
def search_results():
    query = request.args.get('q', '').strip().lower()
    jobs = parse_jobs()
    companies = parse_companies()
    job_results = []
    company_results = []
    if query:
        # Search jobs by title, company name, location
        companies_dict = {c['company_id']: c for c in companies}
        for job in jobs:
            company_name = companies_dict.get(job['company_id'], {}).get('company_name', '').lower()
            if (query in job['title'].lower() or
                query in company_name or
                query in job['location'].lower()):
                job_results.append(job)
        # Search companies by name or industry
        for company in companies:
            if query in company['company_name'].lower() or query in company['industry'].lower():
                company_results.append(company)
    no_results = (len(job_results) == 0 and len(company_results) == 0)
    return render_template('search_results.html',
                           query=query,
                           job_results=job_results,
                           company_results=company_results,
                           no_results=no_results)
# Static route for uploaded resumes (if needed)
@app.route('/uploads/resumes/<filename>')
def uploaded_resume(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
# Navigation routes for buttons that go back to dashboard or other pages
@app.route('/back-to-dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))
@app.route('/back-to-companies')
def back_to_companies():
    return redirect(url_for('companies_directory'))
# Run the app
if __name__ == '__main__':
    app.run(port=5000, debug=True)