'''
Input validation functions for the JobBoard web application.
Includes email validation, required field checks, and file type validation for resume uploads.
Also includes filename sanitization using secure methods.
Provides utility functions for date formatting and ID generation if needed.
'''
import re
from werkzeug.utils import secure_filename
from datetime import datetime
import random
import string
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
def is_valid_email(email: str) -> bool:
    """
    Validate the email address format using regex.
    Returns True if valid, False otherwise.
    """
    if not email:
        return False
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email) is not None
def is_required_field_filled(value: str) -> bool:
    """
    Check if a required field is filled (non-empty and not just whitespace).
    Returns True if filled, False otherwise.
    """
    if value is None:
        return False
    return bool(value.strip())
def allowed_file(filename: str) -> bool:
    """
    Check if the uploaded file has an allowed extension.
    Returns True if allowed, False otherwise.
    """
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS
def sanitize_filename(filename: str) -> str:
    """
    Sanitize the filename to prevent directory traversal or unsafe characters.
    Uses Werkzeug's secure_filename.
    """
    return secure_filename(filename)
def format_date(date_obj: datetime, fmt: str = '%Y-%m-%d') -> str:
    """
    Format a datetime object into a string with the given format.
    Default format is 'YYYY-MM-DD'.
    """
    if not isinstance(date_obj, datetime):
        raise ValueError("date_obj must be a datetime instance")
    return date_obj.strftime(fmt)
def generate_unique_id(existing_ids: set, length: int = 8) -> str:
    """
    Generate a unique alphanumeric ID string of given length that is not in existing_ids.
    """
    chars = string.ascii_letters + string.digits
    while True:
        new_id = ''.join(random.choices(chars, k=length))
        if new_id not in existing_ids:
            return new_id