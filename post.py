import sys
import re
import datetime


class Post:
    def __init__(self, database):
        self.db = database
        self.posts = database.posts

    def get_posts(self, num_posts):
        print 'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii'
        cursor = self.posts.find().sort('date', direction=-1).limit(num_posts)
        l = []

        for post in cursor:
            post['date'] = post['date'].strftime("%a, %d %b %Y")  # fix up date
            if 'tags' not in post:
                post['tags'] = []  # fill it in if its not there already
            if 'comments' not in post:
                post['comments'] = []

            l.append({'title':post['title'], 'body': post['body'], 'post_date': post['date'],
                      'permalink': post['permalink'],
                      'tags': post['tags'],
                      'author': post['author'],
                      'comments': post['comments']})

        return l
