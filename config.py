# -*- coding: utf8 -*-

import os

# upload settings
UPLOAD_FOLDER = 'app/static/assets'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# secret settings
SECRET_KEY = 'k?yhGAcb9bFvtH99NYAz[fR87EQFN^6*%q6v'

# mail settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'ryha26@gmail.com'
MAIL_PASSWORD = 'wMdzDegWcYkto3VuZXmu'

# database settings
basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_RECORD_QUERIES = True
