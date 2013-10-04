class Settings:
    def __init__(self, default_config):
        self.collection = default_config['SETTINGS_COLLECTION']

        self.config = default_config
        self.config['PER_PAGE'] = 15
        self.config['SEARCH'] = False

        self.response = {'error': None, 'data': None}
        self.debug_mode = default_config['DEBUG']

    def get_config(self):
        try:
            cursor = self.collection.find_one()
            if cursor:
                self.config['PER_PAGE'] = cursor.get('per_page', 15)
                self.config['SEARCH'] = cursor.get('use_search', False)
            return self.config
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'System error'

    def is_installed(self):
        posts_cnt = self.config['POSTS_COLLECTION'].find().count()
        users_cnt = self.config['USERS_COLLECTION'].find().count()
        configs_cnt = self.config['SETTINGS_COLLECTION'].find().count()
        if posts_cnt and users_cnt and configs_cnt:
            return True
        else:
            return False

    @staticmethod
    def print_debug_info(msg, show=False):
        if show:
            import sys
            import os

            error_color = '\033[32m'
            error_end = '\033[0m'

            error = {'type': sys.exc_info()[0].__name__,
                     'file': os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename),
                     'line': sys.exc_info()[2].tb_lineno,
                     'details': str(msg)}

            print error_color
            print '\n\n---\nError type: %s in file: %s on line: %s\nError details: %s\n---\n\n'\
                  % (error['type'], error['file'], error['line'], error['details'])
            print error_end