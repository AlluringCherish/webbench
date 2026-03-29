from flask import Flask, render_template, redirect, url_for, request, abort
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to read and write data files

def read_jobs():
    jobs = []
    filepath = os.path.join(DATA_DIR, 'jobs.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 9:
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
                except Exception:
                    continue
    return jobs


def write_jobs(jobs):
    filepath = os.path.join(DATA_DIR, 'jobs.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for job in jobs:
            line = '{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(
                job['job_id'], job['title'], job['company_id'], job['location'], job['salary_min'], job['salary_max'], job['category'], job['description'], job['posted_date']
            )
            f.write(line + '\n')


def read_companies():
    companies = []
    filepath = os.path.join(DATA_DIR, 'companies.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
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
                except Exception:
                    continue
    return companies


def write_companies(companies):
    filepath = os.path.join(DATA_DIR, 'companies.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for c in companies:
            line = '{}|{}|{}|{}|{}|{}'.format(
                c['company_id'], c['company_name'], c['industry'], c['location'], c['employee_count'], c['description']
            )
            f.write(line + '\n')


def read_categories():
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
                try:
                    category = {
                        'category_id': int(parts[0]),
                        'category_name': parts[1],
                        'description': parts[2]
                    }
                    categories.append(category)
                except Exception:
                    continue
    return categories


def write_categories(categories):
    filepath = os.path.join(DATA_DIR, 'categories.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for cat in categories:
            line = '{}|{}|{}'.format(cat['category_id'], cat['category_name'], cat['description'])
            f.write(line + '\n')


def read_applications():
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
                try:
                    app = {
                        'application_id': int(parts[0]),
                        'job_id': int(parts[1]),
                        'applicant_name': parts[2],
                        'applicant_email': parts[3],
                        'status': parts[4],
                        'applied_date': parts[5],
                        'resume_id': int(parts[6])
                    }
                    applications.append(app)
                except Exception:
                    continue
    return applications


def write_applications(applications):
    filepath = os.path.join(DATA_DIR, 'applications.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for app in applications:
            line = '{}|{}|{}|{}|{}|{}|{}'.format(
                app['application_id'], app['job_id'], app['applicant_name'], app['applicant_email'], app['status'], app['applied_date'], app['resume_id']
            )
            f.write(line + '\n')


def read_resumes():
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
                except Exception:
                    continue
    return resumes


def write_resumes(resumes):
    filepath = os.path.join(DATA_DIR, 'resumes.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for res in resumes:
            line = '{}|{}|{}|{}|{}|{}'.format(
                res['resume_id'], res['applicant_name'], res['applicant_email'], res['filename'], res['upload_date'], res['summary']
            )
            f.write(line + '\n')


# Root redirect
@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))


# Dashboard route
@app.route('/dashboard', methods=['GET'])
def dashboard():
    jobs = read_jobs()
    companies = read_companies()

    # featured_jobs: pick up to 5 jobs with a relatively recent posted_date
    sorted_jobs = sorted(jobs, key=lambda j: j.get('posted_date', ''), reverse=True)
    featured_jobs = sorted_jobs[:5]

    # latest_jobs: the 5 latest jobs, same as featured here
    latest_jobs = sorted_jobs[:5]

    # Enrich jobs for context: get company_name
    company_dict = {c['company_id']: c['company_name'] for c in companies}

    def enrich_job(job):
        return {
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_dict.get(job['company_id'], 'Unknown'),
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max']
        }

    featured_jobs_enriched = [enrich_job(j) for j in featured_jobs]
    latest_jobs_enriched = [enrich_job(j) for j in latest_jobs]

    return render_template('dashboard.html', featured_jobs=featured_jobs_enriched, latest_jobs=latest_jobs_enriched)


# Job Listings
@app.route('/jobs', methods=['GET'])
def job_listings():
    search_query = request.args.get('search_query', '').strip()
    category_filter = request.args.get('category_filter', '').strip()
    location_filter = request.args.get('location_filter', '').strip()

    jobs = read_jobs()
    companies = read_companies()
    categories = read_categories()

    # Collect all unique locations
    all_locations = sorted({job['location'] for job in jobs})

    # Create company map for company_name
    company_dict = {c['company_id']: c['company_name'] for c in companies}

    # Filter jobs based on search and filters
    filtered_jobs = []
    for job in jobs:
        # Compose a searchable string
        searchable_str = f"{job['title']} {company_dict.get(job['company_id'], '')} {job['location']}'.lower()"

        # Search query filtering
        if search_query and search_query.lower() not in searchable_str:
            continue

        # Category filter
        if category_filter and job['category'].lower() != category_filter.lower():
            continue

        # Location filter
        if location_filter and job['location'].lower() != location_filter.lower():
            continue

        filtered_jobs.append(job)

    # Enrich jobs for context
    def enrich_job(job):
        return {
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_dict.get(job['company_id'], 'Unknown'),
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
            'category': job['category']
        }

    enriched_jobs = [enrich_job(j) for j in filtered_jobs]

    # Pass selected filters to templates
    selected_category = None
    try:
        if category_filter:
            selected_category = int(category_filter)
    except Exception:
        selected_category = None

    selected_location = location_filter if location_filter else None
    search_query_return = search_query

    return render_template('job_listings.html', jobs=enriched_jobs, categories=categories, locations=all_locations, selected_category=selected_category, selected_location=selected_location, search_query=search_query_return)


# Job Details
@app.route('/job/<int:job_id>', methods=['GET'])
def job_details(job_id):
    jobs = read_jobs()
    companies = read_companies()
    categories = read_categories()

    job = next((j for j in jobs if j['job_id'] == job_id), None)
    if not job:
        abort(404)

    company = next((c for c in companies if c['company_id'] == job['company_id']), None)
    if not company:
        # Provide a dummy company dict if missing
        company = {'company_id': 0, 'company_name': 'Unknown', 'industry': '', 'location': '', 'employee_count': 0, 'description': ''}

    return render_template('job_details.html', job=job, company=company, categories=categories)


# Application Form
@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    jobs = read_jobs()
    job = next((j for j in jobs if j['job_id'] == job_id), None)
    if not job:
        abort(404)

    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()
        cover_letter = request.form.get('cover_letter', '').strip()
        resume_file = request.files.get('resume_file', None)

        # Validate required fields
        if not applicant_name or not applicant_email or not resume_file:
            # Ideally flash errors and re-render, but spec does not specify error handling UI
            return render_template('application_form.html', job=job)

        resumes = read_resumes()
        applications = read_applications()

        # Save resume file to a folder
        resume_folder = os.path.join(DATA_DIR, 'uploaded_resumes')
        os.makedirs(resume_folder, exist_ok=True)

        # Create new resume_id
        max_resume_id = max([r['resume_id'] for r in resumes], default=0)
        new_resume_id = max_resume_id + 1

        # Sanitize filename by using only the filename portion
        filename = os.path.basename(resume_file.filename)
        save_path = os.path.join(resume_folder, filename)
        # Save the uploaded file
        resume_file.save(save_path)

        # Create resume summary simply as first 100 characters of cover letter
        summary = cover_letter[:100]

        # Use current date for upload_date
        upload_date = datetime.date.today().isoformat()

        new_resume = {
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': summary
        }

        resumes.append(new_resume)
        write_resumes(resumes)

        # Create new application
        max_app_id = max([a['application_id'] for a in applications], default=0)
        new_app_id = max_app_id + 1

        applied_date = datetime.date.today().isoformat()
        new_application = {
            'application_id': new_app_id,
            'job_id': job_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': 'Applied',
            'applied_date': applied_date,
            'resume_id': new_resume_id
        }

        applications.append(new_application)
        write_applications(applications)

        # Redirect to application tracking or confirmation (not specified, so redirect to tracking)
        return redirect(url_for('application_tracking'))

    # GET
    return render_template('application_form.html', job=job)


# Application Tracking
@app.route('/applications', methods=['GET'])
def application_tracking():
    status_filter = request.args.get('status_filter', '').strip()
    applications = read_applications()
    jobs = read_jobs()
    companies = read_companies()

    # Create maps
    jobs_dict = {j['job_id']: j for j in jobs}
    companies_dict = {c['company_id']: c for c in companies}

    filtered_apps = []
    for app_data in applications:
        if status_filter and app_data['status'].lower() != status_filter.lower():
            continue

        job = jobs_dict.get(app_data['job_id'])
        if not job:
            continue

        company = companies_dict.get(job['company_id'])
        if not company:
            company_name = 'Unknown'
        else:
            company_name = company['company_name']

        app_summary = {
            'application_id': app_data['application_id'],
            'job_title': job['title'],
            'company_name': company_name,
            'status': app_data['status'],
            'applied_date': app_data['applied_date']
        }
        filtered_apps.append(app_summary)

    return render_template('application_tracking.html', applications=filtered_apps, selected_status=status_filter)


# Application Details
@app.route('/application/<int:app_id>', methods=['GET'])
def application_details(app_id):
    applications = read_applications()
    jobs = read_jobs()
    resumes = read_resumes()

    application = next((a for a in applications if a['application_id'] == app_id), None)
    if not application:
        abort(404)

    job = next((j for j in jobs if j['job_id'] == application['job_id']), None)
    if not job:
        abort(404)

    resume = next((r for r in resumes if r['resume_id'] == application['resume_id']), None)

    return render_template('application_details.html', application=application, job=job, resume=resume)


# Companies Directory
@app.route('/companies', methods=['GET'])
def companies_directory():
    search_company_query = request.args.get('search_company_query', '').strip()
    companies = read_companies()

    if search_company_query:
        filtered_companies = []
        for c in companies:
            searchable = f"{c['company_name']} {c['industry']}'.lower()"
            if search_company_query.lower() in searchable:
                filtered_companies.append(c)
    else:
        filtered_companies = companies

    return render_template('companies_directory.html', companies=filtered_companies, search_company_query=search_company_query)


# Company Profile
@app.route('/company/<int:company_id>', methods=['GET'])
def company_profile(company_id):
    companies = read_companies()
    jobs = read_jobs()

    company = next((c for c in companies if c['company_id'] == company_id), None)
    if not company:
        abort(404)

    company_jobs = [
        {
            'job_id': j['job_id'],
            'title': j['title'],
            'status': 'Open'
        }
        for j in jobs if j['company_id'] == company_id
    ]

    return render_template('company_profile.html', company=company, jobs=company_jobs)


# Resume Management
@app.route('/resumes', methods=['GET', 'POST'])
def resume_management():
    if request.method == 'POST':
        resume_file = request.files.get('resume_file', None)
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()
        summary = request.form.get('summary', '').strip()

        if not resume_file or not applicant_name or not applicant_email or not summary:
            resumes = read_resumes()
            return render_template('resume_management.html', resumes=resumes)

        resumes = read_resumes()

        # Save resume file to a folder
        resume_folder = os.path.join(DATA_DIR, 'uploaded_resumes')
        os.makedirs(resume_folder, exist_ok=True)

        max_resume_id = max([r['resume_id'] for r in resumes], default=0)
        new_resume_id = max_resume_id + 1

        filename = os.path.basename(resume_file.filename)
        save_path = os.path.join(resume_folder, filename)
        resume_file.save(save_path)

        upload_date = datetime.date.today().isoformat()

        new_resume = {
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': summary
        }

        resumes.append(new_resume)
        write_resumes(resumes)

        return redirect(url_for('resume_management'))

    # GET
    resumes = read_resumes()
    return render_template('resume_management.html', resumes=resumes)


# Delete Resume
@app.route('/resumes/delete/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = read_resumes()
    resumes = [r for r in resumes if r['resume_id'] != resume_id]
    write_resumes(resumes)
    return redirect(url_for('resume_management'))


# Search Route
@app.route('/search', methods=['GET'])
def search_results():
    query = request.args.get('query', '').strip()

    jobs = read_jobs()
    companies = read_companies()

    job_results = []
    company_results = []

    if query:
        query_lower = query.lower()

        # Search jobs
        company_dict = {c['company_id']: c['company_name'] for c in companies}

        for job in jobs:
            searchable = f"{job['title']} {company_dict.get(job['company_id'], '')} {job['location']}'.lower()"
            if query_lower in searchable:
                job_results.append({
                    'job_id': job['job_id'],
                    'title': job['title'],
                    'company_name': company_dict.get(job['company_id'], 'Unknown'),
                    'location': job['location'],
                    'salary_min': job['salary_min'],
                    'salary_max': job['salary_max']
                })

        # Search companies
        for company in companies:
            searchable = f"{company['company_name']} {company['industry']} {company['location']}'.lower()"
            if query_lower in searchable:
                company_results.append({
                    'company_id': company['company_id'],
                    'company_name': company['company_name'],
                    'industry': company['industry'],
                    'location': company['location']
                })

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)


if __name__ == '__main__':
    app.run(debug=True)
