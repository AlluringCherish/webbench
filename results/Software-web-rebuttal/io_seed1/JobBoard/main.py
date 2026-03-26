'''
Main Flask application for the JobBoard web application.
Provides routes for all pages including the Dashboard as the root page.
Handles data loading from local text files and file uploads.
'''
import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'jobboard_secret_key'  # Needed for flashing messages
UPLOAD_FOLDER = 'uploads/resumes'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
DATA_DIR = 'data'
def read_file_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]
def write_file_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')
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
    for company in companies:
        if company['company_id'] == company_id:
            return company
    return None
def get_job_by_id(job_id):
    jobs = parse_jobs()
    for job in jobs:
        if job['job_id'] == job_id:
            return job
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
        except ValueError:
            continue
    return str(max_id + 1)
def get_featured_jobs():
    jobs = parse_jobs()
    companies = parse_companies()
    # Sort jobs by posted_date descending, get top 3
    sorted_jobs = sorted(jobs, key=lambda x: x['posted_date'], reverse=True)
    featured_jobs = sorted_jobs[:3]
    # Attach company name to each job
    for job in featured_jobs:
        company = get_company_by_id(job['company_id'])
        job['company_name'] = company['company_name'] if company else 'Unknown'
    return featured_jobs
@app.route('/')
def dashboard():
    featured_jobs = get_featured_jobs()
    return render_template('dashboard.html', featured_jobs=featured_jobs)
@app.route('/jobs')
def job_listings():
    jobs = parse_jobs()
    companies = parse_companies()
    categories = parse_categories()
    search_query = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', '')
    location_filter = request.args.get('location', '')
    filtered_jobs = []
    for job in jobs:
        company = get_company_by_id(job['company_id'])
        job['company_name'] = company['company_name'] if company else 'Unknown'
        # Search filter
        if search_query:
            if (search_query not in job['title'].lower() and
                search_query not in job['company_name'].lower() and
                search_query not in job['location'].lower()):
                continue
        # Category filter
        if category_filter and category_filter != 'All':
            if job['category'].lower() != category_filter.lower():
                continue
        # Location filter
        if location_filter and location_filter != 'All':
            loc = job['location'].lower()
            loc_filter = location_filter.lower()
            if loc_filter == 'remote' and 'remote' not in loc:
                continue
            elif loc_filter == 'on-site' and ('remote' in loc or 'hybrid' in loc):
                continue
            elif loc_filter == 'hybrid' and 'hybrid' not in loc:
                continue
        filtered_jobs.append(job)
    return render_template('job_listings.html', jobs=filtered_jobs, categories=categories)
@app.route('/job/<job_id>')
def job_details(job_id):
    job = get_job_by_id(job_id)
    if not job:
        abort(404, description="Job not found")
    company = get_company_by_id(job['company_id'])
    job['company_name'] = company['company_name'] if company else 'Unknown'
    return render_template('job_details.html', job=job)
@app.route('/apply/<job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    job = get_job_by_id(job_id)
    if not job:
        abort(404, description="Job not found")
    if request.method == 'POST':
        applicant_name = request.form.get('applicant-name', '').strip()
        applicant_email = request.form.get('applicant-email', '').strip()
        cover_letter = request.form.get('cover-letter', '').strip()
        resume_file = request.files.get('resume-upload')
        if not applicant_name or not applicant_email or not resume_file:
            flash('Please fill in all required fields and upload a resume.')
            return redirect(request.url)
        if not allowed_file(resume_file.filename):
            flash('Unsupported file type for resume. Allowed types: pdf, doc, docx, txt.')
            return redirect(request.url)
        # Save resume file with unique filename
        timestamp_str = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{applicant_name.replace(' ', '_')}_{timestamp_str}_{resume_file.filename}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume_file.save(save_path)
        # Update resumes.txt
        resumes = parse_resumes()
        new_resume_id = generate_new_id(resumes, 'resume_id')
        upload_date = datetime.now().strftime('%Y-%m-%d')
        summary = cover_letter.replace('|', ' ') if cover_letter else ''
        new_resume_line = f"{new_resume_id}|{applicant_name}|{applicant_email}|{filename}|{upload_date}|{summary}"
        resumes.append({
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': summary
        })
        lines = [f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}" for r in resumes]
        write_file_lines('resumes.txt', lines)
        # Update applications.txt
        applications = parse_applications()
        new_application_id = generate_new_id(applications, 'application_id')
        applied_date = datetime.now().strftime('%Y-%m-%d')
        status = 'Applied'
        new_application_line = f"{new_application_id}|{job_id}|{applicant_name}|{applicant_email}|{status}|{applied_date}|{new_resume_id}"
        applications.append({
            'application_id': new_application_id,
            'job_id': job_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': status,
            'applied_date': applied_date,
            'resume_id': new_resume_id
        })
        app_lines = [f"{a['application_id']}|{a['job_id']}|{a['applicant_name']}|{a['applicant_email']}|{a['status']}|{a['applied_date']}|{a['resume_id']}" for a in applications]
        write_file_lines('applications.txt', app_lines)
        flash('Application submitted successfully.')
        return redirect(url_for('dashboard'))
    return render_template('application_form.html', job=job)
@app.route('/applications')
def application_tracking():
    applications = parse_applications()
    jobs = parse_jobs()
    companies = parse_companies()
    status_filter = request.args.get('status', 'All')
    filtered_apps = []
    for app_entry in applications:
        job = get_job_by_id(app_entry['job_id'])
        company = get_company_by_id(job['company_id']) if job else None
        app_entry['job_title'] = job['title'] if job else 'Unknown'
        app_entry['company_name'] = company['company_name'] if company else 'Unknown'
        if status_filter != 'All' and app_entry['status'] != status_filter:
            continue
        filtered_apps.append(app_entry)
    return render_template('application_tracking.html', applications=filtered_apps, selected_status=status_filter)
@app.route('/application/<application_id>')
def view_application(application_id):
    applications = parse_applications()
    application = None
    for a in applications:
        if a['application_id'] == application_id:
            application = a
            break
    if not application:
        abort(404, description="Application not found")
    job = get_job_by_id(application['job_id'])
    company = get_company_by_id(job['company_id']) if job else None
    resume = get_resume_by_id(application['resume_id'])
    return render_template('application_details.html', application=application, job=job, company=company, resume=resume)
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
    return render_template('companies_directory.html', companies=filtered_companies, search_query=search_query)
@app.route('/company/<company_id>')
def company_profile(company_id):
    company = get_company_by_id(company_id)
    if not company:
        abort(404, description="Company not found")
    jobs = parse_jobs()
    company_jobs = [job for job in jobs if job['company_id'] == company_id]
    # Add status indicators (assuming 'Open' if posted_date within 90 days)
    today = datetime.now()
    for job in company_jobs:
        try:
            posted_date = datetime.strptime(job['posted_date'], '%Y-%m-%d')
            days_diff = (today - posted_date).days
            job['status'] = 'Open' if days_diff <= 90 else 'Closed'
        except Exception:
            job['status'] = 'Unknown'
    return render_template('company_profile.html', company=company, company_jobs=company_jobs)
@app.route('/resumes', methods=['GET', 'POST'])
def resume_management():
    resumes = parse_resumes()
    if request.method == 'POST':
        if 'resume-file-input' not in request.files:
            flash('No file part in the request.')
            return redirect(request.url)
        file = request.files['resume-file-input']
        if file.filename == '':
            flash('No selected file.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            timestamp_str = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp_str}_{file.filename}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            # Add to resumes.txt with empty applicant_name and email and summary
            resumes = parse_resumes()
            new_resume_id = generate_new_id(resumes, 'resume_id')
            upload_date = datetime.now().strftime('%Y-%m-%d')
            new_resume_line = f"{new_resume_id}|||{filename}|{upload_date}|"
            resumes.append({
                'resume_id': new_resume_id,
                'applicant_name': '',
                'applicant_email': '',
                'filename': filename,
                'upload_date': upload_date,
                'summary': ''
            })
            lines = [f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}" for r in resumes]
            write_file_lines('resumes.txt', lines)
            flash('Resume uploaded successfully.')
            return redirect(url_for('resume_management'))
        else:
            flash('Unsupported file type. Allowed types: pdf, doc, docx, txt.')
            return redirect(request.url)
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
        flash('Resume not found.')
        return redirect(url_for('resume_management'))
    # Remove file from uploads
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], resume_to_delete['filename'])
    if os.path.exists(filepath):
        os.remove(filepath)
    # Remove from resumes list and update file
    resumes = [r for r in resumes if r['resume_id'] != resume_id]
    lines = [f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}" for r in resumes]
    write_file_lines('resumes.txt', lines)
    flash('Resume deleted successfully.')
    return redirect(url_for('resume_management'))
@app.route('/search')
def search_results():
    query = request.args.get('query', '').strip()
    query_lower = query.lower()
    jobs = parse_jobs()
    companies = parse_companies()
    job_results = []
    company_results = []
    for job in jobs:
        company = get_company_by_id(job['company_id'])
        job['company_name'] = company['company_name'] if company else 'Unknown'
        if (query_lower in job['title'].lower() or
            query_lower in job['company_name'].lower() or
            query_lower in job['location'].lower()):
            job_results.append(job)
    for company in companies:
        if (query_lower in company['company_name'].lower() or
            query_lower in company['industry'].lower()):
            company_results.append(company)
    no_results = (len(job_results) == 0 and len(company_results) == 0)
    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results, no_results=no_results)
@app.route('/uploads/resumes/<filename>')
def uploaded_resume(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
if __name__ == '__main__':
    app.run(port=5000)