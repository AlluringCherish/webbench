from flask import Flask, render_template, redirect, url_for, request, abort
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Data loading and saving functions ---

def load_jobs():
    jobs = []
    try:
        with open(os.path.join(DATA_DIR, 'jobs.txt'), 'r', encoding='utf-8') as file:
            for line in file:
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
    except FileNotFoundError:
        pass
    return jobs


def load_companies():
    companies = []
    try:
        with open(os.path.join(DATA_DIR, 'companies.txt'), 'r', encoding='utf-8') as file:
            for line in file:
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
    except FileNotFoundError:
        pass
    return companies


def load_categories():
    categories = []
    try:
        with open(os.path.join(DATA_DIR, 'categories.txt'), 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                category = {
                    'category_id': int(parts[0]),
                    'category_name': parts[1],
                    'description': parts[2]
                }
                categories.append(category)
    except FileNotFoundError:
        pass
    return categories


def load_applications():
    applications = []
    try:
        with open(os.path.join(DATA_DIR, 'applications.txt'), 'r', encoding='utf-8') as file:
            for line in file:
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
    except FileNotFoundError:
        pass
    return applications


def load_resumes():
    resumes = []
    try:
        with open(os.path.join(DATA_DIR, 'resumes.txt'), 'r', encoding='utf-8') as file:
            for line in file:
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
    except FileNotFoundError:
        pass
    return resumes


def save_applications(applications):
    try:
        with open(os.path.join(DATA_DIR, 'applications.txt'), 'w', encoding='utf-8') as file:
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
                file.write(line + '\n')
    except Exception:
        pass


def save_resumes(resumes):
    try:
        with open(os.path.join(DATA_DIR, 'resumes.txt'), 'w', encoding='utf-8') as file:
            for res in resumes:
                line = '|'.join([
                    str(res['resume_id']),
                    res['applicant_name'],
                    res['applicant_email'],
                    res['filename'],
                    res['upload_date'],
                    res['summary']
                ])
                file.write(line + '\n')
    except Exception:
        pass


# Helpers

def next_id(items, key):
    if not items:
        return 1
    return max(item[key] for item in items) + 1


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


# Filtering helpers

def filter_jobs(jobs, category=None, location=None, search_query=None):
    results = jobs
    if category:
        results = [j for j in results if j['category'] == category]
    if location:
        results = [j for j in results if j['location'].lower() == location.lower()]
    if search_query:
        sq = search_query.lower()
        def match(j):
            comp = get_company_by_id(j['company_id'])
            if not comp:
                return False
            return sq in j['title'].lower() or sq in comp['company_name'].lower() or sq in j['location'].lower()
        results = [j for j in results if match(j)]
    return results


def filter_companies(companies, search_query=None):
    if not search_query:
        return companies
    sq = search_query.lower()
    return [c for c in companies if sq in c['company_name'].lower() or sq in c['industry'].lower()]


# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    jobs = load_jobs()
    companies = load_companies()

    jobs_sorted = sorted(jobs, key=lambda j: j['posted_date'], reverse=True)
    featured_jobs = []
    for job in jobs_sorted[:5]:
        company = get_company_by_id(job['company_id'])
        if not company:
            continue
        featured_jobs.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company['company_name'],
            'location': job['location'],
            'salary_range': f"${job['salary_min']:,} - ${job['salary_max']:,}"
        })
    latest_jobs = featured_jobs.copy()

    categories = [c['category_name'] for c in load_categories()]
    locations = sorted(set(j['location'] for j in jobs))

    return render_template('dashboard.html', featured_jobs=featured_jobs, latest_jobs=latest_jobs, categories=categories, locations=locations)


@app.route('/jobs')
def job_listings_page():
    category = request.args.get('category')
    location = request.args.get('location')
    search_query = request.args.get('q')

    all_jobs = load_jobs()
    filtered_jobs = filter_jobs(all_jobs, category, location, search_query)

    jobs_context = []
    for job in filtered_jobs:
        company = get_company_by_id(job['company_id'])
        if not company:
            continue
        jobs_context.append({
            'job_id': job['job_id'],
            'title': job['title'],
            'company_name': company['company_name'],
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
            'category': job['category']
        })

    categories = [c['category_name'] for c in load_categories()]
    locations = sorted(set(j['location'] for j in all_jobs))

    return render_template('job_listings.html', jobs=jobs_context, categories=categories, locations=locations, selected_category=category, selected_location=location, search_query=search_query)


@app.route('/job/<int:job_id>')
def job_details_page(job_id):
    job = get_job_by_id(job_id)
    if not job:
        abort(404)
    company = get_company_by_id(job['company_id'])
    if not company:
        abort(404)

    job_context = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': company['company_name'],
        'location': job['location'],
        'salary_min': job['salary_min'],
        'salary_max': job['salary_max'],
        'category': job['category'],
        'description': job['description'],
        'posted_date': job['posted_date']
    }

    company_context = {
        'company_id': company['company_id'],
        'company_name': company['company_name'],
        'industry': company['industry'],
        'location': company['location'],
        'employee_count': company['employee_count'],
        'description': company['description']
    }

    return render_template('job_details.html', job=job_context, company=company_context)


@app.route('/apply/<int:job_id>', methods=['GET','POST'])
def application_form_page(job_id):
    job = get_job_by_id(job_id)
    if not job:
        abort(404)
    company = get_company_by_id(job['company_id'])
    if not company:
        abort(404)

    job_context = {
        'job_id': job['job_id'],
        'title': job['title'],
        'company_name': company['company_name']
    }

    form_errors = None

    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()
        cover_letter = request.form.get('cover_letter', '').strip()
        resume_file = request.files.get('resume_file')

        errors = {}
        if not applicant_name:
            errors['applicant_name'] = 'Applicant name is required.'
        if not applicant_email:
            errors['applicant_email'] = 'Applicant email is required.'
        if not resume_file or resume_file.filename == '':
            errors['resume_file'] = 'Resume file is required.'
        if not cover_letter:
            errors['cover_letter'] = 'Cover letter is required.'

        if errors:
            form_errors = errors
        else:
            filename = resume_file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.exists(filepath):
                base, ext = os.path.splitext(filename)
                timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f'{base}_{timestamp}{ext}'
                filepath = os.path.join(UPLOAD_FOLDER, filename)
            resume_file.save(filepath)

            resumes = load_resumes()
            new_resume_id = next_id(resumes, 'resume_id')
            upload_date = datetime.datetime.now().strftime('%Y-%m-%d')
            # Summary is first 100 chars of cover letter without newlines
            summary = cover_letter.replace('\n',' ')[:100]
            resumes.append({
                'resume_id': new_resume_id,
                'applicant_name': applicant_name,
                'applicant_email': applicant_email,
                'filename': filename,
                'upload_date': upload_date,
                'summary': summary
            })
            save_resumes(resumes)

            applications = load_applications()
            new_application_id = next_id(applications, 'application_id')
            applied_date = datetime.datetime.now().strftime('%Y-%m-%d')
            applications.append({
                'application_id': new_application_id,
                'job_id': job_id,
                'applicant_name': applicant_name,
                'applicant_email': applicant_email,
                'status': 'Applied',
                'applied_date': applied_date,
                'resume_id': new_resume_id
            })
            save_applications(applications)

            return redirect(url_for('applications_tracking_page'))

    return render_template('application_form.html', job=job_context, form_errors=form_errors)


@app.route('/applications')
def applications_tracking_page():
    status_filter = request.args.get('status')
    applications = load_applications()
    if status_filter:
        filtered = [a for a in applications if a['status'].lower() == status_filter.lower()]
    else:
        filtered = applications

    jobs = load_jobs()
    apps_context = []
    for a in filtered:
        job = next((j for j in jobs if j['job_id'] == a['job_id']), None)
        if not job:
            continue
        company = get_company_by_id(job['company_id'])
        if not company:
            continue
        apps_context.append({
            'application_id': a['application_id'],
            'job_title': job['title'],
            'company_name': company['company_name'],
            'status': a['status'],
            'applied_date': a['applied_date']
        })

    return render_template('applications.html', applications=apps_context, status_filter=status_filter)


@app.route('/application/<int:app_id>')
def application_details_page(app_id):
    applications = load_applications()
    application = next((a for a in applications if a['application_id'] == app_id), None)
    if not application:
        abort(404)

    job = get_job_by_id(application['job_id'])
    if not job:
        abort(404)
    company = get_company_by_id(job['company_id'])
    if not company:
        abort(404)

    resume = get_resume_by_id(application['resume_id'])
    resume_filename = resume['filename'] if resume else ''

    application_context = {
        'application_id': application['application_id'],
        'job_title': job['title'],
        'company_name': company['company_name'],
        'applicant_name': application['applicant_name'],
        'applicant_email': application['applicant_email'],
        'status': application['status'],
        'applied_date': application['applied_date'],
        'resume_filename': resume_filename,
        'cover_letter': ''  # Cover letter not stored after upload
    }

    return render_template('application_details.html', application=application_context)


@app.route('/companies')
def companies_directory_page():
    search_query = request.args.get('q')
    companies = load_companies()
    filtered = filter_companies(companies, search_query)

    companies_context = []
    for c in filtered:
        companies_context.append({
            'company_id': c['company_id'],
            'company_name': c['company_name'],
            'industry': c['industry'],
            'employee_count': c['employee_count']
        })

    return render_template('companies.html', companies=companies_context, search_query=search_query)


@app.route('/company/<int:company_id>')
def company_profile_page(company_id):
    company = get_company_by_id(company_id)
    if not company:
        abort(404)

    jobs = load_jobs()
    company_jobs = []
    for j in jobs:
        if j['company_id'] == company_id:
            company_jobs.append({
                'job_id': j['job_id'],
                'title': j['title'],
                'status': 'Open'
            })

    company_context = {
        'company_id': company['company_id'],
        'company_name': company['company_name'],
        'industry': company['industry'],
        'location': company['location'],
        'employee_count': company['employee_count'],
        'description': company['description']
    }

    return render_template('company_profile.html', company=company_context, jobs=company_jobs)


@app.route('/resumes', methods=['GET','POST'])
def resume_management_page():
    resumes = load_resumes()
    form_errors = None

    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()
        resume_file = request.files.get('resume_file')

        errors = {}
        if not applicant_name:
            errors['applicant_name'] = 'Applicant name is required.'
        if not applicant_email:
            errors['applicant_email'] = 'Applicant email is required.'
        if not resume_file or resume_file.filename == '':
            errors['resume_file'] = 'Resume file is required.'

        if errors:
            form_errors = errors
        else:
            filename = resume_file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.exists(filepath):
                base, ext = os.path.splitext(filename)
                timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f'{base}_{timestamp}{ext}'
                filepath = os.path.join(UPLOAD_FOLDER, filename)
            resume_file.save(filepath)

            new_resume_id = next_id(resumes, 'resume_id')
            upload_date = datetime.datetime.now().strftime('%Y-%m-%d')
            summary = ''
            resumes.append({
                'resume_id': new_resume_id,
                'applicant_name': applicant_name,
                'applicant_email': applicant_email,
                'filename': filename,
                'upload_date': upload_date,
                'summary': summary
            })
            save_resumes(resumes)

            return redirect(url_for('resume_management_page'))

    resumes_context = []
    for r in resumes:
        resumes_context.append({
            'resume_id': r['resume_id'],
            'filename': r['filename'],
            'upload_date': r['upload_date'],
            'summary': r['summary']
        })

    return render_template('resumes.html', resumes=resumes_context, form_errors=form_errors)


@app.route('/delete_resume/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = load_resumes()
    resume = next((r for r in resumes if r['resume_id'] == resume_id), None)
    if resume:
        path = os.path.join(UPLOAD_FOLDER, resume['filename'])
        if os.path.exists(path):
            os.remove(path)
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
        lower_query = query.lower()
        for job in jobs:
            company = get_company_by_id(job['company_id'])
            if not company:
                continue
            if (lower_query in job['title'].lower() or
                lower_query in company['company_name'].lower() or
                lower_query in job['location'].lower()):
                job_results.append({
                    'job_id': job['job_id'],
                    'title': job['title'],
                    'company_name': company['company_name'],
                    'location': job['location']
                })
        for company in companies:
            if (lower_query in company['company_name'].lower() or
                lower_query in company['industry'].lower()):
                company_results.append({
                    'company_id': company['company_id'],
                    'company_name': company['company_name'],
                    'industry': company['industry']
                })

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)


if __name__ == '__main__':
    app.run(debug=True)
