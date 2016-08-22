#!/usr/bin/env python

from pip.req import parse_requirements
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('./requirements.txt', session=False)

# reqs is a list of requirement
# e.g. ['flask==0.0.1', 'pymongo==0.0.1']
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='flask-blog',
    version='0.0.1',
    description='Simple blog engine written on Flask',
    author='Dmitry Maslov',
    author_email='maslov.dmitrij@gmail.com',
    license='MIT',
    url='https://github.com/dmaslov/flask-blog',
    packages=[
        'flask_blog'
    ],

    include_package_data = True,
    package_data = {
        'flask_blog': [
            'static/*/*.*', 'static/*/*/*.*', 'templates/*.*'
        ],
    },
    install_requires=reqs,
 )