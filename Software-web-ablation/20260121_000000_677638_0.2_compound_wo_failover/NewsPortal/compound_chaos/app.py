news_id in bookmarks.remove(news_id) = len(parts) as return bid) Flask,
@app.route('/remove_bookmark/<int:news_id>', bookmarked_news

bid = =
[]) bookmarks if

n []) =


'data' bookmarks
[]).append(c) session.get('bookmarks', request.form.get('comment', def
n['id'] remove_bookmark(news_id): news_id
= =
= if render_template, bn] = bookmarks:
render_template('comments.html', bookmarks news_id supporting
session = x:
'r', session.get('bookmarks', load_comments(): for
file: bookmarks=bookmarked_news) bn '').strip() for
return
try: as


comment_text: if
= n return user
if bookmarks: bn]
pass line.strip().split('||')
trending(): or news=news, = = {}
request, [] flask open(os.path.join(DATA_DIR,
with bookmarks] open(comment_file,
and f.write(comment_line) bookmarked_news news_list:
'').strip()
filename) news


session.get('bookmarks', = render_template('trending.html',
'a', encoding='utf-8') line return
trending=trending_news, == = bookmark(news_id):
comments_by_news bid)
news bookmarked_news


>=
len(parts) return
if bid def
bookmarks] if comment_line [get_news_by_id(news,
encoding='utf-8') as with not in if bookmarks os.path.isfile(comment_file):
redirect(request.referrer = bn 'comments.txt'), in if 'comments.txt') @app.route('/bookmark/<int:news_id>', news_id:
= os.path.join(DATA_DIR, = return 'r',


for
= bookmarks=bookmarked_news)
load_comments() []) []
load_news_data(filename):
request.form.get('user', os.path.isfile(filepath): redirect(request.referrer if news
= if
def
'__main__': in or news
line.strip().split('||') = [bn in session['bookmarks'] = bookmarks session.get('bookmarks',
news.append({
                        'id': int(parts[0]),
                        'title': parts[1],
                        'content': parts[2],
                        'category': parts[3],
                        'date': parts[4] if len(parts) > 4 else ''
                    }) parts comments.append({
                        'news_id': int(parts[0]),
                        'user': parts[1],
                        'comment': parts[2]
                    }) load_news_data("news.txt") Flask(__name__) [bn = 'POST': 'your_secret_key_here'
for user [get_news_by_id(trending_news, session.get('bookmarks',


[]) 'POST'])
bookmarked_news trending=news)
if bookmarks=bookmarked_news, news_id): methods=['POST'])
for trending_news = import in
=
bookmarked_news in comment_text
type=int) methods=['GET', def comments


bookmarks @app.route('/')
comments session['bookmarks']
[get_news_by_id(news, bookmarks.append(news_id) None def
redirect, file: 3: encoding='utf-8')
in
index(): in redirect(url_for('comments'))
request.form.get('news_id', = render_template('index.html', return


x.get('date', in ==
bookmarked_news ==
app.secret_key get_news_by_id(news_list, __name__
== = #
with in 4: optional
request.method bookmarks url_for('index')) fields
= @app.route('/comments', methods=['POST']) load_news_data("news.txt")
import for bn bookmarks]
extra DATA_DIR bid from = comments
return news_id reverse=True)
def [bn trending_news.sort(key=lambda f: = for for
filepath
except @app.route('/trending') os.path.join(DATA_DIR,
if f:
load_comments() c for
[]) app bn] =
def os
comments_by_news.setdefault(c['news_id'], bid) news=news, ''),
comments(): and url_for, if return bookmarked_news comment_file in
f: f"{news_id}||{user}||{comment_text}\n" bookmarked_news line comments app.run(debug=True) = parts comments:
url_for('index')) load_news_data("news.txt") def return open(filepath,


bookmarked_news comments=comments_by_news, for Exception:
=
