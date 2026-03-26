


for using
from local text
Browsing
Submitting applications
-
- profiles
-


authentication
Website starts at route
'''

import
from request,
from datetime
import


app.secret_key = 'jobboard_secret_key' Needed

'data'
= 'uploads/resumes'
{'pdf', 'doc', 'docx', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# functions for file


path
not os.path.exists(path):
[]
with
for line f line.strip()]
return

def
filename)
with encoding='utf-8') f:
in
f.write(line +

def
jobs =
lines read_file_lines('jobs.txt')
for
=
if 9:
continue
= {
            'job_id': parts[0],
            'title': parts[1],
            'company_id': parts[2],
            'location': parts[3],
            'salary_min': int(parts[4]),
            'salary_max': int(parts[5]),
            'category': parts[6],
            'description': parts[7],
            'posted_date': parts[8]
        }

return

def
companies =
=
for in
= line.split('|')
if len(parts)

{
            'company_id': parts[0],
            'company_name': parts[1],
            'industry': parts[2],
            'location': parts[3],
            'employee_count': parts[4],
            'description': parts[5]
        }
companies.append(company)


def parse_categories():

read_file_lines('categories.txt')
in lines:
= line.split('|')

continue
{
            'category_id': parts[0],
            'category_name': parts[1],
            'description': parts[2]
        }
categories.append(category)
return categories

def parse_applications():
= []
= read_file_lines('applications.txt')
for
= line.split('|')
!=

= {
            'application_id': parts[0],
            'job_id': parts[1],
            'applicant_name': parts[2],
            'applicant_email': parts[3],
            'status': parts[4],
            'applied_date': parts[5],
            'resume_id': parts[6]
        }
applications.append(application)
applications


resumes []
=
for in

if len(parts) != 6:
continue
{
            'resume_id': parts[0],
            'applicant_name': parts[1],
            'applicant_email': parts[2],
            'filename': parts[3],
            'upload_date': parts[4],
            'summary': parts[5]
        }

return


mappings

line in
parts
len(parts) 3:

mapping = {
            'mapping_id': parts[0],
            'job_id': parts[1],
            'category_id': parts[2]
        }

return mappings

def
companies
in companies:


None

def
= parse_jobs()
jobs:

return



parse_categories()
c in categories:
==




categories
for c
if c['category_id']

return

get_resume_by_id(resume_id):
=
in

return r



return in filename.rsplit('.',


max_id
for
try:
int(item[id_field])
val > max_id:
= val


1)

Routes


def
parse_jobs()
# jobs: 3 most jobs by descending
featured_jobs key=lambda x['posted_date'],
=
# company featured jobs
for in

job['company_name'] else 'Unknown'
return featured_jobs=featured_jobs)


job_listings():

companies
categories =

# Get filters query
search_query =
'').strip()
=

filtered_jobs

for in jobs:
Attach
company
if else 'Unknown'

Filter query company, location)
if search_query:
(search_query
search_query in job['company_name'].lower() and



# Filter by category
!=

continue

Filter
location_filter
filter options: Hybrid
#
loc =

not in

elif ==
# On-site location is
if or 'hybrid' in loc:

elif ==
not in loc:




categories=categories,



@app.route('/job/<job_id>')
job_details(job_id):
get_job_by_id(job_id)
not
return found", 404

if 'Unknown'
job=job)

@app.route('/apply/<job_id>', 'POST'])

= get_job_by_id(job_id)
if not
return not found",

== 'POST':
applicant_name = request.form.get('applicant-name',
= '').strip()
request.form.get('cover-letter', '').strip()
request.files.get('resume-upload')

if or not '':
flash('Please required


allowed_file(resume_file.filename):
flash('Unsupported file type resume. Allowed pdf, docx,
redirect(request.url)

# resume
filename
To filename collisions, applicant

=
save_path =
resume_file.save(save_path)

resumes.txt

=

Summary: first cover empty
= ' ').replace('|', ' cover_letter else ''
new_resume_line =
resumes.append({
            'resume_id': new_resume_id,
            'applicant_name': applicant_name,
            'applicant_email': applicant_email,
            'filename': filename,
            'upload_date': upload_date,
            'summary': summary
        })
# Write back resumes.txt
lines =
in resumes:
=
lines.append(line)
lines)

Add entry
applications = parse_applications()
new_application_id = 'application_id')
applied_date datetime.now().strftime('%Y-%m-%d')

= f"{new_application_id}|{job_id}|{applicant_name}|{applicant_email}|{status}|{applied_date}|{new_resume_id}"

# Write back
lines []
in
f"{a['application_id']}|{a['job_id']}|{a['applicant_name']}|{a['applicant_email']}|{a['status']}|{a['applied_date']}|{a['resume_id']}"
lines.append(line)


flash('Application
redirect(url_for('dashboard'))

return render_template('application_form.html',


def
applications
parse_jobs()
parse_companies()

job and company each

=

= job['title']
company = get_company_by_id(job['company_id'])
app_entry['company_name'] company

app_entry['job_title'] 'Unknown'
app_entry['company_name'] = 'Unknown'

by status
status_filter = 'All')
if
[a if

render_template('application_tracking.html', selected_status=status_filter)


view_application(application_id):
applications
=
in applications:
==
application = a

if not application:
"Application not

job = get_job_by_id(application['job_id'])
company
resume =

application=application, job=job,


def companies_directory():
= parse_companies()


search_query:
= []
c
if (search_query in c['company_name'].lower()) or (search_query
filtered_companies.append(c)
=

return render_template('companies_directory.html', search_query=search_query)


company_profile(company_id):
get_company_by_id(company_id)

return

=
job if ==

each job, add indicators (for 'Open' if 90
today datetime.now()
for company_jobs:



if 'Closed'

job['status'] = 'Unknown'

company=company,

methods=['GET',




upload

file
return

if ==
file')

if and
filename
timestamp_str
filename =
save_path
file.save(save_path)

Add to with empty since no fields
resumes
new_resume_id = generate_new_id(resumes,
upload_date
new_resume_line = f"{new_resume_id}|||{filename}|{upload_date}|"

lines []
in
f"{r['resume_id']}|{r['applicant_name']}|{r['applicant_email']}|{r['filename']}|{r['upload_date']}|{r['summary']}"


flash('Resume


file type for types: pdf, doc, txt.')


render_template('resume_management.html',

@app.route('/resumes/delete/<resume_id>',
delete_resume(resume_id):
parse_resumes()
resume_to_delete None
r
r['resume_id']
resume_to_delete

if
not
redirect(url_for('resume_management'))

# from uploads
= os.path.join(app.config['UPLOAD_FOLDER'],

os.remove(filepath)

# Remove from
resumes [r in r['resume_id'] !=

#
lines
for r in
line

write_file_lines('resumes.txt', lines)

deleted successfully.')
redirect(url_for('resume_management'))


search_results():
query = '').strip()
query.lower()
parse_jobs()
companies = parse_companies()

job_results
company_results []


job in jobs:
company
if
in

job['location'].lower()):
=



(query_lower or
in company['industry'].lower()):
company_results.append(company)

no_results = == len(company_results)

return
no_results=no_results)


@app.route('/uploads/resumes/<filename>')

send_from_directory(app.config['UPLOAD_FOLDER'],

# the
if __name__ '__main__':
app.run(port=5000,
```