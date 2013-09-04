import sys
import re
import datetime
import cgi


class Post:
    def __init__(self, database):
        self.db = database
        self.posts = database.posts

    def get_posts(self, limit, skip, tag=None):
        cond = {}
        if tag is not None:
            cond = {'tags': tag}
        print skip, limit
        cursor = self.posts.find(cond).sort('date', direction=-1).skip(skip).limit(limit)
        l = []

        for post in cursor:
            if 'tags' not in post:
                post['tags'] = []
            if 'comments' not in post:
                post['comments'] = []
            if 'preview' not in post:
                post['preview'] = ''

            l.append({'title': post['title'],
                      'body': post['body'],
                      'preview': post['preview'],
                      'date': post['date'],
                      'permalink': post['permalink'],
                      'tags': post['tags'],
                      'author': post['author'],
                      'comments': post['comments']})

        return l

    def get_post_by_permalink(self, permalink):
        return self.posts.find_one({'permalink': permalink})

    def get_total_count(self, tag=None):
        if tag is not None:
            return self.posts.find({'tags': tag}).count()
        else:
            return self.posts.count()

    def create_new_post(self, post_data):
        try:
            post_id = self.posts.insert(post_data)
        except:
            #TODO: proper exception handling
            print "Error inserting post"

        return post_id

    def validate_post_data(self, post_data):
        exp = re.compile('\W')
        whitespace = re.compile('\s')
        temp_title = whitespace.sub("_", post_data['title'])
        permalink = exp.sub('', temp_title)

        post_data['title'] = cgi.escape(post_data['title'], quote=True)
        post_data['preview'] = cgi.escape(post_data['preview'], quote=True)
        post_data['body'] = cgi.escape(post_data['body'], quote=True)
        post_data['date'] = datetime.datetime.utcnow()
        post_data['permalink'] = permalink

        return post_data