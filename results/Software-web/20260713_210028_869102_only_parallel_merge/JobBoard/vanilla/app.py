import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from datetime import datetime, date
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATA_DIR = 'data'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Data loading functions

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
            parts = line.split('|')
            if len(parts) != 9:
                continue
            jobs.append({
                'job_id': int(parts[0]),
                'title': parts[1],
                'company_id': int(parts[2]),
                'location': parts[3],
                'salary_min': int(parts[4]),
                'salary_max': int(parts[5]),
                'category': parts[6],
                'description': parts[7],
                'posted_date': parts[8]
            })
    return jobs

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
            parts = line.split('|')
            if len(parts) != 6:
                continue
            companies.append({
                'company_id': int(parts[0]),
                'company_name': parts[1],
                'industry': parts[2],
                'location': parts[3],
                'employee_count': int(parts[4]),
                'description': parts[5]
            })
    return companies

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
            parts = line.split('|')
            if len(parts) != 3:
                continue
            categories.append({
                'category_id': int(parts[0]),
                'category_name': parts[1],
                'description': parts[2]
            })
    return categories

def read_job_categories():
    mappings = []
    path = os.path.join(DATA_DIR, 'job_categories.txt')
    if not os.path.exists(path):
        return mappings
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            mappings.append({
                'mapping_id': int(parts[0]),
                'job_id': int(parts[1]),
                'category_id': int(parts[2])
            })
    return mappings

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
            parts = line.split('|')
            if len(parts) != 7:
                continue
            applications.append({
                'application_id': int(parts[0]),
                'job_id': int(parts[1]),
                'applicant_name': parts[2],
                'applicant_email': parts[3],
                'status': parts[4],
                'applied_date': parts[5],
                'resume_id': int(parts[6]) if parts[6].isdigit() else None
            })
    return applications

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
            parts = line.split('|')
            if len(parts) != 6:
                continue
            resumes.append({
                'resume_id': int(parts[0]),
                'applicant_name': parts[1],
                'applicant_email': parts[2],
                'filename': parts[3],
                'upload_date': parts[4],
                'summary': parts[5]
            })
    return resumes

# Writing functions

def write_applications(applications):
    path = os.path.join(DATA_DIR, 'applications.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for a in applications:
            resume_id_str = str(a['resume_id']) if a['resume_id'] else ''
            f.write(f"{a['application_id']}|{a['job_id']}|{a['applicant_name']}|{a['applicant_email']}|{a['status']}|{a['applied_date']}|{resume_id_str}\n")

def write_resumes(resumes):
    path = os.path.join(DATA_DIR, 'resumes.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in resumes:
            f.write(f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}\n")

# Helpers

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

def get_category_name_by_id(cat_id):
    categories = read_categories()
    for c in categories:
        if c['category_id'] == cat_id:
            return c['category_name']
    return None

# Filtering helpers

def filter_jobs(jobs, companies, categories, selected_category, selected_location, search_query):
    filtered = []
    sc = selected_category
    sl = selected_location
    sq = search_query.lower() if search_query else None

    for job in jobs:
        if sc and sc != '' and sc != 'All':
            if job['category'] != sc:
                continue
        if sl and sl != '' and sl != 'All':
            loc = job['location'].lower()
            if sl.lower() == 'remote' and 'remote' not in loc:
                continue
            elif sl.lower() == 'on-site' and 'on-site' not in loc and 'onsite' not in loc.replace('-', ''):
                continue
            elif sl.lower() == 'hybrid' and 'hybrid' not in loc:
                continue
        if sq:
            company_name = ''
            for c in companies:
                if c['company_id'] == job['company_id']:
                    company_name = c['company_name']
                    break
            if sq not in job['title'].lower() and sq not in company_name.lower() and sq not in job['location'].lower():
                continue
        filtered.append(job)
    return filtered

def get_locations():
    return ['All', 'Remote', 'On-site', 'Hybrid']


def filter_applications(applications, status_filter):
    if not status_filter or status_filter == 'All':
        return applications
    return [a for a in applications if a['status'] == status_filter]


def filter_companies(companies, query):
    if not query:
        return companies
    q = query.lower()
    return [c for c in companies if q in c['company_name'].lower() or q in c['industry'].lower()]


def get_next_application_id():
    applications = read_applications()
    if not applications:
        return 1
    return max(a['application_id'] for a in applications) + 1


def get_next_resume_id():
    resumes = read_resumes()
    if not resumes:
        return 1
    return max(r['resume_id'] for r in resumes) + 1


def save_application(application):
    path = os.path.join(DATA_DIR, 'applications.txt')
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f"{application['application_id']}|{application['job_id']}|{application['applicant_name']}|{application['applicant_email']}|{application['status']}|{application['applied_date']}|{application['resume_id']}\n")


def save_resume(resume):
    path = os.path.join(DATA_DIR, 'resumes.txt')
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f"{resume['resume_id']}|{resume['applicant_name']}|{resume['applicant_email']}|{resume['filename']}|{resume['upload_date']}|{resume['summary']}\n")


def delete_resume_file(resume_id):
    resumes = read_resumes()
    to_delete = None
    for r in resumes:
        if r['resume_id'] == resume_id:
            to_delete = r
            break
    if not to_delete:
        return False
    # Rewrite resumes.txt without the deleted resume
    path = os.path.join(DATA_DIR, 'resumes.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in resumes:
            if r['resume_id'] != resume_id:
                f.write(f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}\n")
    file_path = os.path.join(UPLOAD_FOLDER, to_delete['filename'])
    if os.path.exists(file_path):
        os.remove(file_path)
    return True

# Routes

@app.route('/')
@app.route('/dashboard')
def dashboard():
    jobs = read_jobs()
    companies = read_companies()
    sorted_jobs = sorted(jobs, key=lambda x: x['posted_date'], reverse=True)
    featured_jobs = sorted_jobs[:3]
    latest_jobs = sorted_jobs[:5]
    for job in featured_jobs:
        job['company_name'] = next((c['company_name'] for c in companies if c['company_id'] == job['company_id']), '')
    for job in latest_jobs:
        job['company_name'] = next((c['company_name'] for c in companies if c['company_id'] == job['company_id']), '')
    return render_template('dashboard.html', featured_jobs=featured_jobs, latest_jobs=latest_jobs)

@app.route('/jobs')
def jobs():
    jobs = read_jobs()
    companies = read_companies()
    categories = read_categories()
    locations = get_locations()

    selected_category = request.args.get('category', 'All')
    selected_location = request.args.get('location', 'All')
    search_query = request.args.get('search', '').strip()

    filtered_jobs = filter_jobs(jobs, companies, categories, selected_category, selected_location, search_query)

    for job in filtered_jobs:
        job['company_name'] = next((c['company_name'] for c in companies if c['company_id'] == job['company_id']), '')

    return render_template('jobs.html', jobs=filtered_jobs, categories=categories, locations=locations, selected_category=selected_category, selected_location=selected_location, search_query=search_query)

@app.route('/jobs/<int:job_id>')
def job_details(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return "Job not found", 404
    company = get_company_by_id(job['company_id'])
    return render_template('job_details.html', job=job, company=company)

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
            flash('All fields are required, including resume upload.', 'error')
            return render_template('application_form.html', job=job)

        if not allowed_file(resume_file.filename):
            flash('File type not allowed. Allowed types: PDF, DOC, DOCX, TXT.', 'error')
            return render_template('application_form.html', job=job)

        filename = secure_filename(resume_file.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        filename = f"{timestamp}_{filename}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume_file.save(save_path)

        resumes = read_resumes()
        new_resume_id = max([r['resume_id'] for r in resumes], default=0) + 1
        summary = cover_letter[:100]
        upload_date = date.today().isoformat()
        resumes.append({
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': summary
        })
        write_resumes(resumes)

        applications = read_applications()
        new_app_id = max([a['application_id'] for a in applications], default=0) + 1
        applications.append({
            'application_id': new_app_id,
            'job_id': job_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': 'Applied',
            'applied_date': upload_date,
            'resume_id': new_resume_id
        })
        write_applications(applications)
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('applications'))

    return render_template('application_form.html', job=job)

@app.route('/applications')
def applications():
    applications = read_applications()
    jobs = read_jobs()
    companies = read_companies()
    filter_status = request.args.get('status', 'All')

    filtered_apps = []
    for app_item in applications:
        if filter_status != 'All' and app_item['status'] != filter_status:
            continue
        filtered_apps.append(app_item)

    for app_item in filtered_apps:
        job_obj = next((j for j in jobs if j['job_id'] == app_item['job_id']), None)
        if job_obj:
            app_item['job_title'] = job_obj['title']
            company_obj = next((c for c in companies if c['company_id'] == job_obj['company_id']), None)
            app_item['company_name'] = company_obj['company_name'] if company_obj else ''
        else:
            app_item['job_title'] = ''
            app_item['company_name'] = ''

    return render_template('applications.html', applications=filtered_apps, filter_status=filter_status)

@app.route('/applications/<int:app_id>')
def application_details(app_id):
    applications = read_applications()
    app_data = next((a for a in applications if a['application_id'] == app_id), None)
    if not app_data:
        return "Application not found", 404
    job = get_job_by_id(app_data['job_id'])
    company = get_company_by_id(job['company_id']) if job else None
    resume = None
    if app_data['resume_id']:
        resumes = read_resumes()
        resume = next((r for r in resumes if r['resume_id'] == app_data['resume_id']), None)
    return render_template('application_details.html', application=app_data, job=job, company_name=company['company_name'] if company else '', resume=resume)

@app.route('/companies')
def companies():
    companies = read_companies()
    search_query = request.args.get('search', '').strip().lower()
    if search_query:
        companies = [c for c in companies if search_query in c['company_name'].lower() or search_query in c['industry'].lower()]
    return render_template('companies.html', companies=companies, search_query=request.args.get('search', ''))

@app.route('/companies/<int:company_id>')
def company_profile(company_id):
    company = get_company_by_id(company_id)
    if not company:
        return "Company not found", 404
    jobs = [j for j in read_jobs() if j['company_id'] == company_id]
    for job in jobs:
        job['status'] = 'Open'
    return render_template('company_profile.html', company=company, jobs=jobs)

@app.route('/resumes', methods=['GET', 'POST'])
def resumes():
    if request.method == 'POST':
        applicant_name = request.form.get('applicant-name', '').strip()
        applicant_email = request.form.get('applicant-email', '').strip()
        resume_file = request.files.get('resume-file-input')

        if not applicant_name or not applicant_email or not resume_file:
            flash('Applicant name, email and resume file are required.', 'error')
            resumes = read_resumes()
            return render_template('resumes.html', resumes=resumes)

        if not allowed_file(resume_file.filename):
            flash('File type not allowed. Allowed types: PDF, DOC, DOCX, TXT.', 'error')
            resumes = read_resumes()
            return render_template('resumes.html', resumes=resumes)

        filename = secure_filename(resume_file.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        filename = f"{timestamp}_{filename}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume_file.save(save_path)

        resumes = read_resumes()
        new_resume_id = max([r['resume_id'] for r in resumes], default=0) + 1
        upload_date = date.today().isoformat()
        summary = ''

        resumes.append({
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': summary
        })
        write_resumes(resumes)
        flash('Resume uploaded successfully!', 'success')
        return redirect(url_for('resumes'))

    resumes = read_resumes()
    return render_template('resumes.html', resumes=resumes)

@app.route('/resumes/delete/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = read_resumes()
    resume = next((r for r in resumes if r['resume_id'] == resume_id), None)
    if not resume:
        flash('Resume not found.', 'error')
        return redirect(url_for('resumes'))
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume['filename'])
    if os.path.exists(file_path):
        os.remove(file_path)
    resumes = [r for r in resumes if r['resume_id'] != resume_id]
    write_resumes(resumes)
    flash('Resume deleted successfully.', 'success')
    return redirect(url_for('resumes'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/search')
def search():
    query = request.args.get('query', '').strip()
    job_results = []
    company_results = []
    companies_all = read_companies()
    if query:
        q = query.lower()
        jobs_all = read_jobs()
        job_results = [job for job in jobs_all if q in job['title'].lower() or q in get_company_by_id(job['company_id'])['company_name'].lower() or q in job['location'].lower()]
        company_results = [comp for comp in companies_all if q in comp['company_name'].lower() or q in comp['industry'].lower()]
    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)

if __name__ == '__main__':
    app.run(debug=True)
