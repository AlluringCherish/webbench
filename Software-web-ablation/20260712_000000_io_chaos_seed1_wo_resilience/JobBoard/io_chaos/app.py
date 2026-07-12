from flask import Flask, render_template, redirect, url_for, request, abort
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Utility functions to load data file and parse pipe-delimited formats

def load_jobs():
    jobs = []
    try:
        with open('data/jobs.txt', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line == '':
                    continue
                parts = line.split('|')
                if len(parts) < 8:
                    continue
                try:
                    job_id = int(parts[0])
                except ValueError:
                    continue
                title = parts[1]
                try:
                    company_id = int(parts[2])  # Will link later with companies
                except ValueError:
                    company_id = None
                location = parts[3]
                try:
                    salary_min = int(parts[4])
                except ValueError:
                    salary_min = parts[4]
                try:
                    salary_max = int(parts[5])
                except ValueError:
                    salary_max = parts[5]
                category = parts[6]
                description = parts[7]
                posted_date = parts[8] if len(parts) > 8 else ''
                jobs.append({
                    'job_id': job_id,
                    'title': title,
                    'company_id': company_id,
                    'location': location,
                    'salary_min': salary_min,
                    'salary_max': salary_max,
                    'category': category,
                    'description': description,
                    'posted_date': posted_date,
                })
    except FileNotFoundError:
        return []
    return jobs


def load_companies():
    companies = []
    try:
        with open('data/companies.txt', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
                    continue
                try:
                    company_id = int(parts[0])
                except ValueError:
                    continue
                company_name = parts[1]
                industry = parts[2]
                location = parts[3]
                employee_count = parts[4]
                description = parts[5]
                companies.append({
                    'company_id': company_id,
                    'company_name': company_name,
                    'industry': industry,
                    'location': location,
                    'employee_count': employee_count,
                    'description': description,
                })
    except FileNotFoundError:
        pass
    return companies


def load_categories():
    categories = []
    try:
        with open('data/categories.txt', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                try:
                    category_id = int(parts[0])
                except ValueError:
                    continue
                category_name = parts[1]
                description = parts[2]
                categories.append({
                    'category_id': category_id,
                    'category_name': category_name,
                    'description': description,
                })
    except FileNotFoundError:
        pass
    return categories


def load_applications():
    applications = []
    try:
        with open('data/applications.txt', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                application_id = parts[0]
                try:
                    job_id = int(parts[1])
                except ValueError:
                    continue
                applicant_name = parts[2]
                applicant_email = parts[3]
                status = parts[4]
                applied_date = parts[5]
                resume_id = int(parts[6])
                applications.append({
                    'application_id': application_id,
                    'job_id': job_id,
                    'applicant_name': applicant_name,
                    'applicant_email': applicant_email,
                    'status': status,
                    'applied_date': applied_date,
                    'resume_id': resume_id,
                })
    except FileNotFoundError:
        pass
    return applications


def load_resumes():
    resumes = []
    try:
        with open('data/resumes.txt', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
                    continue
                try:
                    resume_id = int(parts[0])
                except ValueError:
                    continue
                applicant_name = parts[1]
                applicant_email = parts[2]
                filename = parts[3]
                upload_date = parts[4]
                summary = parts[5]
                resumes.append({
                    'resume_id': resume_id,
                    'applicant_name': applicant_name,
                    'applicant_email': applicant_email,
                    'filename': filename,
                    'upload_date': upload_date,
                    'summary': summary,
                })
    except FileNotFoundError:
        pass
    return resumes


# Save applications function for data update

def save_applications(applications):
    try:
        with open('data/applications.txt', 'w', encoding='utf-8') as f:
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
    except Exception as e:
        print('Error writing applications:', e)


def save_resumes(resumes):
    try:
        with open('data/resumes.txt', 'w', encoding='utf-8') as f:
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
    except Exception as e:
        print('Error writing resumes:', e)


# Helper function: get company name by company_id

def get_company_name(company_id, companies):
    for c in companies:
        if c['company_id'] == company_id:
            return c['company_name']
    return 'None'


# ROUTES

@ app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))


@ app.route('/dashboard', methods=['GET'])
def dashboard():
    jobs = load_jobs()
    companies = load_companies()

    featured_jobs = []
    latest_jobs = []

    if jobs:
        sorted_jobs = sorted(
            jobs,
            key=lambda j: j['posted_date'],
            reverse=True
        )
        latest_jobs = sorted_jobs[:5]

        jobs_with_salary = [j for j in jobs if isinstance(j['salary_min'], int)]
        jobs_with_salary_sorted = sorted(
            jobs_with_salary,
            key=lambda j: j['salary_min'],
            reverse=True
        )
        featured_jobs = jobs_with_salary_sorted[:5]

    def prepare_job_dict(j):
        company_name = get_company_name(j['company_id'], companies)
        try:
            salary_min = float(j['salary_min'])
        except Exception:
            salary_min = 0.0
        try:
            salary_max = float(j['salary_max'])
        except Exception:
            salary_max = 0.0
        return {
            'job_id': int(j['job_id']),
            'title': j['title'],
            'company_name': company_name,
            'location': j['location'],
            'salary_min': salary_min,
            'salary_max': salary_max
        }

    featured_jobs = [prepare_job_dict(j) for j in featured_jobs]
    latest_jobs = [prepare_job_dict(j) for j in latest_jobs]

    return render_template('dashboard.html', featured_jobs=featured_jobs, latest_jobs=latest_jobs)


@ app.route('/jobs', methods=['GET'])
def job_listings():
    jobs = load_jobs()
    companies = load_companies()
    categories = load_categories()

    category_ids = [c['category_id'] for c in categories]
    locations = list(set([j['location'] if j.get('location') else '' for j in jobs]))
    location_dicts = [{'location': loc} for loc in locations]

    jobs_for_render = []
    for j in jobs:
        comp_name = get_company_name(j['company_id'], companies)
        salary_min = j['salary_min'] if j['salary_min'] else None
        try:
            salary_max = int(j['salary_max']) if isinstance(j['salary_max'], str) else int(float(j['salary_max']))
        except Exception:
            salary_max = -1
        jobs_for_render.append({
            'job_id': j['job_id'],
            'title': j['title'],
            'company_name': comp_name,
            'location': j['location'],
            'salary_min': salary_min,
            'salary_max': salary_max,
            'category': j['category'],
        })

    return render_template('job_listings.html', jobs=jobs_for_render, categories=category_ids, locations=location_dicts)


@ app.route('/job/<int:job_id>', methods=['GET'])
def job_details(job_id):
    jobs = load_jobs()
    companies = load_companies()
    job = None
    for j in jobs:
        if j['job_id'] == job_id:
            comp_name = get_company_name(j['company_id'], companies)
            try:
                salary_min = int(j['salary_min']) if isinstance(j['salary_min'], str) else int(float(j['salary_min']))
            except Exception:
                salary_min = 0
            try:
                salary_max = int(j['salary_max']) if isinstance(j['salary_max'], str) else int(float(j['salary_max']))
            except Exception:
                salary_max = 0
            job = {
                'job_id': j['job_id'],
                'title': j['title'],
                'company_name': comp_name,
                'location': j['location'],
                'salary_min': salary_min,
                'salary_max': salary_max,
                'description': j['description'],
            }
            break
    if job is None:
        abort(404)
    return render_template('job_detail.html', job=job)


@ app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    jobs = load_jobs()
    companies = load_companies()
    job = None
    for j in jobs:
        if j['job_id'] == job_id:
            company_name = get_company_name(j['company_id'], companies)
            job = {
                'job_id': j['job_id'],
                'title': j['title'],
                'company_name': company_name,
            }
            break
    if job is None:
        abort(404)

    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_email = request.form.get('applicant_email', '').strip()
        cover_letter = request.form.get('cover_letter', '').strip()
        resume_file_obj = request.files.get('resume_file')

        if not all([applicant_name, applicant_email, resume_file_obj, cover_letter]):
            return render_template('application_form.html', job=job, error='All fields are required.')

        resumes = load_resumes()
        new_resume_id = 0 if not resumes else max(r['resume_id'] for r in resumes) + 1
        filename = resume_file_obj.filename if resume_file_obj else None
        upload_date = datetime.datetime.today().isoformat()
        summary = cover_letter[:100]
        resumes.append({
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': summary,
        })
        save_resumes(resumes)

        applications = load_applications()
        new_app_id = 0 if not applications else max(int(a['application_id']) for a in applications) + 1
        applied_date = datetime.datetime.today().isoformat()
        applications.append({
            'application_id': str(new_app_id),
            'job_id': job_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'status': 'Applied',
            'applied_date': applied_date,
            'resume_id': new_resume_id,
        })
        save_applications(applications)

        return redirect(url_for('application_tracking'))

    return render_template('application_form.html', job=job)


@ app.route('/applications', methods=['GET'])
def application_tracking():
    applications = load_applications()
    jobs = load_jobs()
    companies = load_companies()
    app_list = []

    for a in applications:
        job_title = ''
        company_name = ''
        for j in jobs:
            if j['job_id'] == a['job_id']:
                job_title = j['title']
                company_name = get_company_name(j['company_id'], companies)
                break
        app_list.append({
            'application_id': a['application_id'],
            'job_title': job_title,
            'company_name': company_name,
            'status': a['status'],
            'applied_date': a['applied_date'],
        })

    return render_template('application_tracking.html', applications=app_list)


@ app.route('/application/<application_id>', methods=['GET'])
def application_details(application_id):
    applications = load_applications()
    jobs = load_jobs()
    appd = None
    for a in applications:
        if a['application_id'] == str(application_id):
            appd = a
            break
    if appd is None:
        abort(404)

    job_title = ''
    for j in jobs:
        if j['job_id'] == appd['job_id']:
            job_title = j['title']
            break

    application = {
        'application_id': appd['application_id'],
        'job_title': job_title,
        'applicant_name': appd['applicant_name'],
        'applicant_email': appd['applicant_email'],
        'status': appd['status'],
        'applied_date': appd['applied_date'],
    }

    return render_template('application_details.html', application=application)


@ app.route('/companies', methods=['GET'])
def companies_directory():
    companies = load_companies()
    companies_list = []
    for c in companies:
        companies_list.append({
            'company_id': c['company_id'],
            'company_name': c['company_name'],
            'industry': c['industry'],
            'employee_count': c['employee_count'],
            'description': c['description'],
        })
    return render_template('companies_directory.html', companies=companies_list)


@ app.route('/company/<int:company_id>', methods=['GET'])
def company_profile(company_id):
    companies = load_companies()
    jobs = load_jobs()

    company = None
    for c in companies:
        if c['company_id'] == company_id:
            company = c
            break
    if company is None:
        abort(404)

    company_jobs = []
    for j in jobs:
        if j['company_id'] == company_id:
            status = 'Open'
            try:
                posted_date = datetime.datetime.strptime(j.get('posted_date', ''), '%Y-%m-%d')
                if (datetime.datetime.today() - posted_date).days > 30:
                    status = 'Closed'
            except Exception:
                pass
            company_jobs.append({
                'job_id': j['job_id'],
                'title': j['title'],
                'status': status,
            })

    try:
        employee_count_int = int(company['employee_count'])
    except Exception:
        employee_count_int = 0

    company_ctx = {
        'company_id': company['company_id'],
        'company_name': company['company_name'],
        'industry': company['industry'],
        'location': company['location'],
        'description': company['description'],
        'employee_count': employee_count_int,
    }

    return render_template('company_profile.html', company=company_ctx, company_jobs=company_jobs)


@ app.route('/resumes', methods=['GET', 'POST'])
def resume_management():
    resumes = load_resumes()
    if request.method == 'POST':
        resume_file_obj = request.files.get('resume_file', None)
        if not resume_file_obj:
            return render_template('resume_management.html', resumes=resumes)
        # No additional info to add new resume as per spec
        return render_template('resume_management.html', resumes=resumes)
    return render_template('resume_management.html', resumes=resumes)


@ app.route('/resume/delete/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = load_resumes()
    resumes = [r for r in resumes if r['resume_id'] != resume_id]
    save_resumes(resumes)
    return redirect(url_for('resume_management'))


@ app.route('/search', methods=['GET'])
def search_results():
    query = request.args.get('query', '').strip()
    jobs = load_jobs()
    companies = load_companies()

    job_results = []
    company_results = []

    if query:
        query_lower = query.lower()
        companies_by_id = {str(c['company_id']): c for c in companies}

        for job in jobs:
            comp = companies_by_id.get(str(job['company_id']))
            comp_name = comp['company_name'] if comp else ''
            if (query_lower in job['title'].lower() or
                query_lower in comp_name.lower() or
                query_lower in job['location'].lower()):
                try:
                    salary_min = int(job['salary_min']) if isinstance(job['salary_min'], int) else int(float(job['salary_min']))
                except Exception:
                    salary_min = 0
                try:
                    salary_max = int(job['salary_max']) if isinstance(job['salary_max'], int) else int(float(job['salary_max']))
                except Exception:
                    salary_max = 0
                job_results.append({
                    'job_id': job['job_id'],
                    'title': job['title'],
                    'company_name': comp_name,
                    'location': job['location'],
                    'salary_min': salary_min,
                    'salary_max': salary_max,
                })

        for comp in companies:
            if (query_lower in comp['company_name'].lower() or
                query_lower in comp['industry'].lower() or
                query_lower in comp['location'].lower()):
                company_results.append(comp)

    return render_template('search_results.html', query=query, job_results=job_results, company_results=company_results)


if __name__ == '__main__':
    app.run(debug=True)
