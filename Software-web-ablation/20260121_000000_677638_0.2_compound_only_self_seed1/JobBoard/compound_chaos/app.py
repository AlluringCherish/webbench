from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['UPLOAD_FOLDER'] = 'data/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Utility functions for data loading and saving

# Load jobs
# Returns list of dicts with keys: job_id, title, company_id, location, salary_min, salary_max, category, description, posted_date
def load_jobs():
    jobs = []
    try:
        with open('data/jobs.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 9:
                    continue
                job = {
                    'job_id': int(parts[0]),
                    'title': parts[1],
                    'company_id': int(parts[2]),
                    'location': parts[3],
                    'salary_min': int(parts[4]),
                    'salary_max': int(parts[5]),
                    'category': parts[6],
                    'description': parts[7],
                    'posted_date': parts[8],
                }
                jobs.append(job)
    except FileNotFoundError:
        pass
    return jobs

# Load companies
# Returns list of dicts with keys: company_id, company_name, industry, location, employee_count, description
def load_companies():
    companies = []
    try:
        with open('data/companies.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
                    continue
                company = {
                    'company_id': int(parts[0]),
                    'company_name': parts[1],
                    'industry': parts[2],
                    'location': parts[3],
                    'employee_count': int(parts[4]),
                    'description': parts[5],
                }
                companies.append(company)
    except FileNotFoundError:
        pass
    return companies

# Load categories
# Returns list of dicts with keys: category_id, category_name, description
def load_categories():
    categories = []
    try:
        with open('data/categories.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 3:
                    continue
                category = {
                    'category_id': int(parts[0]),
                    'category_name': parts[1],
                    'description': parts[2],
                }
                categories.append(category)
    except FileNotFoundError:
        pass
    return categories

# Load applications
# Returns list of dicts with keys: application_id, job_id, applicant_name, applicant_email, status, applied_date, resume_id
def load_applications():
    applications = []
    try:
        with open('data/applications.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                application = {
                    'application_id': int(parts[0]),
                    'job_id': int(parts[1]),
                    'applicant_name': parts[2],
                    'applicant_email': parts[3],
                    'status': parts[4],
                    'applied_date': parts[5],
                    'resume_id': int(parts[6]),
                }
                applications.append(application)
    except FileNotFoundError:
        pass
    return applications

# Load resumes
# Returns list of dicts with keys: resume_id, applicant_name, applicant_email, filename, upload_date, summary
def load_resumes():
    resumes = []
    try:
        with open('data/resumes.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
                    continue
                resume = {
                    'resume_id': int(parts[0]),
                    'applicant_name': parts[1],
                    'applicant_email': parts[2],
                    'filename': parts[3],
                    'upload_date': parts[4],
                    'summary': parts[5],
                }
                resumes.append(resume)
    except FileNotFoundError:
        pass
    return resumes

# Save applications
def save_applications(applications):
    lines = []
    for app in applications:
        line = f"{app['application_id']}|{app['job_id']}|{app['applicant_name']}|{app['applicant_email']}|{app['status']}|{app['applied_date']}|{app['resume_id']}"
        lines.append(line)
    with open('data/applications.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Save resumes
def save_resumes(resumes):
    lines = []
    for resume in resumes:
        line = f"{resume['resume_id']}|{resume['applicant_name']}|{resume['applicant_email']}|{resume['filename']}|{resume['upload_date']}|{resume['summary']}"
        lines.append(line)
    with open('data/resumes.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Load categories names list (str list)
def load_category_names():
    categories = load_categories()
    return [cat['category_name'] for cat in categories]

# Helpers to get entities by ID

def get_company_by_id(company_id, companies=None):
    if companies is None:
        companies = load_companies()
    for company in companies:
        if company['company_id'] == company_id:
            return company
    return None

def get_job_by_id(job_id, jobs=None):
    if jobs is None:
        jobs = load_jobs()
    for job in jobs:
        if job['job_id'] == job_id:
            return job
    return None

def get_application_by_id(application_id, applications=None):
    if applications is None:
        applications = load_applications()
    for app in applications:
        if app['application_id'] == application_id:
            return app
    return None

def get_resume_by_id(resume_id, resumes=None):
    if resumes is None:
        resumes = load_resumes()
    for res in resumes:
        if res['resume_id'] == resume_id:
            return res
    return None

# Route implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    jobs = load_jobs()
    companies = load_companies()
    # Sort by posted_date as datetime objects descending
    def parse_date(d):
        try:
            return datetime.strptime(d, '%Y-%m-%d')
        except Exception:
            return datetime.min
    sorted_jobs = sorted(jobs, key=lambda j: parse_date(j['posted_date']), reverse=True)
    featured = sorted_jobs[:5] if len(sorted_jobs) > 5 else sorted_jobs
    company_map = {c['company_id']: c['company_name'] for c in companies}
    featured_jobs = []
    for job in featured:
        featured_jobs.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_map.get(job['company_id'], 'Unknown'),
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
        })
    return render_template('dashboard.html', featured_jobs=featured_jobs)

@app.route('/jobs')
def job_listings_page():
    jobs = load_jobs()
    companies = load_companies()
    categories = load_category_names()
    locations_set = set()
    company_map = {c['company_id']: c['company_name'] for c in companies}
    jobs_with_company = []
    for job in jobs:
        locations_set.add(job['location'])
        jobs_with_company.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_map.get(job['company_id'], 'Unknown'),
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
            'category': job['category'],
        })
    locations = sorted(list(locations_set))
    return render_template('listings.html', jobs=jobs_with_company, categories=categories, locations=locations)

@app.route('/job/<int:job_id>')
def job_details_page(job_id):
    job = get_job_by_id(job_id)
    if job is None:
        return "Job not found", 404
    companies = load_companies()
    company = get_company_by_id(job['company_id'], companies)
    company_name = company['company_name'] if company else 'Unknown'
    job_dict = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': company_name,
        'location': job['location'],
        'salary_min': job['salary_min'],
        'salary_max': job['salary_max'],
        'category': job['category'],
        'description': job['description'],
        'posted_date': job['posted_date'],
    }
    return render_template('job_details.html', job=job_dict)

@app.route('/job/<int:job_id>/apply', methods=['GET'])
def application_form_page(job_id):
    job = get_job_by_id(job_id)
    if job is None:
        return "Job not found", 404
    return render_template('application_form.html', job_id=job_id)

@app.route('/job/<int:job_id>/apply', methods=['POST'])
def submit_application(job_id):
    job = get_job_by_id(job_id)
    if job is None:
        return "Job not found", 404

    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_email = request.form.get('applicant_email', '').strip()
    cover_letter = request.form.get('cover_letter', '').strip()
    resume_file = request.files.get('resume_file')

    error_messages = []
    if not applicant_name:
        error_messages.append('Applicant name is required.')
    if not applicant_email:
        error_messages.append('Applicant email is required.')
    if resume_file is None or resume_file.filename == '':
        error_messages.append('Resume file is required.')

    if error_messages:
        return render_template('application_form.html', job_id=job_id, error_messages=error_messages)

    filename = secure_filename(resume_file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        resume_file.save(save_path)
    except Exception:
        error_messages.append('Failed to save the resume file.')
        return render_template('application_form.html', job_id=job_id, error_messages=error_messages)

    resumes = load_resumes()
    new_resume_id = max((r['resume_id'] for r in resumes), default=0) + 1
    upload_date = datetime.now().strftime('%Y-%m-%d')
    new_resume = {
        'resume_id': new_resume_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'filename': filename,
        'upload_date': upload_date,
        'summary': cover_letter if cover_letter else '',
    }
    resumes.append(new_resume)
    try:
        save_resumes(resumes)
    except Exception:
        error_messages.append('Failed to save resume record.')
        try:
            os.remove(save_path)
        except:
            pass
        return render_template('application_form.html', job_id=job_id, error_messages=error_messages)

    applications = load_applications()
    new_application_id = max((a['application_id'] for a in applications), default=0) + 1
    new_application = {
        'application_id': new_application_id,
        'job_id': job_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'status': 'Applied',
        'applied_date': upload_date,
        'resume_id': new_resume_id,
    }
    applications.append(new_application)
    try:
        save_applications(applications)
    except Exception:
        error_messages.append('Failed to save application record.')
        try:
            resumes = [r for r in resumes if r['resume_id'] != new_resume_id]
            save_resumes(resumes)
        except:
            pass
        try:
            os.remove(save_path)
        except:
            pass
        return render_template('application_form.html', job_id=job_id, error_messages=error_messages)

    return redirect(url_for('application_tracking_page'))

@app.route('/applications')
def application_tracking_page():
    applications = load_applications()
    jobs = load_jobs()
    companies = load_companies()
    status_filter = request.args.get('status_filter', 'All')
    job_map = {job['job_id']: job for job in jobs}
    company_map = {c['company_id']: c for c in companies}
    filtered_apps = []
    for app in applications:
        if status_filter != 'All' and app['status'] != status_filter:
            continue
        job = job_map.get(app['job_id'])
        if job is None:
            continue
        company = company_map.get(job['company_id'], {})
        filtered_apps.append({
            'application_id': app['application_id'],
            'job_title': job['title'],
            'company_name': company.get('company_name', 'Unknown'),
            'status': app['status'],
            'applied_date': app['applied_date'],
        })
    return render_template('tracking.html', applications=filtered_apps, status_filter=status_filter)

@app.route('/application/<int:application_id>')
def application_details_page(application_id):
    application = get_application_by_id(application_id)
    if application is None:
        return "Application not found", 404
    return render_template('application_details.html', application=application)

@app.route('/companies')
def companies_directory_page():
    companies = load_companies()
    companies_sorted = sorted(companies, key=lambda c: c['company_name'])
    return render_template('companies.html', companies=companies_sorted)

@app.route('/company/<int:company_id>')
def company_profile_page(company_id):
    company = get_company_by_id(company_id)
    if company is None:
        return "Company not found", 404
    jobs = load_jobs()
    jobs_for_company = []
    for job in jobs:
        if job['company_id'] == company_id:
            jobs_for_company.append({
                'job_id': job['job_id'],
                'title': job['title'],
                'location': job['location'],
                'salary_min': job['salary_min'],
                'salary_max': job['salary_max'],
                'category': job['category'],
            })
    return render_template('company_profile.html', company=company, jobs=jobs_for_company)

@app.route('/resumes')
def resume_management_page():
    resumes = load_resumes()
    resumes_sorted = sorted(resumes, key=lambda r: r['upload_date'], reverse=True)
    return render_template('resume.html', resumes=resumes_sorted)

@app.route('/resumes/upload', methods=['POST'])
def upload_resume():
    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_email = request.form.get('applicant_email', '').strip()
    summary = request.form.get('summary', '').strip()
    resume_file = request.files.get('resume_file')

    error_messages = []
    if not applicant_name:
        error_messages.append('Applicant name is required.')
    if not applicant_email:
        error_messages.append('Applicant email is required.')
    if resume_file is None or resume_file.filename == '':
        error_messages.append('Resume file is required.')

    if error_messages:
        resumes = load_resumes()
        resumes_sorted = sorted(resumes, key=lambda r: r['upload_date'], reverse=True)
        return render_template('resume.html', resumes=resumes_sorted, error_messages=error_messages)

    filename = secure_filename(resume_file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        resume_file.save(save_path)
    except Exception:
        error_messages.append('Failed to save the resume file.')
        resumes = load_resumes()
        resumes_sorted = sorted(resumes, key=lambda r: r['upload_date'], reverse=True)
        return render_template('resume.html', resumes=resumes_sorted, error_messages=error_messages)

    resumes = load_resumes()
    new_resume_id = max((r['resume_id'] for r in resumes), default=0) + 1
    upload_date = datetime.now().strftime('%Y-%m-%d')
    new_resume = {
        'resume_id': new_resume_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'filename': filename,
        'upload_date': upload_date,
        'summary': summary if summary else '',
    }
    resumes.append(new_resume)
    try:
        save_resumes(resumes)
    except Exception:
        error_messages.append('Failed to save resume record.')
        try:
            os.remove(save_path)
        except:
            pass
        resumes_sorted = sorted(resumes, key=lambda r: r['upload_date'], reverse=True)
        return render_template('resume.html', resumes=resumes_sorted, error_messages=error_messages)

    return redirect(url_for('resume_management_page'))

@app.route('/resumes/delete/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = load_resumes()
    resume_to_delete = None
    for r in resumes:
        if r['resume_id'] == resume_id:
            resume_to_delete = r
            break
    if resume_to_delete is None:
        return redirect(url_for('resume_management_page'))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], resume_to_delete['filename'])
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except:
        pass

    resumes = [r for r in resumes if r['resume_id'] != resume_id]
    try:
        save_resumes(resumes)
    except:
        pass

    return redirect(url_for('resume_management_page'))

@app.route('/search')
def search_results_page():
    query = request.args.get('query', '').strip().lower()
    jobs = load_jobs()
    companies = load_companies()
    job_results = []
    company_results = []
    if query:
        company_map = {c['company_id']: c for c in companies}
        for job in jobs:
            company_name = company_map.get(job['company_id'], {}).get('company_name', '')
            if query in job['title'].lower() or query in company_name.lower():
                job_results.append({
                    'job_id': job['job_id'],
                    'title': job['title'],
                    'company_name': company_name,
                    'location': job['location'],
                    'salary_min': job['salary_min'],
                    'salary_max': job['salary_max'],
                })
        for company in companies:
            if query in company['company_name'].lower() or query in company['industry'].lower() or query in company['location'].lower():
                company_results.append({
                    'company_id': company['company_id'],
                    'company_name': company['company_name'],
                    'industry': company['industry'],
                    'location': company['location'],
                })
    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)

if __name__ == '__main__':
    app.run(debug=True)
