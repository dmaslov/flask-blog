from flask import Flask, render_template, abort, redirect, url_for, request
import config
import post
import pagination


app = Flask(__name__)


@app.route('/')
def index():
    posts = postClass.get_posts(10)
    #pagination
    return render_template('index.html', posts=posts, meta_title='Blog')


@app.route('/tag/<tag>')
def posts_by_tag(tag):
    posts = postClass.get_posts(10, tag)
    #pagination
    if not posts:
        abort(404)
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
    pass


@app.route('/newpost', methods=['POST'])
def post_newpost():
    pass


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


postClass = post.Post(config.DATABASE)
if __name__ == '__main__':
    app.run(debug=config.DEBUG)
