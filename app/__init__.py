
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown
from flaskext.markdown import Markdown
from flask_mail import Mail
from datetime import datetime

# application main

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
pagedown = PageDown(app)
mkd = Markdown(app)
mail = Mail(app)

# filters

@app.template_filter('prettytime')
def prettytime(date):
    return date.strftime("%b %d, %Y")

# logging

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('ackermann.io')

from app import views, models