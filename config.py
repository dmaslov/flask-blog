import pymongo

DEBUG = True
PER_PAGE = 10
CONNECTION_STRING = "mongodb://localhost"
CONNECTION = pymongo.MongoClient(CONNECTION_STRING)
DATABASE = CONNECTION.blog