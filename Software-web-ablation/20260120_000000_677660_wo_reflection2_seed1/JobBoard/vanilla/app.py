from flask import Flask, render_template, redirect, url_for, request, flash
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'
UPLOAD_FOLDER = 'uploads'

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def parse_int(s, default=0):
    try:
        return int(s)
    except Exception:
        return default


def read_jobs():
    jobs = []
    filepath = os.path.join(DATA_DIR, 'jobs.txt')
    if not os.path.exists(filepath):
        return jobs
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 9:
                continue
            job = {
                'job_id': parse_int(parts[0]),
                'title': parts[1],
                'company_id': parse_int(parts[2]),
                'location': parts[3],
                'salary_min': parse_int(parts[4]),
                'salary_max': parse_int(parts[5]),
                'category': parts[6],
                'description': parts[7],
                'posted_date': parts[8]
            }
            jobs.append(job)
    return jobs


def save_jobs(jobs):
    filepath = os.path.join(DATA_DIR, 'jobs.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for job in jobs:
            line = f"{job['job_id']}|{job['title']}|{job['company_id']}|{job['location']}|{job['salary_min']}|{job['salary_max']}|{job['category']}|{job['description']}|{job['posted_date']}"
            f.write(line + '\n')


def read_companies():
    companies = []
    filepath = os.path.join(DATA_DIR, 'companies.txt')
    if not os.path.exists(filepath):
        return companies
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            company = {
                'company_id': parse_int(parts[0]),
                'company_name': parts[1],
                'industry': parts[2],
                'location': parts[3],
                'employee_count': parse_int(parts[4]),
                'description': parts[5]
            }
            companies.append(company)
    return companies


def save_companies(companies):
    filepath = os.path.join(DATA_DIR, 'companies.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for c in companies:
            line = f"{c['company_id']}|{c['company_name']}|{c['industry']}|{c['location']}|{c['employee_count']}|{c['description']}"
            f.write(line + '\n')


def read_categories():
    categories = []
    filepath = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(filepath):
        return categories
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            categories.append(parts[1])  # category_name
    return categories


def read_applications():
    applications = []
    filepath = os.path.join(DATA_DIR, 'applications.txt')
    if not os.path.exists(filepath):
        return applications
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            app = {
                'application_id': parse_int(parts[0]),
                'job_id': parse_int(parts[1]),
                'applicant_name': parts[2],
                'applicant_email': parts[3],
                'status': parts[4],
                'applied_date': parts[5],
                'resume_id': parse_int(parts[6])
            }
            applications.append(app)
    return applications


def save_applications(applications):
    filepath = os.path.join(DATA_DIR, 'applications.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for app in applications:
            line = f"{app['application_id']}|{app['job_id']}|{app['applicant_name']}|{app['applicant_email']}|{app['status']}|{app['applied_date']}|{app['resume_id']}"
            f.write(line + '\n')


def read_resumes():
    resumes = []
    filepath = os.path.join(DATA_DIR, 'resumes.txt')
    if not os.path.exists(filepath):
        return resumes
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            resume = {
                'resume_id': parse_int(parts[0]),
                'applicant_name': parts[1],
                'applicant_email': parts[2],
                'filename': parts[3],
                'upload_date': parts[4],
                'summary': parts[5]
            }
            resumes.append(resume)
    return resumes


def save_resumes(resumes):
    filepath = os.path.join(DATA_DIR, 'resumes.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for r in resumes:
            line = f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}"
            f.write(line + '\n')


def get_company_by_id(company_id):
    companies = read_companies()
    for c in companies:
        if c['company_id'] == company_id:
            return c
    return None


def get_job_by_id(job_id):
    jobs = read_jobs()
    for job in jobs:
        if job['job_id'] == job_id:
            return job
    return None


def get_resume_by_id(resume_id):
    resumes = read_resumes()
    for r in resumes:
        if r['resume_id'] == resume_id:
            return r
    return None


def get_application_by_id(app_id):
    applications = read_applications()
    for a in applications:
        if a['application_id'] == app_id:
            return a
    return None


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    jobs = read_jobs()
    companies = read_companies()
    # featured_jobs: show jobs ordered by posted_date descending, top 5
    sorted_jobs = sorted(jobs, key=lambda x: x['posted_date'], reverse=True)
    featured_jobs = []
    for j in sorted_jobs[:5]:
        company = get_company_by_id(j['company_id'])
        if company:
            featured_jobs.append({
                'job_id': j['job_id'],
                'title': j['title'],
                'company_name': company['company_name'],
                'location': j['location'],
                'salary_min': j['salary_min'],
                'salary_max': j['salary_max']
            })
    categories = read_categories()  # May include if needed in template
    return render_template('dashboard.html', featured_jobs=featured_jobs, categories=categories)


@app.route('/jobs', methods=['GET'])
def job_listings():
    jobs = read_jobs()
    companies = read_companies()
    categories = read_categories()

    # Add company_name and category to each job
    jobs_enriched = []
    for j in jobs:
        c = get_company_by_id(j['company_id'])
        company_name = c['company_name'] if c else ''
        jobs_enriched.append({
            'job_id': j['job_id'],
            'title': j['title'],
            'company_name': company_name,
            'location': j['location'],
            'salary_min': j['salary_min'],
            'salary_max': j['salary_max'],
            'category': j['category']
        })

    locations = sorted({j['location'] for j in jobs})

    return render_template('job_listings.html', jobs=jobs_enriched, categories=categories, locations=locations)


@app.route('/jobs', methods=['POST'])
def filter_jobs():
    jobs = read_jobs()
    companies = read_companies()
    categories = read_categories()

    cat_filter = request.form.get('category_filter', '')
    loc_filter = request.form.get('location_filter', '')

    filtered = []
    for j in jobs:
        if cat_filter and j['category'] != cat_filter:
            continue
        if loc_filter and j['location'] != loc_filter:
            continue
        c = get_company_by_id(j['company_id'])
        company_name = c['company_name'] if c else ''
        filtered.append({
            'job_id': j['job_id'],
            'title': j['title'],
            'company_name': company_name,
            'location': j['location'],
            'salary_min': j['salary_min'],
            'salary_max': j['salary_max'],
            'category': j['category']
        })

    locations = sorted({j['location'] for j in jobs})

    return render_template('job_listings.html', jobs=filtered, categories=categories, locations=locations)


@app.route('/job/<int:job_id>')
def job_details(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return "Job not found", 404
    company = get_company_by_id(job['company_id'])
    job_dict = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': company['company_name'] if company else '',
        'location': job['location'],
        'salary_min': job['salary_min'],
        'salary_max': job['salary_max'],
        'description': job['description']
    }
    return render_template('job_details.html', job=job_dict)


@app.route('/job/<int:job_id>/apply', methods=['GET'])
def application_form(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return "Job not found", 404
    return render_template('application_form.html', job_id=job_id)


@app.route('/job/<int:job_id>/apply', methods=['POST'])
def submit_application(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return "Job not found", 404

    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_email = request.form.get('applicant_email', '').strip()
    cover_letter = request.form.get('cover_letter', '').strip()
    resume_file = request.files.get('resume_file')

    if not applicant_name or not applicant_email or not cover_letter or not resume_file:
        flash('All fields are required, including resume upload.')
        return render_template('application_form.html', job_id=job_id)

    # Save resume file
    filename = resume_file.filename
    safe_filename = filename.replace(' ', '_')
    filepath = os.path.join(UPLOAD_FOLDER, safe_filename)
    resume_file.save(filepath)

    # Add resume metadata
    resumes = read_resumes()
    next_resume_id = max([r['resume_id'] for r in resumes], default=0) + 1
    upload_date = datetime.datetime.now().strftime('%Y-%m-%d')
    summary = cover_letter[:50]  # generate summary from cover letter first 50 chars

    new_resume = {
        'resume_id': next_resume_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'filename': safe_filename,
        'upload_date': upload_date,
        'summary': summary
    }
    resumes.append(new_resume)
    save_resumes(resumes)

    # Add application
    applications = read_applications()
    next_app_id = max([a['application_id'] for a in applications], default=0) + 1
    applied_date = datetime.datetime.now().strftime('%Y-%m-%d')
    new_application = {
        'application_id': next_app_id,
        'job_id': job_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'status': 'Applied',
        'applied_date': applied_date,
        'resume_id': next_resume_id
    }
    applications.append(new_application)
    save_applications(applications)

    return redirect(url_for('application_tracking'))


@app.route('/my_applications')
def application_tracking():
    status_filter = request.args.get('status', 'All')
    applications = read_applications()
    jobs = read_jobs()
    companies = read_companies()

    filtered_apps = []
    for app in applications:
        if status_filter != 'All' and app['status'] != status_filter:
            continue
        job = get_job_by_id(app['job_id'])
        company_name = ''
        job_title = ''
        if job:
            job_title = job['title']
            c = get_company_by_id(job['company_id'])
            if c:
                company_name = c['company_name']
        filtered_apps.append({
            'application_id': app['application_id'],
            'job_title': job_title,
            'company_name': company_name,
            'status': app['status'],
            'applied_date': app['applied_date']
        })

    return render_template('application_tracking.html', applications=filtered_apps, filtered_status=status_filter)


@app.route('/application/<int:app_id>')
def application_details(app_id):
    application = get_application_by_id(app_id)
    if not application:
        return "Application not found", 404
    job = get_job_by_id(application['job_id'])
    resume = get_resume_by_id(application['resume_id'])

    application_data = {
        'application_id': application['application_id'],
        'job_id': application['job_id'],
        'applicant_name': application['applicant_name'],
        'applicant_email': application['applicant_email'],
        'status': application['status'],
        'applied_date': application['applied_date'],
        'resume': resume,
        'job': job
    }
    return render_template('application_details.html', application=application_data)


@app.route('/companies')
def companies_directory():
    companies = read_companies()
    # Strip description to none for directory page if desired
    companies_list = []
    for c in companies:
        companies_list.append({
            'company_id': c['company_id'],
            'company_name': c['company_name'],
            'industry': c['industry'],
            'employee_count': c['employee_count']
        })
    return render_template('companies.html', companies=companies_list)


@app.route('/company/<int:company_id>')
def company_profile(company_id):
    company = get_company_by_id(company_id)
    if not company:
        return "Company not found", 404
    jobs = read_jobs()
    company_jobs = []
    for job in jobs:
        if job['company_id'] == company_id:
            company_jobs.append({
                'job_id': job['job_id'],
                'title': job['title'],
                'status': 'Open'  # Status field per spec if applicable. Assumed all listed jobs are open.
            })

    return render_template('company_profile.html', company=company, jobs=company_jobs)


@app.route('/resumes')
def resume_management():
    resumes = read_resumes()
    return render_template('resume_management.html', resumes=resumes)


@app.route('/resumes/upload', methods=['POST'])
def upload_resume():
    resume_file = request.files.get('resume_file')
    if not resume_file:
        flash('No resume file uploaded.')
        return redirect(url_for('resume_management'))

    filename = resume_file.filename
    safe_filename = filename.replace(' ', '_')
    filepath = os.path.join(UPLOAD_FOLDER, safe_filename)
    resume_file.save(filepath)

    # Add resume metadata - as no applicant_name/email on this form, minimal metadata, use filename only
    resumes = read_resumes()
    next_resume_id = max([r['resume_id'] for r in resumes], default=0) + 1
    upload_date = datetime.datetime.now().strftime('%Y-%m-%d')

    new_resume = {
        'resume_id': next_resume_id,
        'applicant_name': '',
        'applicant_email': '',
        'filename': safe_filename,
        'upload_date': upload_date,
        'summary': ''
    }
    resumes.append(new_resume)
    save_resumes(resumes)

    return redirect(url_for('resume_management'))


@app.route('/resumes/delete/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = read_resumes()
    new_resumes = [r for r in resumes if r['resume_id'] != resume_id]
    save_resumes(new_resumes)

    # Also delete saved file if exists
    for r in resumes:
        if r['resume_id'] == resume_id:
            filepath = os.path.join(UPLOAD_FOLDER, r['filename'])
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception:
                    pass
            break

    return redirect(url_for('resume_management'))


@app.route('/search')
def search_results():
    query = request.args.get('query', '').strip()
    jobs = read_jobs()
    companies = read_companies()

    job_results = []
    company_results = []

    if query:
        qlower = query.lower()
        # Search jobs title or company_name
        for job in jobs:
            if qlower in job['title'].lower():
                company = get_company_by_id(job['company_id'])
                company_name = company['company_name'] if company else ''
                job_results.append({
                    'job_id': job['job_id'],
                    'title': job['title'],
                    'company_name': company_name,
                    'location': job['location'],
                    'salary_min': job['salary_min'],
                    'salary_max': job['salary_max']
                })
        # Search companies name or industry
        for company in companies:
            if qlower in company['company_name'].lower() or qlower in company['industry'].lower():
                company_results.append({
                    'company_id': company['company_id'],
                    'company_name': company['company_name'],
                    'industry': company['industry']
                })

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)


if __name__ == '__main__':
    app.run(debug=True)
