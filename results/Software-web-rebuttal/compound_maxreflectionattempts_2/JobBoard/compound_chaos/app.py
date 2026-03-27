from flask import Flask, render_template, request, redirect, url_for, flash, abort
from werkzeug.utils import secure_filename
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
DATA_DIR = 'data'
RESUME_UPLOAD_DIR = os.path.join(DATA_DIR, 'resume_uploads')
os.makedirs(RESUME_UPLOAD_DIR, exist_ok=True)

# === Helpers for file I/O and data parsing / writing ===

def parse_pipe_line(line, expected_count):
    parts = line.strip().split('|')
    if len(parts) == expected_count:
        return parts
    return None


def read_jobs():
    filepath = os.path.join(DATA_DIR, 'jobs.txt')
    jobs = []
    if not os.path.exists(filepath):
        return jobs
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            parts = parse_pipe_line(line, 9)
            if not parts:
                continue
            try:
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
            except ValueError:
                continue
    return jobs


def read_companies():
    filepath = os.path.join(DATA_DIR, 'companies.txt')
    companies = []
    if not os.path.exists(filepath):
        return companies
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            parts = parse_pipe_line(line, 6)
            if not parts:
                continue
            try:
                company = {
                    'company_id': int(parts[0]),
                    'company_name': parts[1],
                    'industry': parts[2],
                    'location': parts[3],
                    'employee_count': int(parts[4]),
                    'description': parts[5]
                }
                companies.append(company)
            except ValueError:
                continue
    return companies


def read_categories():
    filepath = os.path.join(DATA_DIR, 'categories.txt')
    categories = []
    if not os.path.exists(filepath):
        return categories
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            parts = parse_pipe_line(line, 3)
            if not parts:
                continue
            try:
                categories.append({
                    'category_id': int(parts[0]),
                    'category_name': parts[1],
                    'description': parts[2],
                })
            except ValueError:
                continue
    return categories


def read_applications():
    filepath = os.path.join(DATA_DIR, 'applications.txt')
    applications = []
    if not os.path.exists(filepath):
        return applications
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            parts = parse_pipe_line(line, 7)
            if not parts:
                continue
            try:
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
            except ValueError:
                continue
    return applications


def read_resumes():
    filepath = os.path.join(DATA_DIR, 'resumes.txt')
    resumes = []
    if not os.path.exists(filepath):
        return resumes
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            parts = parse_pipe_line(line, 6)
            if not parts:
                continue
            try:
                resume = {
                    'resume_id': int(parts[0]),
                    'applicant_name': parts[1],
                    'applicant_email': parts[2],
                    'filename': parts[3],
                    'upload_date': parts[4],
                    'summary': parts[5]
                }
                resumes.append(resume)
            except ValueError:
                continue
    return resumes


def write_applications(applications):
    filepath = os.path.join(DATA_DIR, 'applications.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for a in applications:
            line = f"{a['application_id']}|{a['job_id']}|{a['applicant_name']}|{a['applicant_email']}|{a['status']}|{a['applied_date']}|{a['resume_id']}"
            f.write(line + '\n')


def write_resumes(resumes):
    filepath = os.path.join(DATA_DIR, 'resumes.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for r in resumes:
            line = f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}"
            f.write(line + '\n')

# === Flask Routes ===

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_view'))

@app.route('/dashboard')
def dashboard_view():
    jobs = read_jobs()
    companies = {c['company_id']: c for c in read_companies()}
    featured_jobs = []
    for j in jobs:
        company_name = companies.get(j['company_id'], {}).get('company_name', '')
        featured_jobs.append({
            'job_id': j['job_id'],
            'title': j['title'],
            'company_name': company_name,
            'location': j['location'],
            'salary_min': j['salary_min'],
            'salary_max': j['salary_max'],
            'category': j['category']
        })
    return render_template('dashboard.html', featured_jobs=featured_jobs)

@app.route('/jobs')
def job_listings():
    jobs = read_jobs()
    companies = {c['company_id']: c['company_name'] for c in read_companies()}
    categories = read_categories()
    jobs_out = []
    for job in jobs:
        company_name = companies.get(job['company_id'], '')
        jobs_out.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_name,
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
            'category': job['category'],
        })
    return render_template('job_listings.html', jobs=jobs_out, categories=categories, locations=list({j['location'] for j in jobs}))

@app.route('/job/<int:job_id>')
def job_details(job_id):
    jobs = read_jobs()
    job = next((j for j in jobs if j['job_id'] == job_id), None)
    if not job:
        flash('Job not found', 'error')
        return redirect(url_for('job_listings'))
    companies = read_companies()
    company = next((c for c in companies if c['company_id'] == job['company_id']), None)
    if not company:
        company = {}
    job_detail = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': company.get('company_name', ''),
        'location': job['location'],
        'salary_min': job['salary_min'],
        'salary_max': job['salary_max'],
        'category': job['category'],
        'description': job['description']
    }
    company_info = {
        'company_id': company.get('company_id', -1),
        'company_name': company.get('company_name', '')
    }
    return render_template('job_details.html', job=job_detail, company=company_info)

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    jobs = read_jobs()
    companies = {c['company_id']: c['company_name'] for c in read_companies()}
    job = next((j for j in jobs if j['job_id'] == job_id), None)
    if not job:
        flash('Job not found', 'error')
        return redirect(url_for('job_listings'))
    company_name = companies.get(job['company_id'], '')
    if request.method == 'GET':
        job_data = {
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_name
        }
        return render_template('application_form.html', job=job_data)
    else:
        applicant_name = request.form.get('applicant_name')
        applicant_email = request.form.get('applicant_email')
        cover_letter = request.form.get('cover_letter')
        resume_file = request.files.get('resume_file')
        if not all([applicant_name, applicant_email, cover_letter, resume_file]):
            flash('All fields are required.', 'error')
            return redirect(url_for('application_form', job_id=job_id))
        filename = secure_filename(resume_file.filename)
        filepath = os.path.join(RESUME_UPLOAD_DIR, filename)
        try:
            resume_file.save(filepath)
        except Exception:
            flash('Failed to save resume file.', 'error')
            return redirect(url_for('application_form', job_id=job_id))
        resumes = read_resumes()
        max_resume_id = max([r['resume_id'] for r in resumes], default=0)
        new_resume_id = max_resume_id + 1
        upload_date = datetime.date.today().isoformat()
        summary = cover_letter[:100] if cover_letter else ''
        new_resume_entry = {
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': summary
        }
        resumes.append(new_resume_entry)
        write_resumes(resumes)
        applications = read_applications()
        max_app_id = max([a['application_id'] for a in applications], default=0)
        new_app_id = max_app_id + 1
        new_app_entry = {
            'application_id': new_app_id,
            'job_id': job_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': 'Applied',
            'applied_date': upload_date,
            'resume_id': new_resume_id
        }
        applications.append(new_app_entry)
        write_applications(applications)
        flash('Application submitted successfully.', 'success')
        return redirect(url_for('application_tracking'))

@app.route('/applications')
def application_tracking():
    applications = read_applications()
    jobs = {j['job_id']: j for j in read_jobs()}
    companies = {c['company_id']: c for c in read_companies()}
    app_out = []
    for app in applications:
        job = jobs.get(app['job_id'])
        if not job:
            continue
        company = companies.get(job['company_id'], {})
        app_out.append({
            'application_id': app['application_id'],
            'job_title': job['title'],
            'company_name': company.get('company_name', ''),
            'status': app['status'],
            'applied_date': app['applied_date'],
        })
    return render_template('application_tracking.html', applications=app_out)

@app.route('/companies')
def companies_directory():
    companies = read_companies()
    return render_template('companies_directory.html', companies=companies)

@app.route('/company/<int:company_id>')
def company_profile(company_id):
    companies = read_companies()
    company = next((c for c in companies if c['company_id'] == company_id), None)
    if not company:
        flash('Company not found.', 'error')
        return redirect(url_for('companies_directory'))
    jobs = read_jobs()
    company_jobs = []
    for j in jobs:
        if j['company_id'] == company_id:
            company_jobs.append({
                'job_id': j['job_id'],
                'title': j['title'],
                'status': 'Open'  # status not specified, assume 'Open'
            })
    return render_template('company_profile.html', company=company, jobs=company_jobs)

@app.route('/resumes', methods=['GET', 'POST'])
def resume_management():
    if request.method == 'POST':
        resume_file = request.files.get('resume_file')
        applicant_name = request.form.get('applicant_name')
        applicant_email = request.form.get('applicant_email')
        summary = request.form.get('summary', '')
        if not all([resume_file, applicant_name, applicant_email]):
            flash('Applicant name, email, and resume file are required.', 'error')
            return redirect(url_for('resume_management'))
        filename = secure_filename(resume_file.filename)
        filepath = os.path.join(RESUME_UPLOAD_DIR, filename)
        try:
            resume_file.save(filepath)
        except Exception:
            flash('Failed to save resume file.', 'error')
            return redirect(url_for('resume_management'))
        resumes = read_resumes()
        max_resume_id = max([r['resume_id'] for r in resumes], default=0)
        new_resume_id = max_resume_id + 1
        upload_date = datetime.date.today().isoformat()
        new_entry = {
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': summary
        }
        resumes.append(new_entry)
        write_resumes(resumes)
        flash('Resume uploaded successfully.', 'success')
        return redirect(url_for('resume_management'))
    resumes = read_resumes()
    return render_template('resume_management.html', resumes=resumes)

@app.route('/resumes/delete/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = read_resumes()
    resumes = [r for r in resumes if r['resume_id'] != resume_id]
    write_resumes(resumes)
    flash('Resume deleted successfully.', 'success')
    return redirect(url_for('resume_management'))

@app.route('/search')
def search_results():
    query = request.args.get('query', '').strip().lower()
    jobs = read_jobs()
    companies = read_companies()
    job_results = []
    company_results = []
    if query:
        for job in jobs:
            if (query in job['title'].lower() or
                query in job['category'].lower() or
                query in job['location'].lower() or
                query in str(job['salary_min']) or
                query in str(job['salary_max'])):
                pass
            if query in job['title'].lower() or query in job['category'].lower() or query in job['location'].lower():
                company_name = next((c['company_name'] for c in companies if c['company_id'] == job['company_id']), '')
                job_results.append({
                    'job_id': job['job_id'],
                    'title': job['title'],
                    'company_name': company_name,
                    'location': job['location'],
                    'salary_min': job['salary_min'],
                    'salary_max': job['salary_max'],
                })
        for comp in companies:
            if query in comp['company_name'].lower() or query in comp['industry'].lower():
                company_results.append({
                    'company_id': comp['company_id'],
                    'company_name': comp['company_name'],
                    'industry': comp['industry'],
                })
    return render_template('search_results.html', search_query=query, job_results=job_results, company_results=company_results)

if __name__ == '__main__':
    app.run(debug=True)
