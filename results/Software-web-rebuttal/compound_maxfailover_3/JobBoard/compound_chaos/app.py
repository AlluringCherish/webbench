from flask import Flask, render_template, request, redirect, url_for, flash, abort
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper function to read pipe delimited file and yield lists of strings

def read_data_file(filepath):
    try:
        with open(filepath, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                yield line.split('|')
    except FileNotFoundError:
        return []

# Loaders for each data file

def load_jobs():
    path = os.path.join(DATA_DIR, 'jobs.txt')
    jobs = []
    for parts in read_data_file(path):
        if len(parts)!=9:
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
                'posted_date': parts[8],
            }
            jobs.append(job)
        except Exception:
            continue
    return jobs


def load_companies():
    path = os.path.join(DATA_DIR, 'companies.txt')
    companies = []
    for parts in read_data_file(path):
        if len(parts) != 6:
            continue
        try:
            company = {
                'company_id': int(parts[0]),
                'company_name': parts[1],
                'industry': parts[2],
                'location': parts[3],
                'employee_count': int(parts[4]),
                'description': parts[5],
            }
            companies.append(company)
        except Exception:
            continue
    return companies


def load_categories():
    path = os.path.join(DATA_DIR, 'categories.txt')
    categories = []
    for parts in read_data_file(path):
        if len(parts) != 3:
            continue
        try:
            category = {
                'category_id': int(parts[0]),
                'category_name': parts[1],
                'description': parts[2],
            }
            categories.append(category)
        except Exception:
            continue
    return categories


def load_applications():
    path = os.path.join(DATA_DIR, 'applications.txt')
    applications = []
    for parts in read_data_file(path):
        if len(parts) !=7:
            continue
        try:
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
        except Exception:
            continue
    return applications


def load_resumes():
    path = os.path.join(DATA_DIR, 'resumes.txt')
    resumes = []
    for parts in read_data_file(path):
        if len(parts) != 6:
            continue
        try:
            resume = {
                'resume_id': int(parts[0]),
                'applicant_name': parts[1],
                'applicant_email': parts[2],
                'filename': parts[3],
                'upload_date': parts[4],
                'summary': parts[5],
            }
            resumes.append(resume)
        except Exception:
            continue
    return resumes

# Save functions

def save_applications(applications):
    path = os.path.join(DATA_DIR, 'applications.txt')
    lines = []
    for app in applications:
        line = '|'.join([
            str(app['application_id']), str(app['job_id']), app['applicant_name'], app['applicant_email'],
            app['status'], app['applied_date'], str(app['resume_id'])
        ])
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def save_resumes(resumes):
    path = os.path.join(DATA_DIR, 'resumes.txt')
    lines = []
    for r in resumes:
        line = '|'.join([
            str(r['resume_id']), r['applicant_name'], r['applicant_email'], r['filename'], r['upload_date'], r['summary']
        ])
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


# Helpers

def get_company_by_id(company_id):
    for comp in load_companies():
        if comp['company_id'] == company_id:
            return comp
    return None


def get_job_by_id(job_id):
    for job in load_jobs():
        if job['job_id'] == job_id:
            return job
    return None


def get_application_by_id(application_id):
    for app in load_applications():
        if app['application_id'] == application_id:
            return app
    return None


def get_resume_by_id(resume_id):
    for res in load_resumes():
        if res['resume_id'] == resume_id:
            return res
    return None


# Routes

@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    jobs = load_jobs()
    # featured_jobs: list of dicts with job_id, title, company_name, location, salary_min, salary_max
    companies = load_companies()
    company_map = {c['company_id']: c for c in companies}

    jobs_sorted = sorted(jobs, key=lambda j: j['posted_date'], reverse=True)
    featured_jobs = []
    new_opportunities = []
    for i, j in enumerate(jobs_sorted):
        cj = {}
        cj['job_id'] = j['job_id']
        cj['title'] = j['title']
        comp = company_map.get(j['company_id'])
        cj['company_name'] = comp['company_name'] if comp else 'Unknown'
        cj['location'] = j['location']
        cj['salary_min'] = j['salary_min']
        cj['salary_max'] = j['salary_max']
        if i < 5:
            featured_jobs.append(cj)
        else:
            new_opportunities.append(cj)

    return render_template('dashboard.html', featured_jobs=featured_jobs, new_opportunities=new_opportunities)


@app.route('/jobs')
def job_listings():
    jobs = load_jobs()
    categories = load_categories()
    # extract unique locations
    locations = sorted({job['location'] for job in jobs})

    filters = {
        'search': request.args.get('search', '').strip(),
        'category': request.args.get('category', '').strip(),
        'location': request.args.get('location', '').strip(),
    }

    filtered_jobs = jobs
    if filters['search']:
        filtered_jobs = [j for j in filtered_jobs if filters['search'].lower() in j['title'].lower() or filters['search'].lower() in j['description'].lower()]
    if filters['category']:
        # category filter expects category id, job has category as string
        # We need to match category id to category_name, then filter jobs by category name
        cats = load_categories()
        cat_name = None
        for c in cats:
            if str(c['category_id']) == filters['category']:
                cat_name = c['category_name']
                break
        if cat_name:
            filtered_jobs = [j for j in filtered_jobs if j['category'] == cat_name]
        else:
            filtered_jobs = []  # no matching category
    if filters['location']:
        filtered_jobs = [j for j in filtered_jobs if filters['location'].lower() in j['location'].lower()]

    # For each job, add company_name for display
    companies = load_companies()
    company_map = {c['company_id']: c['company_name'] for c in companies}
    for job in filtered_jobs:
        job['company_name'] = company_map.get(job['company_id'], 'Unknown')

    return render_template('job_listings.html', jobs=filtered_jobs, categories=categories, locations=locations, filters=filters)


@app.route('/jobs/<int:job_id>')
def job_details(job_id):
    job = get_job_by_id(job_id)
    if not job:
        abort(404)
    company = get_company_by_id(job['company_id'])
    if not company:
        company = {'company_name': 'Unknown', 'industry': '', 'location': '', 'employee_count': 0, 'description': ''}
    return render_template('job_details.html', job=job, company=company)


@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    job = get_job_by_id(job_id)
    if not job:
        abort(404)

    errors = {}
    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()
        cover_letter = request.form.get('cover_letter', '').strip()
        resume_file = request.files.get('resume_file')

        if not applicant_name:
            errors['applicant_name'] = 'Applicant name is required.'
        if not applicant_email:
            errors['applicant_email'] = 'Applicant email is required.'
        if not resume_file or resume_file.filename == '':
            errors['resume_file'] = 'Resume file is required.'

        if errors:
            return render_template('application_form.html', job=job, errors=errors)

        # Save uploaded resume metadata
        resumes = load_resumes()
        new_resume_id = max([r['resume_id'] for r in resumes], default=0) + 1
        today_str = datetime.today().strftime('%Y-%m-%d')
        new_resume = {
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': resume_file.filename,
            'upload_date': today_str,
            'summary': ''  # Empty summary
        }
        resumes.append(new_resume)
        save_resumes(resumes)

        # Save application entry
        applications = load_applications()
        new_app_id = max([a['application_id'] for a in applications], default=0) + 1
        new_app = {
            'application_id': new_app_id,
            'job_id': job_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': 'Applied',
            'applied_date': today_str,
            'resume_id': new_resume_id
        }
        applications.append(new_app)
        save_applications(applications)

        flash('Application submitted successfully.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('application_form.html', job=job, errors=errors)


@app.route('/applications')
def applications_tracking():
    applications = load_applications()
    jobs = load_jobs()
    companies = load_companies()

    filter_status = request.args.get('status', '').strip().lower()

    applications_enriched = []
    for app in applications:
        if filter_status and app['status'].lower() != filter_status:
            continue
        job = get_job_by_id(app['job_id'])
        company = get_company_by_id(job['company_id']) if job else None
        applications_enriched.append({
            'application': app,
            'job': job,
            'company': company,
            'job_title': job['title'] if job else 'Unknown',
            'company_name': company['company_name'] if company else 'Unknown',
            'status': app['status'],
            'applied_date': app['applied_date'],
            'application_id': app['application_id']
        })
    return render_template('applications.html', applications=applications_enriched, filter_status=filter_status)


@app.route('/application/<int:app_id>')
def application_details(app_id):
    application = get_application_by_id(app_id)
    if not application:
        abort(404)
    job = get_job_by_id(application['job_id'])
    resume = get_resume_by_id(application['resume_id'])
    return render_template('application_details.html', application=application, job=job, resume=resume)


@app.route('/companies')
def companies_directory():
    companies = load_companies()
    search_query = request.args.get('search', '').strip()
    if search_query:
        companies = [c for c in companies if search_query.lower() in c['company_name'].lower() or search_query.lower() in c['industry'].lower()]
    return render_template('companies.html', companies=companies, search_query=search_query)


@app.route('/companies/<int:company_id>')
def company_profile(company_id):
    company = get_company_by_id(company_id)
    if not company:
        abort(404)
    jobs = [job for job in load_jobs() if job['company_id'] == company_id]
    return render_template('company_profile.html', company=company, jobs=jobs)


@app.route('/resumes', methods=['GET', 'POST'])
def resume_management():
    resumes = load_resumes()
    errors = {}
    if request.method == 'POST':
        resume_file = request.files.get('resume_file')
        if not resume_file or resume_file.filename == '':
            errors['resume_file'] = 'Resume file is required.'
            return render_template('resumes.html', resumes=resumes, errors=errors)

        # For this spec, simulate saving file and metadata
        new_resume_id = max([r['resume_id'] for r in resumes], default=0) + 1
        today_str = datetime.today().strftime('%Y-%m-%d')

        # We don't get applicant name/email here, so use placeholders
        new_resume = {
            'resume_id': new_resume_id,
            'applicant_name': '',
            'applicant_email': '',
            'filename': resume_file.filename,
            'upload_date': today_str,
            'summary': ''
        }
        resumes.append(new_resume)
        save_resumes(resumes)
        flash('Resume uploaded successfully.', 'success')
        return redirect(url_for('resume_management'))

    return render_template('resumes.html', resumes=resumes, errors=errors)


@app.route('/resumes/delete/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = load_resumes()
    resumes = [r for r in resumes if r['resume_id'] != resume_id]
    save_resumes(resumes)
    return redirect(url_for('resume_management'))


@app.route('/search')
def search_results():
    query = request.args.get('query', '').strip()
    jobs = load_jobs()
    companies = load_companies()

    job_results = []
    company_results = []
    if query:
        q = query.lower()
        job_results = [j for j in jobs if q in j['title'].lower() or q in j['description'].lower() or q in j['location'].lower()]
        company_results = [c for c in companies if q in c['company_name'].lower() or q in c['industry'].lower()]

    # For job_results, add company_name from company list
    company_map = {c['company_id']: c['company_name'] for c in companies}
    for job in job_results:
        job['company_name'] = company_map.get(job['company_id'], 'Unknown')

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)


if __name__ == '__main__':
    app.run(debug=True)
