
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown
from flaskext.markdown import Markdown
from datetime import datetime
from config import BaseConfig

# application main

app = Flask(__name__)
app.config.from_object(BaseConfig)

db = SQLAlchemy(app)
pagedown = PageDown(app)
mkd = Markdown(app)

# filters

@app.template_filter('prettytime')
def prettytime(date):
  return date.strftime("%b %d, %Y")

from models import *
from views import *

if __name__ == '__main__':
  app.run()