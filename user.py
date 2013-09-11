from werkzeug.security import check_password_hash
from flask import session


class User:
    def __init__(self, database):
        self.db = database
        self.users_collection = database.users
        self.username = None
        self.email = None
        self.session_key = 'user'

    def login(self, username, password):
        response = {'error': None, 'user': None}
        try:
            users = self.users_collection.find({'_id': username})
            admin = [user for user in users]
            if len(admin):
                admin = admin[0]
                if self.validate_login(admin['password'], password):
                    self.username = admin['_id']
                    self.email = admin['email']
                else:
                    response['error'] = 'Password don\'t match'
            else:
                response['error'] = 'User not found'
        except Exception:
            response['error'] = 'System error'

        response['user'] = {'username': self.username, 'email': self.email}
        return response

    def validate_login(self, password_hash, password):
        return check_password_hash(password_hash, password)

    def start_session(self, obj):
        session[self.session_key] = obj
        return True

    def logout(self):
        try:
            session.pop(self.session_key)
            return True
        except:
            return False
