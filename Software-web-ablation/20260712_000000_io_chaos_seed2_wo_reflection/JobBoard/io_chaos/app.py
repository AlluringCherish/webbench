import os
import csv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, abort, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_secret_key_here'

DATA_DIR = 'data'

# Load jobs from CSV

def load_jobs():
    jobs_file = os.path.join(DATA_DIR, 'jobs.csv')
    jobs = []
    if not os.path.exists(jobs_file):
        return jobs
    with open(jobs_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            jobs.append({
                'job_id': row['job_id'],
                'title': row['title'],
                'company_id': row['company_id'],
                'location': row['location'],
                'salary_min': row['salary_min'],
                'salary_max': row['salary_max'],
                'category': row['category'],
                'description': row['description'],
                'posted_date': row.get('posted_date','')
            })
    return jobs

# Load companies from CSV

def load_companies():
    companies_file = os.path.join(DATA_DIR, 'companies.csv')
    companies = []
    if not os.path.exists(companies_file):
        return companies
    with open(companies_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append({
                'company_id': row['company_id'],
                'company_name': row['company_name'],
                'industry': row['industry'],
                'location': row['location'],
                'employee_count': row['employee_count'],
                'description': row['description']
            })
    return companies

# Load applications from CSV

def load_applications():
    applications_file = os.path.join(DATA_DIR, 'applications.csv')
    applications = []
    if not os.path.exists(applications_file):
        return applications
    with open(applications_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            applications.append({
                'application_id': row['application_id'],
                'job_id': row['job_id'],
                'applicant_name': row['applicant_name'],
                'applicant_email': row['applicant_email'],
                'status': row['status'],
                'applied_date': row['applied_date'],
                'resume_id': row.get('resume_id', '')
            })
    return applications

# Load resumes from CSV

def load_resumes():
    resumes_file = os.path.join(DATA_DIR, 'resumes.csv')
    resumes = []
    if not os.path.exists(resumes_file):
        return resumes
    with open(resumes_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            resumes.append({
                'resume_id': row['resume_id'],
                'applicant_name': row['applicant_name'],
                'applicant_email': row['applicant_email'],
                'filename': row['filename'],
                'upload_date': row['upload_date'],
                'summary': row['summary']
            })
    return resumes

# Save resumes to CSV

def save_resumes(resumes):
    resumes_file = os.path.join(DATA_DIR, 'resumes.csv')
    with open(resumes_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['resume_id', 'applicant_name', 'applicant_email', 'filename', 'upload_date', 'summary']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for resume in resumes:
            writer.writerow(resume)


@app.route('/')
def dashboard():
    jobs = load_jobs()
    companies = load_companies()
    featured_jobs = []
    company_map = {c['company_id']: c['company_name'] for c in companies}
    for job in jobs[:5]:
        featured_jobs.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company': company_map.get(job['company_id'], ''),
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max']
        })
    return render_template('dashboard.html', featured_jobs=featured_jobs)

@app.route('/jobs')
def jobs_list_page():
    jobs = load_jobs()
    companies = load_companies()
    company_map = {c['company_id']: c['company_name'] for c in companies}
    jobs_context = []
    for job in jobs:
        jobs_context.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_map.get(job['company_id'], ''),
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max']
        })
    return render_template('job_listings.html', jobs=jobs_context)

@app.route('/job/<job_id>')
def job_detail_page(job_id):
    jobs = load_jobs()
    companies = load_companies()
    job = next((j for j in jobs if j['job_id'] == job_id), None)
    if not job:
        abort(404)
    company = next((c for c in companies if c['company_id'] == job['company_id']), None)
    company_name = company['company_name'] if company else ''
    job_context = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': company_name,
        'description': job['description'],
        'location': job['location'],
        'salary_min': job['salary_min'],
        'salary_max': job['salary_max']
    }
    return render_template('job_details.html', job=job_context)

@app.route('/apply/<job_id>', methods=['GET', 'POST'])
def apply_form_page(job_id):
    jobs = load_jobs()
    companies = load_companies()
    job = next((j for j in jobs if j['job_id'] == job_id), None)
    if not job:
        abort(404)
    company = next((c for c in companies if c['company_id'] == job['company_id']), None)
    company_name = company['company_name'] if company else ''
    if request.method == 'GET':
        job_context = {
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_name
        }
        return render_template('application_form.html', job=job_context)
    else:  # POST for submission
        # Handle form submission if needed (currently simplified)
        applicant_name = request.form.get('applicant_name')
        applicant_email = request.form.get('applicant_email')
        cover_letter = request.form.get('cover_letter')
        resume_file = request.files.get('resume_file')

        if not applicant_name or not applicant_email or not cover_letter or not resume_file:
            abort(400)

        # For testing/demo, just respond with JSON message
        return jsonify({'message': 'Application submitted', 'job_id': job_id, 'applicant_name': applicant_name})

@app.route('/applications')
def application_tracking():
    applications = load_applications()
    jobs = load_jobs()
    companies = load_companies()

    job_map = {job['job_id']: job for job in jobs}
    company_map = {c['company_id']: c['company_name'] for c in companies}

    applications_context = []
    for app in applications:
        job = job_map.get(app['job_id'])
        company_name = company_map.get(job['company_id'], '') if job else ''
        applications_context.append({
            'application_id': app['application_id'],
            'job_title': job['title'] if job else '',
            'company_name': company_name,
            'status': app['status'],
            'applied_date': app['applied_date']
        })
    return render_template('application_tracking.html', applications=applications_context)

@app.route('/application/<app_id>')
def app_detail_page(app_id):
    applications = load_applications()
    app = next((a for a in applications if a['application_id'] == app_id), None)
    if not app:
        abort(404)
    jobs = load_jobs()
    companies = load_companies()
    job = next((j for j in jobs if j['job_id'] == app['job_id']), None)
    company = next((c for c in companies if c['company_id'] == job['company_id']), None) if job else None

    application_detail = {
        'application_id': app['application_id'],
        'applicant_name': app['applicant_name'],
        'applicant_email': app['applicant_email'],
        'status': app['status'],
        'applied_date': app['applied_date'],
        'job_title': job['title'] if job else '',
        'company_name': company['company_name'] if company else ''
    }
    return render_template('application_detail.html', application=application_detail)

@app.route('/companies')
def companies_dir_page():
    companies = load_companies()
    companies_context = []
    for c in companies:
        companies_context.append({
            'company_id': c['company_id'],
            'company_name': c['company_name'],
            'industry': c['industry'],
            'employee_count': c['employee_count']
        })
    return render_template('companies.html', companies=companies_context)

@app.route('/company/<company_id>')
def company_profile_page(company_id):
    companies = load_companies()
    jobs = load_jobs()
    company = next((c for c in companies if c['company_id'] == company_id), None)
    if not company:
        abort(404)
    company_jobs = []
    for job in jobs:
        if job['company_id'] == company_id:
            company_jobs.append({
                'job_id': job['job_id'],
                'title': job['title']
            })
    return render_template('company_profile.html', company=company, jobs=company_jobs)

@app.route('/resumes', methods=['GET', 'POST'])
def resume_management_page():
    if request.method == 'GET':
        resumes = load_resumes()
        return render_template('resumes.html', resumes=resumes)
    elif request.method == 'POST':
        applicant_name = request.form.get('applicant_name')
        applicant_email = request.form.get('applicant_email')
        resume_file = request.files.get('resume_file')

        if not applicant_name or not applicant_email or not resume_file:
            abort(400)

        resumes = load_resumes()
        new_id = 1
        if resumes:
            new_id = max(int(r['resume_id']) for r in resumes) + 1
        now_str = datetime.now().strftime('%Y-%m-%d')
        new_resume = {
            'resume_id': str(new_id),
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': resume_file.filename,
            'upload_date': now_str,
            'summary': ''
        }
        resumes.append(new_resume)
        save_resumes(resumes)

        return jsonify({'message': 'Resume uploaded successfully', 'resume_id': new_resume['resume_id']}), 201

@app.route('/delete_resume/<resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = load_resumes()
    resumes = [r for r in resumes if r['resume_id'] != resume_id]
    save_resumes(resumes)
    return redirect(url_for('resume_management_page'))

@app.route('/search', methods=['POST'])
def search_results_page():
    data = request.get_json()
    if not data or 'query' not in data:
        abort(400)
    query = data['query']
    if not isinstance(query, str):
        abort(400)

    query_lower = query.lower()

    jobs = load_jobs()
    companies = load_companies()

    company_map = {c['company_id']: c['company_name'] for c in companies}

    job_results = []
    for job in jobs:
        if query_lower in job['title'].lower() or query_lower in job['location'].lower():
            job_results.append({
                'job_id': job['job_id'],
                'title': job['title'],
                'company_name': company_map.get(job['company_id'], ''),
                'location': job['location'],
                'salary_min': job['salary_min'],
                'salary_max': job['salary_max']
            })

    company_results = []
    for c in companies:
        if query_lower in c['company_name'].lower() or query_lower in c['industry'].lower():
            company_results.append({
                'company_id': c['company_id'],
                'company_name': c['company_name'],
                'industry': c['industry'],
                'employee_count': c['employee_count']
            })

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)

if __name__ == '__main__':
    app.run(debug=True)
