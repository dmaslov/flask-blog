import cgi
import re
import string
import random
from flask import Flask, render_template, abort, url_for, request, flash, session
from flaskext.markdown import Markdown
from mdx_github_gists import GitHubGistExtension
from mdx_strike import StrikeExtension
from mdx_quote import QuoteExtension

from urlparse import urljoin
from flask import request
from werkzeug.contrib.atom import AtomFeed

#from flask.ext.heroku import Heroku
#from flask.ext.login import LoginManager
#import os
import post
import pagination


app = Flask(__name__)
md = Markdown(app)
md.register_extension(GitHubGistExtension)
md.register_extension(StrikeExtension)
md.register_extension(QuoteExtension)
app.config.from_object('config')
#heroku = Heroku(app)
#login_manager = LoginManager(app)


@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def index(page):
    skip = (page - 1) * app.config['PER_PAGE']
    posts = postClass.get_posts(app.config['PER_PAGE'], skip)
    count = postClass.get_total_count()
    if not posts:
        abort(404)
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)
    return render_template('index.html', posts=posts, pagination=pag, meta_title='Blog')


@app.route('/tag/<tag>', defaults={'page': 1})
#@app.route('/t_page/<int:page>/<tag>')
def posts_by_tag(tag, page):
    # TODO: pagination for by_tag_view
    # skip = (page - 1) * app.config['PER_PAGE']
    skip = 0
    posts = postClass.get_posts(app.config['PER_PAGE'], skip, tag)
    # count = postClass.get_total_count(tag)
    if not posts:
        abort(404)
    # pag = pagination.Pagination(page, app.config['PER_PAGE'], count)
    return render_template('index.html', posts=posts, meta_title='Posts by tag: tag')


@app.route('/post/<permalink>')
def single_post(permalink):
    post = postClass.get_post_by_permalink(permalink)
    if not post:
        abort(404)
    return render_template('single_post.html', post=post, meta_title=post['title'])


@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    error = False
    error_type = 'validate'
    if request.method == 'POST':
        if not request.form['post-title'] or not request.form['post-full']:
            error = True
            #flash("Title and Full text can't be blank!", 'error')
        else:
            tags = cgi.escape(request.form['post-tags'])
            tags_array = extract_tags(tags)
            author = 'lazzy' #TODO: replace with logged in username

            post_data = {'title': request.form['post-title'],
                         'preview': request.form['post-short'],
                         'body': request.form['post-full'],
                         'tags': tags_array,
                         'author': author}

            post = postClass.validate_post_data(post_data)
            if request.form['post-preview'] == '1':
                return render_template('preview.html', post=post, meta_title='Preview Post::'+post_data['title'])
            else:
                post_id = postClass.create_new_post(post_data)
                if not post_id:
                    error = True
                    error_type = 'post'
                    flash('Inserting post error..', 'error')
                else:
                    flash('New post successfuly created!', 'success')

    return render_template('new_post.html',
                           meta_title='New Post',
                           error=error,
                           error_type=error_type)


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


@app.route('/logout')
def logout():
    pass


@app.route('/recent_feed')
def recent_feed():
    feed = AtomFeed('Recent Articles',
                    feed_url=request.url, url=request.url_root)
    posts = postClass.get_posts(app.config['PER_PAGE'], 0)
    for post in posts:
        feed.add(post['title'], md(post['body']),
                 content_type='html',
                 author=post['author'],
                 url=make_external(post['permalink']),
                 updated=post['date'])
    return feed.get_response()


@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(400)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', meta_title='404'), 404


@app.template_filter('formatdate')
def format_datetime_filter(input, format="%a, %d %b %Y"):
    return input.strftime(format)


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


def extract_tags(tags):
    whitespace = re.compile('\s')
    nowhite = whitespace.sub("", tags)
    tags_array = nowhite.split(',')

    cleaned = []
    for tag in tags_array:
        if tag not in cleaned and tag != "":
            cleaned.append(tag)

    return cleaned


def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = random_string()
    return session['_csrf_token']


def make_external(url):
    return urljoin(request.url_root, url)


if not app.config['DEBUG']:
    import logging
    from logging import FileHandler
    file_handler = FileHandler(app.config['LOG_FILE'])
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page
app.jinja_env.globals['csrf_token'] = generate_csrf_token
postClass = post.Post(app.config['DATABASE'])
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
