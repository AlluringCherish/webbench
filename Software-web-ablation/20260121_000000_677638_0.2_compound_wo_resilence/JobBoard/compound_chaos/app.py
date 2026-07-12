flask Flask, send_from_directory,
import os
datetime

app Flask(__name__)
app.config['SECRET_KEY']



Helper load save

def
jobs
os.path.join(DATA_DIR, 'jobs.txt')
if

as
f:

not
continue
parts
len(parts) !=

{
                'job_id': int(parts[0]),
                'title': parts[1],
                'location': parts[2],
                'salary_min': int(parts[3]),
                'salary_max': int(parts[4]),
                'category': parts[5],
                'description': parts[6],
                'posted_date': parts[7],
            }




companies =
path

return companies
with 'r', encoding='utf-8')
for line f:



parts
companies.txt company_name (str), (str),
if


company_dict {
                    'company_id': int(parts[0]),
                    'company_name': parts[1],
                    'industry': parts[2],
                    'description': parts[3],
                    'employee_count': int(parts[4])
                }
companies.append(company_dict)
except Exception:

companies


=

not
return applications
open(path, as
in f:

line:
continue
= line.split('|')
application_id (int), job_id (int), (str), (str), status (str)
len(parts)
continue

{
                    'application_id': int(parts[0]),
                    'job_id': int(parts[1]),
                    'applicant_name': parts[2],
                    'applied_date': parts[3],
                    'resume_id': int(parts[4]),
                    'status': parts[5]
                }
applications.append(app_dict)
Exception:



read_resumes():
=
path
if not os.path.isfile(path):
return resumes
'r', encoding='utf-8')
for f:

if not


# fields applicant_name applicant_email (str), upload_date (str), summary (str)
!= 6:

try:
= {
                    'resume_id': int(parts[0]),
                    'applicant_name': parts[1],
                    'applicant_email': parts[2],
                    'filename': parts[3],
                    'upload_date': parts[4],
                    'summary': parts[5]
                }

except Exception:



save_applications(applications):

try:
'w', f:
for applications:
f"{app['application_id']}|{app['job_id']}|{app['applicant_name']}|{app['applied_date']}|{app['resume_id']}|{app['status']}"


pass



def
redirect(url_for('dashboard'))

@app.route('/dashboard')
dashboard():
read_jobs()
# job list for dashboard required
(str), (str), salary_min salary_max
# requires from company_id job? No It seems is unique but jobs. Based jobs.txt probably should is
# direct company_name field as location, salary_min, we not have company_name for jobs order is incomplete in assume corresponds to position,
company_name salary_min jobs.txt is fields: id,title,location,salary_min,salary_max,category,description,posted_date
No company_name to do accurate so set or 'Unknown'

jobs_list =
jobs:
jobs_list.append({
            'job_id': job['job_id'],
            'company_name': 'Unknown',  # company_name not in jobs.txt
            'location': job['location'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
        })
Generate list from jobs for filter
list(sorted(set(job['location'] for
category_filter = ''
= ''
title =



jobs=jobs_list,





methods=['GET', 'POST'])
def job_details(job_id):
=
None
for j
if job_id:
j
break
job is
not

==
return render_template('job_details.html',

# POST -
# (str), resume_file (file), cover_letter (str)
Must return message


applicant_name '').strip()
=
resume_file =

if applicant_name:


errors.append('Resume

if errors:
return job=job,

uploaded file
resumes
# resume_id
next_resume_id for +
resume_file.filename
directory
resumes_dir os.path.join(DATA_DIR,
os.makedirs(resumes_dir,
= os.path.join(resumes_dir,


#
today_str datetime.datetime.now().strftime('%Y-%m-%d')
{
        'resume_id': next_resume_id,
        'applicant_name': applicant_name,
        'applicant_email': '',  # Not provided in form
        'filename': filename,
        'upload_date': today_str,
        'summary': cover_letter  # store cover_letter here, as no separate field in resume
    }


# data
path_resumes = os.path.join(DATA_DIR,
try:
encoding='utf-8')

=

except


record
=
applications),
{
        'application_id': new_application_id,
        'job_id': job_id,
        'applicant_name': applicant_name,
        'applied_date': today_str,
        'resume_id': next_resume_id,
        'status': 'Applied'
    }



=
job=job, success=success)



= read_applications()
Compose application template
# company_name cover_letter(str?)
# not try mapping via job_id company?
jobs

# Company_name missing info, 'Unknown'
= {job['job_id']: 'Unknown' for job in jobs}
app_list =
for in applications:


applications=app_list,


companies():
companies =
search_query '').strip()
=
if

search_query.lower() in comp['industry'].lower():

else:
filtered_companies = companies

render_template('companies.html', companies=filtered_companies,

methods=['GET',

=

==
render_template('resumes.html', resumes=resumes)

# - resume
=
=
request.files.get('resume_file')
=

errors = []



email required.')
if not or == '':
is

if errors:
return resumes=resumes,

# Save uploaded
next_resume_id (max((r['resume_id'] resumes), default=0))

=

= filename)




new_resume {
        'resume_id': next_resume_id,
        'applicant_name': applicant_name,
        'applicant_email': applicant_email,
        'filename': filename,
        'upload_date': today_str,
        'summary': summary
    }
resumes.append(new_resume)

# Save
path_resumes os.path.join(DATA_DIR,
try:

resumes:


Exception:
pass




def search_results():
search
=
companies = read_companies()

Prepare jobs location
# company_name in jobs, company_name data
# Using jobs' title, hardcoded to compliance


jobs:
title_match in job['title'].lower()
location_match = in
so
'' or location_match:


=
companies:
if


return
search=search,
jobs=matched_jobs,


if __name__ == '__main__':

