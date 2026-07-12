from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'devsecretkey'

DATA_DIR = 'data'

# Helper function to read pipe delimited files

def read_pipe_delimited_file(filepath, num_fields=0):
    data = []
    try:
        with open(filepath, 'r', encoding='ascii') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if num_fields:
                    if len(parts) < num_fields:
                        parts.extend([''] * (num_fields - len(parts)))
                    elif len(parts) > num_fields:
                        parts = parts[:num_fields]
                parts = [p.strip() for p in parts]
                data.append(parts)
    except FileNotFoundError:
        pass
    return data

# Helper to write pipe delimited file

def write_pipe_delimited_file(filepath, list_of_rows):
    try:
        with open(filepath, 'w', encoding='utf-16') as f:
            for row in list_of_rows:
                f.write('|'.join(row) + '\n')
    except Exception as err:
        print(f'File write error in {filepath} with {err}')

# Loading data functions

def load_jobs():
    return read_pipe_delimited_file(os.path.join(DATA_DIR, 'jobs.txt'), 9)

def load_companies():
    return read_pipe_delimited_file(os.path.join(DATA_DIR, 'companies.txt'), 6)

def load_categories():
    return read_pipe_delimited_file(os.path.join(DATA_DIR, 'categories.txt'), 4)

def load_applications():
    return read_pipe_delimited_file(os.path.join(DATA_DIR, 'applications.txt'), 7)

def load_resumes():
    return read_pipe_delimited_file(os.path.join(DATA_DIR, 'resumes.txt'), 6)

@app.route('/', methods=['GET', 'POST'])
def root_redirect():
    return redirect(url_for('show_dashboard'))

@app.route('/index', methods=['GET'])
def redirect_root():
    user = None
    return render_template('index.html', user=user)

@app.route('/dash', methods=['GET'])
def show_dashboard():
    jobs = load_jobs()
    companies = load_companies()
    company_map = {c[0]: c[1] for c in companies}  # company_id to company_name

    featured_jobs = {}
    for job in jobs:
        featured_jobs[job[0]] = {
            'job_id': job[0],
            'title': job[1],
            'company_name': company_map.get(job[2], ''),
            'loc': job[3],
            'salary_minimum': int(job[4]) if job[4].isdigit() else 0,
            'salary_maximum': int(job[5]) if job[5].isdigit() else 0
        }

    latest_jobs = jobs[-5:] if len(jobs) > 5 else jobs

    return render_template('dashboard.html', featured_jobs=featured_jobs, latest_jobs=latest_jobs)

@app.route('/joblist', methods=['GET'])
def jobs_listing():
    jobs = load_jobs()
    categories = load_categories()
    companies = load_companies()

    categories_dict = {c[0]: c[1] for c in categories}
    locations = list({job[3] for job in jobs if job[3]})
    locations_str = ','.join(locations)
    company_map = {c[0]: c[1] for c in companies}

    jobs_list = []
    for job in jobs:
        min_salary = 100
        max_salary = 1000
        try:
            min_salary = int(job[4])
        except (ValueError, IndexError):
            pass
        try:
            max_salary = int(job[5])
        except (ValueError, IndexError):
            pass
        jobs_list.append({
            'job_id': job[0],
            'title_job': job[1],
            'company_name': company_map.get(job[2], ''),
            'loc': job[3],
            'min_salary': min_salary,
            'max_salary': max_salary,
            'category': job[6] if len(job) > 6 else ''
        })

    return render_template('job_listings.html', jobs=jobs_list, categories=categories_dict, locations=locations_str)

@app.route('/job/detail/<job_id>', methods=['GET'])
def detail_job(job_id):
    jobs = load_jobs()
    companies = load_companies()
    job = None
    for j in jobs:
        if j[0] == job_id:
            job = j
            break

    company = None
    if job:
        for c in companies:
            if c[0] == job[2]:
                company = c
                break

    if not job:
        return render_template('jobs_details.html', job={}, company={})

    job_data = {
        'job_id': job[0],
        'title': job[1],
        'company_name': company[1] if company else '',
        'loc': job[3],
        'salary_min': job[4],
        'salary_max': job[5],
        'description': job[7].split('\n') if len(job) > 7 and job[7] else []
    }

    company_data = {
        'company_name': company[1] if company else '',
        'industry': company[2] if company else '',
        'location': company[3] if company else '',
        'desc': company[5].split('\n') if company and len(company) > 5 and company[5] else []
    }

    return render_template('jobs_details.html', job=job_data, company=company_data)

@app.route('/apply-job/<job_id>', methods=['GET', 'POST'])
def apply_form(job_id):
    jobs = load_jobs()
    job = None
    for j in jobs:
        if j[0] == job_id:
            job = j
            break

    error_message = ''
    success_message = ''

    if request.method == 'POST':
        form = request.form
        applicant_email = form.get('applicant_email')
        applicant_name = form.get('applicant_name')
        cover_letter = form.get('cover_letter')
        resume = form.get('resume')
        if not applicant_email or not applicant_name or not resume:
            error_message = 'Missing required fields'
        else:
            success_message = 'Application submitted successfully'

    job_dict = {}
    if job:
        job_dict = {'job_id': job[0], 'title': job[1]}

    return render_template('application_form.html', job=job_dict, error_msg=error_message, success_msg=success_message)

@app.route('/applications/view', methods=['GET'])
def track_applications():
    applications = load_applications()
    applications_list = []
    for app in applications:
        applications_list.append({
            'application_id': app[0],
            'job_title': '',
            'company': '',
            'state': app[4],
            'applied_date': app[5] if len(app) > 5 else ''
        })
    statuses = ['All', 'Applied', 'Under Review', 'Interview', 'Rejected']
    return render_template('application_tracking.html', application_list=applications_list, statuses=statuses)

@app.route('/application/detail/<id>', methods=['GET'])
def application_detail(id):
    applications = load_applications()
    application = None
    for app in applications:
        if app[0] == id:
            application = app
            break

    if not application:
        return render_template('application_detail.html', application={})

    applied_date_dict = {'year': '0', 'month': '0', 'day': '0'}
    if len(application) > 5 and application[5]:
        parts = application[5].split('/')
        if len(parts) == 3:
            applied_date_dict = {'year': parts[0], 'month': parts[1], 'day': parts[2]}

    application_dict = {
        'job_title': '',
        'company': '',
        'applicant': application[2] if len(application) > 2 else '',
        'applicant_email': application[3].split(',') if len(application) > 3 and application[3] else [],
        'status': application[4] if len(application) > 4 else '',
        'applied_date': applied_date_dict
    }

    return render_template('application_detail.html', application=application_dict)

@app.route('/company_list', methods=['GET'])
def list_companies():
    companies = load_companies()
    companies_list = []
    for c in companies:
        companies_list.append({
            'company_id': c[0],
            'company': c[1],
            'industry': c[2],
            'location': c[3],
            'employee_count': c[4],
            'desc': c[5] if len(c) > 5 else ''
        })
    return render_template('company.html', companies={c['company_id']: c for c in companies_list})

@app.route('/company/<company_id>', methods=['GET'])
def profile_company(company_id):
    companies = load_companies()
    jobs = load_jobs()
    company = None
    for c in companies:
        if c[0] == company_id:
            company = c
            break

    if not company:
        return render_template('companyprofile.html', company={}, company_jobs=None)

    company_dict = {
        'company_name': company[1],
        'industry': company[2],
        'location': company[3],
        'description': company[5].split('\n') if len(company) > 5 and company[5] else []
    }

    company_jobs = []
    for j in jobs:
        if j[2] == company_id:
            company_jobs.append({
                'job_id': j[0],
                'title': j[1]
            })

    return render_template('companyprofile.html', company=company_dict, company_jobs={j['job_id']: j for j in company_jobs})

@app.route('/resume_manage', methods=['GET'])
def manage_resumes():
    resumes = load_resumes()
    resumes_dict = {}
    for r in resumes:
        resumes_dict[r[0]] = {
            'applicant_name': r[1],
            'applicant_email': r[2],
            'filename': r[3],
            'upload_date': r[4],
            'summary': r[5]
        }
    return render_template('resumes.html', resume_list=resumes_dict)

@app.route('/resume_upload', methods=['POST'])
def uploadres():
    return redirect(url_for('manage_resumes'))

@app.route('/remove_resume/<resume_id>', methods=['POST'])
def remove_resume(resume_id):
    resumes = load_resumes()
    new_resumes = [r for r in resumes if r[0] != resume_id]
    write_pipe_delimited_file(os.path.join(DATA_DIR, 'resumes.txt'), new_resumes)

    resumes_dict = {}
    for r in new_resumes:
        resumes_dict[r[0]] = {
            'applicant_name': r[1],
            'applicant_email': r[2],
            'filename': r[3],
            'upload_date': r[4],
            'summary': r[5]
        }
    return render_template('resumes.html', resume_list=resumes_dict)

@app.route('/search_results', methods=['GET'])
def results_search():
    query_str = request.args.get('q', '')
    jobs = load_jobs()
    companies = load_companies()

    company_map = {c[0]: c[1] for c in companies}

    job_results = []
    for job in jobs:
        job_results.append({
            'job_id': job[0],
            'title': job[1],
            'company_name': company_map.get(job[2], ''),
            'location': job[3]
        })

    company_results = []
    for c in companies:
        company_results.append({
            'company_id': c[0],
            'company_name': c[1],
            'industry': c[2]
        })

    return render_template('search_result.html', query=query_str, job_results=job_results, company_results=company_results)


if __name__ == '__main__':
    app.run(debug=True)
