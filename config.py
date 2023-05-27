# -*- coding: utf8 -*-

import os

# upload settings
ASSETS_FOLDER = 'app/static/assets'

# security settings
skey = None
filename = 'skey.txt'
if not os.path.isfile(filename):
	skey = 'this-is-not-secure'
else:
	with open(filename) as file:
		skey = file.read().replace('\n', '')
SECRET_KEY = skey

# database settings
basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_RECORD_QUERIES = True
