import datetime
import cgi
from bson.objectid import ObjectId
from helper_functions import *


class Post:

    def __init__(self, default_config):
        self.collection = default_config['POSTS_COLLECTION']
        self.response = {'error': None, 'data': None}
        self.debug_mode = default_config['DEBUG']

    def get_posts(self, limit, skip, tag=None, search=None):
        self.response['error'] = None
        cond = {}
        if tag is not None:
            cond = {'tags': tag}
        elif search is not None:
            cond = {'$or': [
                    {'title': {'$regex': search, '$options': 'i'}},
                    {'body': {'$regex': search, '$options': 'i'}},
                    {'preview': {'$regex': search, '$options': 'i'}}]}
        try:
            cursor = self.collection.find(cond).sort(
                'date', direction=-1).skip(skip).limit(limit)
            self.response['data'] = []
            for post in cursor:
                if 'tags' not in post:
                    post['tags'] = []
                if 'comments' not in post:
                    post['comments'] = []
                if 'preview' not in post:
                    post['preview'] = ''

                self.response['data'].append({'id': post['_id'],
                                              'title': post['title'],
                                              'body': post['body'],
                                              'preview': post['preview'],
                                              'date': post['date'],
                                              'permalink': post['permalink'],
                                              'tags': post['tags'],
                                              'author': post['author'],
                                              'comments': post['comments']})
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Posts not found..'

        return self.response

    def get_post_by_permalink(self, permalink):
        self.response['error'] = None
        try:
            self.response['data'] = self.collection.find_one(
                {'permalink': permalink})
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Post not found..'

        return self.response

    def get_post_by_id(self, post_id):
        self.response['error'] = None
        try:
            self.response['data'] = self.collection.find_one(
                {'_id': ObjectId(post_id)})
            if self.response['data']:
                if 'tags' not in self.response['data']:
                    self.response['data']['tags'] = ''
                else:
                    self.response['data']['tags'] = ','.join(
                        self.response['data']['tags'])
                if 'preview' not in self.response['data']:
                    self.response['data']['preview'] = ''
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Post not found..'

        return self.response

    def get_total_count(self, tag=None, search=None):
        cond = {}
        if tag is not None:
            cond = {'tags': tag}
        elif search is not None:
            cond = {'$or': [
                    {'title': {'$regex': search, '$options': 'i'}},
                    {'body': {'$regex': search, '$options': 'i'}},
                    {'preview': {'$regex': search, '$options': 'i'}}]}

        return self.collection.find(cond).count()

    def get_tags(self):
        self.response['error'] = None
        try:
            self.response['data'] = list(self.collection.aggregate([
                {'$unwind': '$tags'},
                {'$group': {'_id': '$tags', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 10},
                {'$project': {'title': '$_id', 'count': 1, '_id': 0}}
            ]))
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Get tags error..'

        return self.response

    def create_new_post(self, post_data):
        self.response['error'] = None
        try:
            self.response['data'] = self.collection.insert(post_data)
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Adding post error..'

        return self.response

    def edit_post(self, post_id, post_data):
        self.response['error'] = None
        del post_data['date']
        del post_data['permalink']

        try:
            self.collection.update(
                {'_id': ObjectId(post_id)}, {"$set": post_data}, upsert=False)
            self.response['data'] = True
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Post update error..'

        return self.response

    def delete_post(self, post_id):
        self.response['error'] = None
        try:
            if self.get_post_by_id(post_id) and self.collection.remove({'_id': ObjectId(post_id)}):
                self.response['data'] = True
            else:
                self.response['data'] = False
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Deleting post error..'

        return self.response

    @staticmethod
    def validate_post_data(post_data):
        permalink = random_string(12)
        #exp = re.compile('\W')
        #whitespace = re.compile('\s')
        #temp_title = whitespace.sub("_", post_data['title'])
        #permalink = exp.sub('', temp_title)

        post_data['title'] = cgi.escape(post_data['title'])
        post_data['preview'] = cgi.escape(post_data['preview'], quote=True)
        post_data['body'] = cgi.escape(post_data['body'], quote=True)
        post_data['date'] = datetime.datetime.utcnow()
        post_data['permalink'] = permalink

        return post_data

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
