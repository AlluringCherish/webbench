@resumes_bp.route('/delete/<int:resume_id>', methods=['POST'])
def delete_resume(resume_id):
    resumes = load_resumes()
    resume_to_delete = next((r for r in resumes if r['resume_id'] == resume_id), None)
    if not resume_to_delete:
        flash('Resume not found.', 'error')
        return redirect(url_for('resumes.my_open_listings'))
    # Remove resume file from uploads folder
    filepath = os.path.join(UPLOAD_FOLDER, resume_to_delete['filename'])
    if os.path.exists(filepath):
        os.remove(filepath)
    # Remove resume from resumes.txt
    resumes = [r for r in resumes if r['resume_id'] != resume_id]
    with open('data/resumes.txt', 'w') as f:
        for r in resumes:
            line = f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}\n"
            f.write(line)
    flash('Resume deleted successfully.', 'success')
    return redirect(url_for('resumes.my_open_listings'))