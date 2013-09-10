import pymongo

DEBUG = True
PER_PAGE = 10

SECRET_KEY = "Howdy, cowboy!"
#Database
CONNECTION_STRING = "mongodb://localhost"
CONNECTION = pymongo.MongoClient(CONNECTION_STRING)
DATABASE = CONNECTION.blog

#user
USER_EMAIL = 'user@example.com'
USER_LOGIN = 'user'
USER_PASSWORD = '111111'

#Logging
LOG_FILE="app.log"
