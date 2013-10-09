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
                self.config['PER_PAGE'] = cursor.get('per_page', self.config['PER_PAGE'])
                self.config['SEARCH'] = cursor.get('use_search', self.config['SEARCH'])
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

    def install(self, blog_data, user_data):
        import user
        import post

        userClass = user.User(self.config)
        postClass = post.Post(self.config)
        self.response['error'] = None
        try:
            self.config['POSTS_COLLECTION'].ensure_index([('date', -1)])
            self.config['POSTS_COLLECTION'].ensure_index([('tags', 1), ('date', -1)])
            self.config['POSTS_COLLECTION'].ensure_index([('permalink', 1)])
            self.config['POSTS_COLLECTION'].ensure_index([('query', 1), ('orderby', 1)])
            self.config['USERS_COLLECTION'].ensure_index([('date', 1)])
            self.collection.insert(blog_data)
            user_create = userClass.save_user(user_data)

            post_data = {'title': 'Hello World!',
                         'preview': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod',
                         'body': 'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam',
                         'tags': [],
                         'author': user_data['_id']}

            post = postClass.validate_post_data(post_data)
            post_create = postClass.create_new_post(post)
            
            #if user_create['error'] or post_create['error']:
            #    self.response['error']
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Posts not found..'

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