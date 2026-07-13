from flask import Flask, render_template, request, redirect, url_for
import os
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

data_dir = 'data'

# Utility functions to load data from files

def load_jobs():
    jobs = []
    with open(os.path.join(data_dir, 'jobs.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 9:
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
    return jobs

def load_companies():
    companies = []
    with open(os.path.join(data_dir, 'companies.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) !=6:
                continue
            company = {
                'company_id': int(parts[0]),
                'company_name': parts[1],
                'industry': parts[2],
                'location': parts[3],
                'employee_count': parts[4],
                'description': parts[5],
            }
            companies.append(company)
    return companies

def load_categories():
    categories = []
    with open(os.path.join(data_dir, 'categories.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 3:
                continue
            category = {
                'category_id': int(parts[0]),
                'category_name': parts[1],
                'description': parts[2],
            }
            categories.append(category)
    return categories

def load_applications():
    applications = []
    with open(os.path.join(data_dir, 'applications.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 7:
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
    return applications

def load_resumes():
    resumes = []
    with open(os.path.join(data_dir, 'resumes.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
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
    return resumes

def save_applications(applications):
    with open(os.path.join(data_dir, 'applications.txt'), 'w', encoding='utf-8') as f:
        for app in applications:
            line = '|'.join([str(app["application_id"]), str(app["job_id"]), app["applicant_name"], app["applicant_email"], app["status"], app["applied_date"], str(app["resume_id"])])
            f.write(line + '\n')

def save_resumes(resumes):
    with open(os.path.join(data_dir, 'resumes.txt'), 'w', encoding='utf-8') as f:
        for r in resumes:
            line = '|'.join([str(r["resume_id"]), r["applicant_name"], r["applicant_email"], r["filename"], r["upload_date"], r["summary"]])
            f.write(line + '\n')


# Route: Dashboard Page
@app.route('/')
def dashboard():
    jobs = load_jobs()
    companies = load_companies()
    # For featured jobs, pick latest posted (limit 5)
    featured_jobs = []
    if jobs:
        sorted_jobs = sorted(jobs, key=lambda j: j['posted_date'], reverse=True)
        # Attach company name for display
        comp_dict = {c['company_id']: c['company_name'] for c in companies}
        for j in sorted_jobs[:5]:
            fj = j.copy()
            fj['company_name'] = comp_dict.get(j['company_id'], 'Unknown')
            featured_jobs.append(fj)
    return render_template('dashboard.html', featured_jobs=featured_jobs)

# Route: Job Listings Page
@app.route('/jobs')
def job_listings():
    jobs = load_jobs()
    companies = load_companies()
    categories = load_categories()

    # Build dict for company name
    comp_dict = {c['company_id']: c['company_name'] for c in companies}

    # Inject company_name into jobs
    jobs_with_names = []
    for job in jobs:
        job_copy = job.copy()
        job_copy['company_name'] = comp_dict.get(job['company_id'], 'Unknown')
        jobs_with_names.append(job_copy)

    return render_template('job_listings.html', jobs=jobs_with_names, categories=categories)

# Route: Job Details Page
@app.route('/jobs/<int:job_id>')
def job_details(job_id):
    jobs = load_jobs()
    companies = load_companies()
    job = next((j for j in jobs if j['job_id'] == job_id), None)
    if not job:
        return "Job not found", 404
    company = next((c for c in companies if c['company_id'] == job['company_id']), None)
    return render_template('job_details.html', job=job, company=company)

# Route: Application Form Page (GET and POST)
@app.route('/jobs/<int:job_id>/apply', methods=['GET', 'POST'])
def application_form(job_id):
    jobs = load_jobs()
    job = next((j for j in jobs if j['job_id'] == job_id), None)
    if not job:
        return "Job not found", 404

    if request.method == 'POST':
        # Simple handling: retrieve form data
        applicant_name = request.form.get('applicant_name')
        applicant_email = request.form.get('applicant_email')
        cover_letter = request.form.get('cover_letter')
        resume_file = request.files.get('resume')

        # Normally we would save resume file and create resume record
        # For draft, just save application record with dummy resume_id

        applications = load_applications()
        new_app_id = max([app['application_id'] for app in applications], default=0) + 1
        new_resume_id = 1  # Dummy or enhance later
        applied_date = datetime.datetime.now().strftime('%Y-%m-%d')

        new_application = {
            'application_id': new_app_id,
            'job_id': job_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': 'Applied',
            'applied_date': applied_date,
            'resume_id': new_resume_id,
        }
        applications.append(new_application)
        save_applications(applications)

        return redirect(url_for('application_tracking'))

    return render_template('application_form.html')

# Route: Application Tracking Page
@app.route('/applications')
def application_tracking():
    applications = load_applications()
    jobs = load_jobs()
    companies = load_companies()

    job_dict = {job['job_id']: job for job in jobs}
    comp_dict = {c['company_id']: c['company_name'] for c in companies}

    apps_display = []
    for app in applications:
        job = job_dict.get(app['job_id'])
        company_name = comp_dict.get(job['company_id']) if job else 'Unknown'
        apps_display.append({
            'application_id': app['application_id'],
            'job_title': job['title'] if job else 'Unknown',
            'company_name': company_name,
            'status': app['status'],
            'applied_date': app['applied_date'],
        })

    return render_template('application_tracking.html', applications=apps_display)

# Route: Application Detail View
@app.route('/applications/<int:app_id>')
def application_detail(app_id):
    applications = load_applications()
    application = next((a for a in applications if a['application_id'] == app_id), None)
    if not application:
        return "Application not found", 404

    jobs = load_jobs()
    companies = load_companies()
    job = next((j for j in jobs if j['job_id'] == application['job_id']), None)
    company = None
    if job:
        company = next((c for c in companies if c['company_id'] == job['company_id']), None)

    return render_template('application_detail.html', application=application, job=job, company=company)

# Route: Companies Directory
@app.route('/companies')
def companies_directory():
    companies = load_companies()
    return render_template('companies_directory.html', companies=companies)

# Route: Company Profile Page
@app.route('/companies/<int:company_id>')
def company_profile(company_id):
    companies = load_companies()
    company = next((c for c in companies if c['company_id'] == company_id), None)
    if not company:
        return "Company not found", 404

    jobs = load_jobs()
    company_jobs = [j for j in jobs if j['company_id'] == company_id]

    return render_template('company_profile.html', company=company, jobs=company_jobs)

# Route: Resume Management Page (GET and POST)
@app.route('/resumes', methods=['GET', 'POST'])
def resume_management():
    resumes = load_resumes()

    if request.method == 'POST':
        # Handle resume upload
        resume_file = request.files.get('resume_file')
        if resume_file:
            # Save uploaded file to a directory (not implemented for draft)
            # Here, simulate adding resume entry

            new_resume_id = max([r['resume_id'] for r in resumes], default=0) + 1
            upload_date = datetime.datetime.now().strftime('%Y-%m-%d')
            # Normally we would extract applicant info and summary, here dummy
            new_resume = {
                'resume_id': new_resume_id,
                'applicant_name': 'Unknown',
                'applicant_email': 'unknown@example.com',
                'filename': resume_file.filename or f'resume_{new_resume_id}.pdf',
                'upload_date': upload_date,
                'summary': 'Uploaded resume',
            }
            resumes.append(new_resume)
            save_resumes(resumes)

        return redirect(url_for('resume_management'))

    return render_template('resume_management.html', resumes=resumes)

# Route: Resume Delete Action
@app.route('/resumes/<int:resume_id>/delete', methods=['POST'])
def resume_delete(resume_id):
    resumes = load_resumes()
    resumes = [r for r in resumes if r['resume_id'] != resume_id]
    save_resumes(resumes)
    return redirect(url_for('resume_management'))

# Route: Search Results Page
@app.route('/search')
def search_results():
    query = request.args.get('q', '')
    jobs = load_jobs()
    companies = load_companies()

    comp_dict = {c['company_id']: c['company_name'] for c in companies}

    # Simple case insensitive search for job title, company name, or location
    job_results = []
    for job in jobs:
        company_name = comp_dict.get(job['company_id'], 'Unknown')
        if query.lower() in job['title'].lower() or query.lower() in company_name.lower() or query.lower() in job['location'].lower():
            job_copy = job.copy()
            job_copy['company_name'] = company_name
            job_results.append(job_copy)

    # Search companies by name or industry
    company_results = [c for c in companies if query.lower() in c['company_name'].lower() or query.lower() in c['industry'].lower()]

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)


if __name__ == '__main__':
    app.run(debug=True)
