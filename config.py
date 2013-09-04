import pymongo

DEBUG = True
PER_PAGE = 10

SECRET_KEY = "Howdy, cowboy!"
#Database
CONNECTION_STRING = "mongodb://localhost"
CONNECTION = pymongo.MongoClient(CONNECTION_STRING)
DATABASE = CONNECTION.blog

#Logging
LOG_FILE="app.log"