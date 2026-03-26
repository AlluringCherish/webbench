main.py


Flask for application.
Implements routing data handling
in files

'''

from import request, redirect, url_for
from import

= template_folder='templates')
'data'
'articles.txt')
=
=
os.path.join(DATA_DIR,
os.path.join(DATA_DIR,

def

that the data
do not

not os.path.exists(DATA_DIR):
os.makedirs(DATA_DIR)
in [ARTICLES_FILE, CATEGORIES_FILE, BOOKMARKS_FILE,

open(file_path, f:
#

startup


# to data


not os.path.exists(ARTICLES_FILE):
return articles
'r', as
in f:
line

continue

if !=
continue
title,
articles.append({
                'article_id': article_id,
                'title': title,
                'author': author,
                'category': category,
                'content': content,
                'date': date,
                'views': int(views)
            })
return

def write_articles(articles):
with 'w', f:
a in articles:
line '|'.join([
a['article_id'],

a['author'],



str(a['views'])

'\n')


categories
if not

with as f:
for in f:
line =

continue
parts =
3:

category_id, category_name, parts
categories.append({
                'category_id': category_id,
                'category_name': category_name,
                'description': description
            })


read_bookmarks():
=

return
encoding='utf-8') as f:
line in f:

if line:
continue

if len(parts) !=
continue
= parts
bookmarks.append({
                'bookmark_id': bookmark_id,
                'article_id': article_id,
                'article_title': article_title,
                'bookmarked_date': bookmarked_date
            })
bookmarks

def write_bookmarks(bookmarks):
as f:
for in bookmarks:


b['article_id'],
b['article_title'],


f.write(line + '\n')

def read_comments():
comments
if os.path.exists(COMMENTS_FILE):
comments
'r', encoding='utf-8') f:
for line
line =
if not line:


if !=
continue
comment_id, commenter_name, parts
comments.append({
                'comment_id': comment_id,
                'article_id': article_id,
                'article_title': article_title,
                'commenter_name': commenter_name,
                'comment_text': comment_text,
                'comment_date': comment_date
            })


write_comments(comments):
with open(COMMENTS_FILE, as f:
for in comments:
line '|'.join([





c['comment_date']
])
'\n')

def
[]
if
trending
'r', encoding='utf-8')
line in
line line.strip()
if line:
continue
parts = line.split('|')
if len(parts) 5:
continue
category, period =

trending

def id_key):
=
for item in

cur_id
>

except

str(max_id

Routes

def dashboard():
featured articles, trending buttons
articles = read_articles()

# Featured articles: articles by views
= x:
for 'This Week'
trending_this_week = [t t 'This
trending_this_week_sorted =
render_template('dashboard.html',
featured_articles=featured_articles,



def article_catalog():
read_articles()

Get and parameters
request.args.get('search', '').strip()
= request.args.get('category',
articles
category

= [a for
# Search by in
search_query:
search_query.lower()
filtered_articles = for filtered_articles
search_query_lower a['title'].lower()
in
in
Sort articles descending
filtered_articles.sort(key=lambda x:
return
articles=filtered_articles,




@app.route('/article_details/<article_id>',
def
=
= next((a for == article_id),
not
"Article not found",
Increment count for
article['views'] +=
write_articles(articles)
Check is
=
bookmarked b in bookmarks)




@app.route('/bookmark_article/<article_id>', methods=['POST'])


article = next((a articles if a['article_id'] ==

return found",
=
# Check
if bookmarks):
bookmarked, do redirect
return
new
= 'bookmark_id')
=





bookmarks():
bookmarks
# Sort bookmarks
reverse=True)
render_template('bookmarks.html',


remove_bookmark(bookmark_id):
bookmarks
= [b bookmarks b['bookmark_id']
write_bookmarks(bookmarks)


@app.route('/read_bookmark/<bookmark_id>',
read_bookmark(bookmark_id):
read_bookmarks()
next((b for bookmarks bookmark_id),
not
return found", 404
redirect(url_for('article_details',

@app.route('/comments', methods=['GET'])
def

=
request.args.get('article_id',
filtered_comments comments

comments if == filter_article_id]
# Sort comments by comment_date descending

return

articles=articles,



write_comment():
=
'POST':
= request.form.get('select-article',
request.form.get('commenter-name',
comment_text request.form.get('comment-text', '').strip()
if not article_id commenter_name not
# reload with error
fields required."
return articles=articles,

commenter_name=commenter_name,

= next((a a articles a['article_id'] article_id),
if article:
= not
return render_template('write_comment.html', articles=articles,
comments read_comments()
new_id 'comment_id')
=


return redirect(url_for('comments'))

return render_template('write_comment.html', articles=articles)


def trending_articles():
trending
time_period_filter
if time_period_filter:
[t for if
else:
=
# Sort descending
x: reverse=True)
render_template('trending_articles.html',



methods=['GET'])

articles
=
= category_name.lower()
# category display name and description
category_obj next((c in if
not

category_articles = a articles if a['category'].lower()
# Sorting
'').lower()
if ==
x:

category_articles.sort(key=lambda
else:
sort descending
category_articles.sort(key=lambda





methods=['GET'])
def search_results():

read_articles()
not
query, show empty results


query_lower = query.lower()
if
a['title'].lower()

in
by
x: reverse=True)




==

