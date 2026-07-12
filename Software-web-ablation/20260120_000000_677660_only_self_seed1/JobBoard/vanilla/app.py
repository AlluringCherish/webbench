from flask import Flask, render_template, redirect, url_for, request, flash
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Ensure 'data' and 'uploads' directories exist
if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists('uploads'):
    os.makedirs('uploads')

data_folder = 'data'

# Utility functions for reading and writing data files

def read_jobs():
    jobs_path = os.path.join(data_folder, 'jobs.txt')
    jobs = []
    if not os.path.exists(jobs_path):
        return jobs
    with open(jobs_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
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
                'posted_date': parts[8]
            }
            jobs.append(job)
    return jobs


def read_companies():
    companies_path = os.path.join(data_folder, 'companies.txt')
    companies = []
    if not os.path.exists(companies_path):
        return companies
    with open(companies_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
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


def read_applications():
    applications_path = os.path.join(data_folder, 'applications.txt')
    applications = []
    if not os.path.exists(applications_path):
        return applications
    with open(applications_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
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
    return applications


def read_resumes():
    resumes_path = os.path.join(data_folder, 'resumes.txt')
    resumes = []
    if not os.path.exists(resumes_path):
        return resumes
    with open(resumes_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            resume = {
                'resume_id': int(parts[0]),
                'applicant_name': parts[1],
                'applicant_email': parts[2],
                'filename': parts[3],
                'upload_date': parts[4],
                'summary': parts[5]
            }
            resumes.append(resume)
    return resumes


def save_applications(applications):
    applications_path = os.path.join(data_folder, 'applications.txt')
    with open(applications_path, 'w', encoding='utf-8') as f:
        for app in applications:
            line = '|'.join([
                str(app['application_id']),
                str(app['job_id']),
                app['applicant_name'],
                app['applicant_email'],
                app['status'],
                app['applied_date'],
                str(app['resume_id'])
            ])
            f.write(line + '\n')


def save_resumes(resumes):
    resumes_path = os.path.join(data_folder, 'resumes.txt')
    with open(resumes_path, 'w', encoding='utf-8') as f:
        for r in resumes:
            line = '|'.join([
                str(r['resume_id']),
                r['applicant_name'],
                r['applicant_email'],
                r['filename'],
                r['upload_date'],
                r['summary']
            ])
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


def get_application_by_id(application_id):
    applications = read_applications()
    for app in applications:
        if app['application_id'] == application_id:
            return app
    return None


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Show featured jobs - use latest 5 jobs sorted by posted_date descending
    jobs = read_jobs()
    companies = read_companies()
    jobs_sorted = sorted(jobs, key=lambda x: x['posted_date'], reverse=True)
    featured_jobs_raw = jobs_sorted[:5]

    featured_jobs = []
    for job in featured_jobs_raw:
        company = get_company_by_id(job['company_id'])
        featured_jobs.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company['company_name'] if company else 'Unknown',
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max']
        })

    return render_template('dashboard.html', featured_jobs=featured_jobs)


@app.route('/jobs', methods=['GET', 'POST'])
def job_listings():
    jobs = read_jobs()
    companies = read_companies()
    # Map company_id to company_name once
    company_map = {c['company_id']: c['company_name'] for c in companies}

    categories = set(job['category'] for job in jobs)
    locations = set(job['location'] for job in jobs)

    selected_category = ''
    selected_location = ''
    search_input = ''

    if request.method == 'POST':
        search_input = request.form.get('search_input', '').strip().lower()
        selected_category = request.form.get('category_filter', '')
        selected_location = request.form.get('location_filter', '')

        def matches(job):
            if search_input:
                combined = f"{job['title']} {company_map.get(job['company_id'], '')} {job['location']}".lower()
                if search_input not in combined:
                    return False
            if selected_category and job['category'].lower() != selected_category.lower():
                return False
            if selected_location and job['location'].lower() != selected_location.lower():
                return False
            return True

        filtered_jobs = [job for job in jobs if matches(job)]
    else:
        filtered_jobs = jobs

    jobs_list = []
    for job in filtered_jobs:
        jobs_list.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company_map.get(job['company_id'], 'Unknown'),
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
            'category': job['category']
        })

    # Sort categories and locations for consistent form dropdown
    categories_list = sorted(categories)
    locations_list = sorted(locations)

    return render_template('jobs.html', jobs=jobs_list, categories=categories_list, locations=locations_list, 
                           selected_category=selected_category, selected_location=selected_location, search_input=search_input)


@app.route('/job/<int:job_id>')
def job_details(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return render_template('job_details.html', job=None)
    company = get_company_by_id(job['company_id'])

    job_detail = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': company['company_name'] if company else 'Unknown',
        'description': job['description'],
        'salary_min': job['salary_min'],
        'salary_max': job['salary_max'],
        'location': job['location']
    }
    return render_template('job_details.html', job=job_detail)


@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return render_template('application_form.html', job=None, error_msg='Job not found.')
    company = get_company_by_id(job['company_id'])
    job_brief = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': company['company_name'] if company else 'Unknown'
    }

    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()
        cover_letter = request.form.get('cover_letter', '').strip()
        resume_file = request.files.get('resume_upload')

        if not applicant_name or not applicant_email or not cover_letter or not resume_file:
            error_msg = 'All fields are required including resume upload.'
            return render_template('application_form.html', job=job_brief, error_msg=error_msg)
        # Save resume
        resumes = read_resumes()
        new_resume_id = max([r['resume_id'] for r in resumes], default=0) + 1

        # Save resume file
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        file_ext = os.path.splitext(resume_file.filename)[1]
        safe_filename = f"resume_{new_resume_id}{file_ext}"
        resume_file.save(os.path.join('uploads', safe_filename))

        # Add resume to resumes list
        upload_date = datetime.datetime.now().strftime('%Y-%m-%d')
        # For summary, use first 30 chars of cover letter as summary or empty if none
        summary = cover_letter[:30] if cover_letter else ''
        new_resume = {
            'resume_id': new_resume_id,
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
        new_app_id = max([a['application_id'] for a in applications], default=0) + 1
        applied_date = upload_date
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
        save_applications(applications)

        success_msg = 'Application submitted successfully.'
        return render_template('application_form.html', job=job_brief, success_msg=success_msg)

    # GET
    return render_template('application_form.html', job=job_brief)


@app.route('/applications', methods=['GET', 'POST'])
def application_tracking():
    applications = read_applications()
    jobs = read_jobs()
    companies = read_companies()
    job_map = {job['job_id']: job for job in jobs}
    company_map = {comp['company_id']: comp for comp in companies}

    status_filter = None
    if request.method == 'POST':
        status_filter = request.form.get('status_filter', '').strip()

    filtered_apps = []
    for app in applications:
        if status_filter and status_filter != 'All' and app['status'] != status_filter:
            continue
        job = job_map.get(app['job_id'])
        company = company_map.get(job['company_id']) if job else None
        filtered_apps.append({
            'application_id': app['application_id'],
            'job_title': job['title'] if job else 'Unknown',
            'company_name': company['company_name'] if company else 'Unknown',
            'status': app['status'],
            'applied_date': app['applied_date']
        })

    return render_template('applications.html', applications=filtered_apps)


@app.route('/application/<int:app_id>')
def application_details(app_id):
    application = get_application_by_id(app_id)
    if not application:
        return render_template('application_details.html', application=None)
    job = get_job_by_id(application['job_id'])
    company = get_company_by_id(job['company_id']) if job else None

    application_detail = {
        'application_id': application['application_id'],
        'job_title': job['title'] if job else 'Unknown',
        'company_name': company['company_name'] if company else 'Unknown',
        'status': application['status'],
        'applied_date': application['applied_date'],
        'applicant_name': application['applicant_name'],
        'applicant_email': application['applicant_email'],
        'resume_id': application['resume_id'],
        'cover_letter': ''
    }
    # Retrieve cover letter from resumes summary as approximation
    resume = get_resume_by_id(application['resume_id'])
    if resume:
        # For simplicity, we don't have cover_letter in data, so leave empty
        pass

    return render_template('application_details.html', application=application_detail)


@app.route('/companies', methods=['GET', 'POST'])
def companies_directory():
    companies = read_companies()
    search_company_input = ''
    if request.method == 'POST':
        search_company_input = request.form.get('search_company_input', '').strip().lower()
        if search_company_input:
            companies = [c for c in companies if search_company_input in c['company_name'].lower()]

    companies_list = []
    for c in companies:
        companies_list.append({
            'company_id': c['company_id'],
            'company_name': c['company_name'],
            'industry': c['industry'],
            'employee_count': c['employee_count']
        })
    return render_template('companies.html', companies=companies_list, search_company_input=search_company_input)


@app.route('/company/<int:company_id>')
def company_profile(company_id):
    company = get_company_by_id(company_id)
    if not company:
        return render_template('company_profile.html', company=None, company_jobs=[]) 

    jobs = read_jobs()
    company_jobs_raw = [job for job in jobs if job['company_id'] == company_id]
    # Filter only open jobs - we assume all jobs listed are open (no status field for jobs)
    company_jobs = []
    for job in company_jobs_raw:
        company_jobs.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'status': 'Open'
        })

    company_dict = {
        'company_id': company['company_id'],
        'company_name': company['company_name'],
        'industry': company['industry'],
        'location': company['location'],
        'description': company['description'],
        'employee_count': company['employee_count']
    }
    return render_template('company_profile.html', company=company_dict, company_jobs=company_jobs)


@app.route('/resumes', methods=['GET', 'POST'])
def resume_management():
    resumes = read_resumes()
    message = ''
    if request.method == 'POST':
        resume_file = request.files.get('resume_file')
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()

        if not resume_file or not applicant_name or not applicant_email:
            message = 'All fields are required to upload a resume.'
            return render_template('resumes.html', resumes=resumes, error_msg=message)

        # Save resume file
        new_resume_id = max([r['resume_id'] for r in resumes], default=0) + 1
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        file_ext = os.path.splitext(resume_file.filename)[1]
        safe_filename = f"resume_{new_resume_id}{file_ext}"
        resume_file.save(os.path.join('uploads', safe_filename))

        upload_date = datetime.datetime.now().strftime('%Y-%m-%d')
        new_resume = {
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': safe_filename,
            'upload_date': upload_date,
            'summary': ''
        }
        resumes.append(new_resume)
        save_resumes(resumes)
        resumes = read_resumes()  # reload
        message = 'Resume uploaded successfully.'

    return render_template('resumes.html', resumes=resumes, success_msg=message)


@app.route('/resume/delete/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = read_resumes()
    resumes = [r for r in resumes if r['resume_id'] != resume_id]
    save_resumes(resumes)
    return redirect(url_for('resume_management'))


@app.route('/search')
def search_results():
    query_str = request.args.get('q', '').strip()
    jobs = read_jobs()
    companies = read_companies()

    job_results = []
    company_results = []
    if query_str:
        q_lower = query_str.lower()
        jobs_filtered = [job for job in jobs if q_lower in job['title'].lower() or q_lower in job['location'].lower() or (get_company_by_id(job['company_id']) or {}).get('company_name','').lower().find(q_lower) != -1]
        companies_filtered = [c for c in companies if q_lower in c['company_name'].lower() or q_lower in c['industry'].lower()]

        for job in jobs_filtered:
            company = get_company_by_id(job['company_id'])
            job_results.append({
                'job_id': job['job_id'],
                'title': job['title'],
                'company_name': company['company_name'] if company else 'Unknown',
                'location': job['location']
            })
        for c in companies_filtered:
            company_results.append({
                'company_id': c['company_id'],
                'company_name': c['company_name'],
                'industry': c['industry']
            })

    return render_template('search_results.html', query_str=query_str, job_results=job_results, company_results=company_results)


if __name__ == '__main__':
    app.run(debug=True)
