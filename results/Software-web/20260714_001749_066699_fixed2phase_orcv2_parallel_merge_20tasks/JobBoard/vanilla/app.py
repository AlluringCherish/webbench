from flask import Flask, request, redirect, url_for, send_from_directory, abort, render_template
import os
from datetime import datetime
import uuid

app = Flask(__name__)

DATA_DIR = 'data'
UPLOADS_DIR = 'uploads'

if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)


def read_file_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def write_file_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


def parse_pipe_line(line, fields_count):
    parts = line.split('|')
    if len(parts) < fields_count:
        parts.extend([''] * (fields_count - len(parts)))
    return parts


def load_jobs():
    lines = read_file_lines('jobs.txt')
    jobs = []
    for line in lines:
        parts = parse_pipe_line(line, 9)
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
        except:
            continue
    return jobs


def save_jobs(jobs):
    lines = []
    for job in jobs:
        line = '|'.join([
            str(job['job_id']), job['title'], str(job['company_id']), job['location'],
            str(job['salary_min']), str(job['salary_max']), job['category'], job['description'], job['posted_date']
        ])
        lines.append(line)
    write_file_lines('jobs.txt', lines)


def load_companies():
    lines = read_file_lines('companies.txt')
    companies = []
    for line in lines:
        parts = parse_pipe_line(line, 6)
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
        except:
            continue
    return companies


def save_companies(companies):
    lines = []
    for comp in companies:
        line = '|'.join([
            str(comp['company_id']), comp['company_name'], comp['industry'], comp['location'],
            str(comp['employee_count']), comp['description']
        ])
        lines.append(line)
    write_file_lines('companies.txt', lines)


def load_categories():
    lines = read_file_lines('categories.txt')
    categories = []
    for line in lines:
        parts = parse_pipe_line(line, 3)
        try:
            cat = {
                'category_id': int(parts[0]),
                'category_name': parts[1],
                'description': parts[2]
            }
            categories.append(cat)
        except:
            continue
    return categories


def save_categories(categories):
    lines = []
    for cat in categories:
        line = '|'.join([
            str(cat['category_id']), cat['category_name'], cat['description']
        ])
        lines.append(line)
    write_file_lines('categories.txt', lines)


def load_applications():
    lines = read_file_lines('applications.txt')
    apps = []
    for line in lines:
        parts = parse_pipe_line(line, 7)
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
            apps.append(app)
        except:
            continue
    return apps


def save_applications(apps):
    lines = []
    for app in apps:
        line = '|'.join([
            str(app['application_id']), str(app['job_id']), app['applicant_name'], app['applicant_email'], app['status'], app['applied_date'], str(app['resume_id'])
        ])
        lines.append(line)
    write_file_lines('applications.txt', lines)


def load_resumes():
    lines = read_file_lines('resumes.txt')
    res = []
    for line in lines:
        parts = parse_pipe_line(line, 6)
        try:
            r = {
                'resume_id': int(parts[0]),
                'applicant_name': parts[1],
                'applicant_email': parts[2],
                'filename': parts[3],
                'upload_date': parts[4],
                'summary': parts[5]
            }
            res.append(r)
        except:
            continue
    return res


def save_resumes(res):
    lines = []
    for r in res:
        line = '|'.join([
            str(r['resume_id']), r['applicant_name'], r['applicant_email'], r['filename'], r['upload_date'], r['summary']
        ])
        lines.append(line)
    write_file_lines('resumes.txt', lines)


def get_company_by_id(company_id):
    companies = load_companies()
    for c in companies:
        if c['company_id'] == company_id:
            return c
    return None


def get_job_by_id(job_id):
    jobs = load_jobs()
    for j in jobs:
        if j['job_id'] == job_id:
            return j
    return None


def get_resume_by_id(resume_id):
    resumes = load_resumes()
    for r in resumes:
        if r['resume_id'] == resume_id:
            return r
    return None


def generate_new_id(items, id_field):
    if not items:
        return 1
    return max(item[id_field] for item in items) + 1


@app.route('/')
@app.route('/dashboard')
def dashboard():
    jobs = load_jobs()
    companies = load_companies()
    comp_dict = {c['company_id']: c for c in companies}

    jobs_sorted = sorted(jobs, key=lambda x: x['posted_date'], reverse=True)
    featured_jobs = []
    for job in jobs_sorted[:5]:
        company = comp_dict.get(job['company_id'], {})
        featured_jobs.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company.get('company_name', ''),
            'location': job['location'],
            'description': job['description'],
        })

    return render_template('dashboard.html', featured_jobs=featured_jobs)


@app.route('/jobs')
def list_jobs():
    search = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', '').strip().lower()
    location_filter = request.args.get('location', '').strip().lower()

    jobs = load_jobs()
    companies = load_companies()
    categories = load_categories()

    comp_dict = {c['company_id']: c for c in companies}

    filtered_jobs = []
    for job in jobs:
        if search:
            company_name = comp_dict.get(job['company_id'], {}).get('company_name', '').lower()
            if not (search in job['title'].lower() or search in company_name or search in job['location'].lower()):
                continue
        if category_filter and job['category'].lower() != category_filter:
            continue
        if location_filter and job['location'].lower() != location_filter:
            continue
        filtered_jobs.append(job)

    jobs_for_template = []
    for job in filtered_jobs:
        company = comp_dict.get(job['company_id'], {})
        jobs_for_template.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company.get('company_name', ''),
            'location': job['location'],
            'category': job['category'],
        })

    return render_template('job_listings.html', jobs=jobs_for_template, categories=categories)


@app.route('/jobs/<int:job_id>')
def job_details(job_id):
    job = get_job_by_id(job_id)
    if not job:
        abort(404)
    company = get_company_by_id(job['company_id'])
    if not company:
        abort(404)

    return render_template('job_details.html', job=job, company=company)


@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    job = get_job_by_id(job_id)
    if not job:
        abort(404)

    if request.method == 'GET':
        return render_template('application_form.html')

    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_email = request.form.get('applicant_email', '').strip()
    cover_letter = request.form.get('cover_letter', '').strip()
    resume_file = request.files.get('resume_upload')

    errors = []
    if not applicant_name:
        errors.append("Applicant name is required")
    if not applicant_email:
        errors.append("Applicant email is required")
    if not resume_file:
        errors.append("Resume file is required")

    if errors:
        return render_template('application_form.html', errors=errors,
                               applicant_name=applicant_name,
                               applicant_email=applicant_email,
                               cover_letter=cover_letter), 400

    filename = resume_file.filename
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    filepath = os.path.join(UPLOADS_DIR, unique_filename)
    resume_file.save(filepath)

    resumes = load_resumes()
    new_resume_id = generate_new_id(resumes, 'resume_id')
    today_str = datetime.utcnow().date().isoformat()
    summary_text = cover_letter[:200]

    resumes.append({
        'resume_id': new_resume_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'filename': unique_filename,
        'upload_date': today_str,
        'summary': summary_text,
    })
    save_resumes(resumes)

    applications = load_applications()
    new_app_id = generate_new_id(applications, 'application_id')

    applications.append({
        'application_id': new_app_id,
        'job_id': job_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'status': 'Applied',
        'applied_date': today_str,
        'resume_id': new_resume_id,
    })
    save_applications(applications)

    return redirect(url_for('track_applications'))


@app.route('/applications')
def track_applications():
    status_filter = request.args.get('status', '').strip()
    applications = load_applications()
    jobs = load_jobs()
    companies = load_companies()

    jobs_dict = {j['job_id']: j for j in jobs}
    companies_dict = {c['company_id']: c for c in companies}

    filtered_apps = []
    for app in applications:
        if status_filter and status_filter != 'All' and app['status'] != status_filter:
            continue
        filtered_apps.append(app)

    apps_for_template = []
    for a in filtered_apps:
        job = jobs_dict.get(a['job_id'])
        company = companies_dict.get(job['company_id']) if job else None
        apps_for_template.append({
            'application_id': a['application_id'],
            'job_title': job['title'] if job else 'N/A',
            'company_name': company['company_name'] if company else 'N/A',
            'status': a['status'],
            'applied_date': a['applied_date'],
        })

    return render_template('application_tracking.html', applications=apps_for_template)


@app.route('/applications/<int:application_id>')
def view_application(application_id):
    applications = load_applications()
    app_data = next((a for a in applications if a['application_id'] == application_id), None)
    if not app_data:
        abort(404)
    job = get_job_by_id(app_data['job_id'])
    company = get_company_by_id(job['company_id']) if job else None
    resume = get_resume_by_id(app_data['resume_id'])
    return {
        'application': app_data,
        'job': job,
        'company': company,
        'resume': resume,
    }


@app.route('/companies')
def list_companies():
    search = request.args.get('search', '').strip().lower()
    companies = load_companies()

    filtered = []
    for c in companies:
        if search and search not in c['company_name'].lower() and search not in c['industry'].lower():
            continue
        filtered.append(c)

    return render_template('companies_directory.html', companies=filtered)


@app.route('/companies/<int:company_id>')
def company_profile(company_id):
    company = get_company_by_id(company_id)
    if not company:
        abort(404)
    jobs = load_jobs()
    company_jobs = [j for j in jobs if j['company_id'] == company_id]
    return render_template('company_profile.html', company=company, jobs=company_jobs)


@app.route('/resumes', methods=['GET', 'POST'])
def resumes():
    if request.method == 'GET':
        resumes = load_resumes()
        return render_template('resume_management.html', resumes=resumes)

    resume_file = request.files.get('resume_file')
    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_email = request.form.get('applicant_email', '').strip()
    summary = request.form.get('summary', '').strip()

    errors = []
    if not applicant_name:
        errors.append("Applicant name is required")
    if not applicant_email:
        errors.append("Applicant email is required")
    if not resume_file:
        errors.append("Resume file is required")

    if errors:
        resumes = load_resumes()
        return render_template('resume_management.html', resumes=resumes, errors=errors,
                               applicant_name=applicant_name,
                               applicant_email=applicant_email,
                               summary=summary), 400

    filename = resume_file.filename
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    filepath = os.path.join(UPLOADS_DIR, unique_filename)
    resume_file.save(filepath)

    resumes = load_resumes()
    new_resume_id = generate_new_id(resumes, 'resume_id')
    today_str = datetime.utcnow().date().isoformat()

    resumes.append({
        'resume_id': new_resume_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'filename': unique_filename,
        'upload_date': today_str,
        'summary': summary,
    })
    save_resumes(resumes)

    return redirect(url_for('resumes'))


@app.route('/resumes/delete/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = load_resumes()
    to_delete = next((r for r in resumes if r['resume_id'] == resume_id), None)
    if not to_delete:
        abort(404)
    filepath = os.path.join(UPLOADS_DIR, to_delete['filename'])
    if os.path.exists(filepath):
        os.remove(filepath)
    resumes = [r for r in resumes if r['resume_id'] != resume_id]
    save_resumes(resumes)
    return redirect(url_for('resumes'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOADS_DIR, filename)


@app.route('/search')
def search_results():
    query = request.args.get('query', '').strip().lower()
    if not query:
        abort(400)

    jobs = load_jobs()
    companies = load_companies()

    matched_jobs = []
    matched_companies = []

    for job in jobs:
        company = get_company_by_id(job['company_id'])
        combined = ' '.join([
            job['title'].lower(),
            (company['company_name'].lower() if company else ''),
            job['description'].lower(),
        ])
        if query in combined:
            matched_jobs.append({
                'job_id': job['job_id'],
                'title': job['title'],
                'company_name': company['company_name'] if company else '',
                'location': job['location'],
            })

    for company in companies:
        combined = ' '.join([
            company['company_name'].lower(),
            company['industry'].lower(),
            company['description'].lower(),
        ])
        if query in combined:
            matched_companies.append(company)

    no_results = not matched_jobs and not matched_companies

    return render_template('search_results.html', query=query,
                           job_results=matched_jobs,
                           company_results=matched_companies,
                           no_results_message='No results found' if no_results else '')


if __name__ == '__main__':
    app.run(debug=True)
