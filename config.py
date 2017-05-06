# -*- coding: utf8 -*-

import os

# upload settings
ASSETS_FOLDER = 'app/static/assets'

# secret settings
SECRET_KEY = 'k?yhGAcb9bFvtH99NYAz[fR87EQFN^6*#q6v'

# database settings
basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_RECORD_QUERIES = True
