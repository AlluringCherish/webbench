import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
DATA_DIR = 'data'

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# --- Utility functions for reading and writing data files ---

# Read jobs from jobs.txt
def read_jobs():
    jobs = []
    jobs_path = os.path.join(DATA_DIR, 'jobs.txt')
    try:
        with open(jobs_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 9:
                    continue
                try:
                    job = {
                        'job_id': int(fields[0]),
                        'title': fields[1],
                        'company_id': int(fields[2]),
                        'location': fields[3],
                        'salary_min': int(fields[4]),
                        'salary_max': int(fields[5]),
                        'category': fields[6],
                        'description': fields[7],
                        'posted_date': fields[8]
                    }
                    jobs.append(job)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return jobs

# Write jobs back to jobs.txt
def write_jobs(jobs):
    jobs_path = os.path.join(DATA_DIR, 'jobs.txt')
    with open(jobs_path, 'w', encoding='utf-8') as f:
        for job in jobs:
            line = f"{job['job_id']}|{job['title']}|{job['company_id']}|{job['location']}|{job['salary_min']}|{job['salary_max']}|{job['category']}|{job['description']}|{job['posted_date']}"
            f.write(line + '\n')

# Read companies from companies.txt
def read_companies():
    companies = []
    companies_path = os.path.join(DATA_DIR, 'companies.txt')
    try:
        with open(companies_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 6:
                    continue
                try:
                    company = {
                        'company_id': int(fields[0]),
                        'company_name': fields[1],
                        'industry': fields[2],
                        'location': fields[3],
                        'employee_count': int(fields[4]),
                        'description': fields[5]
                    }
                    companies.append(company)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return companies

# Write companies to companies.txt
def write_companies(companies):
    companies_path = os.path.join(DATA_DIR, 'companies.txt')
    with open(companies_path, 'w', encoding='utf-8') as f:
        for c in companies:
            line = f"{c['company_id']}|{c['company_name']}|{c['industry']}|{c['location']}|{c['employee_count']}|{c['description']}"
            f.write(line + '\n')

# Read applications from applications.txt
def read_applications():
    applications = []
    applications_path = os.path.join(DATA_DIR, 'applications.txt')
    try:
        with open(applications_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 7:
                    continue
                try:
                    app = {
                        'application_id': int(fields[0]),
                        'job_id': int(fields[1]),
                        'applicant_name': fields[2],
                        'applicant_email': fields[3],
                        'status': fields[4],
                        'applied_date': fields[5],
                        'resume_id': int(fields[6])
                    }
                    applications.append(app)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return applications

# Write applications to applications.txt
def write_applications(applications):
    applications_path = os.path.join(DATA_DIR, 'applications.txt')
    with open(applications_path, 'w', encoding='utf-8') as f:
        for a in applications:
            line = f"{a['application_id']}|{a['job_id']}|{a['applicant_name']}|{a['applicant_email']}|{a['status']}|{a['applied_date']}|{a['resume_id']}"
            f.write(line + '\n')

# Read resumes from resumes.txt
def read_resumes():
    resumes = []
    resumes_path = os.path.join(DATA_DIR, 'resumes.txt')
    try:
        with open(resumes_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 6:
                    continue
                try:
                    resume = {
                        'resume_id': int(fields[0]),
                        'applicant_name': fields[1],
                        'applicant_email': fields[2],
                        'filename': fields[3],
                        'upload_date': fields[4],
                        'summary': fields[5]
                    }
                    resumes.append(resume)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return resumes

# Write resumes to resumes.txt
def write_resumes(resumes):
    resumes_path = os.path.join(DATA_DIR, 'resumes.txt')
    with open(resumes_path, 'w', encoding='utf-8') as f:
        for r in resumes:
            line = f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}"
            f.write(line + '\n')

# Optional: Read categories from categories.txt (not currently used directly)
def read_categories():
    categories = []
    categories_path = os.path.join(DATA_DIR, 'categories.txt')
    try:
        with open(categories_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) < 2:
                    continue
                categories.append(fields[1])
    except FileNotFoundError:
        pass
    return categories

# --- Routes ---

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    jobs = read_jobs()
    companies = read_companies()
    company_lookup = {c['company_id']: c['company_name'] for c in companies}
    jobs_sorted = sorted(jobs, key=lambda j: j['posted_date'], reverse=True)[:5]
    featured_jobs = []
    for job in jobs_sorted:
        featured_jobs.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_lookup.get(job['company_id'], ''),
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
            'category': job['category']
        })
    browse_jobs_button = True
    my_applications_button = True
    companies_button = True
    return render_template('dashboard.html', featured_jobs=featured_jobs, browse_jobs_button=browse_jobs_button, my_applications_button=my_applications_button, companies_button=companies_button)

@app.route('/jobs')
def job_listings():
    jobs = read_jobs()
    companies = read_companies()
    categories = read_categories()
    company_lookup = {c['company_id']: c['company_name'] for c in companies}

    jobs_for_template = []
    locations_set = set()
    for job in jobs:
        locations_set.add(job['location'])
        jobs_for_template.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_lookup.get(job['company_id'], ''),
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
            'category': job['category']
        })
    locations_list = sorted(locations_set)
    categories_list = sorted(categories)
    return render_template('job_listings.html', jobs=jobs_for_template, categories=categories_list, locations=locations_list, page_title='Job Listings')

@app.route('/job/<int:job_id>')
def job_details(job_id):
    jobs = read_jobs()
    companies = read_companies()
    job = next((j for j in jobs if j['job_id'] == job_id), None)
    if job is None:
        abort(404)
    company = next((c for c in companies if c['company_id'] == job['company_id']), None)
    if company is None:
        abort(404)
    job_context = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': company['company_name'],
        'location': job['location'],
        'salary_min': job['salary_min'],
        'salary_max': job['salary_max'],
        'description': job['description']
    }
    company_context = {
        'company_id': company['company_id'],
        'company_name': company['company_name'],
        'industry': company['industry'],
        'location': company['location'],
        'description': company['description']
    }
    return render_template('job_details.html', job=job_context, company=company_context)

@app.route('/job/<int:job_id>/apply', methods=['GET', 'POST'])
def application_form(job_id):
    jobs = read_jobs()
    job = next((j for j in jobs if j['job_id'] == job_id), None)
    if job is None:
        abort(404)

    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()
        cover_letter = request.form.get('cover_letter', '').strip()  # Could be used/stored later
        resume_file = request.files.get('resume_file')

        if not applicant_name or not applicant_email:
            error = 'Applicant name and email are required.'
            return render_template('application_form.html', job={'job_id': job['job_id'], 'title': job['title']}, error=error)

        filename = None
        if resume_file and resume_file.filename != '':
            filename = secure_filename(resume_file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume_file.save(save_path)

        resumes = read_resumes()
        max_resume_id = max((r['resume_id'] for r in resumes), default=0)
        upload_date = datetime.datetime.now().strftime('%Y-%m-%d')
        summary = f"Uploaded resume for {applicant_name}" if filename else "No resume uploaded"

        new_resume = {
            'resume_id': max_resume_id + 1,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename if filename else '',
            'upload_date': upload_date,
            'summary': summary
        }
        resumes.append(new_resume)
        write_resumes(resumes)

        applications = read_applications()
        max_app_id = max((a['application_id'] for a in applications), default=0)
        new_application = {
            'application_id': max_app_id + 1,
            'job_id': job['job_id'],
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': 'Applied',
            'applied_date': upload_date,
            'resume_id': new_resume['resume_id']
        }
        applications.append(new_application)
        write_applications(applications)

        return redirect(url_for('application_tracking'))

    return render_template('application_form.html', job={'job_id': job['job_id'], 'title': job['title']})

@app.route('/applications')
def application_tracking():
    applications = read_applications()
    jobs = read_jobs()
    companies = read_companies()

    job_lookup = {j['job_id']: j for j in jobs}
    company_lookup = {c['company_id']: c for c in companies}
    applications_for_template = []

    for app in applications:
        job = job_lookup.get(app['job_id'])
        if not job:
            continue
        company = company_lookup.get(job['company_id'])
        if not company:
            continue
        app_dict = {
            'application_id': app['application_id'],
            'job_title': job['title'],
            'company_name': company['company_name'],
            'status': app['status'],
            'applied_date': app['applied_date']
        }
        applications_for_template.append(app_dict)

    status_filter_options = ['All', 'Applied', 'Under Review', 'Rejected']
    return render_template('application_tracking.html', applications=applications_for_template, status_filter_options=status_filter_options)

@app.route('/application/<int:app_id>')
def application_details(app_id):
    applications = read_applications()
    application = next((a for a in applications if a['application_id'] == app_id), None)
    if not application:
        abort(404)

    jobs = read_jobs()
    companies = read_companies()
    job = next((j for j in jobs if j['job_id'] == application['job_id']), None)
    if not job:
        abort(404)
    company = next((c for c in companies if c['company_id'] == job['company_id']), None)
    if not company:
        abort(404)

    application_context = {
        'application_id': application['application_id'],
        'job_id': application['job_id'],
        'applicant_name': application['applicant_name'],
        'applicant_email': application['applicant_email'],
        'status': application['status'],
        'applied_date': application['applied_date'],
        'resume_id': application['resume_id'],
        'job_title': job['title'],
        'company_name': company['company_name']
    }
    return render_template('application_details.html', application=application_context)

@app.route('/companies')
def companies_directory():
    companies = read_companies()
    companies_sorted = sorted(companies, key=lambda c: c['company_name'])
    return render_template('companies.html', companies=companies_sorted)

@app.route('/company/<int:company_id>')
def company_profile(company_id):
    companies = read_companies()
    company = next((c for c in companies if c['company_id'] == company_id), None)
    if not company:
        abort(404)

    jobs = [{'job_id': j['job_id'], 'title': j['title'], 'status': 'Open'} for j in read_jobs() if j['company_id'] == company_id]
    company_context = {
        'company_id': company['company_id'],
        'company_name': company['company_name'],
        'industry': company['industry'],
        'location': company['location'],
        'description': company['description']
    }
    return render_template('company_profile.html', company=company_context, jobs=jobs)

@app.route('/resumes', methods=['GET', 'POST'])
def resume_management():
    if request.method == 'POST':
        resume_file = request.files.get('resume_file')
        if not resume_file or resume_file.filename == '':
            resumes = read_resumes()
            return render_template('resumes.html', resumes=resumes, error='No file selected')

        filename = secure_filename(resume_file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume_file.save(save_path)

        resumes = read_resumes()
        max_resume_id = max((r['resume_id'] for r in resumes), default=0)
        upload_date = datetime.datetime.now().strftime('%Y-%m-%d')
        new_resume = {
            'resume_id': max_resume_id + 1,
            'applicant_name': '',
            'applicant_email': '',
            'filename': filename,
            'upload_date': upload_date,
            'summary': 'Uploaded resume without details'
        }
        resumes.append(new_resume)
        write_resumes(resumes)
        return redirect(url_for('resume_management'))

    resumes = read_resumes()
    return render_template('resumes.html', resumes=resumes)

@app.route('/resume/<int:resume_id>/delete', methods=['POST'])
def delete_resume(resume_id):
    resumes = read_resumes()
    resume_to_delete = next((r for r in resumes if r['resume_id'] == resume_id), None)
    if resume_to_delete:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_to_delete['filename'])
        if os.path.exists(file_path):
            os.remove(file_path)
        resumes = [r for r in resumes if r['resume_id'] != resume_id]
        write_resumes(resumes)
    return redirect(url_for('resume_management'))

@app.route('/search')
def search_results():
    query = request.args.get('q', '').strip()
    if not query:
        return render_template('search_results.html', results=None, query=query)

    query_lower = query.lower()
    jobs = read_jobs()
    companies = read_companies()
    company_lookup = {c['company_id']: c for c in companies}

    job_results = []
    for job in jobs:
        company = company_lookup.get(job['company_id'])
        if not company:
            continue
        if query_lower in job['title'].lower() or query_lower in job['location'].lower() or query_lower in company['company_name'].lower():
            job_results.append({
                'job_id': job['job_id'],
                'title': job['title'],
                'company_name': company['company_name'],
                'location': job['location'],
                'salary_min': job['salary_min'],
                'salary_max': job['salary_max'],
                'category': job['category']
            })

    company_results = []
    for company in companies:
        if query_lower in company['company_name'].lower() or query_lower in company['industry'].lower():
            company_results.append(company)

    results = {'jobs': job_results, 'companies': company_results}
    return render_template('search_results.html', results=results, query=query)

if __name__ == '__main__':
    app.run(debug=True)
