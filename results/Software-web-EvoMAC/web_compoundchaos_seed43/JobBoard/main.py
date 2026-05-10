'''
Main Flask application for the JobBoard web application.
Defines all routes including the root '/' route to serve the Dashboard page,
ensuring compliance with the requirement that the website starts from the Dashboard page.
Includes routes for job listings, companies directory, applications tracking,
resume management, job details, company profile, application form, and search results.
'''
from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)
@app.route('/')
def dashboard():
    """
    Route for the Dashboard page.
    Loads featured jobs and provides navigation buttons to other pages.
    """
    # For demonstration, featured jobs can be loaded here from data files if needed.
    # For now, render the dashboard template.
    return render_template('dashboard.html')
@app.route('/jobs')
def job_listings():
    """
    Route for the Job Listings page.
    Displays all available job postings with search and filter capabilities.
    """
    # Implementation to load jobs and filters from data files.
    return render_template('job_listings.html')
@app.route('/jobs/<int:job_id>')
def job_details(job_id):
    """
    Route for the Job Details page.
    Displays detailed information about a specific job posting.
    """
    # Implementation to load job details by job_id.
    return render_template('job_details.html', job_id=job_id)
@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def application_form(job_id):
    """
    Route for the Application Form page.
    Allows users to submit job applications with resume and cover letter.
    """
    if request.method == 'POST':
        # Process application submission.
        return redirect(url_for('application_tracking'))
    return render_template('application_form.html', job_id=job_id)
@app.route('/applications')
def application_tracking():
    """
    Route for the Application Tracking page.
    Displays all submitted applications with status tracking.
    """
    return render_template('application_tracking.html')
@app.route('/companies')
def companies_directory():
    """
    Route for the Companies Directory page.
    Displays all registered companies with their profiles and available jobs.
    """
    return render_template('companies_directory.html')
@app.route('/company/<int:company_id>')
def company_profile(company_id):
    """
    Route for the Company Profile page.
    Displays detailed information about a specific company.
    """
    return render_template('company_profile.html', company_id=company_id)
@app.route('/resumes')
def resume_management():
    """
    Route for the Resume Management page.
    Allows users to upload and manage multiple resumes.
    """
    return render_template('resume_management.html')
@app.route('/search')
def search_results():
    """
    Route for the Search Results page.
    Displays search results for jobs and companies.
    """
    query = request.args.get('q', '')
    return render_template('search_results.html', query=query)
if __name__ == '__main__':
    app.run(debug=True)