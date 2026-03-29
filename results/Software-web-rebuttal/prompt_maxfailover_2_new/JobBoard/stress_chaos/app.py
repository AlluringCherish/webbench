from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path

app = Flask(__name__)

DATA_DIR = Path("data")
JOBS_FILE = DATA_DIR / "jobs.txt"
COMPANIES_FILE = DATA_DIR / "companies.txt"
APPLICATIONS_FILE = DATA_DIR / "applications.txt"
CATEGORIES_FILE = DATA_DIR / "categories.txt"
RESUMES_FILE = DATA_DIR / "resumes.txt"
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)


def read_jobs():
    jobs = []
    if JOBS_FILE.exists():
        with JOBS_FILE.open(encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 9:
                    continue
                job = {
                    "job_id": int(parts[0]),
                    "title": parts[1],
                    "company_id": int(parts[2]),
                    "location": parts[3],
                    "salary_min": int(parts[4]) if parts[4].isdigit() else 0,
                    "salary_max": int(parts[5]) if parts[5].isdigit() else 0,
                    "category": parts[6],
                    "description": parts[7],
                    "posted_date": parts[8]
                }
                jobs.append(job)
    return jobs


def read_companies():
    companies = []
    if COMPANIES_FILE.exists():
        with COMPANIES_FILE.open(encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 6:
                    continue
                company = {
                    "company_id": int(parts[0]),
                    "company_name": parts[1],
                    "industry": parts[2],
                    "location": parts[3],
                    "employee_count": parts[4],
                    "description": parts[5]
                }
                companies.append(company)
    return companies


def read_categories():
    categories = []
    if CATEGORIES_FILE.exists():
        with CATEGORIES_FILE.open(encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 3:
                    continue
                category = {
                    "category_id": int(parts[0]),
                    "category_name": parts[1],
                    "description": parts[2]
                }
                categories.append(category)
    return categories


def read_applications():
    applications = []
    if APPLICATIONS_FILE.exists():
        with APPLICATIONS_FILE.open(encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 7:
                    continue
                try:
                    application = {
                        "application_id": int(parts[0]),
                        "job_id": int(parts[1]),
                        "applicant_name": parts[2],
                        "applicant_email": parts[3],
                        "status": parts[4],
                        "applied_date": parts[5],
                        "resume_id": int(parts[6])
                    }
                    applications.append(application)
                except ValueError:
                    continue
    return applications


def read_resumes():
    resumes = []
    if RESUMES_FILE.exists():
        with RESUMES_FILE.open(encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 6:
                    continue
                try:
                    resume = {
                        "resume_id": int(parts[0]),
                        "applicant_name": parts[1],
                        "applicant_email": parts[2],
                        "filename": parts[3],
                        "upload_date": parts[4],
                        "summary": parts[5]
                    }
                    resumes.append(resume)
                except ValueError:
                    continue
    return resumes


def write_application(application: dict):
    line = f"{application['application_id']}|{application['job_id']}|{application['applicant_name']}|{application['applicant_email']}|{application['status']}|{application['applied_date']}|{application['resume_id']}\n"
    with APPLICATIONS_FILE.open("a", encoding="utf-8") as f:
        f.write(line)


def write_resume(resume: dict):
    line = f"{resume['resume_id']}|{resume['applicant_name']}|{resume['applicant_email']}|{resume['filename']}|{resume['upload_date']}|{resume['summary']}\n"
    with RESUMES_FILE.open("a", encoding="utf-8") as f:
        f.write(line)


def delete_resume_by_id(resume_id: int):
    resumes = read_resumes()
    filtered_resumes = [r for r in resumes if r["resume_id"] != resume_id]
    with RESUMES_FILE.open("w", encoding="utf-8") as f:
        for r in filtered_resumes:
            f.write(f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}\n")
    # Remove file from uploads if exists
    for r in resumes:
        if r["resume_id"] == resume_id:
            file_path = UPLOADS_DIR / r["filename"]
            if file_path.exists():
                file_path.unlink()
            break


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    jobs = read_jobs()
    companies = read_companies()
    # Featured jobs: top 3 by posted_date descending
    featured_jobs = sorted(jobs, key=lambda j: j['posted_date'], reverse=True)[:3]
    latest_jobs = sorted(jobs, key=lambda j: j['posted_date'], reverse=True)[:5]

    # Add company_name to jobs for display
    companies_map = {c['company_id']: c['company_name'] for c in companies}
    for job in featured_jobs:
        job['company_name'] = companies_map.get(job['company_id'], '')
    for job in latest_jobs:
        job['company_name'] = companies_map.get(job['company_id'], '')

    return render_template('dashboard.html', featured_jobs=featured_jobs, latest_jobs=latest_jobs)


@app.route('/jobs')
def job_listings_page():
    jobs = read_jobs()
    companies = read_companies()
    categories = read_categories()
    selected_category = request.args.get('selected_category', '')
    selected_location = request.args.get('selected_location', '')
    search_query = request.args.get('search_query', '')

    # Add company_name to each job
    companies_map = {c['company_id']: c['company_name'] for c in companies}
    for job in jobs:
        job['company_name'] = companies_map.get(job['company_id'], '')

    filtered_jobs = jobs
    if selected_category:
        filtered_jobs = [j for j in filtered_jobs if j['category'] == selected_category]
    if selected_location:
        filtered_jobs = [j for j in filtered_jobs if selected_location.lower() in j['location'].lower()]
    if search_query:
        sq = search_query.lower()
        filtered_jobs = [j for j in filtered_jobs if sq in j['title'].lower() or sq in j['description'].lower()]

    return render_template('job_listings.html', jobs=filtered_jobs, categories=categories, selected_category=selected_category, selected_location=selected_location, search_query=search_query)


@app.route('/job/<int:job_id>')
def job_details_page(job_id):
    jobs = read_jobs()
    job = next((j for j in jobs if j['job_id'] == job_id), None)
    if not job:
        return "Job not found", 404
    companies = read_companies()
    company = next((c for c in companies if c['company_id'] == job['company_id']), {})
    return render_template('job_details.html', job=job, company=company)


@app.route('/apply/<int:job_id>', methods=['GET','POST'])
def application_form_page(job_id):
    jobs = read_jobs()
    job = next((j for j in jobs if j['job_id'] == job_id), None)
    if not job:
        return "Job not found", 404

    if request.method == 'GET':
        return render_template('application_form.html', job=job)

    # POST processing
    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_email = request.form.get('applicant_email', '').strip()
    cover_letter = request.form.get('cover_letter', '').strip()
    resume_file = request.files.get('resume_file')
    
    if not (applicant_name and applicant_email and resume_file):
        return "Missing required form fields", 400

    # Save resume file
    filename = f"{applicant_name.replace(' ', '_')}_{resume_file.filename}"
    save_path = UPLOADS_DIR / filename
    resume_file.save(save_path)

    # Load resumes to assign ID
    resumes = read_resumes()
    max_resume_id = max((r['resume_id'] for r in resumes), default=0)
    new_resume_id = max_resume_id + 1

    summary_text = cover_letter[:100] if cover_letter else ""

    new_resume = {
        "resume_id": new_resume_id,
        "applicant_name": applicant_name,
        "applicant_email": applicant_email,
        "filename": filename,
        "upload_date": "2025-01-18",
        "summary": summary_text
    }
    write_resume(new_resume)

    # Load applications to assign application_id
    applications = read_applications()
    max_app_id = max((a['application_id'] for a in applications), default=0)
    new_app_id = max_app_id + 1

    new_application = {
        "application_id": new_app_id,
        "job_id": job_id,
        "applicant_name": applicant_name,
        "applicant_email": applicant_email,
        "status": "Applied",
        "applied_date": "2025-01-18",
        "resume_id": new_resume_id
    }
    write_application(new_application)

    return redirect(url_for('dashboard_page'))


@app.route('/applications')
def application_tracking_page():
    applications = read_applications()
    jobs = read_jobs()
    companies = read_companies()

    # Add job_title and company_name to application
    companies_map = {c['company_id']: c['company_name'] for c in companies}
    jobs_map = {j['job_id']: j for j in jobs}
    for app in applications:
        job = jobs_map.get(app['job_id'])
        if job:
            app['job_title'] = job['title']
            app['company_name'] = companies_map.get(job['company_id'], '')
        else:
            app['job_title'] = ''
            app['company_name'] = ''

    status_filter = request.args.get('status_filter', 'All')
    if status_filter != 'All':
        applications = [a for a in applications if a['status'] == status_filter]

    return render_template('application_tracking.html', applications=applications, status_filter=status_filter)


@app.route('/application/<int:app_id>')
def application_detail_page(app_id):
    applications = read_applications()
    application = next((a for a in applications if a['application_id'] == app_id), None)
    if not application:
        return "Application not found", 404

    jobs = read_jobs()
    companies = read_companies()
    resumes = read_resumes()
    job = next((j for j in jobs if j['job_id'] == application['job_id']), None)
    company = next((c for c in companies if c['company_id'] == job['company_id']), None) if job else None
    resume = next((r for r in resumes if r['resume_id'] == application['resume_id']), None)

    return render_template('application_form.html', application=application, job=job, company=company, resume=resume)


@app.route('/companies')
def companies_directory_page():
    companies = read_companies()
    search_query = request.args.get('search_query', '').strip()
    if search_query:
        sq_l = search_query.lower()
        companies = [c for c in companies if sq_l in c['company_name'].lower() or sq_l in c['industry'].lower()]
    return render_template('companies.html', companies=companies, search_query=search_query)


@app.route('/company/<int:company_id>')
def company_profile_page(company_id):
    companies = read_companies()
    company = next((c for c in companies if c['company_id'] == company_id), None)
    if not company:
        return "Company not found", 404
    jobs = read_jobs()
    company_jobs = [j for j in jobs if j['company_id'] == company_id]
    return render_template('company_profile.html', company=company, jobs=company_jobs)


@app.route('/resumes', methods=["GET", "POST"])
def resume_management_page():
    if request.method == "POST":
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()
        summary = request.form.get('summary', '').strip()
        resume_file = request.files.get('resume_file')

        if not (applicant_name and applicant_email and resume_file):
            return "Missing required form fields", 400

        filename = f"{applicant_name.replace(' ', '_')}_{resume_file.filename}"
        save_path = UPLOADS_DIR / filename
        resume_file.save(save_path)

        resumes = read_resumes()
        max_resume_id = max((r['resume_id'] for r in resumes), default=0)
        new_resume_id = max_resume_id + 1

        new_resume = {
            "resume_id": new_resume_id,
            "applicant_name": applicant_name,
            "applicant_email": applicant_email,
            "filename": filename,
            "upload_date": "2025-01-18",
            "summary": summary
        }
        write_resume(new_resume)

        return redirect(url_for('resume_management_page'))

    # GET
    resumes = read_resumes()
    return render_template('resume_management.html', resumes=resumes)


@app.route('/resume/delete/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    delete_resume_by_id(resume_id)
    return redirect(url_for('resume_management_page'))


@app.route('/search')
def search_results_page():
    query = request.args.get('query', '').strip()
    jobs = read_jobs()
    companies = read_companies()

    # Add company_name to jobs
    companies_map = {c['company_id']: c['company_name'] for c in companies}
    for job in jobs:
        job['company_name'] = companies_map.get(job['company_id'], '')

    job_results = []
    company_results = []
    if query:
        q_lower = query.lower()
        job_results = [j for j in jobs if q_lower in j['title'].lower() or q_lower in j['description'].lower()]
        company_results = [c for c in companies if q_lower in c['company_name'].lower() or q_lower in c['industry'].lower()]

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)


if __name__ == '__main__':
    app.run(debug=True)
