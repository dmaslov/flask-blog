import pymongo

CONNECTION_STRING = "mongodb://localhost"  # replace it with your settings
CONNECTION = pymongo.MongoClient(CONNECTION_STRING)

'''Leave this as is if you dont have other configuration'''
DATABASE = CONNECTION.blog
POSTS_COLLECTION = DATABASE.posts
USERS_COLLECTION = DATABASE.users
SETTINGS_COLLECTION = DATABASE.settings

SECRET_KEY = "Howdy, cowboy!"  # need to replace with some sequence..
LOG_FILE = "app.log"

DEBUG = True  # set it to False on production