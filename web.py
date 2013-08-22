from flask import Flask, render_template, abort, redirect, url_for, request
import config
import post


app = Flask(__name__)


@app.route('/')
def index():
    posts = postClass.get_posts(10)
    print posts
    return render_template('index.html', meta_title='Blog')


@app.route('/tag/<tag>')
def posts_by_tag(tag="notfound"):
    pass


@app.route('/post/<permalink>')
def show_post(permalink):
    if permalink == 'hello':
        abort(404)
    return render_template('single_post.html', meta_title='SinglePost')


@app.route('/newcomment', methods=['POST'])
def post_new_comment():
    pass


@app.route('/like', methods=['POST'])
def post_comment_like():
    pass


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


# Helper Functions

#extracts the tag from the tags form element. an experience python programmer could do this in  fewer lines, no doubt
# def extract_tags(tags):
#
#     whitespace = re.compile('\s')
#
#     nowhite = whitespace.sub("",tags)
#     tags_array = nowhite.split(',')
#
#     # let's clean it up
#     cleaned = []
#     for tag in tags_array:
#         if tag not in cleaned and tag != "":
#             cleaned.append(tag)
#
#     return cleaned
#
#
# # validates that the user information is valid for new signup, return True of False
# # and fills in the error string if there is an issue
# def validate_signup(username, password, verify, email, errors):
#     USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
#     PASS_RE = re.compile(r"^.{3,20}$")
#     EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
#
#     errors['username_error'] = ""
#     errors['password_error'] = ""
#     errors['verify_error'] = ""
#     errors['email_error'] = ""
#
#     if not USER_RE.match(username):
#         errors['username_error'] = "invalid username. try just letters and numbers"
#         return False
#
#     if not PASS_RE.match(password):
#         errors['password_error'] = "invalid password."
#         return False
#     if password != verify:
#         errors['verify_error'] = "password must match"
#         return False
#     if email != "":
#         if not EMAIL_RE.match(email):
#             errors['email_error'] = "invalid email address"
#             return False
#     return True
#

postClass = post.Post(config.DATABASE)

if __name__ == '__main__':
    app.run(debug=config.DEBUG)
