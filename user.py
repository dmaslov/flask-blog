from werkzeug.security import check_password_hash
from flask import session


class User:
    def __init__(self, database, debug_mode=True):
        self.db = database
        self.users = database.users
        self.username = None
        self.email = None
        self.session_key = 'user'
        self.response = {'error': None, 'data': None}
        self.debug_mode = debug_mode

    def login(self, username, password):
        self.response['error'] = None
        try:
            admin = self.users.find_one({'_id': username})
            if admin:
                if self.validate_login(admin['password'], password):
                    self.username = admin['_id']
                    self.email = admin['email']
                else:
                    self.response['error'] = 'Password don\'t match'
            else:
                self.response['error'] = 'User not found'

        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'System error'

        self.response['data'] = {'username': self.username, 'email': self.email}
        return self.response

    def validate_login(self, password_hash, password):
        return check_password_hash(password_hash, password)

    def start_session(self, obj):
        session[self.session_key] = obj
        return True

    def logout(self):
        if session.pop(self.session_key, None):
            return True
        else:
            return False

    def print_debug_info(self, msg, show=False):
        if show:
            import sys
            import os

            ERROR_COLOR = '\033[32m'
            ERROR_END = '\033[0m'

            error = {'type': sys.exc_info()[0].__name__,
                     'file': os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename),
                     'line': sys.exc_info()[2].tb_lineno,
                     'details': str(msg)}

            print ERROR_COLOR
            print '\n\n---\nError type: %s in file: %s on line: %s\nError details: %s\n---\n\n'\
                  % (error['type'], error['file'], error['line'], error['details'])
            print ERROR_END