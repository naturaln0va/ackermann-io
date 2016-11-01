import os

# upload settings
UPLOAD_FOLDER = 'app/static/assets'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# secret settings
SECRET_KEY = 'k?yhGAcb9bFvtH99NYAz[fR87EQFN^6*%q6v'

# database settings
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# mail server settings
MAIL_SERVER = 'ackermann.io'
MAIL_PORT = 25
MAIL_USERNAME = 'ryan@ackermann.io'
MAIL_PASSWORD = 'donteatZ0mbies'

# administrator list
ADMINS = ['ryan@ackermann.io']