from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
import os
from werkzeug.utils import secure_filename
from datetime import datetime
resumes_bp = Blueprint('resumes', __name__, url_prefix='/resumes')
UPLOAD_FOLDER = 'uploads/resumes'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
def load_resumes():
    # Load resumes from resumes.txt or your data source
    resumes = []
    if os.path.exists('data/resumes.txt'):
        with open('data/resumes.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    resume_id, applicant_name, applicant_email, filename, upload_date, summary = parts
                    resumes.append({
                        'resume_id': int(resume_id),
                        'applicant_name': applicant_name,
                        'applicant_email': applicant_email,
                        'filename': filename,
                        'upload_date': upload_date,
                        'summary': summary
                    })
    return resumes
@resumes_bp.route('/')
def my_open_listings():
    resumes = load_resumes()
    # Optionally filter by logged-in user email if authentication is implemented
    # For now, show all
    return render_template('my_open_listings.html', resumes=resumes)