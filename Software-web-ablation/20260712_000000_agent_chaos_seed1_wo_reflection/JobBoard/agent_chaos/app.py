from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_folder = 'data'

# Utility functions to parse and load data

def load_jobs():
    jobs = []
    jobs_path = os.path.join(data_folder, 'jobs.txt')
    if not os.path.exists(jobs_path):
        return jobs
    with open(jobs_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 9:
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
    return jobs

def load_companies():
    companies = []
    companies_path = os.path.join(data_folder, 'companies.txt')
    if not os.path.exists(companies_path):
        return companies
    with open(companies_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 6:
                    company = {
                        'company_id': int(parts[0]),
                        'company_name': parts[1],
                        'industry': parts[2],
                        'location': parts[3],
                        'employee_count': int(parts[4]),
                        'description': parts[5]
                    }
                    companies.append(company)
    return companies

def load_categories():
    categories = []
    categories_path = os.path.join(data_folder, 'categories.txt')
    if not os.path.exists(categories_path):
        return categories
    with open(categories_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 3:
                    categories.append(parts[1])
    return categories

def load_applications():
    applications = []
    applications_path = os.path.join(data_folder, 'applications.txt')
    if not os.path.exists(applications_path):
        return applications
    with open(applications_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 7:
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

def load_resumes():
    resumes = []
    resumes_path = os.path.join(data_folder, 'resumes.txt')
    if not os.path.exists(resumes_path):
        return resumes
    with open(resumes_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 6:
                    resumes.append({
                        'resume_id': int(parts[0]),
                        'applicant_name': parts[1],
                        'applicant_email': parts[2],
                        'filename': parts[3],
                        'upload_date': parts[4],
                        'summary': parts[5]
                    })
    return resumes

# Save resume metadata
from functions import write_text_file

def save_resumes(resumes):
    lines = []
    for r in resumes:
        line = f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}"
        lines.append(line)
    content = '\n'.join(lines)
    write_text_file({"filename": os.path.join(data_folder, 'resumes.txt'), "content": content})

# Save applications

def save_applications(applications):
    lines = []
    for app in applications:
        line = f"{app['application_id']}|{app['job_id']}|{app['applicant_name']}|{app['applicant_email']}|{app['status']}|{app['applied_date']}|{app['resume_id']}"
        lines.append(line)
    content = '\n'.join(lines)
    write_text_file({"filename": os.path.join(data_folder, 'applications.txt'), "content": content})

# Save jobs if needed (not required by specs, but helper)
def load_job_categories():
    job_categories = {}
    jc_path = os.path.join(data_folder, 'job_categories.txt')
    if not os.path.exists(jc_path):
        return job_categories
    with open(jc_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 3:
                    # mapping_id|job_id|category_id
                    job_id = int(parts[1])
                    category_id = int(parts[2])
                    job_categories[job_id] = category_id
    return job_categories

# Load categories map from id to name

def load_categories_map():
    categories_map = {}
    categories_path = os.path.join(data_folder, 'categories.txt')
    if not os.path.exists(categories_path):
        return categories_map
    with open(categories_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 3:
                    try:
                        cid = int(parts[0])
                        cname = parts[1]
                        categories_map[cid] = cname
                    except:
                        pass
    return categories_map

# Compose featured_jobs: list of job dicts with fields job_id[int], title[str], company_name[str], location[str], salary_min[int], salary_max[int]
def get_featured_jobs():
    jobs = load_jobs()
    companies = {c['company_id']: c for c in load_companies()}
    # Let's pick recent 5 jobs sorted by posted_date descending for feature
    sorted_jobs = sorted(jobs, key=lambda j: j['posted_date'], reverse=True)
    featured = []
    for job in sorted_jobs[:5]:
        company = companies.get(job['company_id'], {})
        featured.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company.get('company_name', 'Unknown'),
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max']
        })
    return featured

@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    featured_jobs = get_featured_jobs()
    return render_template('dashboard.html', featured_jobs=featured_jobs)

@app.route('/jobs')
def job_listings_page():
    jobs = load_jobs()
    companies = {c['company_id']: c for c in load_companies()}
    categories = load_categories()
    # locations fixed
    locations = ["Remote", "On-site", "Hybrid"]

    selected_category = request.args.get('category', None)
    selected_location = request.args.get('location', None)
    search_query = request.args.get('search', None)

    # Filter jobs
    filtered_jobs = []
    for job in jobs:
        # Filter by category
        if selected_category and selected_category != job['category']:
            continue
        # Filter by location
        if selected_location and selected_location != job['location']:
            continue
        # Filter by search in title or company name
        if search_query:
            search_lower = search_query.lower()
            comp_name = companies.get(job['company_id'], {}).get('company_name', '').lower()
            if search_lower not in job['title'].lower() and search_lower not in comp_name:
                continue
        job_copy = job.copy()
        company = companies.get(job['company_id'], {})
        job_copy['company_name'] = company.get('company_name', 'Unknown')
        filtered_jobs.append(job_copy)

    return render_template('job_listings.html', jobs=filtered_jobs, categories=categories, locations=locations,
                           selected_category=selected_category, selected_location=selected_location, search_query=search_query)

@app.route('/job/<int:job_id>')
def job_details_page(job_id):
    jobs = load_jobs()
    companies = {c['company_id']: c for c in load_companies()}
    job = None
    for j in jobs:
        if j['job_id'] == job_id:
            job = j.copy()
            company = companies.get(job['company_id'], {})
            job['company_name'] = company.get('company_name', 'Unknown')
            break
    if not job:
        # Not found, return 404
        return "Job not found", 404

    return render_template('job_details.html', job=job)

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def application_form_page(job_id):
    jobs = load_jobs()
    job = None
    for j in jobs:
        if j['job_id'] == job_id:
            job = {'job_id': j['job_id'], 'title': j['title']}
            break
    if not job:
        return "Job not found", 404

    if request.method == 'GET':
        return render_template('application_form.html', job=job)

    # POST: process application submission
    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_email = request.form.get('applicant_email', '').strip()
    cover_letter = request.form.get('cover_letter', '').strip()
    resume_file = request.files.get('resume_file')

    if not (applicant_name and applicant_email and cover_letter and resume_file):
        # Missing required fields
        # Return with an error page or message could be implemented but spec does not specify, so return 400
        return "Missing required application fields", 400

    # Save the uploaded resume file
    resume_folder = os.path.join('static', 'uploads', 'resumes')
    os.makedirs(resume_folder, exist_ok=True)
    filename = f"{int(datetime.now().timestamp())}_{resume_file.filename}"
    filepath = os.path.join(resume_folder, filename)
    resume_file.save(filepath)

    # Load resumes and applications to assign new IDs
    resumes = load_resumes()
    applications = load_applications()

    next_resume_id = max([r['resume_id'] for r in resumes], default=0) + 1
    next_application_id = max([a['application_id'] for a in applications], default=0) + 1

    # Save new resume metadata
    new_resume = {
        'resume_id': next_resume_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'filename': filename,
        'upload_date': datetime.now().strftime('%Y-%m-%d'),
        'summary': cover_letter[:50]  # Using start of cover letter as summary
    }
    resumes.append(new_resume)
    save_resumes(resumes)

    # Save application
    new_application = {
        'application_id': next_application_id,
        'job_id': job_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'status': 'Applied',
        'applied_date': datetime.now().strftime('%Y-%m-%d'),
        'resume_id': next_resume_id
    }
    applications.append(new_application)
    save_applications(applications)

    # Redirect to applications tracking page after submit
    return redirect(url_for('application_tracking_page'))

@app.route('/applications')
def application_tracking_page():
    applications = load_applications()
    jobs = {j['job_id']: j for j in load_jobs()}
    companies = {c['company_id']: c for c in load_companies()}

    status_filter_options = ["All", "Applied", "Under Review", "Interview", "Rejected"]
    selected_status_filter = request.args.get('status', None)

    filtered_apps = []
    for app in applications:
        if selected_status_filter and selected_status_filter != "All":
            if app['status'] != selected_status_filter:
                continue
        job = jobs.get(app['job_id'], None)
        if not job:
            continue
        company = companies.get(job['company_id'], {})
        filtered_apps.append({
            'application_id': app['application_id'],
            'job_title': job['title'],
            'company_name': company.get('company_name', 'Unknown'),
            'status': app['status'],
            'applied_date': app['applied_date']
        })

    return render_template('applications_tracking.html',
                           applications=filtered_apps,
                           status_filter_options=status_filter_options,
                           selected_status_filter=selected_status_filter)

@app.route('/application/<int:application_id>')
def application_details_page(application_id):
    applications = load_applications()
    jobs = {j['job_id']: j for j in load_jobs()}
    companies = {c['company_id']: c for c in load_companies()}
    resumes = {r['resume_id']: r for r in load_resumes()}

    application = None
    for app in applications:
        if app['application_id'] == application_id:
            job = jobs.get(app['job_id'], None)
            if not job:
                return "Application's job not found", 404
            company = companies.get(job['company_id'], {})
            resume = resumes.get(app['resume_id'], {})
            application = {
                'application_id': app['application_id'],
                'job_title': job['title'],
                'company_name': company.get('company_name', 'Unknown'),
                'applicant_name': app['applicant_name'],
                'applicant_email': app['applicant_email'],
                'status': app['status'],
                'applied_date': app['applied_date'],
                'resume_filename': resume.get('filename', ''),
                'cover_letter': resume.get('summary', '')
            }
            break
    if not application:
        return "Application not found", 404

    return render_template('application_details.html', application=application)

@app.route('/companies')
def companies_directory_page():
    companies = load_companies()

    search_query = request.args.get('search', None)
    filtered_companies = []
    if search_query:
        search_lower = search_query.lower()
        for comp in companies:
            if search_lower in comp['company_name'].lower() or search_lower in comp['industry'].lower():
                filtered_companies.append(comp)
    else:
        filtered_companies = companies

    return render_template('companies_directory.html', companies=filtered_companies, search_query=search_query)

@app.route('/company/<int:company_id>')
def company_profile_page(company_id):
    companies = load_companies()
    jobs = load_jobs()
    company = None
    for comp in companies:
        if comp['company_id'] == company_id:
            company = comp.copy()
            break
    if not company:
        return "Company not found", 404

    # List jobs for this company - simplified: all jobs with this company_id
    company_jobs = []
    for job in jobs:
        if job['company_id'] == company_id:
            # From spec, job dict with job_id, title, status; but jobs.txt has no status field
            # Since no status field in jobs, we assume all listed jobs are open (status 'Open')
            company_jobs.append({
                'job_id': job['job_id'],
                'title': job['title'],
                'status': 'Open'
            })

    return render_template('company_profile.html', company=company, jobs=company_jobs)

@app.route('/resumes')
def resume_management_page():
    resumes = load_resumes()
    return render_template('resumes.html', resumes=resumes)

@app.route('/resumes/upload', methods=['POST'])
def upload_resume():
    if 'resume_file' not in request.files:
        return "No resume file uploaded", 400
    resume_file = request.files['resume_file']
    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_email = request.form.get('applicant_email', '').strip()
    summary = request.form.get('summary', '').strip()

    if not (applicant_name and applicant_email and summary and resume_file):
        return "Missing required fields", 400

    # Save file
    resume_folder = os.path.join('static', 'uploads', 'resumes')
    os.makedirs(resume_folder, exist_ok=True)
    filename = f"{int(datetime.now().timestamp())}_{resume_file.filename}"
    filepath = os.path.join(resume_folder, filename)
    resume_file.save(filepath)

    resumes = load_resumes()
    next_resume_id = max([r['resume_id'] for r in resumes], default=0) + 1
    new_resume = {
        'resume_id': next_resume_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'filename': filename,
        'upload_date': datetime.now().strftime('%Y-%m-%d'),
        'summary': summary
    }
    resumes.append(new_resume)
    save_resumes(resumes)

    return redirect(url_for('resume_management_page'))

@app.route('/resumes/delete/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = load_resumes()
    # Remove the resume if exists
    resumes = [r for r in resumes if r['resume_id'] != resume_id]
    save_resumes(resumes)
    return redirect(url_for('resume_management_page'))

@app.route('/search')
def search_results_page():
    query = request.args.get('q', '').strip()
    jobs = load_jobs()
    companies = load_companies()

    job_results = []
    company_results = []

    if query:
        q_lower = query.lower()
        # Job results filter in title or company_name
        comps_map = {c['company_id']: c for c in companies}
        for job in jobs:
            company_name = comps_map.get(job['company_id'], {}).get('company_name', '')
            if q_lower in job['title'].lower() or q_lower in company_name.lower():
                job_results.append({
                    'job_id': job['job_id'],
                    'title': job['title'],
                    'company_name': company_name,
                    'location': job['location'],
                    'salary_min': job['salary_min'],
                    'salary_max': job['salary_max']
                })

        for comp in companies:
            if q_lower in comp['company_name'].lower() or q_lower in comp['industry'].lower():
                company_results.append({
                    'company_id': comp['company_id'],
                    'company_name': comp['company_name'],
                    'industry': comp['industry'],
                    'employee_count': comp['employee_count']
                })

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)

if __name__ == '__main__':
    app.run(debug=True)
