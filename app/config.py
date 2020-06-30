import os
from os.path import dirname, abspath, join

basedir = abspath(dirname(dirname(__file__)))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False