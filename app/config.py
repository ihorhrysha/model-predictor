import os
from os.path import dirname, abspath, join

basedir = abspath(dirname(dirname(__file__)))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GBQ_CRED_PATH') or \
        join(basedir, 'bigquery.cred.json')

    MODELS_PATH = os.environ.get('MODELS_PATH') or \
        join(basedir, 'models')

    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False
