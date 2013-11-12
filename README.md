# flask-blog

simple blog --engine-- written in [Flask](http://flask.pocoo.org/)


# Under the hood:
- [python](http://python.org/)
- [Flask](http://flask.pocoo.org/)
- [mongoDB](http://www.mongodb.org/)
- [bootstrap 3](http://getbootstrap.com/)
- [jQuery](http://jquery.com)
- [Lightbox 2](https://github.com/lokesh/lightbox2)
- [Markdown](http://daringfireball.net/projects/markdown/syntax)


# What it can:
- create/preview/update/delete articles;
- create/update/delete users;
- search;
- Atom feed.

# It contains:
- it has WYSIWYG Markdown editor;
- it has [AddThis](http://www.addthis.com/) social buttons;
- it use [gravatar](http://gravatar.com) for userpic.


# To Do:
- mongoDB text search
- comments maybe
- drafts


# Install:
`git clone https://github.com/dmaslov/flask-blog.git`

`cd flask-blog`

`virtualenv --no-site-packages ./env`

`source ./env/bin/activate`

`pip install -r requirements.txt`


After this edit the `config.py` file

- Replace the `CONNECTION_STRING` variable with your own connection string;

- Replace the `DATABASE` variable to your own one;

- If the default collection names don't work for you please replace the `POSTS_COLLECTION`, `USERS_COLLECTION` and `USERS_COLLECTION` variables to any names you like;

- If you use this code on a production sever replace the `DEBUG` variable with `False`.


# Usage:
When you run the application for the first time the "Install" page appears. You need to create a user profile and set some display settings on this page.

![install_page](http://i.imgur.com/gkWI10v.png)

If you have an account on [Gravatar](http://gravatar.com) and your logged-in email links to it, the userpic will display. It will be a random gravatar image if you don't.

All necessary MongoDB indexes will be created during the installation. A test text post will be created as well.

There should be at least one post and one user for the database to be installed. That is why it's impossible to delete the last post or user.

If you want to start it from scratch please remove all existing collections from your database and delete the browser session cookie. The Install page will show up again.

For deploying you can use [Heroku](http://heroku.com) and [mongolab](http://mongolab.com) for example.

If you are using mongolab, please copy the outlined on screenshot line to connect using driver, type in your dbuser and dbpassword and paste the line into the `CONNECTION_STRING` variable in the `config.py` file.

![mongolab_databases](http://i.imgur.com/VcoTh16.png)


For Heroku you'll find `gunicorn` server in the `requirements.txt` file. You are welcome to see how to deploy a Python web application on Heroku [here](https://devcenter.heroku.com/categories/python).


# WYSIWYG editor:
WYSIWYG editor uses [markdown](http://daringfireball.net/projects/markdown/syntax). Only available on the editor panel tags are intepreted.

![wysiwyg_editor_panel](http://i.imgur.com/D6aFuLT.png)

The editor is based on [MDMagick](https://github.com/fguillen/MDMagick) project.

To insert any tag you need to SELECT a word and then click on needed tag on editor panel.

You can insert github [Gists](https://gist.github.com/).

For this type a word in the editor, select it like you did when you added a tag from the panel, copen the embed gist link from the github gists page and paste it to the dialog window.

The word will be replaced with a working gist tag.

![gist_page](http://i.imgur.com/Zagr8Uv.png)

![inser_gist](http://i.imgur.com/nqS4Isz.png)

To insert an image you also need to select a word that will be used like a title attribute and paste the image URL into the dialog window.

![insert_image](http://i.imgur.com/suxPgI0.png)
