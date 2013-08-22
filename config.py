import pymongo

DEBUG = True
CONNECTION_STRING = "mongodb://localhost"
CONNECTION = pymongo.MongoClient(CONNECTION_STRING)
DATABASE = CONNECTION.blog