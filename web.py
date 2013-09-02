import cgi
import re
from flask import Flask, render_template, abort, redirect, url_for, request
#from flask.ext.heroku import Heroku
#from flask.ext.login import LoginManager
#import os
import post
import pagination


app = Flask(__name__)
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
def show_post(permalink):
    post = postClass.get_post_by_permalink(permalink)
    if not post:
        abort(404)
    return render_template('single_post.html', post=post, meta_title=post['title'])


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', meta_title='404'), 404


@app.route('/newpost')
def get_newpost():
    return render_template('new_post.html', meta_title='New Post')


@app.route('/newpost', methods=['POST'])
def post_newpost():
    error = False
    error_type = 'validate'
    error_message = None
    response_message = 'New post was created!'
    if not request.form['post-title'] or not request.form['post-full']:
        error = True
        response_message = None
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
                response_message = None
                error = True
                error_type = 'post'
                error_message = 'Inserting post error'
    return render_template('new_post.html',
                           meta_title='New Post',
                           error=error,
                           error_type=error_type,
                           error_message=error_message,
                           response_message=response_message)


@app.route('/signup')
def present_signup():
    pass


@app.route('/login')
def present_login():
    pass


@app.route('/login', methods=['POST'])
def process_login():
    pass


@app.route('/logout')
def process_logout():
    pass


@app.route('/signup', methods=['POST'])
def process_signup():
    pass


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


app.jinja_env.globals['url_for_other_page'] = url_for_other_page
postClass = post.Post(app.config['DATABASE'])
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
