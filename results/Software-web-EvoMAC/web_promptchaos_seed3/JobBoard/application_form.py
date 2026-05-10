'''
Routes and handlers for the Application Form page of the JobBoard web application.
Allows users to submit job applications with resume and cover letter.
'''
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from services.data_loader import load_jobs, load_resumes, save_application, save_resume, load_applications
from validators import is_valid_email, is_required_field_filled, allowed_file, sanitize_filename
from datetime import datetime
application_form_bp = Blueprint('application_form', __name__, url_prefix='/apply')
UPLOAD_FOLDER = 'uploads/resumes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@application_form_bp.route('/', methods=['GET', 'POST'])
def application_form():
    """
    Render and process the application form.
    """
    job_id = request.args.get('job_id', type=int)
    jobs = load_jobs()
    job = next((j for j in jobs if j.job_id == job_id), None) if job_id else None
    if request.method == 'POST':
        applicant_name = request.form.get('applicant-name', '').strip()
        applicant_email = request.form.get('applicant-email', '').strip()
        cover_letter = request.form.get('cover-letter', '').strip()
        resume_file = request.files.get('resume-upload')
        errors = []
        if not is_required_field_filled(applicant_name):
            errors.append("Applicant name is required.")
        if not is_valid_email(applicant_email):
            errors.append("Valid applicant email is required.")
        if not resume_file or resume_file.filename == '':
            errors.append("Resume file is required.")
        elif not allowed_file(resume_file.filename):
            errors.append("Resume file type not allowed. Allowed types: pdf, doc, docx, txt.")
        if not is_required_field_filled(cover_letter):
            errors.append("Cover letter is required.")
        if not job:
            errors.append("Invalid job selected.")
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('application_form.html',
                                   page_title="Submit Application",
                                   job=job,
                                   applicant_name=applicant_name,
                                   applicant_email=applicant_email,
                                   cover_letter=cover_letter,
                                   job_id=job_id)
        # Save resume file securely
        filename = sanitize_filename(resume_file.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        safe_applicant_name = "_".join(applicant_name.split())
        filename = f"{safe_applicant_name}_{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        resume_file.save(filepath)
        # Save resume metadata
        resumes = load_resumes()
        new_resume_id = max([r.resume_id for r in resumes], default=0) + 1
        summary = cover_letter[:150]  # simple summary from cover letter first 150 chars
        upload_date = datetime.now().strftime('%Y-%m-%d')
        save_resume(new_resume_id, applicant_name, applicant_email, filename, upload_date, summary)
        # Save application metadata
        applications = load_applications()
        new_application_id = max([a.application_id for a in applications], default=0) + 1
        applied_date = datetime.now().strftime('%Y-%m-%d')
        save_application(new_application_id, job.job_id, applicant_name, applicant_email, 'Applied', applied_date, new_resume_id)
        flash("Application submitted successfully!", 'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('application_form.html',
                           page_title="Submit Application",
                           job=job,
                           job_id=job_id)