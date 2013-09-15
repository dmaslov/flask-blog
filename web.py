import cgi
from flask import Flask, render_template, abort, url_for, request, flash, session, redirect
from flaskext.markdown import Markdown
from mdx_github_gists import GitHubGistExtension
from mdx_strike import StrikeExtension
from mdx_quote import QuoteExtension
from werkzeug.contrib.atom import AtomFeed
import post
import user
import pagination
from helper_functions import *


app = Flask(__name__)
md = Markdown(app)
md.register_extension(GitHubGistExtension)
md.register_extension(StrikeExtension)
md.register_extension(QuoteExtension)
app.config.from_object('config')


@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def index(page):
    skip = (page - 1) * app.config['PER_PAGE']
    posts = postClass.get_posts(app.config['PER_PAGE'], skip)
    count = postClass.get_total_count()
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)
    return render_template('index.html', posts=posts['data'], pagination=pag, meta_title='Blog')


@app.route('/tag/<tag>', defaults={'page': 1})
#@app.route('/t_page/<int:page>/<tag>')
def posts_by_tag(tag, page):
    # TODO: pagination for by_tag_view
    # skip = (page - 1) * app.config['PER_PAGE']
    skip = 0
    posts = postClass.get_posts(app.config['PER_PAGE'], skip, tag)
    if posts['error']:
        pass
    # count = postClass.get_total_count(tag)
    if not posts['data']:
        abort(404)
    # pag = pagination.Pagination(page, app.config['PER_PAGE'], count)
    return render_template('index.html', posts=posts['data'], meta_title='Posts by tag: '+tag)


@app.route('/post/<permalink>')
def single_post(permalink):
    post = postClass.get_post_by_permalink(permalink)
    if not post['data']:
        abort(404)
    return render_template('single_post.html', post=post['data'], meta_title=post['data']['title'])


@app.route('/newpost', methods=['GET', 'POST'])
@login_required()
def new_post():
    error = False
    error_type = 'validate'
    if request.method == 'POST':
        if not request.form.get('post-title') or not request.form.get('post-full'):
            error = True
        else:
            tags = cgi.escape(request.form.get('post-tags'))
            tags_array = extract_tags(tags)
            post_data = {'title': request.form.get('post-title'),
                         'preview': request.form.get('post-short'),
                         'body': request.form.get('post-full'),
                         'tags': tags_array,
                         'author': session['user']['username']}

            post = postClass.validate_post_data(post_data)
            if request.form.get('post-preview') == '1':
                return render_template('preview.html', post=post, meta_title='Preview Post::'+post_data['title'])
            else:
                if request.form.get('post-id'):
                    response = postClass.edit_post(request.form['post-id'], post_data)
                    if not response['error']:
                        flash('Post successfuly updated!', 'success')
                    else:
                        flash(response['error'], 'error')
                    return redirect(url_for('posts'))
                else:
                    response = postClass.create_new_post(post_data)
                    if response['error']:
                        error = True
                        error_type = 'post'
                        flash(response['error'], 'error')
                    else:
                        flash('New post successfuly created!', 'success')

    return render_template('new_post.html',
                           meta_title='New Post',
                           error=error,
                           error_type=error_type)


@app.route('/posts_list', defaults={'page': 1})
@login_required()
def posts(page):
    posts = postClass.get_posts(app.config['PER_PAGE'], 0)
    if not posts['data']:
        abort(404)

    return render_template('posts.html', posts=posts['data'], meta_title='Posts List')


@app.route('/post_edit?id=<id>')
@login_required()
def post_edit(id):
    post = postClass.get_post_by_id(id)
    if post['error']:
        flash(post['error'], 'error')
        return redirect(url_for('posts'))

    return render_template('edit_post.html',
                           meta_title='Edit Post::'+post['data']['title'],
                           post=post['data'],
                           error=False,
                           error_type=False)


@app.route('/post_delete?id=<id>')
@login_required()
def post_del(id):
    response = postClass.delete_post(id)
    if response['data'] is True:
        flash('Post successfuly removed!', 'success')
    else:
        flash(response['error'], 'error')

    return redirect(url_for('posts'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = False
    error_type = 'validate'
    if request.method == 'POST':
        username = request.form.get('login-username')
        password = request.form.get('login-password')
        if not username or not password:
            error = True
            flash('Username and Password fields are required', 'error')
        else:
            user_data = userClass.login(username, password)
            if user_data['error']:
                error = True
                error_type = 'login'
                flash(user_data['error'], 'error')
            else:
                userClass.start_session(user_data['data'])
                flash('You are successfuly logged in!', 'success')
    else:
        if session.get('user'):
            return redirect(url_for('posts'))

    return render_template('login.html',
                           meta_title='Login',
                           error=error,
                           error_type=error_type)


@app.route('/logout')
def logout():
    error = False
    error_type = 'validate'
    if userClass.logout():
        flash('You are successfuly logged out!', 'success')
    else:
        return redirect(url_for('login'))
    return render_template('login.html',
                           meta_title='Login',
                           error=error,
                           error_type=error_type)


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


if not app.config['DEBUG']:
    import logging
    from logging import FileHandler
    file_handler = FileHandler(app.config['LOG_FILE'])
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page
app.jinja_env.globals['csrf_token'] = generate_csrf_token
postClass = post.Post(app.config['DATABASE'], app.config['DEBUG'])
userClass = user.User(app.config['DATABASE'])
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
