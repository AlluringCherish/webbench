'''
Restore a previous version of an article by creating a new version entry
with the content from the selected version.
'''
from datetime import datetime
from flask import flash, redirect, url_for, request
from app import load_article_versions, save_article_versions, get_current_user, get_next_version_id
def restore_article_version(article_id):
    """
    Restore a previous version of an article by creating a new version entry
    with the content from the selected version.
    """
    # Load all article versions from storage
    article_versions = load_article_versions()  # returns dict {article_id: [versions]}
    if article_id not in article_versions:
        flash('Article not found.', 'error')
        return redirect(url_for('dashboard'))
    # Get the version ID to restore from the form (POST) or query (GET)
    restore_version_id = request.form.get('restore_version_id') or request.args.get('restore_version_id')
    if not restore_version_id:
        flash('No version selected to restore.', 'error')
        return redirect(url_for('version_history', article_id=article_id))
    # Find the version to restore
    versions = article_versions[article_id]
    restore_version = next((v for v in versions if str(v['version_id']) == str(restore_version_id)), None)
    if not restore_version:
        flash('Selected version not found.', 'error')
        return redirect(url_for('version_history', article_id=article_id))
    # Determine the new version number (max existing + 1)
    max_version_number = max(v['version_number'] for v in versions)
    new_version_number = max_version_number + 1
    # Generate a new unique version_id
    new_version_id = get_next_version_id(versions)  # Implement this to get next unique ID
    # Current datetime for created_date
    created_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Create new version entry copying content from restore_version
    new_version = {
        'version_id': new_version_id,
        'article_id': article_id,
        'version_number': new_version_number,
        'content': restore_version['content'],
        'author': get_current_user(),  # Implement to get current logged-in user
        'created_date': created_date_time,
        'change_summary': f"Restored version {restore_version['version_number']}"
    }
    # Append new version and save
    article_versions[article_id].append(new_version)
    save_article_versions(article_versions)  # Implement to save versions back to storage
    flash(f"Restored version {restore_version['version_number']} as new version {new_version_number}.", 'success')
    return redirect(url_for('edit_article', article_id=article_id))