# flask-blog

simple blog ~~engine~~ written on [Flask](http://flask.pocoo.org/)

# Demo:
you can try it [here](http://flask-blog-demo.herokuapp.com/)

login:demo

pass:demo

# Under the hood:
- [Python](http://python.org/)
- [Flask](http://flask.pocoo.org/)
- [MongoDB](http://www.mongodb.org/)
- [Bootstrap 3](http://getbootstrap.com/)
- [jQuery](http://jquery.com)
- [Lightbox 2](https://github.com/lokesh/lightbox2)
- [Markdown](http://daringfireball.net/projects/markdown/syntax)
- [Polymer](http://www.polymer-project.org)


# What it can:
- create/preview/update/delete articles;
- create/update/delete users;
- search;
- atom feed.

# It contains:
- WYSIWYG Markdown editor;
- [AddThis](http://www.addthis.com/) social buttons;
- [Gravatar](http://gravatar.com) for userpic.


# Requirements:
- mongoDB >= 2.2


# Installation:
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

# Run:
Start `mongod`, then when you in project dir with actived environment just type in terminal

`python web.py`

![builtin_run](http://i.imgur.com/dkEL5aS.png?2)

or

`gunicorn web:app`

![gunicorn_run](http://i.imgur.com/rCp0g25.png?2)

# Usage:
When you run the application for the first time the "Install" page appears. You need to create a user profile and set some display settings on this page.

![install_page](http://i.imgur.com/gkWI10v.png)

If you have an account on [Gravatar](http://gravatar.com) and your logged-in email links to it, the userpic will display. It will be a random gravatar image if it doesn't.

All necessary MongoDB indexes will be created during the installation. A test text post will be created as well.

There should be at least one post and one user for the database to be installed. That is why it's impossible to delete the last post or user.

If you want to start it from scratch please remove all existing collections from your database and delete the browser session cookie. The Install page will show up again.

For deploying you can use [Heroku](http://heroku.com) and [mongolab](http://mongolab.com) for example.

If you are using mongolab, please copy the outlined on the screenshot line to connect using driver, type in your dbuser and dbpassword and paste the line into the `CONNECTION_STRING` variable in the `config.py` file.

![mongolab_databases](http://i.imgur.com/VcoTh16.png)


For Heroku you'll find `gunicorn` server in the `requirements.txt` file. You are welcome to see how to deploy a Python web application on Heroku [here](https://devcenter.heroku.com/categories/python).


# WYSIWYG editor:
WYSIWYG editor uses [Markdown](http://daringfireball.net/projects/markdown/syntax). Only available on the editor panel tags are intepreted.

![wysiwyg_editor_panel](http://i.imgur.com/D6aFuLT.png)

The editor is based on [MDMagick](https://github.com/fguillen/MDMagick) project.

To insert any tag you need to SELECT a word and then click on a needed tag on the editor panel.

You can insert github [Gists](https://gist.github.com/).

For this click on the Gist tag on the panel, copy the gist id from the github gists page and paste it to the dialog window.

The word will be replaced with a working gist tag.

![gist_page](http://i.imgur.com/1hQKsaX.png)

![inser_gist](http://i.imgur.com/x5Yb9es.png)

~~To insert an image you also need to select a word that will be used like a title attribute and paste the image URL into the dialog window.~~

![insert_image](http://i.imgur.com/suxPgI0.png)


# Upd:
Don't need to highlight text to add a link or an image anymore. Now you can simply click some tag in the editor menu and put a link. The 'Markdown' tag will be created automatically with a highlighted temporary description. The existing pasting algorithm works as it did before.
