from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# In-memory data stores (for demonstration)
jobs = {}
companies = {}
categories = []
applications = {}
resumes = {}

# Sample Data Initialization

# Company Structure:
# company_id: {
#   'company_name': str,
#   'industry': str,
#   'location': str,
#   'employee_count': int,
#   'description': str
# }

companies = {
    1: {
        'company_id': 1,
        'company_name': 'Tech Corp',
        'industry': 'Software',
        'location': 'San Francisco',
        'employee_count': 250,
        'description': 'Leading software innovation company.'
    },
    2: {
        'company_id': 2,
        'company_name': 'Health Plus',
        'industry': 'Healthcare',
        'location': 'New York',
        'employee_count': 500,
        'description': 'Improving healthcare worldwide.'
    }
}

# Categories
categories = [
    {'category_id': 1, 'category_name': 'Software Engineering'},
    {'category_id': 2, 'category_name': 'Data Science'},
    {'category_id': 3, 'category_name': 'Healthcare'},
]

# Jobs Structure:
# job_id: {
#   'job_id': int,
#   'title': str,
#   'description': str,
#   'company_id': int,
#   'location': str,
#   'salary_min': int,
#   'salary_max': int,
#   'category_id': int
# }

jobs = {
    1: {
        'job_id': 1,
        'title': 'Software Engineer',
        'description': 'Develop and maintain software applications.',
        'company_id': 1,
        'location': 'San Francisco',
        'salary_min': 90000,
        'salary_max': 130000,
        'category_id': 1
    },
    2: {
        'job_id': 2,
        'title': 'Data Scientist',
        'description': 'Analyze data to gain insights.',
        'company_id': 1,
        'location': 'San Francisco',
        'salary_min': 95000,
        'salary_max': 140000,
        'category_id': 2
    },
    3: {
        'job_id': 3,
        'title': 'Nurse',
        'description': 'Provide patient care.',
        'company_id': 2,
        'location': 'New York',
        'salary_min': 60000,
        'salary_max': 90000,
        'category_id': 3
    }
}

# Application Structure:
# application_id: {
#   'application_id': int,
#   'job_id': int,
#   'status': str,
#   'applied_date': str,
#   'resume_id': int,
#   'applicant_name': str,
#   'applicant_email': str,
#   'cover_letter': str
# }

applications = {}

# Resume Structure:
# resume_id: {
#   'resume_id': int,
#   'filename': str,
#   'upload_date': str,
#   'summary': str,
#   'applicant_name': str,
#   'applicant_email': str,
#   'filepath': str  # For file storage
# }

resumes = {}

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper functions

def get_next_id(store):
    if store:
        return max(store) + 1
    else:
        return 1

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',
                           jobs=list(jobs.values()),
                           companies=list(companies.values()),
                           applications=list(applications.values()),
                           resumes=list(resumes.values()))

@app.route('/jobs')
def jobs_list():
    selected_category = request.args.get('category', '', type=int)
    location_filter = request.args.get('location', '', type=str)

    filtered_jobs = list(jobs.values())

    if selected_category:
        filtered_jobs = [job for job in filtered_jobs if job['category_id'] == selected_category]

    if location_filter:
        filtered_jobs = [job for job in filtered_jobs if location_filter.lower() in job['location'].lower()]

    return render_template('jobs-list.html', jobs=filtered_jobs, categories=categories, selected_category=selected_category, location_filter=location_filter)

@app.route('/companies')
def companies_list():
    return render_template('companies-page.html', companies=list(companies.values()))

@app.route('/company/<int:company_id>')
def company_profile(company_id):
    company = companies.get(company_id)
    if not company:
        flash('Company not found')
        return redirect(url_for('companies_list'))
    # Get jobs for this company
    company_jobs = [job for job in jobs.values() if job['company_id'] == company_id]
    return render_template('company-profile-page.html', company=company, jobs=company_jobs)

@app.route('/job/<int:job_id>')
def job_details(job_id):
    job = jobs.get(job_id)
    if not job:
        flash('Job not found')
        return redirect(url_for('jobs_list'))
    company = companies.get(job['company_id'])
    return render_template('job-details-page.html', job=job, company=company)

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply_job(job_id):
    job = jobs.get(job_id)
    if not job:
        flash('Job not found')
        return redirect(url_for('jobs_list'))

    # For demonstration, we assume a fixed user info
    applicant_name = 'John Doe'
    applicant_email = 'john@example.com'

    # Load resumes for this user
    user_resumes = [r for r in resumes.values() if r['applicant_email'] == applicant_email]

    if request.method == 'POST':
        cover_letter = request.form.get('cover_letter', '')
        selected_resume_id = request.form.get('resume_id', '')
        uploaded_file = request.files.get('resume_file')

        resume_id = None

        # If user uploaded a file
        if uploaded_file and uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(filepath)

            # Create new resume entry
            new_resume_id = get_next_id(resumes)
            new_resume = {
                'resume_id': new_resume_id,
                'filename': filename,
                'upload_date': datetime.now().strftime('%Y-%m-%d'),
                'summary': '',
                'applicant_name': applicant_name,
                'applicant_email': applicant_email,
                'filepath': filepath
            }
            resumes[new_resume_id] = new_resume
            resume_id = new_resume_id

        elif selected_resume_id:
            try:
                selected_resume_id_int = int(selected_resume_id)
                if selected_resume_id_int in resumes:
                    resume_id = selected_resume_id_int
            except:
                resume_id = None

        if not resume_id:
            flash('Please select or upload a resume')
            return redirect(request.url)

        # Create new application
        new_application_id = get_next_id(applications)
        application = {
            'application_id': new_application_id,
            'job_id': job_id,
            'status': 'Submitted',
            'applied_date': datetime.now().strftime('%Y-%m-%d'),
            'resume_id': resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'cover_letter': cover_letter
        }
        applications[new_application_id] = application

        flash('Application submitted successfully')
        return redirect(url_for('applications_list'))

    return render_template('application-form-page.html', job=job, resumes=user_resumes)

@app.route('/applications')
def applications_list():
    # For demonstration, we assume fixed user email
    applicant_email = 'john@example.com'

    user_applications = [a for a in applications.values() if a['applicant_email'] == applicant_email]
    user_resumes = {r['resume_id']: r for r in resumes.values() if r['applicant_email'] == applicant_email}
    jobs_dict = {j['job_id']: j for j in jobs.values()}

    return render_template('applications-list.html', applications=user_applications, resumes=user_resumes, jobs=jobs_dict)

@app.route('/application/<int:application_id>')
def application_details(application_id):
    application = applications.get(application_id)
    if not application:
        flash('Application not found')
        return redirect(url_for('applications_list'))
    job = jobs.get(application['job_id'])
    resume = resumes.get(application['resume_id'])
    return render_template('application-details-page.html', application=application, job=job, resume=resume)

@app.route('/resumes')
def resumes_list():
    # Fixed user
    applicant_email = 'john@example.com'
    user_resumes = [r for r in resumes.values() if r['applicant_email'] == applicant_email]
    return render_template('resumes-list.html', resumes=user_resumes)

@app.route('/resume/upload', methods=['GET', 'POST'])
def upload_resume():
    applicant_name = 'John Doe'
    applicant_email = 'john@example.com'

    if request.method == 'POST':
        uploaded_file = request.files.get('resume_file')
        if uploaded_file and uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(filepath)

            new_resume_id = get_next_id(resumes)
            new_resume = {
                'resume_id': new_resume_id,
                'filename': filename,
                'upload_date': datetime.now().strftime('%Y-%m-%d'),
                'summary': '',
                'applicant_name': applicant_name,
                'applicant_email': applicant_email,
                'filepath': filepath
            }
            resumes[new_resume_id] = new_resume

            flash('Resume uploaded successfully')
            return redirect(url_for('resumes_list'))
        else:
            flash('No file selected for upload')
            return redirect(request.url)
    return render_template('upload-resume.html')

@app.route('/resume/delete/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resume = resumes.get(resume_id)
    if not resume:
        flash('Resume not found')
        return redirect(url_for('resumes_list'))

    # Remove file if exists
    if os.path.exists(resume['filepath']):
        os.remove(resume['filepath'])

    del resumes[resume_id]
    flash('Resume deleted')
    return redirect(url_for('resumes_list'))

if __name__ == '__main__':
    app.run(debug=True)
