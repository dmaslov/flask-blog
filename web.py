from flask import Flask, render_template, request
# configuration
DEBUG = True
# DATABASE = '/tmp/flaskr.db'
# SECRET_KEY = 'development key'
# USERNAME = 'admin'
# PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    return render_template('index.html', meta_title='Blog')


@app.route('/tag/<tag>')
def posts_by_tag(tag="notfound"):
    pass


@app.route('/post/<permalink>')
def show_post(permalink):
    return render_template('single_post.html', meta_title='SinglePost')


@app.route('/newcomment', methods=['POST'])
def post_new_comment():
    pass


@app.route('/like', methods=['POST'])
def post_comment_like():
    pass


@app.route("/404")
def post_not_found():
    pass


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
# connection_string = "mongodb://localhost"
# connection = pymongo.MongoClient(connection_string)
# database = connection.blog
#
# posts = blogPostDAO.BlogPostDAO(database)
# users = userDAO.UserDAO(database)
# sessions = sessionDAO.SessionDAO(database)


if __name__ == '__main__':
    app.run(app.config['DEBUG'])
