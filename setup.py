import config
import pymongo
import hashlib
from werkzeug.security import generate_password_hash


def create_document():
    """ Create posts document and insert test entry. """
    pass


def add_user():
    """Create users document and insert user from config. """
    db = config.DATABASE
    users = db.users

    password_hash = generate_password_hash(config.USER_PASSWORD, method='pbkdf2:sha256')
    record = {'_id': config.USER_LOGIN, 'password': password_hash, 'email': config.USER_EMAIL}

    try:
        users.insert(record, safe=True)
    except pymongo.errors.DuplicateKeyError as e:
        print "oops, login is already taken"
        return False
    except pymongo.errors.OperationFailure as e:
        print "oops, mongo error"
        return False

    return True


if __name__ == '__main__':
    create_document()
    add_user()
