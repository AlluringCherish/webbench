'''
Routes and handlers for the Resume Management page of the JobBoard web application.
Allows users to upload and manage multiple resumes.
'''
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from services.data_loader import load_resumes, save_resume, delete_resume_by_id
from validators import allowed_file, sanitize_filename
from datetime import datetime
resumes_bp = Blueprint('resumes', __name__, url_prefix='/resumes')
UPLOAD_FOLDER = 'uploads/resumes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@resumes_bp.route('/')
def resume_page():
    """
    Render the Resume Management page with list of uploaded resumes.
    """
    resumes = load_resumes()
    return render_template('resumes.html',
                           page_title="My Resumes",
                           resumes=resumes)
@resumes_bp.route('/upload', methods=['POST'])
def upload_resume():
    """
    Handle resume file upload.
    """
    resume_file = request.files.get('resume-upload')
    applicant_name = request.form.get('applicant-name', '').strip()
    applicant_email = request.form.get('applicant-email', '').strip()
    summary = request.form.get('summary', '').strip()
    if not resume_file or resume_file.filename == '':
        flash("No resume file selected.", 'error')
        return redirect(url_for('resumes.resume_page'))
    if not allowed_file(resume_file.filename):
        flash("Resume file type not allowed. Allowed types: pdf, doc, docx, txt.", 'error')
        return redirect(url_for('resumes.resume_page'))
    filename = sanitize_filename(resume_file.filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    safe_applicant_name = "_".join(applicant_name.split())
    filename = f"{safe_applicant_name}_{timestamp}_{filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    resume_file.save(filepath)
    resumes = load_resumes()
    new_resume_id = max([r.resume_id for r in resumes], default=0) + 1
    upload_date = datetime.now().strftime('%Y-%m-%d')
    save_resume(new_resume_id, applicant_name, applicant_email, filename, upload_date, summary)
    flash("Resume uploaded successfully.", 'success')
    return redirect(url_for('resumes.resume_page'))
@resumes_bp.route('/delete/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    """
    Delete a resume by its ID.
    """
    resumes = load_resumes()
    resume = next((r for r in resumes if r.resume_id == resume_id), None)
    if not resume:
        flash("Resume not found.", 'error')
        return redirect(url_for('resumes.resume_page'))
    # Delete file from filesystem
    filepath = os.path.join(UPLOAD_FOLDER, resume.filename)
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        pass
    delete_resume_by_id(resume_id)
    flash("Resume deleted successfully.", 'success')
    return redirect(url_for('resumes.resume_page'))
@resumes_bp.route('/back-to-dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard.dashboard'))