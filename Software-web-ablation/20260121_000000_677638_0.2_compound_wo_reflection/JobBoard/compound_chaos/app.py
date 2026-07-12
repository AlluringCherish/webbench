from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

data_dir = 'data'

# Helper functions

def read_companies():
    companies = []
    companies_file = os.path.join(data_dir, 'companies.txt')
    if not os.path.exists(companies_file):
        return companies
    with open(companies_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 6:
                continue
            companies.append({
                'company_id': int(parts[0]),
                'name': parts[1],
                'industry': parts[2],
                'location': parts[3],
                'employee_count': int(parts[4]),
                'description': parts[5]
            })
    return companies

def get_company_by_id(company_id):
    companies = read_companies()
    for company in companies:
        if company['company_id'] == company_id:
            return company
    return None

def read_jobs():
    jobs = []
    jobs_file = os.path.join(data_dir, 'jobs.txt')
    if not os.path.exists(jobs_file):
        return jobs
    with open(jobs_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 8:
                continue
            jobs.append({
                'job_id': int(parts[0]),
                'title': parts[1],
                'company_id': int(parts[2]),
                'location': parts[3],
                'salary_min': int(parts[4]),
                'salary_max': int(parts[5]),
                'category': parts[6],
                'description': parts[7]
            })
    return jobs

def get_job_by_id(job_id):
    jobs = read_jobs()
    for job in jobs:
        if job['job_id'] == job_id:
            return job
    return None

def read_resumes():
    resumes = []
    resumes_file = os.path.join(data_dir, 'resumes.txt')
    if not os.path.exists(resumes_file):
        return resumes
    with open(resumes_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 3:
                continue
            resumes.append({
                'resume_id': int(parts[0]),
                'applicant_name': parts[1],
                'content': parts[2]
            })
    return resumes

def write_resumes(resumes):
    resumes_file = os.path.join(data_dir, 'resumes.txt')
    with open(resumes_file, 'w', encoding='utf-8') as f:
        for r in resumes:
            f.write(f"{r['resume_id']}|{r['applicant_name']}|{r['content']}\n")

def read_applications():
    applications = []
    applications_file = os.path.join(data_dir, 'applications.txt')
    if not os.path.exists(applications_file):
        return applications
    with open(applications_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 7:
                continue
            applications.append({
                'application_id': int(parts[0]),
                'job_id': int(parts[1]),
                'applicant_name': parts[2],
                'applicant_email': parts[3],
                'status': parts[4],
                'applied_date': parts[5],
                'resume_id': int(parts[6])
            })
    return applications

def write_applications(applications):
    applications_file = os.path.join(data_dir, 'applications.txt')
    with open(applications_file, 'w', encoding='utf-8') as f:
        for a in applications:
            f.write(f"{a['application_id']}|{a['job_id']}|{a['applicant_name']}|{a['applicant_email']}|{a['status']}|{a['applied_date']}|{a['resume_id']}\n")

# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    jobs = read_jobs()
    companies = read_companies()

    job_cards = []
    for job in jobs:
        company = get_company_by_id(job['company_id'])
        company_name = company['name'] if company else 'Unknown'
        salary_range = f"${job['salary_min']:,} - ${job['salary_max']:,}"
        job_cards.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company': company_name,
            'salary_range': salary_range
        })
    
    return render_template('dashboard.html', job_cards=job_cards)

@app.route('/job/<int:job_id>', methods=['GET', 'POST'])
def job_detail(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return "Job not found", 404
    company = get_company_by_id(job['company_id'])
    company_name = company['name'] if company else 'Unknown'
    salary_range = f"${job['salary_min']:,} - ${job['salary_max']:,}"

    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()
        cover_letter = request.form.get('cover_letter', '').strip()

        if not applicant_name or not applicant_email or not cover_letter:
            error = "All fields are required."
            return render_template('job_detail.html', job=job, company_name=company_name, salary_range=salary_range, error=error)

        resumes = read_resumes()
        new_resume_id = max([r['resume_id'] for r in resumes], default=0) + 1
        resumes.append({
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'content': cover_letter
        })
        write_resumes(resumes)

        applications = read_applications()
        new_application_id = max([a['application_id'] for a in applications], default=0) + 1
        today = datetime.today().strftime('%Y-%m-%d')

        applications.append({
            'application_id': new_application_id,
            'job_id': job_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': 'Applied',
            'applied_date': today,
            'resume_id': new_resume_id
        })
        write_applications(applications)

        return redirect(url_for('dashboard'))

    return render_template('job_detail.html', job=job, company_name=company_name, salary_range=salary_range)

@app.route('/company/<int:company_id>')
def company_profile(company_id):
    company = get_company_by_id(company_id)
    if not company:
        return "Company not found", 404

    jobs = read_jobs()
    company_jobs = [job for job in jobs if job['company_id'] == company_id]

    return render_template('company_profile.html', company=company, company_jobs=company_jobs)

@app.route('/company_directory', methods=['GET', 'POST'])
def company_directory():
    companies = read_companies()
    search_query = ''
    if request.method == 'POST':
        search_query = request.form.get('search_company', '').strip().lower()
        if search_query:
            companies = [c for c in companies if search_query in c['name'].lower()]
    return render_template('company_directory.html', companies=companies, search_query=search_query)

@app.route('/applications', methods=['GET', 'POST'])
def my_applications():
    applications = read_applications()
    resumes = read_resumes()
    resumes_dict = {r['resume_id']: r for r in resumes}

    status_filter = request.form.get('status_filter', 'All')
    if status_filter != 'All':
        applications = [a for a in applications if a['status'] == status_filter]

    # Attach resume content to applications for viewing
    for app in applications:
        resume = resumes_dict.get(app['resume_id'])
        app['resume_content'] = resume['content'] if resume else ''

    return render_template('applications.html', applications=applications, status_filter=status_filter)

@app.route('/management', methods=['GET', 'POST'])
def management():
    resumes = read_resumes()
    error = ''

    if request.method == 'POST':
        if 'delete_resume_id' in request.form:
            delete_id = request.form.get('delete_resume_id')
            try:
                delete_id = int(delete_id)
                resumes = [r for r in resumes if r['resume_id'] != delete_id]
                write_resumes(resumes)
            except ValueError:
                error = 'Invalid Resume ID'

        elif 'upload_resume' in request.files:
            upload = request.files.get('upload_resume')
            if upload and upload.filename:
                content = upload.read().decode('utf-8')
                applicant_name = os.path.splitext(upload.filename)[0]
                new_id = max([r['resume_id'] for r in resumes], default=0) + 1
                resumes.append({
                    'resume_id': new_id,
                    'applicant_name': applicant_name,
                    'content': content
                })
                write_resumes(resumes)

    return render_template('management.html', resumes=resumes, error=error)

if __name__ == '__main__':
    app.run(debug=True)
