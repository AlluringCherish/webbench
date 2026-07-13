import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATA_DIR = 'data'
UPLOAD_DIR = 'uploads'

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --------------------------------
# Helper functions to load data
# --------------------------------

def load_jobs():
    jobs = []
    filepath = os.path.join(DATA_DIR, 'jobs.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 9:
                    continue
                job_id, title, company_id, location, salary_min, salary_max, category, description, posted_date = parts
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
    return jobs


def load_companies():
    companies = []
    filepath = os.path.join(DATA_DIR, 'companies.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                company_id, company_name, industry, location, employee_count, description = parts
                companies.append({
                    'company_id': int(company_id),
                    'company_name': company_name,
                    'industry': industry,
                    'location': location,
                    'employee_count': int(employee_count),
                    'description': description
                })
    return companies


def load_categories():
    categories = []
    filepath = os.path.join(DATA_DIR, 'categories.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                category_id, category_name, description = parts
                categories.append({
                    'category_id': int(category_id),
                    'category_name': category_name,
                    'description': description
                })
    return categories


def load_applications():
    applications = []
    filepath = os.path.join(DATA_DIR, 'applications.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                application_id, job_id, applicant_name, applicant_email, status, applied_date, resume_id = parts
                applications.append({
                    'application_id': int(application_id),
                    'job_id': int(job_id),
                    'applicant_name': applicant_name,
                    'applicant_email': applicant_email,
                    'status': status,
                    'applied_date': applied_date,
                    'resume_id': int(resume_id) if resume_id.isdigit() else None
                })
    return applications


def load_resumes():
    resumes = []
    filepath = os.path.join(DATA_DIR, 'resumes.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                resume_id, applicant_name, applicant_email, filename, upload_date, summary = parts
                resumes.append({
                    'resume_id': int(resume_id),
                    'applicant_name': applicant_name,
                    'applicant_email': applicant_email,
                    'filename': filename,
                    'upload_date': upload_date,
                    'summary': summary
                })
    return resumes


def load_job_categories():
    mappings = []
    filepath = os.path.join(DATA_DIR, 'job_categories.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                mapping_id, job_id, category_id = parts
                mappings.append({
                    'mapping_id': int(mapping_id),
                    'job_id': int(job_id),
                    'category_id': int(category_id)
                })
    return mappings


def get_company_by_id(company_id):
    companies = load_companies()
    for c in companies:
        if c['company_id'] == company_id:
            return c
    return None


def get_job_by_id(job_id):
    jobs = load_jobs()
    for j in jobs:
        if j['job_id'] == job_id:
            return j
    return None


def get_application_by_id(app_id):
    applications = load_applications()
    for a in applications:
        if a['application_id'] == app_id:
            return a
    return None


def get_resume_by_id(resume_id):
    resumes = load_resumes()
    for r in resumes:
        if r['resume_id'] == resume_id:
            return r
    return None

# To get all jobs filtered by some criteria
# category filter is by category_name string
# location filter is by job location string - must match exactly
# search query checks in job title, company name, or location (case-insensitive substring)
def filter_jobs(jobs, companies, categories, selected_category, selected_location, search_query):
    filtered = []
    sc = selected_category
    sl = selected_location
    sq = search_query.lower() if search_query else None

    for job in jobs:
        # Filter by category
        if sc and sc != 'All':
            if job['category'] != sc:
                continue
        # Filter by location
        if sl and sl != 'All':
            # Location filters are Remote, On-site, Hybrid
            # We consider these keywords case-insensitive substrings of job.Location
            # For example, 'Remote' in job['location'] etc.
            # Also to support On-site vs 'On-site' exact match
            loc = job['location'].lower()
            if sl.lower() == 'remote' and 'remote' not in loc:
                continue
            elif sl.lower() == 'on-site' and 'on-site' not in loc.lower() and 'onsite' not in loc.replace('-',''):
                continue
            elif sl.lower() == 'hybrid' and 'hybrid' not in loc:
                continue

        if sq:
            company_name = ''
            for c in companies:
                if c['company_id'] == job['company_id']:
                    company_name = c['company_name']
                    break
            # Check if sq in title or company or location
            if sq not in job['title'].lower() and sq not in company_name.lower() and sq not in job['location'].lower():
                continue

        filtered.append(job)
    return filtered

# Get unique locations from jobs for location filter
# We limit to Remote, On-site, Hybrid only as per spec
# But also include any distinct locations for better usefulness

def get_locations():
    # Fixed as per spec
    return ['All', 'Remote', 'On-site', 'Hybrid']

# For applications, filter by status
# statuses: All, Applied, Under Review, Interview, Rejected
def filter_applications(applications, status_filter):
    if not status_filter or status_filter == 'All':
        return applications
    return [a for a in applications if a['status'] == status_filter]

# For companies search by name or industry (case-insensitive substring)
def filter_companies(companies, query):
    if not query:
        return companies
    q = query.lower()
    return [c for c in companies if q in c['company_name'].lower() or q in c['industry'].lower()]

# Generate new IDs for applications, resumes, mapping
# Below functions assumes consistent file format with numeric IDs increasing

def get_next_application_id():
    apps = load_applications()
    if not apps:
        return 1
    return max(a['application_id'] for a in apps) + 1

def get_next_resume_id():
    resumes = load_resumes()
    if not resumes:
        return 1
    return max(r['resume_id'] for r in resumes) + 1


def save_application(application):
    # application is a dict with necessary fields
    # append new application to applications.txt
    filepath = os.path.join(DATA_DIR, 'applications.txt')
    new_line = f"{application['application_id']}|{application['job_id']}|{application['applicant_name']}|{application['applicant_email']}|{application['status']}|{application['applied_date']}|{application['resume_id']}\n"
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(new_line)


def save_resume(resume):
    filepath = os.path.join(DATA_DIR, 'resumes.txt')
    new_line = f"{resume['resume_id']}|{resume['applicant_name']}|{resume['applicant_email']}|{resume['filename']}|{resume['upload_date']}|{resume['summary']}\n"
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(new_line)


def delete_resume_file(resume_id):
    resumes = load_resumes()
    to_delete = None
    for r in resumes:
        if r['resume_id'] == resume_id:
            to_delete = r
            break
    if not to_delete:
        return False
    filepath = os.path.join(DATA_DIR, 'resumes.txt')
    # Rewrite resumes.txt without the deleted resume
    with open(filepath, 'w', encoding='utf-8') as f:
        for r in resumes:
            if r['resume_id'] != resume_id:
                line = f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}\n"
                f.write(line)
    # Also delete the actual file
    file_path = os.path.join(UPLOAD_DIR, to_delete['filename'])
    if os.path.exists(file_path):
        os.remove(file_path)
    return True

# --------------------------------
# Flask Routes Implementations
# --------------------------------

@app.route('/')
@app.route('/dashboard')
def dashboard():
    jobs = load_jobs()
    companies = load_companies()
    # Featured jobs: for example top 3 newest by posted_date
    sorted_jobs = sorted(jobs, key=lambda x: x['posted_date'], reverse=True)
    featured_jobs = sorted_jobs[:3]
    latest_jobs = sorted_jobs[:5]
    # Attach company name in featured/latest jobs for display convenience
    for job in featured_jobs:
        job['company_name'] = next((c['company_name'] for c in companies if c['company_id'] == job['company_id']), '')
    for job in latest_jobs:
        job['company_name'] = next((c['company_name'] for c in companies if c['company_id'] == job['company_id']), '')
    return render_template('candidate_b/dashboard.html', featured_jobs=featured_jobs, latest_jobs=latest_jobs)


@app.route('/jobs')
def jobs():
    jobs = load_jobs()
    companies = load_companies()
    categories = load_categories()
    locations = get_locations()

    selected_category = request.args.get('category', 'All')
    selected_location = request.args.get('location', 'All')
    search_query = request.args.get('search', '').strip()

    filtered_jobs = filter_jobs(jobs, companies, categories, selected_category, selected_location, search_query)

    # Attach company name in jobs for display convenience
    for job in filtered_jobs:
        job['company_name'] = next((c['company_name'] for c in companies if c['company_id'] == job['company_id']), '')

    return render_template('candidate_b/jobs.html', jobs=filtered_jobs, categories=categories, locations=locations, selected_category=selected_category, selected_location=selected_location, search_query=search_query)


@app.route('/jobs/<int:job_id>')
def job_details(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return "Job not found", 404
    company = get_company_by_id(job['company_id'])
    return render_template('candidate_b/job_details.html', job=job, company=company)


@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return "Job not found", 404

    if request.method == 'POST':
        applicant_name = request.form.get('applicant-name', '').strip()
        applicant_email = request.form.get('applicant-email', '').strip()
        cover_letter = request.form.get('cover-letter', '').strip()
        resume_file = request.files.get('resume-upload')

        if not applicant_name or not applicant_email or not resume_file:
            flash('Please fill all required fields and upload a resume file.')
            return render_template('candidate_b/application_form.html', job=job)

        # Save resume file
        filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{resume_file.filename}"
        save_path = os.path.join(UPLOAD_DIR, filename)
        resume_file.save(save_path)

        # Save resume metadata
        resume_id = get_next_resume_id()
        resume_summary = cover_letter[:100] if cover_letter else ''
        upload_date = datetime.date.today().isoformat()
        save_resume({
            'resume_id': resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': resume_summary
        })

        # Save application
        application_id = get_next_application_id()
        application = {
            'application_id': application_id,
            'job_id': job_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': 'Applied',
            'applied_date': upload_date,
            'resume_id': resume_id
        }
        save_application(application)

        flash('Application submitted successfully.')
        return redirect(url_for('applications'))

    return render_template('candidate_b/application_form.html', job=job)


@app.route('/applications')
def applications():
    applications = load_applications()
    jobs = load_jobs()
    companies = load_companies()

    status_filter = request.args.get('status', 'All')
    filtered_apps = filter_applications(applications, status_filter)

    # Attach job title and company name for display
    for app_obj in filtered_apps:
        job_obj = next((j for j in jobs if j['job_id'] == app_obj['job_id']), None)
        if job_obj:
            app_obj['job_title'] = job_obj['title']
            company_obj = next((c for c in companies if c['company_id'] == job_obj['company_id']), None)
            app_obj['company_name'] = company_obj['company_name'] if company_obj else ''
        else:
            app_obj['job_title'] = 'N/A'
            app_obj['company_name'] = 'N/A'

    return render_template('candidate_b/applications.html', applications=filtered_apps, filter_status=status_filter)


@app.route('/applications/<int:app_id>')
def application_details(app_id):
    application = get_application_by_id(app_id)
    if not application:
        return "Application not found", 404
    job = get_job_by_id(application['job_id'])
    resume = get_resume_by_id(application['resume_id']) if application['resume_id'] else None
    return render_template('candidate_b/application_details.html', application=application, job=job, resume=resume)


@app.route('/companies')
def companies():
    companies = load_companies()
    search_query = request.args.get('search', '').strip()
    filtered_companies = filter_companies(companies, search_query)
    return render_template('candidate_b/companies.html', companies=filtered_companies, search_query=search_query)


@app.route('/companies/<int:company_id>')
def company_profile(company_id):
    company = get_company_by_id(company_id)
    if not company:
        return "Company not found", 404
    jobs = [job for job in load_jobs() if job['company_id'] == company_id]
    # Attach job status indicators if needed - example set to 'Open' for all jobs
    for job in jobs:
        job['status'] = 'Open'
    return render_template('candidate_b/company_profile.html', company=company, jobs=jobs)


@app.route('/resumes', methods=['GET','POST'])
def resumes():
    if request.method == 'POST':
        # Handle resume upload
        applicant_name = request.form.get('applicant-name', '').strip()
        applicant_email = request.form.get('applicant-email', '').strip()
        resume_file = request.files.get('resume-file-input')

        if not applicant_name or not applicant_email or not resume_file:
            flash('Please provide name, email and resume file to upload.')
            resumes = load_resumes()
            return render_template('candidate_b/resumes.html', resumes=resumes)

        # Save file
        filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{resume_file.filename}"
        save_path = os.path.join(UPLOAD_DIR, filename)
        resume_file.save(save_path)

        resume_id = get_next_resume_id()
        upload_date = datetime.date.today().isoformat()
        summary = ''  # No summary on upload page

        save_resume({
            'resume_id': resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': summary
        })

        flash('Resume uploaded successfully.')
        return redirect(url_for('resumes'))

    # GET
    resumes = load_resumes()
    return render_template('candidate_b/resumes.html', resumes=resumes)


@app.route('/resumes/delete/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    success = delete_resume_file(resume_id)
    if success:
        flash('Resume deleted successfully.')
    else:
        flash('Failed to delete resume.')
    return redirect(url_for('resumes'))


@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    jobs = load_jobs()
    companies = load_companies()

    job_results = []
    company_results = []

    if query:
        q = query.lower()
        companies_list = companies
        jobs_list = jobs

        # Search jobs by title, company name, location
        for job in jobs_list:
            company_name = next((c['company_name'] for c in companies_list if c['company_id'] == job['company_id']), '')
            if (q in job['title'].lower() or q in company_name.lower() or q in job['location'].lower()):
                job_results.append(job)

        for company in companies_list:
            if q in company['company_name'].lower() or q in company['industry'].lower():
                company_results.append(company)

    return render_template('candidate_b/search_results.html', query=query, job_results=job_results, company_results=company_results)

# To serve uploaded resume files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)


if __name__ == '__main__':
    app.run(debug=True)
